import RPi.GPIO as GPIO
import time
import threading

# GPIOの初期化
def setup_gpio(pins):
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.IN)

# ワイヤーが切断されたか確認
def monitor_wire(wire, stop_event):
    while not stop_event.is_set():
        wire_state = GPIO.input(wire["pin"])

        # ワイヤーが接続されたままの場合（LOW）
        if not wire["connected"] and wire_state == GPIO.LOW:
            wire["connected"] = True
            print(f"{wire['pin']}番のワイヤーが接続された。")

        # ワイヤーが切断された場合（HIGH）
        elif wire["connected"] and wire_state == GPIO.HIGH:
            start_time = time.time()
            while GPIO.input(wire["pin"]) == GPIO.HIGH:
                if time.time() - start_time > 1:
                    wire["connected"] = False
                    print(f"{wire['pin']}番のワイヤーを切断した。")
                    break
        time.sleep(0.1)  # 少し待機してから再チェック

def main():
    wires = [
        {"pin":  4, "connected": False},
        {"pin": 17, "connected": False},
        {"pin": 27, "connected": False},
        {"pin": 22, "connected": False},
        {"pin": 10, "connected": False},
        {"pin":  9, "connected": False},
        {"pin": 11, "connected": False},
        {"pin":  5, "connected": False},
        {"pin":  6, "connected": False},
        {"pin": 13, "connected": False},
        {"pin": 19, "connected": False},
        {"pin": 26, "connected": False},
        {"pin": 14, "connected": False},
        {"pin": 15, "connected": False},
        {"pin": 18, "connected": False},
        {"pin": 23, "connected": False},
        {"pin": 24, "connected": False},
        {"pin": 25, "connected": False},
        {"pin":  8, "connected": False},
        {"pin":  7, "connected": False},
        {"pin": 12, "connected": False},
        {"pin": 16, "connected": False},
        {"pin": 20, "connected": False},
        {"pin": 21, "connected": False},
    ]
    setup_gpio([wire["pin"] for wire in wires])

    stop_event = threading.Event()
    threads = []

    # 各ワイヤーの監視スレッドを開始
    for wire in wires:
        thread = threading.Thread(target=monitor_wire, args=(wire, stop_event))
        threads.append(thread)
        thread.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n操作が中断された。")
    finally:
        stop_event.set()  # 全スレッドを停止
        for thread in threads:
            thread.join()  # スレッドの終了を待つ

if __name__ == '__main__':
    main()
