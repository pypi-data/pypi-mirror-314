from ..util import constants
from ..util.errors import LowWaterError
from pydantic import BaseModel
import RPi.GPIO as GPIO
import adafruit_dht
import board
from threading import Thread
import os
import time

HUMIDIFIER = 12
IRRIGATOR = 23
AIR_CONDITIONING = 27
CULTIVATION_LIGHT = 17
READY_LIGHT = 24
LOW_WATHER_LIGHT = 25
DOOR = 4
LIGHT_MOTOR_UP = 16
LIGHT_MOTOR_DOWN = 20
EXTRATOR_FAN = 26
LIGHT_MOTOR_LIMIT_SWITCH = 21
WATER_LEVEL_SENSOR = 22
VENTILATION = 19

THR1 = board.D5
THR2 = board.D6
THR3 = board.D13

def _set_pin_output_high(pin : int, high: bool):
  GPIO.output(pin, GPIO.HIGH if high else GPIO.LOW)

def _is_on(active : str):
  return True if active == constants.ACTIVE_ON else False

def _is_pressed(pin: int):
  return GPIO.input(pin) == GPIO.LOW

def _is_high(pin: int):
  return GPIO.input(pin) == GPIO.HIGH

class AirChange(BaseModel):
  ventilation_power: int
  extractor_fan: str

class GpioService :

  def __init__(self):
    self.ventilationPower = 0
    self.thr_data = {
      "thr1" : {
        "temperature" : 0,
        "humidity" : 0,
        "err" : ""
      },
      "thr2" : {
        "temperature" : 0,
        "humidity" : 0,
        "err" : ""
      },
      "thr3" : {
        "temperature" : 0,
        "humidity" : 0,
        "err" : ""
      }
    }
    self.thr_thread_stop = False

  def setup(self):
    print('GPIO configuration - Started')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(HUMIDIFIER, GPIO.OUT)
    GPIO.setup(IRRIGATOR, GPIO.OUT)
    GPIO.setup(AIR_CONDITIONING, GPIO.OUT)
    GPIO.setup(CULTIVATION_LIGHT, GPIO.OUT)
    GPIO.setup(READY_LIGHT, GPIO.OUT)
    GPIO.setup(LOW_WATHER_LIGHT, GPIO.OUT)
    GPIO.setup(LIGHT_MOTOR_UP, GPIO.OUT)
    GPIO.setup(LIGHT_MOTOR_DOWN, GPIO.OUT)
    GPIO.setup(EXTRATOR_FAN, GPIO.OUT)
    GPIO.setup(VENTILATION, GPIO.OUT)

    GPIO.setup(WATER_LEVEL_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DOOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LIGHT_MOTOR_LIMIT_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print('GPIO configuration - Done')

    self.use_dht_22 = os.getenv('USE_DHT_22', 'NO') == 'YES'
    self.thr1_active = os.getenv('THR1_ACTIVE', 'OFF') == 'ON'
    self.thr2_active = os.getenv('THR2_ACTIVE', 'OFF') == 'ON'
    self.thr3_active = os.getenv('THR3_ACTIVE', 'OFF') == 'ON'

    if(self.use_dht_22):
        self.thr1 = adafruit_dht.DHT22(THR1) if self.thr1_active else None
        self.thr2 = adafruit_dht.DHT22(THR2) if self.thr2_active else None
        self.thr3 = adafruit_dht.DHT22(THR3) if self.thr3_active else None
    else:
        self.thr1 = adafruit_dht.DHT11(THR1) if self.thr1_active else None
        self.thr2 = adafruit_dht.DHT11(THR2) if self.thr2_active else None
        self.thr3 = adafruit_dht.DHT11(THR3) if self.thr3_active else None

    self.ventilationPwn = GPIO.PWM(VENTILATION, 20000)

    self.thr_thread = Thread(target=self.__read_temperature_humidity_job)
    self.thr_thread.setDaemon(True)
    self.thr_thread.start()

  def cleanUp(self):
    GPIO.cleanup()
  
  def __read_temperature_humidity_job(self) :
    while not self.thr_thread_stop:
      time.sleep(10)
      self.read_temperature_humidity()
      time.sleep(290)
  
  def read_temperature_humidity(self):
    thr1 = self.read_temperature_humidity_from(self.thr1_active, self.thr1, {
      "temperature" : 0,
      "humidity" : 0,
      "err" : "OFF"
    })
    thr2 = self.read_temperature_humidity_from(self.thr2_active, self.thr2, thr1)
    thr3 = self.read_temperature_humidity_from(self.thr3_active, self.thr3, thr1)

    self.thr_data = {
        "thr1" : thr1,
        "thr2" : thr2,
        "thr3" : thr3
    }
  
  def read_temperature_humidity_from(self, isOn, thr, default):
    if isOn:
      try:
        return {
          "temperature" : thr.temperature,
          "humidity" : thr.humidity
        }
      except Exception as e:
        return {
          "temperature" : 0,
          "humidity" : 0,
          "err" : f"{e}"
        }
    else:
      return default

  def read_sensors(self):
    isLowWater = _is_pressed(WATER_LEVEL_SENSOR)

    if isLowWater:
      self.set_irrigator(constants.ACTIVE_OFF)
      self.set_humidifier(constants.ACTIVE_OFF)
      self.set_LowWaterLight(constants.ACTIVE_ON)
    else:
      self.set_LowWaterLight(constants.ACTIVE_OFF)
    
    return {
        "isLowWater" : _is_pressed(WATER_LEVEL_SENSOR),
        "isDoorOpen" :  not _is_pressed(DOOR),
        "isCultivationLightOn": _is_high(CULTIVATION_LIGHT),
        "isAirConditioningOn": _is_high(AIR_CONDITIONING),
        "isIrrigatorOn" : _is_high(IRRIGATOR),
        "isHumidifierOn" : _is_high(HUMIDIFIER),
        "isExtratorFanOn" : _is_high(EXTRATOR_FAN),
        "ventilationPower": self.ventilationPower,
        "th" : self.thr_data
    }
  def set_ventilation(self, percentage : int):
    if percentage <=0:
      self.ventilationPwn.stop()
      self.ventilationPower = 0
    else:
      self.ventilationPwn.stop()
      self.ventilationPower = percentage
      self.ventilationPwn.start(percentage)

  def is_light_motor_limit_switch_pressed(self):
    return _is_pressed(LIGHT_MOTOR_LIMIT_SWITCH)

  def set_ReadyLight(self, active : str) :
    _set_pin_output_high(READY_LIGHT, _is_on(active))

  def set_LowWaterLight(self, active : str) :
    _set_pin_output_high(LOW_WATHER_LIGHT, _is_on(active))

  def set_cultivationLight(self, active : str) :
    _set_pin_output_high(CULTIVATION_LIGHT, _is_on(active))

  def set_air_conditioning(self, active : str) :
    _set_pin_output_high(AIR_CONDITIONING, _is_on(active))

  def set_irrigator(self, active : str) :
    if _is_pressed(WATER_LEVEL_SENSOR) and active == constants.ACTIVE_ON:
      raise LowWaterError()
    
    _set_pin_output_high(IRRIGATOR, _is_on(active))

  def set_humidifier(self, active : str) :
    if _is_pressed(WATER_LEVEL_SENSOR) and active == constants.ACTIVE_ON:
      raise LowWaterError()
    
    _set_pin_output_high(HUMIDIFIER, _is_on(active))

  def set_lightMotorUp(self) :
      _set_pin_output_high(LIGHT_MOTOR_DOWN, False)
      _set_pin_output_high(LIGHT_MOTOR_UP, True)

  def set_lightMotorDown(self) :
      _set_pin_output_high(LIGHT_MOTOR_UP, False)
      _set_pin_output_high(LIGHT_MOTOR_DOWN, True)

  def set_lightMotorStop(self) :
      _set_pin_output_high(LIGHT_MOTOR_UP, False)
      _set_pin_output_high(LIGHT_MOTOR_DOWN, False)

  def set_extratorFan(self, active : str) :
    _set_pin_output_high(EXTRATOR_FAN, _is_on(active))

  def set_air_change(self, request: AirChange):
    self.set_extratorFan(request.extractor_fan)
    self.set_ventilation(request.ventilation_power)
  
gpio = GpioService()