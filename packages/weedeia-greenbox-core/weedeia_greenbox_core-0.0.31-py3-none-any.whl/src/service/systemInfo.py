from ..pin.gpio import gpio
from ..service.lightMotor import lightMotorService

class SystemInfoService:
  def get_data(self):
    data = gpio.read_sensors()
    data["lightMotorPosition"] = lightMotorService.current_poss
    data["lightMotorStatus"] = lightMotorService.state
    return data


systemInfoService = SystemInfoService()