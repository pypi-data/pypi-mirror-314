class ComponentError(Exception):
  def __init__(self, httpCode, errorMessage):
    self.httpCode = httpCode
    self.errorMessage = errorMessage

class LowWaterError(ComponentError):
  def __init__(self):
    super().__init__(400, "low_water_detected")

class LightMotorIsMovingError(ComponentError):
  def __init__(self):
    super().__init__(400, "light_motor_is_moving")