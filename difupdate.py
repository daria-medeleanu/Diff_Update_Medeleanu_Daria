import sys

file_path = "./file.bin"
valid_commands = ['update', 'create']
if len(sys.argv) < 4:
    print('Invalid number of arguments')
    sys.exit(1)

try:

    command = sys.argv[1]
    if command not in valid_commands:
        raise ValueError('The command is not valid. The only accepted commands are: create and update')

    with open(file_path,  "wb") as file:
        binary_data = "salut"
        file.write(binary_data.encode())

    with open(file_path, 'rb') as file:
        fileContent = file.read()
        print(fileContent.decode())
except ValueError as ve:
    print(f"Error: {ve}")




