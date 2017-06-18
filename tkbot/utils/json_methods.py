import json
import settings


def save_adversiting_user_post(user_id, message_text):
    adv_msgs = {}
    adv_msgs[user_id] = message_text
    db_list = [settings.db_path, settings.copy_db_path]
    for db in db_list:
        with open(db, 'a') as db_path:
            json.dump(adv_msgs, db_path)


def delete_double_adversiting_user_post():
    db_list = [settings.db_path, settings.copy_db_path]
    for db in db_list:
        with open(db, 'r') as db_path:
            adv_msgs = json.load(db_path)
            print(adv_msgs)
            print("=========\n")
