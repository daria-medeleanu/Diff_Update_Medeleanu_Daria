import sys

file_path = "./files/file_latest.bin"
valid_commands = ['update', 'create']

def create_diff_file(latest_file, current_file, diff_file_path):
    with open(diff_file_path, 'ab') as diff_file:
        diff_file.write(b'\ndifference-for-'+current_file.encode()+b'\n')
        with open(latest_file, 'rb') as latest:
            with open(current_file, 'rb') as current:
                latest_data = latest.readlines()
                current_data = current.readlines()
                max_lines = max(len(latest_data), len(current_data))
                
                for i in range(max_lines):
                    if(i==len(latest_data) or i==len(current_data)):
                        break
                    if len(current_data[i]) < len(latest_data[i]):
                        diff_file.write(b'line '+str(i+1).encode()+b' insert '+latest_data[i])
                    elif(len(current_data[i]) == len(latest_data[i]) and current_data[i] != latest_data[i]):
                        diff_file.write(b'line '+str(i+1).encode()+ b' update '+ current_data[i])
                        diff_file.write(b'line '+ str(i+1).encode()+ b' update '+ latest_data[i])
                    elif(len(current_data[i]) > len(latest_data[i])):
                        diff_file.write(b'line '+ str(i+1).encode()+ b' delete '+current_data[i])
                        diff_file.write(b'line '+ str(i+1).encode()+ b' insert '+latest_data[i])

                if (i <len(current_data)):
                    for j in range(i, len(current_data)):
                        if len(current_data) > len(latest_data):
                            diff_file.write(b'line '+ str(j+1).encode()+ b' delete ' +current_data[j])
                if( i< len(latest_data)):
                    for j in range(i, len(latest_data)):
                        if len(current_data) < len(latest_data):
                            diff_file.write(b'line '+ str(j+1).encode()+ b' insert '+latest_data[j])

def generate_latest_file(current_file_path, diff_file_path):
    new_latest_file_path = './files/new_latest_file.bin'
    with open(new_latest_file_path, 'wb') as new_latest_file:
        with open(diff_file_path, 'rb') as diff_file:
            diff_data = diff_file.readlines()
            with open(current_file_path, 'rb') as current_file:
                current_data = current_file.readlines()
            
                            
                    
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
            current_file_path = sys.argv[2]
            diff_file_path = sys.argv[3]
            generate_latest_file(current_file_path, diff_file_path)
except ValueError as ve:
    print(f"Error: {ve}")
except Exception as e:
    print(f"An expected error occured: {e}")
    