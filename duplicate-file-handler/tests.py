from hstest.stage_test import StageTest
from hstest.check_result import CheckResult
from hstest import dynamic_test, TestedProgram
import os
import shutil
import hashlib

# dict for creating files
files = {
    'info.txt': {'path': ['root_folder'],
                 'content': 'd2c2ee4cbb368731f1a5399015160d7d_23'},
    'lost.json': {'path': ['root_folder'],
                  'content': '3a70ac2ebacf4174aa11dfbd1af835bd'},
    'phones.csv': {'path': ['root_folder'],
                   'content': '671ab9fbf94dc377568fb7b2928960c9'},
    'python.txt': {'path': ['root_folder'],
                   'content': 'd2c2ee4cbb368731f1a5399015160d7d_1'},
    'bikeshare.csv': {'path': ['root_folder', 'calc'],
                      'content': '671ab9fbf94dc377568fb7b2928960c9'},
    'server.php': {'path': ['root_folder', 'calc'],
                   'content': 'a5c662fe853b7ab48d68532791a86367'},
    'db_cities.js': {'path': ['root_folder', 'files'],
                     'content': 'f2e5cf58ae9b2d2fd0ae9bf8fa1774da'},
    'some_text.txt': {'path': ['root_folder', 'files'],
                      'content': 'd2c2ee4cbb368731f1a5399015160d7d_23'},
    'cars.json': {'path': ['root_folder', 'files', 'stage'],
                  'content': '3a70ac2ebacf4174aa11dfbd1af835bd'},
    'package-lock.json': {'path': ['root_folder', 'files', 'stage'],
                          'content': 'eebf1c62a13284ea1bcfe53820e83f11'},
    'index.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                 'content': '797ac79aa6a3c2ef733fecbaff5a655f'},
    'libs.txt': {'path': ['root_folder', 'files', 'stage', 'src'],
                 'content': '4909fd0404ac7ebe1fb0c50447975a2a'},
    'reviewSlider.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                        'content': 'abc96a9b62c4701f27cf7c8dbd484fdc'},
    'spoiler.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                   'content': 'b614ccac263d3d78b60b37bf35e860f3'},
    'src.txt': {'path': ['root_folder', 'files', 'stage', 'src'],
                'content': 'eed110d0dbd1d89d1ffea807d1d88679_1'},
    'toggleMiniMenu.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                          'content': '7eceb7dd5a0daaccc32739e1dcc6c3b0_1'},
    'extraversion.csv': {'path': ['root_folder', 'project'],
                         'content': 'fc88cf4d79437fa06e6cfdd80bd0eed2_1'},
    'index.html': {'path': ['root_folder', 'project'],
                   'content': '3f0f7b61205b863d2051845037541835_1'},
    'python_copy.txt': {'path': ['root_folder', 'project'],
                        'content': 'd2c2ee4cbb368731f1a5399015160d7d_1'}
}

root_dir_path = os.path.join('module', 'root_folder')


def create_files(path):
    # delete root_folder
    if os.path.isdir(path):
        shutil.rmtree(path)

    # create files
    for key, dict_val in files.items():
        path = os.path.join('module', *dict_val['path'])
        if not os.path.isdir(path):
            os.makedirs(path)
        file_path = os.path.join(path, key)
        with open(file_path, 'a+') as f:
            f.write(dict_val['content'])


# Tests
class DuplicateFileHandlerCheck(StageTest):
    @dynamic_test()
    def check_empty_arg(self):
        main = TestedProgram()
        output = main.start().lower()
        if 'not' in output and 'specified' in output:
            return CheckResult.correct()
        return CheckResult.wrong("You should check command line argument")

    @dynamic_test()
    def check_format_choice(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        if 'format' in output:
            return CheckResult.correct()
        return CheckResult.wrong("You should read the user's choice of file format")

    @dynamic_test()
    def check_sorting_choice(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("csv").lower()
        if 'sort' in output and 'desc' in output and 'asc' in output and 'option' in output:
            output = main.execute("3").lower()
            if 'wrong' in output:
                return CheckResult.correct()
            return CheckResult.wrong("You should read and check the user's choice of sorting option")
        return CheckResult.wrong("You should print out sorting options and add input prompt message")

    @dynamic_test()
    def check_path(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("2").lower().split('\n')
        for val in output:
            if '.' in val:
                if not os.path.exists(val):
                    return CheckResult.wrong(f"{val} path does not exist")
        return CheckResult.correct()

    @dynamic_test()
    def check_group_first_line(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("2").lower().split('\n')
        output = [val for val in output if val]

        if not output:
            return CheckResult.wrong("After choosing ascending sorting order your output is empty!")

        if 'byte' in output[0]:
            return CheckResult.correct()
        return CheckResult.wrong(f"The first line of group of files should contain files size")

    @dynamic_test()
    def check_group_size(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("2").lower().split('\n')
        output = [val for val in output if val]

        for val in output:
            if 'byte' in val and not any(i.isdigit() for i in val.split()):
                return CheckResult.wrong(f"There is no size in the line: {val}")

        return CheckResult.correct()

    @dynamic_test()
    def check_size(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("2").lower().split('\n')
        output = [val for val in output if val]
        size = None

        for val in output:
            if 'byte' in val:
                for i in val.split():
                    if i.isdigit():
                        size = int(i)
            elif val and 'check' not in val:
                if not os.path.exists(val):
                    return CheckResult.wrong('Looks like you printed a file name that doesn\'t exist!')
                file_size = os.path.getsize(val)
                if size != file_size:
                    return CheckResult.wrong(f"{val} has wrong size group")
        return CheckResult.correct()

    @dynamic_test()
    def check_order_asc(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("2").lower().split('\n')
        sizes = []
        size = None

        for val in output:
            if 'byte' in val:
                for i in val.split():
                    if i.isdigit():
                        size = int(i)

                sizes.append(size)

        if len(sizes) != 3:
            return CheckResult.wrong(f"Wrong number of groups of files")
        if sizes[0] == 32 and sizes[1] == 34 and sizes[2] == 35:
            return CheckResult.correct()
        return CheckResult.wrong(f"Wrong sorting order of files")

    @dynamic_test()
    def check_order_desc(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("1").lower().split('\n')
        sizes = []
        size = None

        for val in output:
            if 'byte' in val:
                for i in val.split():
                    if i.isdigit():
                        size = int(i)

                sizes.append(size)

        if len(sizes) != 3:
            return CheckResult.wrong(f"Wrong number of groups of files")
        if sizes[2] == 32 and sizes[1] == 34 and sizes[0] == 35:
            return CheckResult.correct()
        return CheckResult.wrong(f"Wrong sorting order of files")

    @dynamic_test()
    def check_num(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("2").lower().split('\n')
        num_files = []
        sizes = []
        n = 0

        for val in output:
            if val and 'check' not in val:
                if 'byte' in val:
                    num_files.append(n)
                    n = 0
                else:
                    n += 1
        num_files.append(n)

        num_files.append(n)
        if num_files[1] != 11:
            return CheckResult.wrong(f"""Output contains wrong number of files with a size of 32 bytes. 
                                         Number of files in output: {num_files[1]}""")

        if num_files[2] != 6:
            return CheckResult.wrong(f"""Output contains wrong number of files with a size of 34 bytes. 
                                         Number of files in output: {num_files[2]}""")

        if num_files[-1] != 2:
            return CheckResult.wrong(f"""Output contains wrong number of files with a size of 35 bytes. 
                                         Number of files in output: {num_files[-1]}""")

        return CheckResult.correct()

    @dynamic_test()
    def check_format(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("csv").lower()
        output = main.execute("2").lower().split('\n')

        for val in output:
            if '.' in val and 'csv' not in val:
                return CheckResult.wrong(f"Wrong file format in {val}")

        return CheckResult.correct()

    @dynamic_test()
    def check_duplicate_first_line(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("2").lower()
        output = main.execute("yes").lower().split('\n')
        output = [val for val in output if val]

        if not output:
            return CheckResult.wrong("Looks like your output is empty after entering 'Yes'")

        if len(output) < 1 or 'byte' not in output[0]:
            return CheckResult.wrong(f"The first line of group of files should contain files size")
        if len(output) < 2 or 'hash' not in output[1]:
            return CheckResult.wrong(f"The second line of group of files should contain hash value")
        return CheckResult.correct()

    @dynamic_test()
    def check_duplicate_group_size(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("2").lower()
        output = main.execute("yes").lower().split('\n')
        output = [val for val in output if val]

        for val in output:
            if 'byte' in val and not any(i.isdigit() for i in val.split()):
                return CheckResult.wrong(f"There is no size in the line: {val}")
        return CheckResult.correct()

    @dynamic_test()
    def check_size_duplicate(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("2").lower()
        output = main.execute("yes").lower().split('\n')
        output = [val for val in output if val]
        size = None

        for val in output:
            if 'byte' in val:
                for i in val.split():
                    if i.isdigit():
                        size = int(i)
            elif 'delete' not in val and os.sep in val:
                temp = val.split()
                if len(temp) < 2:
                    return CheckResult.wrong("Your output is incorrect! "
                                             "Make sure that the file paths are printed as in the examples")
                path = ' '.join(temp[1:])
                try:
                    file_size = os.path.getsize(path)
                except Exception:
                    return CheckResult.wrong(f"Your output contains invalid file path:\n"
                                             f"{val}")
                if size != file_size:
                    return CheckResult.wrong(f"{val} has wrong size group")
        return CheckResult.correct()

    @dynamic_test()
    def check_duplicate_order_asc(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("2").lower()
        output = main.execute("yes").lower().split('\n')

        sizes = []
        for val in output:
            if 'byte' in val:
                for i in val.split():
                    if i.isdigit():
                        sizes.append(int(i))

        if len(sizes) != 3:
            return CheckResult.wrong(f"Wrong number of groups of files")
        if sizes[0] == 32 and sizes[1] == 34 and sizes[2] == 35:
            return CheckResult.correct()
        return CheckResult.wrong(f"Wrong sorting order of files")

    @dynamic_test()
    def check_duplicate_order_desc(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("1").lower()
        output = main.execute("yes").lower().split('\n')

        sizes = []
        for val in output:
            if 'byte' in val:
                for i in val.split():
                    if i.isdigit():
                        sizes.append(int(i))

        if len(sizes) != 3:
            return CheckResult.wrong(f"Wrong number of groups of files")
        if sizes[2] == 32 and sizes[1] == 34 and sizes[0] == 35:
            return CheckResult.correct()
        return CheckResult.wrong(f"Wrong sorting order of files")

    @dynamic_test()
    def check_duplicate_enum(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("1").lower()
        output = main.execute("yes").lower().split('\n')

        n = 1
        for val in output:
            if '.' in val:
                if val[0] != str(n):
                    return CheckResult.wrong(f"Wrong file numbering. File: {val} ")
                n += 1
        return CheckResult.correct()

    @dynamic_test()
    def check_duplicate_hash(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("1").lower()
        output = main.execute("yes").lower().split('\n')

        hash_user = None
        for val in output:
            if 'hash' in val:
                temp = val.split()
                if len(temp) != 2:
                    return CheckResult.wrong(f"The following line has wrong output format:\n{val}\n"
                                             f"Make sure you output it like in examples!")
                hash_user = temp[1]
            elif '.' in val:
                temp = val.split()
                if len(temp) < 2:
                    return CheckResult.wrong("Your output is incorrect! "
                                             "Make sure that the file paths are printed as in the examples")
                path = ' '.join(temp[1:])
                with open(path, 'rb') as f:
                    hasher = hashlib.md5()
                    hasher.update(f.read())
                    hash_val = hasher.hexdigest()
                if hash_user != hash_val:
                    return CheckResult.wrong(f"Wrong file hash. File: {val}, hash: {hash_user} ")

        return CheckResult.correct()

    @dynamic_test()
    def check_duplicate(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("1").lower()
        output = main.execute("yes").lower().split('\n')

        hash_arr = ['95708df6eb2d9e30c128cf14dcf91f5b',
                    'c2a5ad1655d8d46d7d699594c1ee0dec',
                    'a5ceea9b58986bc87fb85f999d76d9db',
                    'd63a4f1856c5fa167b1aaa6529d9846f']

        n = 0
        for val in output:
            if 'hash' in val:
                n += 1
                string, hash_user = val.split()
                if hash_user not in hash_arr:
                    return CheckResult.wrong(f"There is no duplicate with hash {hash_user}")
        if n < 4:
            return CheckResult.wrong(f"You have missed some files")
        return CheckResult.correct()

    @dynamic_test()
    def check_duplicate_txt(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("txt").lower()
        output = main.execute("1").lower()
        output = main.execute("yes").lower().split('\n')

        for val in output:
            if '.' in val and 'txt' not in val:
                return CheckResult.wrong(f"Wrong file format in {val}")
        return CheckResult.correct()

    @dynamic_test()
    def check_del_choice_space(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("1").lower()
        output = main.execute("yes").lower()
        output = main.execute("yes").lower()
        output = main.execute("").lower()

        if 'wrong' in output:
            return CheckResult.correct()
        return CheckResult.wrong(f"You should check an empty string of files to delete")

    @dynamic_test()
    def check_del_choice_mix(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("1").lower()
        output = main.execute("yes").lower()
        output = main.execute("yes").lower()
        output = main.execute("one 2 3.5").lower()

        if 'wrong' in output:
            return CheckResult.correct()
        return CheckResult.wrong(f"You should check an input")

    @dynamic_test()
    def check_deleting(self):
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("1").lower()
        output = main.execute("yes").lower().split('\n')

        del_choice = "1 2 5 3"
        del_arr = []

        for val in output:
            if '.' in val and val.split()[0][0] in del_choice:
                string, path = val.split(' ', 1)
                del_arr.append(path)

        output = main.execute("yes").lower()
        output = main.execute(del_choice).lower()

        for path in del_arr:
            if os.path.exists(path):
                return CheckResult.wrong(f"Some files still exist")
        return CheckResult.correct()

    @dynamic_test()
    def check_free_space(self):
        create_files(root_dir_path)
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("").lower()
        output = main.execute("1").lower()
        output = main.execute("yes").lower()
        output = main.execute("yes").lower()
        output = main.execute("1 2 5 3").lower()

        if '136' in output:
            return CheckResult.correct()
        return CheckResult.wrong(f"Wrong size of freed space")

    @dynamic_test()
    def check_free_space(self):
        create_files(root_dir_path)
        main = TestedProgram()
        output = main.start(root_dir_path).lower()
        output = main.execute("txt").lower()
        output = main.execute("1").lower()
        output = main.execute("yes").lower()
        output = main.execute("yes").lower()
        output = main.execute("1 4 3").lower()

        if '103' in output:
            return CheckResult.correct()
        return CheckResult.wrong(f"Wrong size of freed space")

    def after_all_tests(self):
        try:
            if os.path.isdir(root_dir_path):
                shutil.rmtree(root_dir_path)
        except Exception as ignored:
            pass

    def generate(self):
        try:
            create_files(root_dir_path)
        except Exception as ignored:
            pass
        return []


if __name__ == '__main__':
    DuplicateFileHandlerCheck().run_tests()
