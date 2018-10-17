import asyncore
import asynchat
import socket

class ChatServer(asyncore.dispatcher):
    def __init__(self,list_num = 20,host = '0.0.0.0',post = 19528):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host,post))
        self.listen(list_num)
        self.clients = list()

    def handle_accept(self):
        conn,addr = self.accept()
        c_ip,c_port = addr
        print('client {} enter'.format(c_ip))
        ChatSession(self,conn,c_ip,c_port)



class ChatSession(asynchat.async_chat):
    def __init__(self,server,conn,addr,port):
        asynchat.async_chat.__init__(self,conn)
        self.server = server
        self.addr = addr
        self.port = port
        self.server.clients.append(self)
        self.set_terminator(b'out')
        self.username = '{}:{}'.format(self.addr,self.port)
        self.coming()

    def coming(self):
        data = '{}进入聊天室'.format(self.username)
        self.broadcast(data)

    def collect_incoming_data(self, data):
        print(data)
        if len(data) > 0:
            msg = '{}say：{}'.format(self.username,data)
            self.broadcast(msg)

    def found_terminator(self):
        print('客户out')
        self.close_when_done()
        self.remove_client()

    def remove_client(self):
        self.server.clients.remove(self)
        self.user_go()

    def user_go(self):
        data = '{}离开聊天室'.format(self.username)
        self.broadcast(data)

    def broadcast(self,data):
        for i in self.server.clients:
            try:
                i.push(data.encode('utf8'))
            except Exception:
                self.remove_client()


if __name__ == '__main__':
    s = ChatServer()
    asyncore.loop()