import socket
import time
from datetime import datetime,timedelta,timezone
from occupancy_rate.models import MachineData
import pytz

tz = pytz.timezone('Asia/Tokyo')
first_run = True

def one_minutes_timer():
    global first_run
    if first_run:
        first_run = False
        return
    timer1 = time.time()
    while True:
        timer2 = time.time()
        if timer2 - timer1 >= 60:
            #main()
            break

def data(response):
    msg = str(response)
    msg = int(msg[-4:])
    is_operational = data_change(msg)
    print(f'PLCのレジスタの値: {msg}')
    return msg,is_operational

def data_change(msg):
    if msg == 1:
        return True
    else:
        return False


def main():
    #ローカル変数
    #サーバ(plc)のIPアドレスとポート番号を格納
    ip = "192.168.16.99"
    port = 4096
    #ip = "192.168.8.114"
    #port = 1234
    is_first_run = True

    #cnt = 0
    #is_operatinaol = data_change(msg)
                    
    while is_first_run:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 新しいソケットを作成
        try:
            client_socket.settimeout(3)  # タイムアウトを設定
            client_socket.connect((ip,port))
            print("サーバに接続できました。")
            is_first_run = False
            client_socket.sendall(b"500000FF03FF00001C002004010000D*0000010001")
            """try :
                response = client_socket.recv(1024).decode()
            except ConnectionResetError:
                print("接続がリセットされました。再接続します...")
                client_socket.close()
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((ip, port))"""
        except (TimeoutError,ConnectionRefusedError):
            print("サーバに接続できません。再試行します...")
            time.sleep(3)

        try:
            while True:
                one_minutes_timer()
                try:
                    #レジスタ読み出し要求(PLCのレジスタはどこを指定するか？→D210)
                    #D210のレジスタに0xffが格納されているかを、D210の値を読み出して確認
                    client_socket.sendall(b"500000FF03FF00001C002004010000D*0000010001")
                    response = client_socket.recv(1024).decode('utf-8')
                
                    """print("接続がリセットされました。再接続します...")
                    client_socket.close()
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((ip, port))"""
                    msg,is_operational = data(response)
                    base_datetime= datetime.now(pytz.timezone('Asia/Tokyo'))
                    base_datetime = base_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"取得時刻: {base_datetime}")
                    print(f"サーバからの読み出し応答: {msg}")
                    print(response)
                    timestamp = base_datetime
                    MachineData.objects.create(
                            timestamp=timestamp,
                            is_operational=is_operational
                    )

                except TimeoutError:
                    print("タイムアウトしました。再試行します...")
                    time.sleep(3)
            
        finally:
            client_socket.close()
            print("ソケットを閉じる")
                    
if __name__ == "__main__":
    main()
