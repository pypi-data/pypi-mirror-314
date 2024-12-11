__version__ = "5.2.0"
__all__ = ["TSkin", "TSkinConfig", "GestureConfig", "TSkinState", "Hand", "Touch", "Angle", "Gyro", "Acceleration", "Gesture", "OneFingerGesture", "TwoFingerGesture"]

import time
import logging
from typing import Optional
from multiprocessing import Pipe

from .hal import Ble
from .middleware import Tactigon_Gesture
from .models import Gesture, Touch, OneFingerGesture, TwoFingerGesture, Angle, Acceleration, Gyro, TSkinState, TSkinConfig, Hand, GestureConfig, TBleSelector

class TSkin:
    TICK: float = Ble.TICK
    _ble: Ble
    _tgesture: Optional[Tactigon_Gesture] = None
    _gesture: Optional[Gesture] = None
    _touch: Optional[Touch] = None

    config: TSkinConfig
    def __init__(self, config: TSkinConfig, debug: bool = False):
        if debug:
            logging.basicConfig(level=logging.DEBUG)

        self.config = config
        self._ble = Ble(self.config.address, self.config.hand, logging.getLogger().level)

        if self.config.gesture_config:
            _sensor_rx, self._ble._sensor_tx = Pipe(duplex=False)

            self._tgesture = Tactigon_Gesture(
                self.config.gesture_config,
                _sensor_rx,
                logging.getLogger(),
            )

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *attr):
        self.join()

    @property
    def connected(self) -> bool:
        return self._ble.connected

    @property
    def selector(self) -> Optional[TBleSelector]:
        return self._ble.selector
      
    @property
    def angle(self) -> Optional[Angle]:
        return self._ble.angle
    
    @property
    def acceleration(self) -> Optional[Acceleration]:
        return self._ble.acceleration
    
    @property
    def gyro(self) -> Optional[Gyro]:
        return self._ble.gyro
    
    @property
    def battery(self) -> float:
        return self._ble.battery

    @property
    def touch(self) -> Optional[Touch]:
        if self._touch:
            t = self._ble.touch
            self._touch = None
        else:
            t = self._ble.touch

        return t
    
    @property
    def touch_preserve(self) -> Optional[Touch]:
        if not self._touch:
            self._touch = self._ble.touch

        return self._touch

    @property
    def gesture(self) -> Optional[Gesture]:
        if not self._tgesture:
            return None
        
        if self._gesture:
            g = self._gesture
            self._gesture = None
        else:
            g = self._tgesture.gesture()
        
        return g
    
    @property
    def gesture_preserve(self) -> Optional[Gesture]:
        if not self._tgesture:
            return None
        
        if not self._gesture:
            self._gesture = self._tgesture.gesture()
            
        return self._gesture
    
    @property
    def state(self) -> TSkinState:
        return TSkinState(
            self._ble.connected,
            self._ble.battery,
            self._ble.selector,
            self._ble.touch,
            self._ble.angle,
            self.gesture,
        )
    
    @property
    def state_preserve_gesture(self) -> TSkinState:
        return TSkinState(
            self._ble.connected,
            self._ble.battery,
            self._ble.selector,
            self._ble.touch,
            self._ble.angle,
            self.gesture_preserve,
        )
    
    def __str__(self):
        return "TSkin(name='{0}', address='{1}', gesture={2})".format(self.config.name, self.config.address, self.config.gesture_config)

    def start(self):
        if self._tgesture:
            self._tgesture.start()
        self._ble.select_sensors()
        self._ble.start()

    def join(self, timeout: Optional[float] = None):
        if self._tgesture:
            self._tgesture.terminate()
        self._ble.join(5)

    def terminate(self):
        self.join()

    def select_sensors(self):
        self._ble.select_sensors()

    def select_audio(self):
        self._ble.select_audio()
