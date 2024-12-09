import re
from collections import OrderedDict

import torch
import torch.nn as nn
import torch.nn.functional as F


def get_child_dict(params, key=None):
  """
  Constructs parameter dictionary for a network module.

  Args:
    params (dict): a parent dictionary of named parameters.
    key (str, optional): a key that specifies the root of the child dictionary.

  Returns:
    child_dict (dict): a child dictionary of model parameters.
  """
  if params is None:
    return None
  if key is None or (isinstance(key, str) and key == ''):
    return params

  key_re = re.compile(r'^{0}\.(.+)'.format(re.escape(key)))
  if not any(filter(key_re.match, params.keys())):  # handles nn.DataParallel
    key_re = re.compile(r'^module\.{0}\.(.+)'.format(re.escape(key)))
  child_dict = OrderedDict(
    (key_re.sub(r'\1', k), value) for (k, value)
      in params.items() if key_re.match(k) is not None)
  return child_dict


class Module(nn.Module):
  def __init__(self):
    super(Module, self).__init__()
    self.efficient = False
    self.first_pass = True

  def go_efficient(self, mode=True):
    """ Switches on / off gradient checkpointing. """
    self.efficient = mode
    for m in self.children():
      if isinstance(m, Module):
        m.go_efficient(mode)

  def is_first_pass(self, mode=True):
    """ Tracks the progress of forward and backward pass when gradient 
    checkpointing is enabled. """
    self.first_pass = mode
    for m in self.children():
      if isinstance(m, Module):
        m.is_first_pass(mode)


class Conv2d(nn.Conv2d, Module):
  def __init__(self, in_channels, out_channels, kernel_size, 
               stride=1, padding=0, bias=True):
    super(Conv2d, self).__init__(in_channels, out_channels, kernel_size, 
                                 stride, padding, bias=bias)

  def forward(self, x, params=None, episode=None):
    if params is None:
      x = super(Conv2d, self).forward(x)
    else:
      weight, bias = params.get('weight'), params.get('bias')
      if weight is None:
        weight = self.weight
      if bias is None:
        bias = self.bias
      x = F.conv2d(x, weight, bias, self.stride, self.padding)
    return x


class Linear(nn.Linear, Module):
  def __init__(self, in_features, out_features, bias=True):
    super(Linear, self).__init__(in_features, out_features, bias=bias)

  def forward(self, x, params=None, episode=None):
    if params is None:
      x = super(Linear, self).forward(x)
    else:
      weight, bias = params.get('weight'), params.get('bias')
      if weight is None:
        weight = self.weight
      if bias is None:
        bias = self.bias
      x = F.linear(x, weight, bias)
    return x


class BatchNorm2d(nn.BatchNorm2d, Module):
  def __init__(self, num_features, eps=1e-5, momentum=0.1, affine=True, 
               track_running_stats=True, episodic=False, n_episode=4,
               alpha=False):
    """
    Args:
      episodic (bool, optional): if True, maintains running statistics for 
        each episode separately. It is ignored if track_running_stats=False. 
        Default: True
      n_episode (int, optional): number of episodes per mini-batch. It is 
        ignored if episodic=False.
      alpha (bool, optional): if True, learns to interpolate between batch 
        statistics computed over the support set and instance statistics from 
        a query at validation time. Default: True
        (It is ignored if track_running_stats=False or meta_learn=False)
    """
    super(BatchNorm2d, self).__init__(num_features, eps, momentum, affine, 
                                      track_running_stats)
    self.episodic = episodic
    self.n_episode = n_episode
    self.alpha = alpha

    if self.track_running_stats:
      if self.episodic:
        for ep in range(n_episode):
          self.register_buffer(
            'running_mean_%d' % ep, torch.zeros(num_features))
          self.register_buffer(
            'running_var_%d' % ep, torch.ones(num_features))
          self.register_buffer(
            'num_batches_tracked_%d' % ep, torch.tensor(0, dtype=torch.int))
      if self.alpha:
        self.register_buffer('batch_size', torch.tensor(0, dtype=torch.int))
        self.alpha_scale = nn.Parameter(torch.tensor(0.))
        self.alpha_offset = nn.Parameter(torch.tensor(0.))
        
  def is_episodic(self):
    return self.episodic

  def _batch_norm(self, x, mean, var, weight=None, bias=None):
    if self.affine:
      assert weight is not None and bias is not None
      weight = weight.view(1, -1, 1, 1)
      bias = bias.view(1, -1, 1, 1)
      x = weight * (x - mean) / (var + self.eps) ** .5 + bias
    else:
      x = (x - mean) / (var + self.eps) ** .5
    return x

  def reset_episodic_running_stats(self, episode):
    if self.episodic:
      getattr(self, 'running_mean_%d' % episode).zero_()
      getattr(self, 'running_var_%d' % episode).fill_(1.)
      getattr(self, 'num_batches_tracked_%d' % episode).zero_()

  def forward(self, x, params=None, episode=None):
    self._check_input_dim(x)
    if params is not None:
      weight, bias = params.get('weight'), params.get('bias')
      if weight is None:
        weight = self.weight
      if bias is None:
        bias = self.bias
    else:
      weight, bias = self.weight, self.bias

    if self.track_running_stats:
      if self.episodic:
        assert episode is not None and episode < self.n_episode
        running_mean = getattr(self, 'running_mean_%d' % episode)
        running_var = getattr(self, 'running_var_%d' % episode)
        num_batches_tracked = getattr(self, 'num_batches_tracked_%d' % episode)
      else:
        running_mean, running_var = self.running_mean, self.running_var
        num_batches_tracked = self.num_batches_tracked

      if self.training:
        exp_avg_factor = 0.
        if self.first_pass: # only updates statistics in the first pass
          if self.alpha:
            self.batch_size = x.size(0)
          num_batches_tracked += 1
          if self.momentum is None:
            exp_avg_factor = 1. / float(num_batches_tracked)
          else:
            exp_avg_factor = self.momentum
        return F.batch_norm(x, running_mean, running_var, weight, bias,
                            True, exp_avg_factor, self.eps)
      else:
        if self.alpha:
          assert self.batch_size > 0
          alpha = torch.sigmoid(
            self.alpha_scale * self.batch_size + self.alpha_offset)
          # exponentially moving-averaged training statistics
          running_mean = running_mean.view(1, -1, 1, 1)
          running_var = running_var.view(1, -1, 1, 1)
          # per-sample statistics
          sample_mean = torch.mean(x, dim=(2, 3), keepdim=True)
          sample_var = torch.var(x, dim=(2, 3), unbiased=False, keepdim=True)
          # interpolated statistics
          mean = alpha * running_mean + (1 - alpha) * sample_mean
          var = alpha * running_var + (1 - alpha) * sample_var + \
                alpha * (1 - alpha) * (sample_mean - running_mean) ** 2
          return self._batch_norm(x, mean, var, weight, bias)
        else:
          return F.batch_norm(x, running_mean, running_var, weight, bias,
                              False, 0., self.eps)
    else:
      return F.batch_norm(x, None, None, weight, bias, True, 0., self.eps)
    

class L2_norm(nn.Module):
    def __init__(self):
        super(L2_norm, self).__init__()

    def forward(self, x):
        return F.normalize(x, p=2, dim=-1)


class Sequential(nn.Sequential, Module):
  def __init__(self, *args):
    super(Sequential, self).__init__(*args)

  def forward(self, x, params=None, episode=None):
    if params is None:
      for module in self:
        x = module(x, None, episode)
    else:
      for name, module in self._modules.items():
        x = module(x, get_child_dict(params, name), episode)
    return x





from collections import OrderedDict

import torch
import torch.nn as nn


__all__ = ['resnet12', 'wide_resnet12']



models = {}
def register(name):
  def decorator(cls):
    models[name] = cls
    return cls
  return decorator


def conv3x3(in_channels, out_channels):
  return Conv2d(in_channels, out_channels, 3, 1, padding=1, bias=False)


def conv1x1(in_channels, out_channels):
  return Conv2d(in_channels, out_channels, 1, 1, padding=0, bias=False)


class Block(Module):
  def __init__(self, in_planes, planes, bn_args):
    super(Block, self).__init__()
    self.in_planes = in_planes
    self.planes = planes

    self.conv1 = conv3x3(in_planes, planes)
    self.bn1 = BatchNorm2d(planes, **bn_args)
    self.conv2 = conv3x3(planes, planes)
    self.bn2 = BatchNorm2d(planes, **bn_args)
    self.conv3 = conv3x3(planes, planes)
    self.bn3 = BatchNorm2d(planes, **bn_args)

    self.res_conv = Sequential(OrderedDict([
      ('conv', conv1x1(in_planes, planes)),
      ('bn', BatchNorm2d(planes, **bn_args)),
    ]))

    self.relu = nn.LeakyReLU(0.1, inplace=True)
    self.pool = nn.MaxPool2d(2)

  def forward(self, x, params=None, episode=None):
    out = self.conv1(x, get_child_dict(params, 'conv1'))
    out = self.bn1(out, get_child_dict(params, 'bn1'), episode)
    out = self.relu(out)

    out = self.conv2(out, get_child_dict(params, 'conv2'))
    out = self.bn2(out, get_child_dict(params, 'bn2'), episode)
    out = self.relu(out)

    out = self.conv3(out, get_child_dict(params, 'conv3'))
    out = self.bn3(out, get_child_dict(params, 'bn3'), episode)

    x = self.res_conv(x, get_child_dict(params, 'res_conv'), episode)
    out = self.pool(self.relu(out + x))
    return out


class ResNet12(Module):
  def __init__(self, channels, bn_args, normalize=True):
    super(ResNet12, self).__init__()
    self.channels = channels

    episodic = bn_args.get('episodic') or []
    bn_args_ep, bn_args_no_ep = bn_args.copy(), bn_args.copy()
    bn_args_ep['episodic'] = True
    bn_args_no_ep['episodic'] = False
    bn_args_dict = dict()
    for i in [1, 2, 3, 4]:
      if 'layer%d' % i in episodic:
        bn_args_dict[i] = bn_args_ep
      else:
        bn_args_dict[i] = bn_args_no_ep

    self.layer1 = Block(1, channels[0], bn_args_dict[1])
    self.layer2 = Block(channels[0], channels[1], bn_args_dict[2])
    self.layer3 = Block(channels[1], channels[2], bn_args_dict[3])
    self.layer4 = Block(channels[2], channels[3], bn_args_dict[4])
    
    self.pool = nn.AdaptiveAvgPool2d(1)
    self.out_dim = channels[3]

    if normalize:
      self.l2_norm = L2_norm()
    else:
      self.l2_norm = nn.Identity()

    for m in self.modules():
      if isinstance(m, Conv2d):
        nn.init.kaiming_normal_(
          m.weight, mode='fan_out', nonlinearity='leaky_relu')
      elif isinstance(m, BatchNorm2d):
        nn.init.constant_(m.weight, 1.)
        nn.init.constant_(m.bias, 0.)

  def get_out_dim(self):
    return self.out_dim

  def forward(self, x, params=None, episode=None):
    out = self.layer1(x, get_child_dict(params, 'layer1'), episode)
    out = self.layer2(out, get_child_dict(params, 'layer2'), episode)
    out = self.layer3(out, get_child_dict(params, 'layer3'), episode)
    out = self.layer4(out, get_child_dict(params, 'layer4'), episode)
    out = self.pool(out).flatten(1)

    return self.l2_norm(out)


@register('resnet12')
def resnet12(bn_args=dict(), normalize=True):
  return ResNet12([64, 128, 256, 512], bn_args, normalize=normalize)


@register('wide-resnet12')
def wide_resnet12(bn_args=dict(), normalize=True):
  return ResNet12([64, 160, 320, 640], bn_args, normalize=normalize)




import numpy as np

import torch
from torchaudio import transforms as T



class RemovePad(object):
    def __init__(self, thershold=0.05, fs=16_000, segment_move=0.025):
        self.thershold = thershold
        segment_move = int(fs * segment_move)
        self.window = np.ones(segment_move) / int(segment_move/2)

    def __call__(self, wav):
        moving_average_wav = np.convolve(np.abs(wav), self.window, mode='same')
        cutoff = np.where(moving_average_wav > self.thershold)[0]

        if len(cutoff) < 2:
            return wav

        return wav[cutoff[0]:cutoff[-1]]


class Normalize(object):
    def __init__(self):
        self.EPS = np.finfo(float).eps
        
    def __call__(self, wav):
        samples_99_percentile = np.percentile(np.abs(wav), 99.9)
        normalized_samples = wav / (samples_99_percentile + self.EPS)
        normalized_samples = np.clip(normalized_samples, -1, 1)
        return normalized_samples


class RandomPadTrimWav(object):
    def __init__(self, segment_length=1, fs=16_000):
        self.segment_length = int(fs * segment_length)

    def __call__(self, wav):
        len_wav = len(wav)

        zeros = np.zeros(self.segment_length, dtype=np.float32)
        if len_wav < self.segment_length:
            random_point = np.random.randint(0, self.segment_length - len_wav)
            zeros[random_point:random_point+len_wav] = wav
        else:
            zeros = wav[:self.segment_length]

        return zeros


class RandomPadTrimMFCC(object):
    def __init__(self, segment_shape=(40,100)):
        self.segment_shape = segment_shape

    def __call__(self, mfcc):
        mfcc = mfcc.numpy()
        mfcc_shape = mfcc.shape

        zeros = np.zeros(self.segment_shape, dtype=np.float32)
        if mfcc_shape[1] <= self.segment_shape[1]:
            random_point = np.random.randint(0, self.segment_shape[1] - mfcc_shape[1] + 1)
            zeros[:, random_point:random_point+mfcc_shape[1]] = mfcc
        else:
            random_point = np.random.randint(0, mfcc_shape[1] - self.segment_shape[1] + 1)
            zeros = mfcc[:, random_point:random_point+self.segment_shape[1]]

        return zeros


class PadTrimMFCC(object):
    def __init__(self, segment_shape=(40,100)):
        self.segment_shape = segment_shape

    def __call__(self, mfcc):
        mfcc = mfcc.numpy()
        mfcc_shape = mfcc.shape

        zeros = np.zeros(self.segment_shape, dtype=np.float32)
        if mfcc_shape[1] <= self.segment_shape[1]:
            start_point = (self.segment_shape[1] - mfcc_shape[1]) // 2
            zeros[:, start_point:start_point+mfcc_shape[1]] = mfcc
        else:
            start_point = (mfcc_shape[1] - self.segment_shape[1]) // 2
            zeros = mfcc[:, start_point:start_point+self.segment_shape[1]]

        return zeros


class ToTensor(object):
    def __call__(self, wav):
        return torch.from_numpy(wav)


class MFCC(object):
    def __init__(self, fs=16_000, n_fft=480, hop_length=160, n_mels=128, n_mfcc=41):
        
        self.mfcc = T.MFCC(
            sample_rate=fs,
            n_mfcc=n_mfcc,
            melkwargs={
                "n_fft": n_fft,
                "n_mels": n_mels,
                "hop_length": hop_length,
                "mel_scale": "htk",
            },
        )
        
    def __call__(self, wav):
        mfcc = self.mfcc(wav)[1:]
        mfcc = mfcc - mfcc.mean(axis=1, keepdims=True)
        return mfcc / 100.0



class SpeedPerturbation(object):
    def __init__(self, scale=[0.65, 1.25], step=0.05 , p=1.0, fs=16_000):
        self.p = p
        self.t = T.SpeedPerturbation(fs, np.arange(scale[0], scale[1], step).tolist())
        
    def __call__(self, wav):
        if np.random.rand() < self.p:
            wav = self.t(wav)[0]
        return wav


class Compose(object):
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, wav):
        for transform in self.transforms:
            wav = transform(wav)

        return wav


def make_transform(shape=(40,100)):
    TRANSFORM = Compose(
        [
            Normalize(),
            #RemovePad(),
            ToTensor(),
            MFCC(),
            PadTrimMFCC(shape),
            ToTensor(),
        ]
    )
    return TRANSFORM





import os
from glob import glob
from tqdm.notebook import tqdm

import numpy as np
import librosa
import matplotlib.pyplot as plt

import torch
from einops import repeat, rearrange


CHUNCK_LENGTH = 20 # ms
SHIFT_LENGTH = 10 # ms
N_CHUNK = 35
SAMPLE_RATE = 16_000

SHIFT_LENGTH = int(SHIFT_LENGTH * SAMPLE_RATE / 1000)
WINDOW_SIZE = int(CHUNCK_LENGTH * N_CHUNK * SAMPLE_RATE / 1000)
N_MFCC = 2 * N_CHUNK

REJECT_THRESHOLD = 0.9
ACCEPT_THRESHOLD = 0.1

FILE_TYPE = ".wav"
N_SUPPORTS = -1
MODEL_PATH = "WideResNet12WithEMA.pth" # path of model

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class DummyModel(torch.nn.Module):
    def __init__(self, n_input=640, n_hidden=32, l_unknown=3):
        super().__init__()
        self.linear1 = torch.nn.Linear(n_input, n_hidden, bias=False)
        self.relu = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(n_hidden, n_hidden, bias=False)
        self.linear3 = torch.nn.Linear(n_hidden, n_input*l_unknown, bias=False)
        

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        x, _ = torch.max(x, axis=0, keepdim=True)
        x = self.linear3(x)
        return x


TRANSFORM = make_transform(shape=(40,N_MFCC))

class WordSpotting(object):
    def __init__(self,
                 support_folder,
                 model_path,
                 n_support=10,
                 file_type=".wav",
                 sample_rate=16_000,
                 gamma=3,
                 device=DEVICE):
        
        self.model_path = model_path
        self.n_support = n_support
        self.sample_rate = sample_rate
        self.gamma = gamma
        self.device = device

        self.support_filenames = glob(os.path.join(support_folder, f"*{file_type}"))
        if self.n_support < 0:
            self.n_support = len(self.support_filenames)
        
        self.read_supports()

        self.load_model()
        self.create_centers()


    def __call__(self, x):
        probs = []
        with torch.no_grad():
            for idx in [0,100,200,300, 400]: # ms
                x_ = x[int(idx*self.sample_rate/1000):]
                x_ = TRANSFORM(x_)[None, None].to(self.device)
                x_ = self.model(x_)
                
                prob = self.calculate_probability(x_).cpu().numpy().squeeze()
                probs.append(prob)
                
        probs = np.stack(probs)
        return [probs[:,0].max(), probs[:,1].min()]


    def calculate_probability(self, output_query):
        distances = torch.cdist(output_query, self.centers, p=2)
        distances = -distances / self.center_weights
        likelihood = torch.exp(distances) / torch.exp(distances).sum(axis=1, keepdim=True)
        return likelihood


    def create_centers(self):
        with torch.no_grad():
            outputs = self.model(self.SUPPORTS)

            support_center = rearrange(outputs, "(w s) e -> w s e", s=self.n_support).mean(axis=1)
            unknown_center = self.dummy_model(support_center)

            centers = torch.concat([support_center, unknown_center], axis=0)

        center_weights = torch.ones((1, centers.shape[0]))
        center_weights[:,-1] = self.gamma
        center_weights = center_weights.to(self.device)

        self.centers = centers
        self.center_weights = center_weights


    def load_model(self):
        model = wide_resnet12(normalize=False)
        model = model.to(self.device)

        dummy_model = DummyModel(l_unknown=1)
        dummy_model = dummy_model.to(self.device)

        checkpoint = torch.load(self.model_path)
        model.load_state_dict(checkpoint['model'])
        dummy_model.load_state_dict(checkpoint['dummy_model'])

        model.eval()
        dummy_model.eval()

        self.model = model
        self.dummy_model = dummy_model
        


    def read_supports(self):
        SUPPORTS = []
        for filename in self.support_filenames[:self.n_support]:
            wav, _ = librosa.load(filename, sr=self.sample_rate)
            wav = TRANSFORM(wav)
            SUPPORTS.append(wav)
            
        SUPPORTS = torch.stack(SUPPORTS, axis=0)
        SUPPORTS = torch.unsqueeze(SUPPORTS, axis=1)
        self.SUPPORTS = SUPPORTS.to(self.device)


def KWS_module(target_audio_filename, target_word):

    word_spotting = WordSpotting(support_folder=target_word,
                             model_path=MODEL_PATH,
                             n_support=N_SUPPORTS,
                             file_type=FILE_TYPE,
                             sample_rate=SAMPLE_RATE)
    
    target_wav, _ = librosa.load(target_audio_filename, sr=SAMPLE_RATE)

    PROB = []
    segment_idx = list(range(0, len(target_wav) - WINDOW_SIZE, SHIFT_LENGTH))
    for idx in tqdm(segment_idx):
        segment = target_wav[idx:idx+WINDOW_SIZE]
        prob = word_spotting(segment)
        PROB.append(prob)
    PROB = np.stack(PROB, axis=0)

    X = np.linspace(0, len(target_wav) / SAMPLE_RATE, len(segment_idx)).tolist()
    Y = np.logical_and(PROB[:,1] < REJECT_THRESHOLD, PROB[:,0] > ACCEPT_THRESHOLD)

    return X, Y

# x, y = KWS_module(target_audio_filename=audio_path, target_word=target_word)