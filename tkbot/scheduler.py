from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler():
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()

    def job_story(self, adv_post):
        self.add_job(adv_post, 'cron', hour=self.hour, minute=self.minute)
