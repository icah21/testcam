# servo_controller.py
import RPi.GPIO as GPIO
import time

class ServoController:
    def __init__(self, pin=18):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pin, 50)  # 50Hz PWM
        self.pwm.start(0)

    def set_angle(self, angle):
        duty = 2.5 + (angle + 90) * 10 / 180
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(0)

    def pulse_for_bean(self, bean_type):
        angles = {
            "Criollo": 45,
            "Forastero": 90,
            "Trinitario": -45,
            "Unknown": -90
        }

        angle = angles.get(bean_type, 0)
        print(f"[Servo] Moving to {angle}° for {bean_type}")
        self.set_angle(angle)
        time.sleep(0.5)
        self.set_angle(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
