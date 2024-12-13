import sys
import difflib
from difflib import unified_diff

file_path = "./files/file_latest.bin"
valid_commands = ['update', 'create']

def create_diff_file(files_versions, latest_version):
    f1 = files_versions[0]
    f2 = files_versions[1]

    with open(f1) as file_1:
        file_1_text = file_1.readlines()
        with open(latest_version) as file_2:
            file_2_text = file_2.readlines()
            for line in difflib.diff_bytes(dfunc = unified_diff, a = file_1, b = file_2):
                print(line)

if len(sys.argv) < 4:
    print('Invalid number of arguments')
    sys.exit(1)

try:

    command = sys.argv[1]
    if command not in valid_commands:
        raise ValueError('The command is not valid. The only accepted commands are: create and update')

    match command:
        case "create":
            print('you used create command')
            files_versions = []
            latest_version = sys.argv[2]
            for f in sys.argv[3:]:
                files_versions.append(f)
            create_diff_file(files_versions, latest_version)
        case "update":
            print('you used update command')

    # with open(file_path,  "wb") as file:
    #     data = ("A venit Isus pe lume intr-o noapte minunata\nIn Betleemul din Iudeea pe cer o stea se-arata\nMagii dupa stea pornesc plini de bucurie\nSa se-nchine Celui care a coborat din vesnicie\n")
    #     file.write(data.encode())
    #
    # with open(file_path, 'rb') as file:
    #     fileContent = file.read()
    #     print(fileContent.decode())
except ValueError as ve:
    print(f"Error: {ve}")
except Exception as e:
    print(f"An expected error occured: {e}")




