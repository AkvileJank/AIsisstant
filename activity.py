from abc import ABC, abstractclassmethod, abstractmethod
from datetime import datetime

# This is a parent class for both Task and Evend classes, contains the logic that applies for both child classes
# not all methods are abstract, concrete methods are exact same for both classes
class Activity(ABC):

    def __init__(self, title, description, date):
        self.title = title
        self.description = description
        self.date = date

    @abstractclassmethod
    def create_new(cls):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @classmethod
    def get_activity_date(cls, activity_type):
        if activity_type == "task":
            date_input = input(f"Enter due date for task (format: YYYY-MM-DD): ")
        else:
            date_input = input(f"Enter date of the event (format: YYYY-MM-DD): ")
        try:
            return datetime.strptime(date_input, "%Y-%m-%d").date()
        except:
            raise ValueError

    def complete(self, activities):
        self.completion = True
        index = activities.index(self)
        return activities.pop(index) # pops from the list element at a given index

    def modify(self):
        while True:
            attribute = input("Attribute to change: ")
            if hasattr(self, attribute):
                new_value = input("New value: ")
                setattr(self, attribute, new_value)
                return True
            else:
                print("There is no such attribute, try again")



