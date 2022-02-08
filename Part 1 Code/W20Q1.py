def linux_permissions_string_to_num(inputString):
    '''
    Convert Linux permission string to octal numeric representation.
    '''
    permissions = {
        '---': '0',
        '--x': '1',
        '-w-': '2',
        '-wx': '3',
        'r--': '4',
        'r-x': '5',
        'rw-': '6',
        'rwx': '7'
    }

    if len(inputString) == 10:
        inputString = inputString[1:]

    x = (inputString[:-6], inputString[3:-3], inputString[6:])
    numeric = permissions[x[0]] + permissions[x[1]] + permissions[x[2]]
    return numeric


x = input("Enter String permissions:")
print(linux_permissions_string_to_num(x))

play = True

while play:
    operation = int(input("Please enter 1 to continue or 2 to quit:"))

    if operation == 1:

        x = input("Enter String permissions:")
        print(linux_permissions_string_to_num(x))

    else:
        break
