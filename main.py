# main.py
import time
from threading import Thread
from Cacao.camera_handler import CacaoClassifier
from Cacao.servo_controller import ServoController

def main():
    classifier = CacaoClassifier()
    servo = ServoController()

    try:
        print("[System] Starting cacao classification system...")
        last_detected = None

        while True:
            result = classifier.detect_bean()
            if result and result != last_detected:
                print(f"[Detected] {result}")
                Thread(target=servo.pulse_for_bean, args=(result,), daemon=True).start()
                last_detected = result
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("[System] Shutting down...")
    finally:
        classifier.release()
        servo.cleanup()

if __name__ == "__main__":
    main()
