import eventlet
eventlet.monkey_patch()  # 필수
import pigpio
import os
import time
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

# pigpio 데몬 시작 (이미 실행 중인지 확인)
if os.system("pgrep pigpiod") != 0:
    os.system("sudo pigpiod")
    time.sleep(2)

# pigpio 초기화
pi = pigpio.pi()

# Flask 및 SocketIO 설정
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# GPIO 모드 읽기 (Input, Output, PWM 등)
def get_gpio_modes():
    modes = {}
    for pin in range(1,26):
        mode = pi.get_mode(pin)
        if mode == pigpio.INPUT:
            modes[pin] = "Input"
        elif mode == pigpio.OUTPUT:
            modes[pin] = "Output"
        elif mode == pigpio.ALT0:
            modes[pin] = "PWM"
        else:
            modes[pin] = f"ALT{mode}"  # 기타 모드는 ALT로 표시
    return modes

# GPIO 상태 읽기
def get_gpio_status():
    status = {pin: pi.read(pin) for pin in range(54)}  # 핀 0~53 상태 읽기
    return status

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

# 실시간으로 GPIO 상태 전송
@socketio.on('connect')
def handle_connect():
    def send_gpio_status():
        while True:
            gpio_status = get_gpio_status()
            socketio.emit('gpio_status', gpio_status)
            socketio.sleep(0.1)  # 상태 전송 주기

    socketio.start_background_task(send_gpio_status)


# GPIO 모드 상태 페이지
@app.route('/pin_modes')
def pin_modes():
    return render_template('pin_modes.html')

# 모드 데이터 전송 (AJAX 사용)
@app.route('/get_modes')
def get_modes():
    modes = get_gpio_modes()
    return jsonify(modes)


# main() 함수 정의
def main():
    print('http://localhost:5001')
    socketio.run(app, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    main()