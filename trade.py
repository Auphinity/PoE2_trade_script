import pyautogui
import time
import random
import pygetwindow as gw
import tkinter as tk
from threading import Thread, Lock, Event

# Блокировка и события
lock = Lock()
stop_event = Event()
pause_event = Event()

def human_delay():
    """Создает случайную задержку, имитируя ввод человека."""
    time.sleep(random.uniform(0.05, 0.1))

def type_text(text):
    """Печатает текст с небольшой задержкой между символами."""
    for char in text:
        pyautogui.write(char)
        human_delay()

def switch_to_process_window(window_title):
    """Переключается на окно с указанным заголовком."""
    with lock:
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            window = windows[0]
            window.activate()
            return True
        return False

def monitor_window(window_title):
    """Следит за активностью окна игры и управляет паузой цикла."""
    global pause_event
    while not stop_event.is_set():
        windows = gw.getWindowsWithTitle(window_title)
        if windows and windows[0].isActive:
            pause_event.set()  # Возобновляем цикл
        else:
            pause_event.clear()  # Приостанавливаем цикл
        time.sleep(0.5)

def trade_cycle():
    """Цикл для выполнения команд /trade."""
    window_title = "Path of Exile"
    if not switch_to_process_window(window_title):
        print("Ошибка: Не удалось найти окно.")
        return
    
    for i in range(2, 31):
        if stop_event.is_set():
            break
        
        pause_event.wait()  # Ожидание активности окна
        
        print(f"Выполняем команду: /trade {i}")
        pyautogui.press('enter')
        human_delay()
        type_text(f'/trade {i}')
        human_delay()
        pyautogui.press('enter')
        human_delay()
        pyautogui.press('enter')
        human_delay()
        pyautogui.press(['up', 'up'])
        human_delay()
        pyautogui.press('enter')
        time.sleep(random.uniform(0.5, 1.0))

def start_trade():
    """Запускает цикл торговли в отдельном потоке."""
    global trade_thread
    stop_event.clear()
    pause_event.set()
    trade_thread = Thread(target=trade_cycle, daemon=True)
    trade_thread.start()

def stop_trade():
    """Останавливает цикл торговли."""
    stop_event.set()
    pause_event.set()
    print("Цикл торговли остановлен.")

def create_ui():
    root = tk.Tk()
    root.title("Автоматизация торговли")
    root.attributes("-topmost", True)
    
    start_button = tk.Button(root, text="Запустить цикл торговли", command=start_trade)
    start_button.pack(pady=10)
    
    stop_button = tk.Button(root, text="Остановить цикл торговли", command=stop_trade)
    stop_button.pack(pady=10)
    
    root.mainloop()

def main():
    """Запуск мониторинга окна и UI."""
    window_monitor_thread = Thread(target=monitor_window, args=("Path of Exile",), daemon=True)
    window_monitor_thread.start()
    create_ui()

if __name__ == "__main__":
    main()