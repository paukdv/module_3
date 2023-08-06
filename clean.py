from pathlib import Path
import os
import shutil
import sys

path = Path(sys.argv[1])

group_folders = {'archive': ('.zip', '.gz', '.tar'), 'documents': ('.doc', '.text', '.docx', '.txt', '.pdf', '.xlsx', '.xls', '.pptx'), 'images': (
    '.jpeg', '.png', '.jpg', '.svg'), 'video': ('.avi', '.mp4', '.mov', '.mkv'), 'audio': ('.mp3', '.ogg', '.wav', '.amr')}


def normalize(name):
    TRANS = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H',
             1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'
             }
    result = ""
    for char in name:
        if char.isalpha() and char.isascii():
            result += char
        elif char.isalpha() and not char.isascii():
            result += TRANS.get(ord(char), "_")
        elif char.isdigit():
            result += char
        else:
            result += "_"
    return result


def parse_folder(path):

    for element in path.iterdir():
        if element.is_dir():
            if element.name in group_folders:
                continue
            else:
                parse_folder(element)
        else:
            for k, v in group_folders.items():
                if element.suffix.lower() in v:
                    if k == 'archive':
                        shutil.unpack_archive(
                            element, f'{path.parts[0]}/{k}/{normalize(element.stem)}')
                    else:
                        path_create = f'{path.parts[0]}/{k}'
                        new_name_element = normalize(element.stem)
                        if Path(path_create).exists():
                            shutil.move(
                                element, f'{path.parts[0]}/{k}/{new_name_element}{element.suffix}')
                        else:
                            Path(path_create).mkdir()
                            shutil.move(
                                element, f'{path.parts[0]}/{k}/{new_name_element}{element.suffix}')


def clean_folder(path):

    folder_unknow = f'{path.parts[0]}/unknow'
    for element in path.iterdir():
        if element.is_dir():
            if not any(Path(element).iterdir()):
                shutil.rmtree(Path(element))
            elif element.name in group_folders:
                continue
            else:
                if Path(folder_unknow).exists():
                    shutil.move(element, f'{folder_unknow}/{element.name}')
                else:
                    Path(folder_unknow).mkdir()
                    shutil.move(element, f'{folder_unknow}/{element.name}')
        else:
            if Path(folder_unknow).exists():
                shutil.move(element, f'{folder_unknow}/{element.name}')
            else:
                Path(folder_unknow).mkdir()
                shutil.move(element, f'{folder_unknow}/{element.name}')


def print_console(path):

    if path.is_dir():
        print(path.name + '/')
        for item in path.iterdir():
            print_console(item)
    else:
        print(path.name)


def run():
    parse_folder(path)
    clean_folder(path)
    print_console(path)


if __name__ == '__main__':
    run()
