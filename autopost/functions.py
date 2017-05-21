# -*- coding: utf-8 -*-


from datetime import datetime
import settings
import json


def log(message, answer):
    print("\n----------------------------")
    print(datetime.now())
    print("Сообщение от {0} {1}, (id = {2})\nТекст: {3}".format(
        message.from_user.first_name, message.from_user.last_name,
        str(message.from_user.id), message.text))


def log_error(error_name, message):
    log_file = open(settings.path_logs + "log_error.txt", 'a')
    copy_log_file = open(settings.path_logs + "copy_log_error.txt", 'a')
    log = {
        # 'time': datetime.now(),
        'Error': error_name,
        'user_id': message.from_user.id,
        'First_Name': message.from_user.first_name,
        'Last_Name': message.from_user.last_name,
    }

    json.dump(log, log_file)
    json.dump(log, copy_log_file)

    log_file.close()
    copy_log_file.close()
