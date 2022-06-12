import string
import random
import re
import parsing
import glob


def obfuscate(path):
    common_dict = {}
    for p in locate_all_script_files(path):
        common_dict = common_dict | create_replacing_dict(
            remove_keywords(delete_extras(separate(read_gdscript_file(p))), parsing.read_set_from_csv()))

    for p in locate_all_script_files(path):
        replace_in_file(p, common_dict)


def read_gdscript_file(path):
    with open(path, "r") as f:
        data = f.read()
    return data


def split_string(string, delimiters):
    pattern = r'|'.join(delimiters)
    return re.split(pattern, string)


def separate(s):
    return split_string(s, ['\n', '\t', '\.', '\(', '\)', '\[', '\]', '{', '}', '"', "'", ' ', ',', ':', ';'])


def delete_extras(l):
    result = [el for el in l if any(c.isalpha() for c in el)]
    return result


def remove_keywords(s, kw):
    s = set(s)
    kw = set(kw)
    return s.difference(kw)


def create_replacing_dict(s):
    return dict(zip(s, set_of_random_strings(len(s))))


def random_string(n):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))


def set_of_random_strings(num):
    result = set()
    while len(result) != num:
        result.add(random_string(calculate_string_len(num)))
    if len(result.intersection(parsing.read_set_from_csv())) > 0:
        return set_of_random_strings(num)
    else:
        return result


def calculate_string_len(number_of_words):
    result = 1
    while number_of_words >= 26 ** result:
        result += 1
    return result + 2


def replace_in_file(path, d):
    code = read_gdscript_file(path)
    for key, value in d.items():
        pattern = re.compile(r'([\n \(\)\[\]\.\,\_\'\"{}\t\:])' + re.escape(key) + r'([\n \(\)\[\]\.\,\_\'\"{}\t\:])')
        code = re.sub(pattern=pattern, repl=lambda m: m.group(1) + value + m.group(2), string=code)
    with open(path, 'w') as f:
        f.write(code)


def locate_all_script_files(path):
    gd_files = glob.glob(path + "/**/*.gd", recursive=True)
    return gd_files


def check_if_folder_contains_gd(path):
    return len(locate_all_script_files(path)) != 0


def main():
    print('Укажите путь до Godot-проекта.')
    path = input()
    if check_if_folder_contains_gd(path):
        obfuscate(path)
        print('Обфускация завершена')
        input()
    else:
        print('Указанный путь некорректен / путь не содержит .gd файлов. Укажите другой путь.')
        main()


main()
