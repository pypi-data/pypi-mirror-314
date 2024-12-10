class TaskBase:
    def __init__(self):
        self.task_description = ""
        self.task_time = ""
        self.task_date = ""

    def validate_time(self, time_string):
        try:
            hour, minute = map(int, time_string.split(":"))
            return 0 <= hour <= 24 and 0 <= minute <= 60
        except ValueError:
            return False

    def validate_date(self, date_string):
        try:
            month, day = map(int, date_string.split(":"))
            return 1 <= month <= 12 and 1 <= day <= 31
        except ValueError:
            return False

class Task(TaskBase):
    def __init__(self, description, time, date):
        super().__init__()
        self.task_description = description
        self.task_time = time
        self.task_date = date

class TaskHistory:
    def __init__(self):
        self.history = []

    def add_history(self, action, task, timestamp):
        self.history.append((action, task, timestamp))

    def get_history(self):
        return self.history