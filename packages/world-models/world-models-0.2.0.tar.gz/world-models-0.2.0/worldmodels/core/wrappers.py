import functools
import time

import elements
import numpy as np


class Wrapper:

  def __init__(self, env):
    self.env = env

  def __len__(self):
    return len(self.env)

  def __bool__(self):
    return bool(self.env)

  def __getattr__(self, name):
    if name.startswith('__'):
      raise AttributeError(name)
    try:
      return getattr(self.env, name)
    except AttributeError:
      raise ValueError(name)


class TimeLimit(Wrapper):

  def __init__(self, env, duration, reset=True):
    super().__init__(env)
    self._duration = duration
    self._reset = reset
    self._step = 0
    self._done = False

  def step(self, action):
    if action['reset'] or self._done:
      self._step = 0
      self._done = False
      if self._reset:
        action.update(reset=True)
        return self.env.step(action)
      else:
        action.update(reset=False)
        obs = self.env.step(action)
        obs['is_first'] = True
        return obs
    self._step += 1
    obs = self.env.step(action)
    if self._duration and self._step >= self._duration:
      obs['is_last'] = True
    self._done = obs['is_last']
    return obs


class ActionRepeat(Wrapper):

  def __init__(self, env, repeat):
    super().__init__(env)
    self._repeat = repeat

  def step(self, action):
    if action['reset']:
      return self.env.step(action)
    reward = 0.0
    for _ in range(self._repeat):
      obs = self.env.step(action)
      reward += obs['reward']
      if obs['is_last'] or obs['is_terminal']:
        break
    obs['reward'] = np.float32(reward)
    return obs


class ClipAction(Wrapper):

  def __init__(self, env, key='action', low=-1, high=1):
    super().__init__(env)
    self._key = key
    self._low = low
    self._high = high

  def step(self, action):
    clipped = np.clip(action[self._key], self._low, self._high)
    return self.env.step({**action, self._key: clipped})


class NormalizeAction(Wrapper):

  def __init__(self, env, key='action'):
    super().__init__(env)
    self._key = key
    self._space = env.act_space[key]
    self._mask = np.isfinite(self._space.low) & np.isfinite(self._space.high)
    self._low = np.where(self._mask, self._space.low, -1)
    self._high = np.where(self._mask, self._space.high, 1)

  @functools.cached_property
  def act_space(self):
    low = np.where(self._mask, -np.ones_like(self._low), self._low)
    high = np.where(self._mask, np.ones_like(self._low), self._high)
    space = elements.Space(np.float32, self._space.shape, low, high)
    return {**self.env.act_space, self._key: space}

  def step(self, action):
    orig = (action[self._key] + 1) / 2 * (self._high - self._low) + self._low
    orig = np.where(self._mask, orig, action[self._key])
    return self.env.step({**action, self._key: orig})


# class ExpandScalars(Wrapper):
#
#   def __init__(self, env):
#     super().__init__(env)
#     self._obs_expanded = []
#     self._obs_space = {}
#     for key, space in self.env.obs_space.items():
#       if space.shape == () and key != 'reward' and not space.discrete:
#         space = elements.Space(space.dtype, (1,), space.low, space.high)
#         self._obs_expanded.append(key)
#       self._obs_space[key] = space
#     self._act_expanded = []
#     self._act_space = {}
#     for key, space in self.env.act_space.items():
#       if space.shape == () and not space.discrete:
#         space = elements.Space(space.dtype, (1,), space.low, space.high)
#         self._act_expanded.append(key)
#       self._act_space[key] = space
#
#   @functools.cached_property
#   def obs_space(self):
#     return self._obs_space
#
#   @functools.cached_property
#   def act_space(self):
#     return self._act_space
#
#   def step(self, action):
#     action = {
#         key: np.squeeze(value, 0) if key in self._act_expanded else value
#         for key, value in action.items()}
#     obs = self.env.step(action)
#     obs = {
#         key: np.expand_dims(value, 0) if key in self._obs_expanded else value
#         for key, value in obs.items()}
#     return obs
#
#
# class FlattenTwoDimObs(Wrapper):
#
#   def __init__(self, env):
#     super().__init__(env)
#     self._keys = []
#     self._obs_space = {}
#     for key, space in self.env.obs_space.items():
#       if len(space.shape) == 2:
#         space = elements.Space(
#             space.dtype,
#             (int(np.prod(space.shape)),),
#             space.low.flatten(),
#             space.high.flatten())
#         self._keys.append(key)
#       self._obs_space[key] = space
#
#   @functools.cached_property
#   def obs_space(self):
#     return self._obs_space
#
#   def step(self, action):
#     obs = self.env.step(action).copy()
#     for key in self._keys:
#       obs[key] = obs[key].flatten()
#     return obs
#
#
# class FlattenTwoDimActions(Wrapper):
#
#   def __init__(self, env):
#     super().__init__(env)
#     self._origs = {}
#     self._act_space = {}
#     for key, space in self.env.act_space.items():
#       if len(space.shape) == 2:
#         space = elements.Space(
#             space.dtype,
#             (int(np.prod(space.shape)),),
#             space.low.flatten(),
#             space.high.flatten())
#         self._origs[key] = space.shape
#       self._act_space[key] = space
#
#   @functools.cached_property
#   def act_space(self):
#     return self._act_space
#
#   def step(self, action):
#     action = action.copy()
#     for key, shape in self._origs.items():
#       action[key] = action[key].reshape(shape)
#     return self.env.step(action)


class UnifyDtypes(Wrapper):

  def __init__(self, env):
    super().__init__(env)
    self._obs_space, _, self._obs_outer = self._convert(env.obs_space)
    self._act_space, self._act_inner, _ = self._convert(env.act_space)

  @property
  def obs_space(self):
    return self._obs_space

  @property
  def act_space(self):
    return self._act_space

  def step(self, action):
    action = action.copy()
    for key, dtype in self._act_inner.items():
      action[key] = np.asarray(action[key], dtype)
    obs = self.env.step(action)
    for key, dtype in self._obs_outer.items():
      obs[key] = np.asarray(obs[key], dtype)
    return obs

  def _convert(self, spaces):
    results, befores, afters = {}, {}, {}
    for key, space in spaces.items():
      before = after = space.dtype
      if np.issubdtype(before, np.floating):
        after = np.float32
      elif np.issubdtype(before, np.uint8):
        after = np.uint8
      elif np.issubdtype(before, np.integer):
        after = np.int32
      befores[key] = before
      afters[key] = after
      results[key] = elements.Space(after, space.shape, space.low, space.high)
    return results, befores, afters


class CheckSpaces(Wrapper):

  def __init__(self, env):
    assert not (env.obs_space.keys() & env.act_space.keys()), (
        env.obs_space.keys(), env.act_space.keys())
    super().__init__(env)

  def step(self, action):
    for key, value in action.items():
      self._check(value, self.env.act_space[key], key)
    obs = self.env.step(action)
    for key, value in obs.items():
      self._check(value, self.env.obs_space[key], key)
    return obs

  def _check(self, value, space, key):
    if not isinstance(value, (
        np.ndarray, np.generic, list, tuple, int, float, bool)):
      raise TypeError(f'Invalid type {type(value)} for key {key}.')
    if value in space:
      return
    dtype = np.array(value).dtype
    shape = np.array(value).shape
    lowest, highest = np.min(value), np.max(value)
    raise ValueError(
        f"Value for '{key}' with dtype {dtype}, shape {shape}, "
        f"lowest {lowest}, highest {highest} is not in {space}.")


class DiscretizeAction(Wrapper):

  def __init__(self, env, key='action', bins=5):
    super().__init__(env)
    self._dims = np.squeeze(env.act_space[key].shape, 0).item()
    self._values = np.linspace(-1, 1, bins)
    self._key = key

  @functools.cached_property
  def act_space(self):
    space = elements.Space(np.int32, self._dims, 0, len(self._values))
    return {**self.env.act_space, self._key: space}

  def step(self, action):
    continuous = np.take(self._values, action[self._key])
    return self.env.step({**action, self._key: continuous})


class ResizeImage(Wrapper):

  def __init__(self, env, size=(64, 64)):
    super().__init__(env)
    self._size = size
    self._keys = [
        k for k, v in env.obs_space.items()
        if len(v.shape) > 1 and v.shape[:2] != size]
    print(f'Resizing keys {",".join(self._keys)} to {self._size}.')
    if self._keys:
      from PIL import Image
      self._Image = Image

  @functools.cached_property
  def obs_space(self):
    spaces = self.env.obs_space
    for key in self._keys:
      shape = self._size + spaces[key].shape[2:]
      spaces[key] = elements.Space(np.uint8, shape)
    return spaces

  def step(self, action):
    obs = self.env.step(action)
    for key in self._keys:
      obs[key] = self._resize(obs[key])
    return obs

  def _resize(self, image):
    image = self._Image.fromarray(image)
    image = image.resize(self._size, self._Image.NEAREST)
    image = np.array(image)
    return image


# class RenderImage(Wrapper):
#
#   def __init__(self, env, key='image'):
#     super().__init__(env)
#     self._key = key
#     self._shape = self.env.render().shape
#
#   @functools.cached_property
#   def obs_space(self):
#     spaces = self.env.obs_space
#     spaces[self._key] = elements.Space(np.uint8, self._shape)
#     return spaces
#
#   def step(self, action):
#     obs = self.env.step(action)
#     obs[self._key] = self.env.render()
#     return obs


class BackwardReturn(Wrapper):

  def __init__(self, env, horizon):
    super().__init__(env)
    self._discount = 1 - 1 / horizon
    self._bwreturn = 0.0

  @functools.cached_property
  def obs_space(self):
    return {
        **self.env.obs_space,
        'bwreturn': elements.Space(np.float32),
    }

  def step(self, action):
    obs = self.env.step(action)
    self._bwreturn *= (1 - obs['is_first']) * self._discount
    self._bwreturn += obs['reward']
    obs['bwreturn'] = np.float32(self._bwreturn)
    return obs


class AddObs(Wrapper):

  def __init__(self, env, key, value, space):
    super().__init__(env)
    self._key = key
    self._value = value
    self._space = space

  @functools.cached_property
  def obs_space(self):
    return {
        **self.env.obs_space,
        self._key: self._space,
    }

  def step(self, action):
    obs = self.env.step(action)
    obs[self._key] = self._value
    return obs


class RestartOnException(Wrapper):

  def __init__(
      self, ctor, exceptions=(Exception,), window=300, maxfails=2, wait=20):
    if not isinstance(exceptions, (tuple, list)):
        exceptions = [exceptions]
    self._ctor = ctor
    self._exceptions = tuple(exceptions)
    self._window = window
    self._maxfails = maxfails
    self._wait = wait
    self._last = time.time()
    self._fails = 0
    super().__init__(self._ctor())

  def step(self, action):
    try:
      return self.env.step(action)
    except self._exceptions as e:
      if time.time() > self._last + self._window:
        self._last = time.time()
        self._fails = 1
      else:
        self._fails += 1
      if self._fails > self._maxfails:
        raise RuntimeError('The env crashed too many times.')
      message = f'Restarting env after crash with {type(e).__name__}: {e}'
      print(message, flush=True)
      time.sleep(self._wait)
      self.env = self._ctor()
      action['reset'] = np.ones_like(action['reset'])
      return self.env.step(action)
