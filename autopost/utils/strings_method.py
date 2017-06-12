def return_concatenation_string(**advertising_messages):
    advertising_message = ''
    for message in advertising_messages.values():
        advertising_message += '\n' + str(message) + '\n'
    return advertising_message


if __name__ == '__main__':
    test = {
        'usr0': 'hello world',
        'usr1': 'my name is...',
    }
    print(return_concatenation_string(**test))
