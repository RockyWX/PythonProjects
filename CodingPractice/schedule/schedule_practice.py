from datetime import datetime


def displaytime_decorator(func):
    def wrapper(*args, **kwargs):
        print(str(datetime.now()))
        return func(*args, **kwargs)
    return wrapper


class Schedule(object):

    name = None
    desp = None
    tasks = None

    def __init__(self, n, d):
        self.name = n
        self.desp = d
        self.tasks = {}  # Empty Dictionary

    @displaytime_decorator
    def add_task(self, name, content, priority):
        if name not in self.tasks:
            task = [name, content, priority]
            self.tasks.update({name: task})
        self.display()

    @displaytime_decorator
    def remove_task(self, name):
        if name in self.tasks:
            self.tasks.pop(name, None)
        self.display()

    def display(self):
        if self.tasks:  # if self.tasks is not None
            print('Here are your tasks:')
            for v in self.tasks.values():
                print('%s, %s, %s' % (v[0], v[1], v[2]))

    def __str__(self):  # print will call __str__ automatically
        return 'Schedule %s, %s' % (self.name, self.desp)


s = Schedule('s1', 'bittiger')
s.add_task('cs105', 'python', 1000)
s.add_task('cs000', 'java', 50)
