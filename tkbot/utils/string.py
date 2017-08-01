class String():
    def formatting_schedule(self, sched_message):
        result = ''
        for string in sched_message:
            if string.isdigit():
                result += string.strip()
        return result[:2] + ':' + result[-2:]

    def formatting_data(self, data):
        result = ''
        for column in data[0]:
            result += column + ' | '
        return result

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
