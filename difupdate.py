import sys

file_path = "./files/file_latest.bin"
valid_commands = ['update', 'create']

def create_diff_file(latest_file, current_file, diff_file_path):
    with open(diff_file_path, 'wb') as diff_file:
        with open(latest_file, 'rb') as latest:
            with open(current_file, 'rb') as current:
                latest_data = latest.readlines()
                current_data = current.readlines()
                max_lines = max(len(latest_data), len(current_data))
                
                for i in range(max_lines):
                    if(i==len(latest_data) or i==len(current_data)):
                        break
                    if len(current_data[i]) < len(latest_data[i]):
                        print('line ', i+1,' insert ',latest_data[i])
                    elif(len(current_data[i]) == len(latest_data[i]) and current_data[i] != latest_data[i]):
                        print('line ', i+1, ' update - ', current_data[i])
                        print('line ', i+1, ' update + ', latest_data[i])
                    elif(len(current_data[i]) > len(latest_data[i])):
                        print('line ', i+1, ' delete',current_data[i])
                        print('line ', i+1, ' insert',latest_data[i])
                print(i, len(latest_data), len(current_data))
                if (i <len(current_data)):
                    for j in range(i, len(current_data)):
                        if len(current_data) > len(latest_data):
                            print('line ', j+1, ' delete' ,current_data[j])
                if( i< len(latest_data)):
                    for j in range(i, len(latest_data)):
                        if len(current_data) < len(latest_data):
                            print('line ', j+1, ' insert',latest_data[j])


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
            for current_file in sys.argv[5:]:
                create_diff_file(latest_file, current_file, diff_file_path)
        case "update":
            print('you used update command')
except ValueError as ve:
    print(f"Error: {ve}")
except Exception as e:
    print(f"An expected error occured: {e}")




