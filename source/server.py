from socket import *
from threading import *
from atexit import *
from random import *
from tkinter import *
import tkinter.messagebox

colors = [
    '\033[31m',     # 빨강
    '\033[32m',     # 초록
    '\033[33m',     # 노랑
    '\033[34m',     # 파랑
    '\033[35m',     # 자홍
    '\033[36m',     # 청록
    '\033[37m',     # 하양
    '\033[34m',     # 밑줄
]
server_socket = None    # 서버 소켓
users = {}              # key를 클라이언트 소켓으로 하여 username을 받는다.
addresses = {}          # key를 클라이언트 소켓으로 하여 address를 받는다.
stop_flag = False       # 클라이언트와 연결시 서버 종료인지 아닌지를 판단해주는 변수

def start_server():
    """ 서버를 시작하는 함수 """
    global server_socket
    register(cleanup)
    ip = '127.0.0.1'
    port = 2500
    btn_start.config(state=DISABLED)
    btn_stop.config(state=NORMAL)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(100)                   # 100명 대기 상태
    tkinter.messagebox.showinfo('정보', '서버 시작!')

    Thread(target=accept_client).start()
    lbl_ip['text'] = 'Ip: ' + ip
    lbl_port['text'] = 'Port: ' + str(port)

def stop_server():
    """ 서버를 종료하는 함수"""
    global server_socket, stop_flag
    stop_flag = True                    # 종료가 맞으므로 True로 설정
    btn_start.config(state=NORMAL)      # 접속 버튼을 활성화한다.
    btn_stop.config(state=DISABLED)     # 종료 버튼을 비활성화한다.
    lbl_ip['text'] = 'Ip: X.X.X.X'
    lbl_port['text'] = 'Port: XXXX'
    cleanup()
    server_socket.close()

def accept_client():
    """ 클라이언트와 연결해주는 함수 """
    global server_socket
    while True:
        try:
            client_socket, address = server_socket.accept()
        except:
            if stop_flag == True:
                tkinter.messagebox.showinfo('정보', '서버 종료!')
            else:
                tkinter.messagebox.showerror('에러', '클라이언트 연결 중 문제 발생!')
            break
        print(f'{address[0]}:{address[1]} 가 연결되었습니다.')
        addresses[client_socket] = address
        Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    """ 클라이언트를 처리하는 함수 """
    color = colors[randint(0, len(colors))]
    address = addresses[client_socket]
    try:
        user = get_username(client_socket)
    except:
        tkinter.messagebox.showwarning('오류', '이미 사용 중인 username입니다.')
        del addresses[client_socket]
        client_socket.close()
        return
    print(f'{address[0]}:{address[1]}의 username : {user}')
    users[client_socket] = user
    try:
        client_socket.send(f'어서오세요~ {color}{user}\033[0m님'.encode('utf-8'))
    except:
        tkinter.messagebox.showerror('에러', f'{address[0]} : {address[1]} ({user}) 연결 오류 발생!')
        del addresses[client_socket]
        del users[client_socket]
        client_socket.close()
        update_display(users.values())
        return
    send_all_clients(f'{color}{user}\033[0m님께서 입장하셨습니다.')
    update_display(users.values())

    while True:
        try:
            message = client_socket.recv(2048).decode('utf-8')
            if message == '/quit':
                client_socket.send('안녕히 가세요~'.encode('utf-8'))
                del addresses[client_socket]
                del users[client_socket]
                client_socket.close()
                tkinter.messagebox.showinfo('정보', f'{address[0]} : {address[1]} ({user}) 연결이 종료되었습니다.')
                send_all_clients(f'{color}{user}\033[0m님께서 퇴장하셨습니다.')
                update_display(users.values())
                break
            elif message == '/online':
                online_users = ', '.join([user for user in sorted(users.values())])
                client_socket.send(f'현재 입장 중인 유저는 {online_users} 입니다.'.encode('utf-8'))
            else:
                print(f'{address[0]}:{address[1]} ({user}) : {message}')
                send_all_clients(message, color, user)
        except:
            tkinter.messagebox.showinfo('정보', f'{address[0]} : {address[1]} ({user}) 연결이 종료되었습니다.')
            del addresses[client_socket]
            del users[client_socket]
            client_socket.close()
            send_all_clients(f'{color}{user}\033[0m님께서 퇴장하셨습니다.')
            update_display(users.values())
            break

def get_username(client_socket):
    """ username을 가져오는 함수 """
    username = client_socket.recv(2048).decode('utf-8')
    already = False
    if username in users.values():
        already = True
        while already:
            client_socket.send('이미 사용 중인 username입니다. 다시 입력해주세요: '.encode('utf-8'))
            username = client_socket.recv(2048).decode('utf-8')
            if username not in users.values():
                already = False
    return username

def send_all_clients(message, color='', sender=''):
    """ 모든 클라이언트에게 전달하는 함수 """
    try:
        if sender == '':
            for user in users:
                user.send(message.encode('utf-8'))
        else:
            for user in users:
                user.send(f'{color}{sender}\033[0m : {message}'.encode('utf-8'))
    except:
        tkinter.messagebox.showerror('에러', '메시지 전송 중 문제 발생!')

def cleanup():
    """ 모든 소켓을 닫는 함수 """
    if len(addresses) != 0:
        for client_socket in addresses.keys():
            client_socket.close()

def update_display(users):
    """ GUI에서 user 목록 업데이트 함수 """
    display.config(state=NORMAL)
    display.delete('1.0', END)

    for user in users:
        display.insert(END, user + '\n')
    display.config(state=DISABLED)

def window_close():
    """ window 창을 닫으려할 때 사용하는 함수 """
    close = tkinter.messagebox.askokcancel('닫기', '프로그램을 종료하시겠습니까?')
    if close:
        root.destroy()
        exit(0)

if __name__ == "__main__":
    root = Tk()
    root.title('서버')

    top_frame = Frame(root)
    btn_start = Button(top_frame, text='접속', command=start_server)
    btn_start.pack(side=LEFT)
    btn_stop = Button(top_frame, text='종료', command=stop_server, state=DISABLED)
    btn_stop.pack(side=LEFT)
    top_frame.pack(side=TOP, pady=(5, 0))

    middle_frame = Frame(root)
    lbl_ip = Label(middle_frame, text='Ip: X.X.X.X')
    lbl_ip.pack(side=LEFT)
    lbl_port = Label(middle_frame, text='Port: XXXX')
    lbl_port.pack(side=LEFT)
    middle_frame.pack(side=TOP, pady=(5, 0))

    client_frame = Frame(root)
    lbl_line = Label(client_frame, text='********** 접속 중인 User **********').pack()
    scrollbar = Scrollbar(client_frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    display = Text(client_frame, height=15, width=30)
    display.pack(side=LEFT, fill=Y, padx=(5, 0))
    scrollbar.config(command=display.yview)
    display.config(yscrollcommand=scrollbar.set, background='#F4F6F7', highlightbackground='grey', state='disabled')
    client_frame.pack(side=BOTTOM, pady=(5, 10))

    root.protocol('WM_DELETE_WINDOW', window_close)     # window에서 X버튼을 누를 시
    root.mainloop()