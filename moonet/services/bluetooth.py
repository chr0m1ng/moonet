import subprocess

from ..config import DefaultConfig


def bt_reconnect(mac: str | None = DefaultConfig.DEFAULT_BT_MAC) -> bool:
  """Attempt to (re)connect a known Bluetooth speaker using bluetoothctl.
  Returns True if the command exits with code 0.
  """
  mac = mac or DefaultConfig.DEFAULT_BT_MAC
  cmd = f"bluetoothctl connect {mac} || (bluetoothctl power on && bluetoothctl connect {mac})"
  return subprocess.call(["bash", "-lc", cmd]) == 0
