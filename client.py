import socket
import time
from datetime import datetime
from gpiozero import TonalBuzzer

import board
import adafruit_ina219


HOST_IP = "192.168.200.1"  # 接続するサーバーのIPアドレス
PORT = 9979  # 接続するサーバーのポート
DATASIZE = 1024  # 受信データバイト数
piezo = TonalBuzzer(26)

i2c=board.I2C()
ina219=adafruit_ina219.INA219(i2c)


class SocketClient():

    def __init__(self, host, port, datasize):
        self.host = host
        self.port = port
        self.datasize = datasize
        self.socket = None

    def send_recv(self, input_data):

        # sockインスタンスを生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # ソケットをオープンにして、サーバーに接続
            sock.connect((self.host, self.port))
            print('[{0}] input data : {1}'.format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), input_data))
            # 入力データをサーバーへ送信
            sock.send(str(input_data).encode('utf-8'))
            # サーバーからのデータを受信
            rcv_data = sock.recv(self.datasize)
            rcv_data = rcv_data.decode('utf-8')
            if int(rcv_data) == 1:
            	piezo.play('A4')
            	time.sleep(3)
            	piezo.stop()
            else:
            	pass
            print('[{0}] recv data : {1}'.format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rcv_data))
            time.sleep(1)


if __name__ == '__main__':

    client = SocketClient(HOST_IP, PORT,DATASIZE)
    while True:
        try:
            input_data =  ina219.current # ターミナルから入力された文字を取得
            client.send_recv(input_data)
        except KeyboardInterrupt:
            break
        except:
            pass
