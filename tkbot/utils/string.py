def formatting_schedule(sched_message):
    result = ''
    for string in sched_message:
        if string.isdigit():
            result += string.strip()
    return result[:2] + ':' + result[-2:]


def formatting_field_user(field):
    result = ''
    for column in field[0]:
        result += column + ' | '
    return result


def get_sched_hour(self, sched_message):
    result = ''
    for string in sched_message:
        if string.isdigit():
            result += string.strip()
    return result[:2]


def get_sched_minute(self, sched_message):
    result = ''
    for string in sched_message:
        if string.isdigit():
            result += string.strip()
    return result[-2:]
