from tinydb import TinyDB, Query
from threading import Thread
import time
from pydantic import BaseModel
from ..pin.gpio import gpio
from ..util.errors import LightMotorIsMovingError

LIGHT_MOTOR_STATE_MOVING = "MOVING"
LIGHT_MOTOR_STATE_STOPPED = "STOPPED"

class MoveToRequest(BaseModel):
  target: int
  distance: int
  cycle: float

class LightMotorService:

  def __init__(self) :
    self.db = TinyDB('light_motor_position-table.json')
    last_poss = self._load_position()
    self.current_poss = last_poss
    self.state = LIGHT_MOTOR_STATE_STOPPED

  def _save_position(self, position : int):
    self.current_poss = position
    self.db.truncate()
    self.db.insert({'position': position})

  def _load_position(self):
    Motor = Query()
    if self.db.search(Motor.position.exists()):
        return self.db.all()[-1]['position']
    else:
        return 0

  def reset(self):
    if (self.state == LIGHT_MOTOR_STATE_MOVING):
      raise LightMotorIsMovingError()
    
    self.state = LIGHT_MOTOR_STATE_MOVING
    job = Thread(target=self.__job_reset)
    job.setDaemon(True)
    job.start()


  def move_to(self, move_data : MoveToRequest):
    if (self.state == LIGHT_MOTOR_STATE_MOVING):
       raise LightMotorIsMovingError()
    
    if move_data.target == self.current_poss:
      return
     
    self.state = LIGHT_MOTOR_STATE_MOVING

    up = self.current_poss > move_data.target

    job = Thread(target=self.__job_move_to, args=(up, move_data.target, move_data.distance, move_data.cycle))
    job.setDaemon(True)
    job.start()
     
  def __job_move_to(self, up: bool, target_poss: int, distance: int, cycle: int):
    print("Job move to started with params:", self.current_poss, up, target_poss, distance, cycle)
    if up:
      if gpio.is_light_motor_limit_switch_pressed():
        self._save_position(0)
        self.state = LIGHT_MOTOR_STATE_STOPPED
        return

      gpio.set_lightMotorUp()

    else:
      gpio.set_lightMotorDown()

    dir = -1 if up else 1

    while (self.current_poss > target_poss) if up else (self.current_poss < target_poss):
      time.sleep(cycle)
      new_poss = self.current_poss + (distance * dir)
      self._save_position(new_poss)

    print("Job move to completed")
    gpio.set_lightMotorStop()
    self.state = LIGHT_MOTOR_STATE_STOPPED

  def __job_reset(self):
    print("Job reset started")
    if not gpio.is_light_motor_limit_switch_pressed():
      gpio.set_lightMotorUp()
      while not gpio.is_light_motor_limit_switch_pressed():
        time.sleep(0.1)
    
    gpio.set_lightMotorStop()
    self._save_position(0)
    self.state = LIGHT_MOTOR_STATE_STOPPED
    print("Job reset completed")

lightMotorService = LightMotorService()