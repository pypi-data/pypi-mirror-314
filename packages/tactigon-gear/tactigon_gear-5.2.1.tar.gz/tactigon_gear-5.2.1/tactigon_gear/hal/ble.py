import time
import struct
import math
import ctypes
import asyncio

from bleak import BleakClient
from multiprocessing import Process, Event, Lock, Value, log_to_stderr
from multiprocessing.synchronize import Event as EventClass, Lock as LockClass
from multiprocessing.sharedctypes import SynchronizedBase
from multiprocessing.connection import _ConnectionBase

from typing import Optional, Tuple, Any

from ..models import  TBleSelector, Hand, Angle, Acceleration, Touch, Gyro, OneFingerGesture, TwoFingerGesture
from ..middleware.Tactigon_Audio import ADPCMEngine

class Ble(Process):
    TICK: float = 0.02
    _RECONNECT_TIMEOUT: float = 0.1
    SENSORS_UUID: str = "bea5760d-503d-4920-b000-101e7306b005"
    TOUCHPAD_UUID: str = "bea5760d-503d-4920-b000-101e7306b009"
    AUDIO_DATA_UUID: str = "08000000-0001-11e1-ac36-0002a5d5c51b"
    AUDIO_SYNC_UUID: str = "40000000-0001-11e1-ac36-0002a5d5c51b"

    address: str
    hand: Hand

    _connected: EventClass
    _is_running: EventClass
    _selector_audio: EventClass
    _selector_sensor: EventClass

    # selector: TBleSelector
    
    _sensor_tx: Optional[_ConnectionBase] = None
    _angle_tx: Optional[_ConnectionBase] = None
    _audio_tx: Optional[_ConnectionBase] = None

    _stop_event: SynchronizedBase
    _roll: SynchronizedBase
    _pitch: SynchronizedBase
    _yaw: SynchronizedBase

    _accX: SynchronizedBase
    _accY: SynchronizedBase
    _accZ: SynchronizedBase

    _gyroX: SynchronizedBase
    _gyroY: SynchronizedBase
    _gyroZ: SynchronizedBase

    _one_finger: SynchronizedBase
    _two_finger: SynchronizedBase
    _x_pos: SynchronizedBase
    _y_pos: SynchronizedBase

    _battery: SynchronizedBase

    # _angle: Optional[Angle] = None
    # _acceleration: Optional[Acceleration] = None
    # _gyro: Optional[Gyro] = None
    # _battery: float = 0
    # _touch: Optional[Touch] = None

    adpcm_engine: ADPCMEngine

    def __init__(self, address: str, hand: Hand, logger_level: int):
        Process.__init__(self)

        self.logger = log_to_stderr()
        self.logger.setLevel(logger_level)

        self.logger.debug("Starting Tactigon Gear")

        self.address = address
        self.hand = hand

        self._stop_event =  Value(ctypes.c_bool, 0)
        self._is_running = Event()
        self._connected = Event()

        self._selector_audio = Event()
        self._selector_sensor = Event()

        self._roll = Value(ctypes.c_float, 0)
        self._pitch = Value(ctypes.c_float, 0)
        self._yaw = Value(ctypes.c_float, 0)

        self._accX = Value(ctypes.c_float, 0)
        self._accY = Value(ctypes.c_float, 0)
        self._accZ = Value(ctypes.c_float, 0)

        self._gyroX = Value(ctypes.c_float, 0)
        self._gyroY = Value(ctypes.c_float, 0)
        self._gyroZ = Value(ctypes.c_float, 0)

        self._one_finger = Value(ctypes.c_int, 0)
        self._two_finger = Value(ctypes.c_int, 0)
        self._x_pos = Value(ctypes.c_float, 0)
        self._y_pos = Value(ctypes.c_float, 0)

        self._battery = Value(ctypes.c_int, 0)

    @staticmethod
    def gravity_comp(hand: Hand, accX: float, accY: float, accZ: float, gyroX: float, gyroY: float, gyroZ: float, roll: float, pitch: float, yaw: float):
        """gravity compensation"""
        G_CONST = 9.81
        ANG_TO_RAD = math.pi / 180
        ACC_RATIO = 1000
        VEL_RATIO = 30

        if hand == Hand.LEFT:
            accX = -accX / ACC_RATIO
            accY = -accY / ACC_RATIO
            accZ = -accZ / ACC_RATIO

            gyroX = -gyroX / VEL_RATIO
            gyroY = -gyroY / VEL_RATIO
            gyroZ = -gyroZ / VEL_RATIO

            _pitch = roll * ANG_TO_RAD
            _roll = pitch * ANG_TO_RAD

        else:
            accX = accX / ACC_RATIO
            accY = accY / ACC_RATIO
            accZ = -accZ / ACC_RATIO

            gyroX = gyroX / VEL_RATIO
            gyroY = gyroY / VEL_RATIO
            gyroZ = -gyroZ / VEL_RATIO

            _pitch = -roll * ANG_TO_RAD
            _roll = -pitch * ANG_TO_RAD

        if accZ == 0:
            beta = math.pi / 2
        else:
            beta = math.atan(
                math.sqrt(math.pow(accX, 2) + math.pow(accY, 2)) / accZ
            )

        accX = accX - G_CONST * math.sin(_roll)
        accY = accY + G_CONST * math.sin(_pitch)
        accZ = accZ - G_CONST * math.cos(beta)

        return accX, accY, accZ, gyroX, gyroY, gyroZ, roll, pitch, yaw

    @property
    def is_running(self) -> bool:
        return self._is_running.is_set()

    @property
    def connected(self) -> bool:
        return self._connected.is_set()
    
    @property
    def angle(self) -> Optional[Angle]:
        if self._selector_sensor.is_set():
            with self._roll.get_lock() and self._pitch.get_lock() and self._yaw.get_lock():
                return Angle(
                    self._roll.get_obj().value,
                    self._pitch.get_obj().value,
                    self._yaw.get_obj().value,
                )
            
        return None

    @property
    def gyro(self) -> Optional[Gyro]:
        if self._selector_sensor.is_set():
            with self._gyroX.get_lock() and self._gyroY.get_lock() and self._gyroZ.get_lock():
                return Gyro(
                    self._gyroX.get_obj().value,
                    self._gyroY.get_obj().value,
                    self._gyroZ.get_obj().value,
                )
            
        return None

    @property
    def acceleration(self) -> Optional[Acceleration]:
        if self._selector_sensor.is_set():
            with self._accX.get_lock() and self._accY.get_lock() and self._accZ.get_lock():
                return Acceleration(
                    self._accX.get_obj().value,
                    self._accY.get_obj().value,
                    self._accZ.get_obj().value,
                )
            
        return None
    
    @property
    def touch(self) -> Optional[Touch]:
        with self._one_finger.get_lock() and self._two_finger.get_lock() and self._x_pos.get_lock() and self._y_pos.get_lock():

            one_finger_g = OneFingerGesture(self._one_finger.get_obj().value)
            two_finger_g = TwoFingerGesture(self._two_finger.get_obj().value)
            x_p = self._x_pos.get_obj().value
            y_p = self._y_pos.get_obj().value

            self._one_finger.get_obj().value = 0
            self._two_finger.get_obj().value = 0
            self._x_pos.get_obj().value = 0
            self._y_pos.get_obj().value = 0

        if one_finger_g == OneFingerGesture.NONE and two_finger_g == TwoFingerGesture.NONE:
            return None
        
        return Touch(one_finger_g, two_finger_g, x_p, y_p)
    
    @property
    def battery(self) -> float:
        return round(self._battery.get_obj().value / 1000, 2)
    
    @property
    def selector(self) -> Optional[TBleSelector]:
        if self._selector_sensor.is_set():
            return TBleSelector.SENSORS
        
        if self._selector_audio.is_set():
            return TBleSelector.AUDIO
        
        return None
    
    def handle_audio_sync(self, char, data: bytearray):
        pass

    def handle_audio(self, char, data: bytearray):
        if self._audio_tx:
            self._audio_tx.send_bytes(self.adpcm_engine.extract_data(data))

    def handle_sensors(self, char, data:bytearray):
        accX = float(struct.unpack("h", data[0:2])[0])
        accY = float(struct.unpack("h", data[2:4])[0])
        accZ = float(struct.unpack("h", data[4:6])[0])
        
        gyroX = float(struct.unpack("h", data[6:8])[0])
        gyroY = float(struct.unpack("h", data[8:10])[0])
        gyroZ = float(struct.unpack("h", data[10:12])[0])
        
        roll = float(struct.unpack("h", data[12:14])[0])
        pitch = float(struct.unpack("h", data[14:16])[0])
        yaw = float(struct.unpack("h", data[16:18])[0])

        battery = int(struct.unpack("h", data[18:20])[0])

        accX, accY, accZ, gyroX, gyroY, gyroZ, roll, pitch, yaw = self.gravity_comp(self.hand, accX, accY, accZ, gyroX, gyroY, gyroZ, roll, pitch, yaw)

        with self._roll.get_lock() and self._pitch.get_lock() and self._yaw.get_lock():
            self._roll.get_obj().value = roll
            self._pitch.get_obj().value = pitch
            self._yaw.get_obj().value = yaw

        with self._accX.get_lock() and self._accY.get_lock() and self._accZ.get_lock():
            self._accX.get_obj().value = accX
            self._accY.get_obj().value = accY
            self._accZ.get_obj().value = accZ

        with self._gyroX.get_lock() and self._gyroY.get_lock() and self._gyroZ.get_lock():
            self._gyroX.get_obj().value = gyroX
            self._gyroY.get_obj().value = gyroY
            self._gyroZ.get_obj().value = gyroZ

        with self._battery.get_lock():
            self._battery.get_obj().value = battery

        if self._sensor_tx:
            self._sensor_tx.send([accX, accY, accZ, gyroX, gyroY, gyroZ])

        if self._angle_tx:
            self._angle_tx.send([roll, pitch, yaw])

    def handle_touchpad(self, char, data: bytearray):
        with self._one_finger.get_lock() and self._two_finger.get_lock() and self._x_pos.get_lock() and self._y_pos.get_lock():
            self._one_finger.get_obj().value = int.from_bytes(data[0:1], "big")
            self._two_finger.get_obj().value = int.from_bytes(data[1:2], "big")
            self._x_pos.get_obj().value = float(struct.unpack("h", data[2:4])[0])
            self._y_pos.get_obj().value = float(struct.unpack("h", data[4:6])[0])

    def start(self):
        self.logger.debug("[BLE] BLE starting on address %s", self.address)
        Process.start(self)

    def join(self, timeout: Optional[float] = None):
        self.logger.debug("[BLE] Stopping BLE on address %s", self.address)
        self._stop_event.get_obj().value = 1

        if timeout:
            _t = 0
            while _t < timeout:
                if not self._is_running.is_set():
                    break
                time.sleep(self.TICK)
                _t += self.TICK

        Process.join(self, timeout)

        if self.is_alive():
            Process.terminate(self)

    def run(self):
        self._is_running.set()
        self.adpcm_engine = ADPCMEngine()
        
        loop = asyncio.get_event_loop()
        main_task = loop.create_task(self.task())
        loop.run_until_complete(main_task)

        self._is_running.clear()

    async def task(self):
        running_selector: Optional[TBleSelector] = None
        while not self._stop_event.get_obj().value:
            client, e = await self.connect_task()
            if not client:
                self.logger.error("[BLE] Cannot connect to %s. %s", self.address, e)
                await asyncio.sleep(self._RECONNECT_TIMEOUT)
                continue

            try:
                await client.start_notify(self.TOUCHPAD_UUID, self.handle_touchpad)
            except:
                await client.disconnect()
                client = None
                continue

            self._connected.set()
            running_selector = None

            while self._connected.is_set():
                if self._stop_event.get_obj().value:
                    await client.disconnect()
                    client = None
                    break

                if not client.is_connected:
                    self._connected.clear()
                    break

                try:
                    running_selector = await self.selector_task(client, running_selector)
                except:
                    self._connected.clear()

                await asyncio.sleep(self._RECONNECT_TIMEOUT)

            await asyncio.sleep(self._RECONNECT_TIMEOUT)       

    async def connect_task(self) -> Tuple[Optional[BleakClient], Any]:
        client = BleakClient(self.address)
        try:
            await client.connect()
        except Exception as e:
            return (None, e)

        return (client, None)
    
    async def selector_task(self, client: BleakClient, running_selector: Optional[TBleSelector]) -> Optional[TBleSelector]:        
        if self._selector_sensor.is_set() and running_selector != TBleSelector.SENSORS:
            if running_selector == TBleSelector.AUDIO:
                await client.stop_notify(self.AUDIO_DATA_UUID)
                await client.stop_notify(self.AUDIO_SYNC_UUID)
                self.logger.debug("[BLE] Stopped notification on AUDIO (%s %s)", self.AUDIO_SYNC_UUID, self.AUDIO_DATA_UUID)

            await client.start_notify(self.SENSORS_UUID, self.handle_sensors)
            self.logger.debug("[BLE] Started notification on sensors (%s)", self.SENSORS_UUID)

            running_selector = TBleSelector.SENSORS
        
        if self._selector_audio.is_set() and running_selector != TBleSelector.AUDIO:
            if running_selector == TBleSelector.SENSORS:
                await client.stop_notify(self.SENSORS_UUID)
                self.logger.debug("[BLE] Stopped notification on sensors (%s)", self.SENSORS_UUID)

            await client.start_notify(self.AUDIO_SYNC_UUID, self.handle_audio_sync)
            await client.start_notify(self.AUDIO_DATA_UUID, self.handle_audio)
            self.logger.debug("[BLE] Started notification on AUDIO (%s %s)", self.AUDIO_SYNC_UUID, self.AUDIO_DATA_UUID)

            running_selector = TBleSelector.AUDIO

        return running_selector

    def select_sensors(self):
        self._selector_sensor.set()
        self._selector_audio.clear()

    def select_audio(self):
        self._selector_audio.set()
        self._selector_sensor.clear()

    def connect(self):
        self.start()

    def disconnect(self):
        self.join()
        self.join()