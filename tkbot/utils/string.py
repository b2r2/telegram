class String():
    def formattingScheduleMessage(self, sched_message):
        result = ''
        for string in sched_message:
            result += string.strip()
        return result[:2] + ':' + result[-2:]

    def formattingTotalAdvertisingMessage(**advertising_messages):
        advertising_message = []
        for message in advertising_messages.values():
            advertising_message.append(str(message))
            advertising_message.sort()
        return '\n'.join(advertising_message) + '\n'
