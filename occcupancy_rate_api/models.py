import socket
import time
from datetime import datetime,timedelta,timezone
from occupancy_rate.models import MachineData
import pytz

first_run = True

def one_seconds_timer():
    global first_run
    if first_run:
        first_run = False
        return
    timer1 = time.time()
    while True:
        timer2 = time.time()
        if timer2 - timer1 >= 1:
            #main()
            break

#1分間計測用関数
"""def one_minutes_timer():
    global first_run
    if first_run:
        first_run = False
        return
    timer1 = time.time()
    while True:
        timer2 = time.time()
        if timer2 - timer1 >= 60:
            #main()
            break"""

#PLCのレジスタを型変換して、値を読み取る関数
def data(response):
    msg = str(response)
    msg = int(msg[-4:])
    is_operational = data_change(msg)
    print(f'PLCのレジスタの値: {msg}')
    return msg,is_operational

#PLCのレジスタの値を判定し、True or Falseを返す関数
def data_change(msg):
    if msg == 1:
        return True
    elif msg == 2 or msg == 3:
        return False
    else:
        return False


def main():
    #ローカル変数
    #サーバ(plc)のIPアドレスとポート番号を格納
    ip = "192.168.16.99"
    port = 4096
    #ip="192.168.8.55"
    #port=1357

    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 新しいソケットを作成

        try:
            client_socket.connect((ip,port))
            print("サーバに接続できました。")
            #client_socket.close()  # ソケットを閉じる
            break  # ループを抜ける

        # 接続が失敗した場合、再試行する
        except ConnectionRefusedError:
            print("サーバに接続できません。再試行します...")
            client_socket.close()
            time.sleep(3)  # 接続が失敗した場合、一定時間待機してから再試行
    try:
        while True:
            #one_minutes_timer()  # 1分間計測
            one_seconds_timer()  # 1秒間計測
            try:
                #レジスタ読み出し要求(PLCのレジスタはどこを指定するか？→D010)
                #D010のレジスタに任意の値が格納されているかを、D010の値を読み出して確認
                client_socket.send(bytes(b"500000FF03FF000018002004010000D*0000100001"))
                #client_socket.send(bytes(b"D202"))
                response = str(client_socket.recv(1024).decode())
                msg,is_operational = data(response)      
                timestamp= datetime.now()    #日本時間で取得
                #timestamp = timestamp.astimezone(pytz.timezone('Asia/Tokyo'))
                timestamp = timestamp.replace(tzinfo=None)
                timestamp = timestamp.replace(microsecond=0)
                #timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")   #文字列に変換
                print(f"取得時刻: {timestamp}")
                print(f"サーバからの読み出し応答: {msg}")
                #timestamp = base_datetime

                #データベースに保存(ここはうまく行っていない)
                MachineData.objects.create(
                        timestamp=timestamp,
                        is_operational=is_operational
                )

            # タイムアウトした場合、再試行する
            except TimeoutError:
                print("タイムアウトしました。再試行します...")
                time.sleep(3)

    # ソケットを閉じる    
    finally:
        client_socket.close()
        print("ソケットを閉じる")
                    
if __name__ == "__main__":
    main()
