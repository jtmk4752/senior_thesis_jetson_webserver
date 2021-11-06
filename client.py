import socket
import time
from datetime import datetime


HOST_IP = "192.168.200.2"  # 接続するサーバーのIPアドレス

PORT = 9979  # 接続するサーバーのポート
DATASIZE = 1024  # 受信データバイト数





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

            print('[{0}] recv data : {1}'.format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rcv_data))
            time.sleep(1)


if __name__ == '__main__':

#    client = SocketClient(HOST_IP, PORT,DATASIZE)
    while True:
        try:
            client = SocketClient(HOST_IP, PORT,DATASIZE)
            input_data =  "10" # ターミナルから入力された文字を取得
            client.send_recv(input_data)

            client2 = SocketClient("192.168.200.3", PORT,DATASIZE)
            input_data =  "100" # ターミナルから入力された文字を取得
            client2.send_recv(input_data)
            time.sleep(1)

        except KeyboardInterrupt:
            break
        except:
            pass
        
