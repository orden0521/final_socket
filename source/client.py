from socket import *
from threading import *
from tkinter import *
from datetime import *
import tkinter.messagebox

thread_flag = False     # 스레드 상태

def current_time():
    """ 시간 표시 함수 """
    now = datetime.now()
    formattedTime = now.strftime('%H:%M')       # 시와 분만 나타나게 해준다.
    return formattedTime

def send(client_socket):
    """ 메시지를 전송하는 함수 """
    while thread_flag:
        try:
            message = input()
            client_socket.send(message.encode('utf-8'))
        except:
            print('메시지 전송 중 에러 발생!')
            break

def receive(client_socket):
    """ 메시지를 받는 함수 """
    while thread_flag:
        try:
            message = client_socket.recv(2048).decode()
            if message:
                print("[{}] {}".format(current_time(), message))
            else:
                break
        except:
            print('서버 문제 발생!')
            break

def main():
    global thread_flag
    ip = '127.0.0.1'
    port = 2500
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((ip, port))
    receive_thread = Thread(target=receive, args=(client_socket,))  # 서버로부터 메시지를 받는 스레드
    send_thread = Thread(target=send, args=(client_socket,))        # 서버로부터 메시지를 주는 스레드
    receive_thread.start()
    send_thread.start()
    while receive_thread.is_alive() and send_thread.is_alive():
        continue
    thread_flag = False         # 두 스레드가 모두 동작하지 않으면 false로 설정
    client_socket.close()
    print('서버 종료!')

# class GUI:
#     def __init__(self):
#         self.root = Tk()
#         self.root.withdraw()
#
#         self.login_window = Toplevel()
#         self.login_window.title('로그인')
#         self.login_window.geometry('250x80')
#
#         frame = Frame(self.login_window)
#         self.lbl_username = Label(frame, text='Username : ')
#         self.lbl_username.pack(side=LEFT)
#         self.ent_username = Entry(frame)
#         self.ent_username.pack(side=LEFT)
#         self.ent_username.focus()
#         frame.pack(side=TOP, pady=(5, 0))
#
#         login_frame = Frame(self.login_window)
#         self.btn_login = Button(login_frame, text='로그인', command=lambda : self.login(self.ent_username.get()))
#         self.btn_login.pack(side=TOP)
#         login_frame.pack(side=TOP, pady=(5, 0))
#
#         self.root.mainloop()
#
#     def login(self, username):
#         """ 로그인 후 함수 """
#         if len(username) < 1:   # username의 길이가 1이면
#             tkinter.messagebox.showerror('에러', '두 글자 이상 입력하세요!')
#         else:
#             self.login_window.destroy()
#             self.chatting_window(username)
#
#     def chatting_window(self, username):
#         client_socket.send(username.encode('utf-8'))
#
#         self.root.deiconify()
#         self.root.title('채팅방')
#
#         display_frame = Frame(self.root)
#         self.scrollbar = Scrollbar(display_frame)
#         self.scrollbar.pack(side=RIGHT, fill=Y)
#         self.display = Text(display_frame, height=20, width=55)
#         self.display.pack(side=LEFT, fill=Y, padx=(5, 0))
#         self.display.tag_config('tag_your_message', foreground='blue')
#         self.scrollbar.config(command=self.display.yview)
#         self.display.config(yscrollcommand=self.scrollbar.set, background='#F4F6F7', highlightbackground='grey', state='disabled')
#         display_frame.pack(side=TOP)
#
#         bottom_frame = Frame(self.root)
#         self.ent_message = Entry(bottom_frame, width=45)
#         self.ent_message.pack(side=LEFT, padx=(5, 13), pady=(5, 10))
#         self.ent_message.focus()
#         self.ent_message.config(highlightbackground='grey')
#         self.btn_send = Button(bottom_frame, text='전송', width=10, command=lambda : self.send())
#         self.btn_send.pack(side=LEFT, padx=(5, 13), pady=(5, 10))
#         bottom_frame.pack(side=BOTTOM)
#
#     def main(self):
#         global client_socket,thread_flag
#         ip = '127.0.0.1'
#         port = 2500
#         client_socket = socket(AF_INET, SOCK_STREAM)
#         client_socket.connect((ip, port))
#         self.receive_thread = Thread(target=GUI.receive)
#         self.send_thread = Thread(target=GUI.send)
#         self.receive_thread.start()
#         self.send_thread.start()
#         self.__init__()
#         while self.receive_thread.is_alive() and self.send_thread.is_alive():
#             continue
#         thread_flag = False
#         client_socket.close()
#
#     def receive(self):
#         while thread_flag:
#             try:
#                 message = client_socket.recv(2048).decode()
#                 self.display.config(state=NORMAL)
#                 if message:
#                     self.display.insert(END, '[{}] {}\n'.format(current_time(), message))
#                     self.display.config(state=DISABLED)
#                 else:
#                     break
#             except:
#                 tkinter.messagebox.showerror('에러', '서버 문제 발생!')
#                 client_socket.close()
#                 break
#
#     def send(self):
#         while thread_flag:
#             try:
#                 client_socket.send(self.ent_message.get('1.0', END).encode('utf-8'))
#             except:
#                 tkinter.messagebox.showerror('에러', '메시지 전송 중 문제 발생!')
#                 break
#
#     def login_window_close(self):
#         close = tkinter.messagebox.askokcancel('닫기', '프로그램을 종료하시겠습니까?')
#         if close:
#             login_window.destroy()
#             exit(0)
#
#     def root_close(self):
#         close = tkinter.messagebox.askokcancel('닫기', '프로그램을 종료하시겠습니까?')
#         if close:
#             root.destroy()
#             exit(0)


if __name__ == '__main__':
    main()