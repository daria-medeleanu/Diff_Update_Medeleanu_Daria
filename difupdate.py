import sys
import os

VALID_COMMANDS = ['update', 'create']

# Creates a binary difference file between 2 binary files (current_file, latest_file)
def create_diff_file(latest_file, current_file_path, diff_file_path):
    with open(diff_file_path, 'ab') as diff_file:
        diff_file.write(b'\ndifference-for-'+current_file.encode("utf-8")+b'\n')
        with open(latest_file, 'rb') as latest:
            with open(current_file, 'rb') as current:
                latest_data = latest.readlines()
                current_data = current.readlines()
                nr_min_lines = min(len(latest_data), len(current_data))
                for i in range(nr_min_lines):
                    if len(current_data[i]) < len(latest_data[i]):
                        diff_file.write(b'line '+str(i+1).encode("utf-8")+b' insert '+latest_data[i]+b'\n')
                    elif(len(current_data[i]) == len(latest_data[i]) and current_data[i] != latest_data[i]):
                        diff_file.write(b'line '+str(i+1).encode("utf-8")+ b' update '+ current_data[i]+b'\n')
                        diff_file.write(b'line '+ str(i+1).encode("utf-8")+ b' update '+ latest_data[i]+b'\n')
                    elif(len(current_data[i]) > len(latest_data[i])):
                        diff_file.write(b'line '+ str(i+1).encode("utf-8")+ b' delete '+current_data[i]+b'\n')
                        diff_file.write(b'line '+ str(i+1).encode("utf-8")+ b' insert '+latest_data[i]+ b'\n')
                
                if (i <len(current_data)):
                    for j in range(i, len(current_data)):
                            diff_file.write(b'line '+ str(j+1).encode("utf-8")+ b' delete ' +current_data[j]+b'\n')
                
                if( i< len(latest_data)):
                    for j in range(i, len(latest_data)):
                            diff_file.write(b'line '+ str(j+1).encode("utf-8")+ b' insert '+latest_data[j]+ b'\n')

# Generates the latest file based on current_file using diff_file
def generate_latest_file(current_file_path, diff_file_path):
    new_latest_file_path = './binary_files/new_latest_file.bin'

    with open(new_latest_file_path, 'wb') as new_latest_file:
        with open(diff_file_path, 'rb') as diff_file:
            diff_data = diff_file.readlines()
            with open(current_file_path, 'rb') as current_file:
                current_data = current_file.readlines()
                current_lines = {i : line for i, line in enumerate(current_data, start=1)}
                file_name_current = os.path.splitext(os.path.basename(current_file_path))[0]+'.txt'+'\n'
                
                flag = False
                for linie in diff_data:
                    if linie.startswith(b'difference-for-') and linie[15:] == file_name_current.encode("utf-8"):
                        flag = True
                        continue
                    elif linie.startswith(b'difference-for-') and linie[15:] != file_name_current.encode("utf-8"):
                        flag = False
                    if flag == True and not linie.startswith(b'\n'):
                        linie_split = linie.split(b' ')
                        line_num = linie_split[1]
                        action = linie_split[2]
                        content = b' '.join(linie_split[3:])
                        line_num = int(line_num)
                        if action == b'insert':
                            current_lines[line_num] = content 
                        elif action == b'delete':
                            if line_num in current_lines:
                                del current_lines[line_num]
                        elif action == b'update':
                                current_lines[line_num] = content 
                
                for i in sorted(current_lines.keys()):
                    new_latest_file.write(current_lines[i])
            
# Deletes content of binary file
def delete_content_of_binary_file(file_path):
    with open(file_path, 'wb') as file:
        pass

# Transforms content of text file into utf-8 encoding and writes it into a binary file
def text_to_binary_file(text_file_path, binary_file_path):
    with open(text_file_path, "r", encoding="utf-8") as text_file:
        content = text_file.read()

    with open(binary_file_path, "wb") as binary_file:
        binary_file.write(content.encode("utf-8"))

# Transforms/decodes binary file content into text content and writes it to a text file 
def binary_file_to_text(binary_file_path, text_file_path):
    with open(binary_file_path, "rb") as binary_file:
        content = binary_file.read().decode("utf-8")

    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(content)

# Creates binary files based on the name of the files provided
def transformVersonFilesIntoBinaryFiles(version_files):
    for file in version_files:
        binary_file_path = 'binary_files/'+os.path.splitext(file)[0]+'.bin'
        text_to_binary_file(file, binary_file_path)

if len(sys.argv) < 4:
    print('Invalid number of arguments')
    sys.exit(1)
    
try:
    command = sys.argv[1]
    if command not in VALID_COMMANDS:
        raise ValueError('The command is not valid. The only accepted commands are: create and update')

    match command:
        case "create":
            latest_file = sys.argv[2]
            version_files = sys.argv[3:]

            transformVersonFilesIntoBinaryFiles(version_files)            
            latest_binary_file_path = 'binary_files/'+os.path.splitext(latest_file)[0]+'.bin'
            text_to_binary_file(latest_file, latest_binary_file_path)

            diff_file_path = "./binary_files/diff_file.bin"
            delete_content_of_binary_file(diff_file_path)

            for current_file in version_files:
                binary_file_path = 'binary_files/'+os.path.splitext(current_file)[0]+'.bin'
                create_diff_file(latest_binary_file_path, binary_file_path, diff_file_path)
        
        case "update":
            current_file_path = sys.argv[2]
            diff_file_path = sys.argv[3]
            generate_latest_file(current_file_path, diff_file_path)
            binary_file_to_text("binary_files/new_latest_file.bin","new_latest_file.txt")

except ValueError as ve:
    print(f"Error: {ve}")
except Exception as e:
    print(f"An expected error occured: {e}")

