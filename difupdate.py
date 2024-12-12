file_path = "./file.bin"

with open(file_path,  "wb") as file:
    binary_data = b"salut"
    file.write(binary_data)

with open(file_path, 'rb') as file:
    fileContent = file.read()
    print(fileContent)



