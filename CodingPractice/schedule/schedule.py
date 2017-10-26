import os
import sys
import yaml
from datetime import datetime


FILEPATH = os.path.expanduser('~') + '/.schedule.yml'  #?


def display_time_decorator(func):
    def wrapper(*arg, **kwargs):
        print(str(datetime.now()))
        return func(*arg, **kwargs)
    return wrapper


class Schedule(object):

    tasks = None

    def __init__(self):  # method contains self
        if os.path.isfile(FILEPATH):
            with open(FILEPATH, 'r+') as f:
                self.tasks = yaml.load(f)
        else:
            self.tasks = {}

    def _save_to_file(self):
        with open(FILEPATH, 'w+') as f:
            yaml.dump(self.tasks, f)

    @display_time_decorator
    def add_task(self, name, description, priority, due_hour=1):
        if name in self.tasks.keys():
            print('Task %s already exists.' % name)
        else:
            new_task = [name, description, priority, due_hour]
            self.tasks.update({name: new_task})
            print('Task %s has been added.' % name)
            self._save_to_file()

    @display_time_decorator
    def delete_task(self, name):
        if name not in self.tasks.keys():
            print('Cannot delete non-exist task %s.' % name)
        else:
            self.tasks.pop(name, None)
            print('Task %s has been deleted.' % name)
            self._save_to_file()

    def display(self):
        if self.tasks:
            for v in self.tasks.values():
                print('%s, %s, %s, %s' % (v[0], v[1], v[2], v[3]))


if __name__ == '__main__':

    schedule = Schedule()

    action = sys.argv[0]
    args = sys.argv[1:]

    def add(name, description, priority, due_hour):
        schedule.add_task(name, description, priority, due_hour)
        display()

    def delete(name):
        schedule.delete_task(name)
        display()

    def display():
        schedule.display()

    options = {
        'add': add,
        'delete': delete,
        'display': display
    }

    options[action](*args)
