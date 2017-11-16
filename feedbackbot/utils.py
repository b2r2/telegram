import json


def encode_message(message, button):  # !!!
    message_data = {
        'cid': message.chat.id,
        'action': button,
        'user_name': message.chat.first_name,
    }
    return json.dumps(message_data)


def decode_message(data):
    return json.loads(data)


def get_formatted_text(data):
    user_name = data['user_name']
    action = data['action']
    action_to_state = {
        'Reset': 'сброшен',
        'Answer': 'выбран',
    }
    chat_state = action_to_state[action]
    if len(user_name) > 0:
        text = 'Чат с {} {}'.format(user_name, chat_state)
    else:
        text = 'Чат {}'.format(chat_state)
    return text
