class String():
    def formattingSchedule(self, sched_message):
        result = ''
        for string in sched_message:
            if string.isdigit():
                result += string.strip()
        return result[:2] + ':' + result[-2:]
