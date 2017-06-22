def returnConcatenationString(**advertising_messages):
    advertising_message = []
    for message in advertising_messages.values():
        advertising_message.append(str(message))
        advertising_message.sort()
    return '\n'.join(advertising_message) + '\n'
