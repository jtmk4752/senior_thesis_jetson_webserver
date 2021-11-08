import socket
import time
from datetime import datetime

HOST_IP = "192.168.200.2" # 接続するサーバーのIPアドレス
PORT = 9979 # 接続するサーバーのポート
DATESIZE = 1024 # 受信データバイト数
INTERVAL = 3 # ソケット接続時のリトライ待ち時間
RETRYTIMES = 5 # ソケット接続時のリトライ回数

class SocketClient():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
    
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
    
        # サーバーとの接続 RETRYTIMESの回数だけリトライ
        for x in range(RETRYTIMES):
            try:
                client_socket.connect((self.host, self.port))
                self.socket =  client_socket
                print('[{0}] server connect -> address : {1}:{2}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.host, self.port) )
                break
            except socket.error:
                # 接続を確立できない場合、INTERVAL秒待ってリトライ
                time.sleep(INTERVAL)
                print('[{0}] retry after wait{1}s'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(INTERVAL)) )
 
    # サーバーへデータ送信関数
    def send(self):
        # ターミナルから入力された文字を取得
        input_data = "1000000"
        input_data = input_data.encode('utf-8')
        self.socket.send(input_data) # データ送信
    
    # サーバーからデータ受信関数
    def recv(self):
        rcv_data = self.socket.recv(DATESIZE) # データ受信
        rcv_data = rcv_data.decode('utf-8')
        rcv_data = float(rcv_data)
        return rcv_data
    
    # 上記の送信/受信関数を順番に行う
    def send_rcv(self):
        self.send()
        return self.recv()


             
if __name__ == '__main__':
    
    client = SocketClient(HOST_IP, PORT)
    client.connect() # はじめの1回だけソケットをオープン
    client.send_rcv()
    client.socket.close()

    client2 = SocketClient("192.168.200.3",PORT)
    client2.connect()
    test = round(client2.send_rcv())
    print(test)
    client2.socket.close()
