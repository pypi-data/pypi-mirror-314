class Env:

  def __repr__(self):
    return (
        f'{self.__class__.__name__}('
        f'obs_space={self.obs_space}, '
        f'act_space={self.act_space})')

  @property
  def obs_space(self):
    # The observation space must contain the keys is_first, is_last, and
    # is_terminal. Commonly, it also contains the keys reward and image. By
    # convention, keys starting with 'log/' are not consumed by the agent.
    raise NotImplementedError('Returns: dict of spaces')

  @property
  def act_space(self):
    # The action space must contain the reset key as well as any actions.
    raise NotImplementedError('Returns: dict of spaces')

  def step(self, action):
    raise NotImplementedError('Returns: dict')

  def close(self):
    pass


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
