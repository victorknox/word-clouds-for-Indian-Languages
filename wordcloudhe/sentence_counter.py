with open('test.txt', 'r') as file:
    file_contents = file.read()

    print('Total words:   ', len(file_contents.split()))
    print('total stops:    ', file_contents.count('। '))