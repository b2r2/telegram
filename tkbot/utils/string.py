class String():
    def __init__(self):
        self.result = ''

    def formatting_sched(self, sched_message):
        for string in sched_message:
            if string.isdigit():
                self.result += string.strip()
        return self.result[:2] + ':' + self.result[-2:]

    def get_sched_hour(self, sched_message):
        for string in sched_message:
            if string.isdigit():
                self.result += string.strip()
        return self.result[:2]

    def get_sched_minute(self, sched_message):
        for string in sched_message:
            if string.isdigit():
                self.result += string.strip()
        return self.result[-2:]
