import sys

file_path = "./files/file_latest.bin"
valid_commands = ['update', 'create']

def create_diff_file(latest_file, current_file, diff_file_path):
    with open(diff_file_path, 'wb') as diff_file:
        with open(latest_file, 'rb') as latest:
            with open(current_file, 'rb') as current:
                latest_data = latest.readlines()
                current_data = current.readlines()
                for l in latest_data:
                    print(l)


if len(sys.argv) < 4:
    print('Invalid number of arguments')
    sys.exit(1)

try:

    command = sys.argv[1]
    if command not in valid_commands:
        raise ValueError('The command is not valid. The only accepted commands are: create and update')

    match command:
        case "create":
            latest_file = sys.argv[2]
            diff_file_path = "./files/diff_file.bin"
            for current_file in sys.argv[3:]:
                create_diff_file(latest_file, current_file, diff_file_path)
        case "update":
            print('you used update command')
except ValueError as ve:
    print(f"Error: {ve}")
except Exception as e:
    print(f"An expected error occured: {e}")




