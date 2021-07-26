import random
import sqlite3

CONST_ = 1000000000


def generate_checksum(id_num):
    numbers = list(id_num)
    numbers = list(map(int, numbers))
    for i in range(0, 15, 2):
        numbers[i] *= 2
        if numbers[i] > 9:
            numbers[i] -= 9
    numbers_sum = sum(numbers)
    if numbers_sum % 10 == 0:
        return id_num + "0"
    else:
        last_num = str((numbers_sum // 10 + 1) * 10 - numbers_sum)
        return id_num + last_num


def check_checksum(num):
    numbers = list(num)
    numbers = list(map(int, numbers))
    for i in range(0, 15, 2):
        numbers[i] = 2 * numbers[i]
        if numbers[i] > 9:
            numbers[i] -= 9
    numbers_sum = sum(numbers)
    if numbers_sum % 10 == 0:
        return True
    return False


def set_account():
    global exist_num
    id_ = "400000" + str(exist_num + CONST_)[1:]
    id_ = generate_checksum(id_)
    print("Your card has been created")
    print("Your card number:\n{}".format(id_))
    num = 10000 + random.randint(0, 9999)
    passwd = str(num)[1:]
    print("Your card PIN:\n{}".format(passwd))
    cur.execute("INSERT INTO card VALUES ({}, {}, {}, 0)".format(exist_num, id_, passwd))
    conn.commit()
    exist_num += 1


def entry(id_num, passwd):
    cur.execute("""
    SELECT 
        number, pin
    FROM card
    WHERE
        number = {}
        AND pin = {}""".format(id_num, passwd))
    conn.commit()
    data_search = cur.fetchone()
    if data_search is None:
        print("Wrong card number or PIN!")
    else:
        print("You have successfully logged in!")
        bank_system(int(id_num[6:15]))


def bank_system(id_int):
    while True:
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        do_in_sys = input(">")
        if do_in_sys == "1":
            show_balance(id_int)
        elif do_in_sys == "2":
            print("Enter income:")
            income = int(input(">"))
            add_income(id_int, income)
            print("Income was added!")
        elif do_in_sys == "3":
            print("Transfer\nEnter card number:")
            id_transfer = input(">")
            if not check_checksum(id_transfer):
                print("Probably you made a mistake in the card number. Please try again!")
                continue
            id_transfer_int = int(id_transfer[6:15])
            if id_transfer_int >= exist_num:
                print("Such a card does not exist.")
                continue
            elif id_transfer_int == id_int:
                print("You can't transfer money to the same account!")
                continue
            print("Enter how much money you want to transfer:")
            money = int(input(">"))
            do_transfer(id_int, id_transfer_int, money)
        elif do_in_sys == "4":
            close_account(id_int)
            print("The account has been closed!")
            break
        elif do_in_sys == "0":
            print("Bye!")
            exit()


def show_balance(id_int):
    cur.execute("""
    SELECT balance
    FROM card
    WHERE id = {}""".format(id_int))
    conn.commit()
    data = cur.fetchone()
    print("Balance: {}".format(data[0]))


def add_income(id_int, income):
    cur.execute("""
    UPDATE card
    SET balance = balance + {}
    WHERE id = {}""".format(income, id_int))
    conn.commit()


def do_transfer(id1_int, id2_int, money):
    cur.execute("""
    SELECT balance
    FROM card
    WHERE id = {}""".format(id1_int))
    conn.commit()
    data = cur.fetchone()
    if data[0] < money:
        print("Not enough money!")
        return
    cur.execute("""
    UPDATE card
    SET balance = balance - {}
    WHERE id = {}""".format(money, id1_int))
    cur.execute("""
    UPDATE card
    SET balance = balance + {}
    WHERE id = {}""".format(money, id2_int))
    conn.commit()
    print("Success!")


def close_account(id_int):
    cur.execute("""
    DELETE FROM card
    WHERE id = {}""".format(id_int))
    conn.commit()


conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
conn.commit()

cur.execute("SELECT id FROM card")
conn.commit()
total_rows = cur.fetchall()
exist_num = len(total_rows)


while True:
    print("1. Create an account\n2. Log into account\n0. Exit")
    do = input(">")
    if do == "1":
        set_account()
    elif do == "2":
        id_num_input = input(">")
        passwd_input = input(">")
        if not check_checksum(id_num_input):
            print("Wrong card number or PIN!")
            continue
        id_num_int = int(id_num_input[6:15])
        if id_num_int >= exist_num:
            print("Wrong card number or PIN!")
            continue
        entry(id_num_input, passwd_input)
    elif do == "0":
        print("Bye!")
        break
