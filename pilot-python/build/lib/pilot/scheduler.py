import sched, time


class Scheduler:

    def __init(self):
        self.s = sched.scheduler(time.time, time.sleep)

    def schedule(self, action):
        self.s.enterabs(1, 1, action, argument=(), kwargs={})

    def cancel(self, event):
        self.s.cancel(event)
