#!/usr/bin/env python
import time
import board
import os
from adafruit_apds9960.apds9960 import APDS9960
import digitalio

i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True
apds.enable_color = False

int_pin = digitalio.DigitalInOut(board.D17)  # 接在 GPIO17 / 引脚11
int_pin.switch_to_input(pull=digitalio.Pull.UP)
apds.proximity_interrupt_threshold = (0, 175)
apds.enable_proximity_interrupt = True

MODIFIER = 0x05  # Ctrl(0x01) + Alt(0x04) = 0x05
KEYCODES = {
    0x01: 0x52,  # Up
    0x02: 0x51,  # Down
    0x03: 0x50,  # Left
    0x04: 0x4F   # Right
}

def send_key(mod, keycode):
    try:
        fd = os.open("/dev/hidg0", os.O_WRONLY | os.O_SYNC)
        os.write(fd, bytes([mod, 0, keycode, 0, 0, 0, 0, 0]))
        time.sleep(0.05)
        os.write(fd, bytes([0]*8))  # 释放键
        os.close(fd)
    except Exception as e:
        print("HID 发送失败:", e)

print("等待手势...")

last_trigger_time = 0
while True:
      gesture = apds.gesture()

      if gesture in KEYCODES:
          direction = {0x01: "Up", 0x02: "Down", 0x03: "Left", 0x04: "Right"}[gesture]
          print(f"检测到手势：{direction} → Ctrl+Alt+{direction}")
          send_key(MODIFIER, KEYCODES[gesture])
#      if not int_pin.value:
#          proximity_value = apds.proximity
#         print(f"检测到靠近，值 = {proximity_value} → Ctrl+Alt+F5")
#          send_key(MODIFIER, 0x3E)  # F5 = 0x3E
#          apds.clear_interrupt()
#          time.sleep(0.5) # 防止连发

      #proximity_value = apds.proximity
      #if proximity_value > 175 and (time.time() - last_trigger_time > 2):
       # print(f"检测到靠近，值 = {proximity_value} → Ctrl+Alt+F5")
        #send_key(MODIFIER, 0x3E)  # F5
        #last_trigger_time = time.time()

