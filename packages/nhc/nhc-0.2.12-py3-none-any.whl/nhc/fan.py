from .action import NHCAction
from .const import PRESET_MODES

class NHCFan(NHCAction):
  def __init__(self, controller, action):
    super().__init__(controller, action)

  @property
  def mode(self) -> str:
    for mode, value in PRESET_MODES.items():
        if value == self._state:
            return mode

    return PRESET_MODES['low']

  def set_mode(self, speed: str):
      return self._controller.execute(self.id, PRESET_MODES[speed])
