import os
import sys
import hashlib
# import argparse


def get_file_format():
    print("Enter file format:")
    return input()


def get_sort_option():
    print("Enter a sorting option:")
    name = input()
    if name == "1":
        return "Descending"
    elif name == "2":
        return "Ascending"
    else:
        print("Wrong option\n")
        return None


def walk_in_root(root_folder, ext_name):
    file_dict = {}
    for root, dirs, files in os.walk(root_folder, topdown=True):
        for name in files:
            file_path = os.path.join(root, name)
            if ext_name == "" or os.path.splitext(file_path)[1] == "." + ext_name:
                file_size = os.path.getsize(file_path)
                if file_size not in file_dict:
                    file_dict[file_size] = [file_path]
                else:
                    file_dict[file_size].append(file_path)

    return file_dict


def hashing_check(ordered_size, file_dict):
    no = 1
    file_no_dict = {}
    for size in ordered_size:
        hash_dict = {}
        for file in file_dict[size]:
            m = hashlib.md5()
            with open(file, "rb") as f:
                m.update(f.read())
                hash_md5 = m.hexdigest()
                if hash_md5 not in hash_dict:
                    hash_dict[hash_md5] = [file]
                else:
                    hash_dict[hash_md5].append(file)

        print(size, "bytes")
        for hash_md5 in hash_dict:
            if len(hash_dict[hash_md5]) <= 1:
                continue
            print("Hash:", hash_md5)
            for file in hash_dict[hash_md5]:
                print(str(no) + ".", file)
                file_no_dict[no] = file
                no += 1
            print()

    return file_no_dict


def delete_file(file_no_dict):
    delete_numbers = []
    while True:
        print("Enter file numbers to delete:")
        delete_numbers = input().split()
        if not delete_numbers:
            print("Wrong format")
            continue

        check = True
        for delete_number in delete_numbers:
            if not delete_number.isdigit() or int(delete_number) > len(file_no_dict):
                check = False
                break

        if check:
            break
        else:
            print("Wrong format")

    delete_numbers = [int(x) for x in delete_numbers]
    total_free = 0
    for delete_number in delete_numbers:
        total_free += os.path.getsize(file_no_dict[delete_number])
        os.remove(file_no_dict[delete_number])

    print("Total freed up space:", total_free, "bytes")


def core_system(root_folder):
    file_format = get_file_format()

    sort_option = None
    print("Size sorting options:\n1. Descending\n2. Ascending\n")
    while sort_option is None:
        sort_option = get_sort_option()

    file_dict = walk_in_root(root_folder, file_format)
    ordered_size = []
    if sort_option == "Ascending":
        ordered_size = sorted(file_dict)
    elif sort_option == "Descending":
        ordered_size = sorted(file_dict, reverse=True)
    for size in ordered_size:
        print(size, "bytes")
        for file_path in file_dict[size]:
            print(file_path)

    file_no_dict = None
    while True:
        print("Check for duplicates?")
        check = input()
        if check == "yes":
            file_no_dict = hashing_check(ordered_size, file_dict)
            break
        elif check == "No":
            break
        else:
            print("Wrong option")

    while True:
        print("Delete files?")
        delete = input()
        if delete == "yes":
            delete_file(file_no_dict)
            break
        elif delete == "no":
            break
        else:
            print("Wrong option")


# parser = argparse.ArgumentParser()
args = sys.argv

os.system("mv module/root_folder/files/stage/src/reviewSlider.js module/root_folder/files/stage/src/reviewslider.js")
os.system("mv module/root_folder/files/stage/src/toggleMiniMenu.js module/root_folder/files/stage/src/toggleminimenu.js")

if len(args) != 2:
    print("Directory is not specified")
else:
    core_system(args[1])
