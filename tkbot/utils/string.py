class String():
    def __init__(self):
        self.result = ''

    def formatting_schedule(self, sched_message):
        for string in sched_message:
            if string.isdigit():
                self.result += string.strip()
        return self.result[:2] + ':' + self.result[-2:]

    def formatting_data(self, data):
        for row in data[0]:
            self.result += row + ' | '
        print(self.result)
        return self.result

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
