from activity import Activity
import re

# All methods except activity_duration are inherited from the parent class (abstract)
class Event(Activity):
    def __init__(self, title, description, date, location, start_time, end_time):
        super().__init__(title, description, date)
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.completion = False

    @classmethod
    def activity_duration(cls, start_or_end):
        while True:
            duration_input = input(
                f'Enter event {start_or_end} time in format HH:MM or "-" if time is unknown: '
            )
            match = re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", duration_input)
            if duration_input == "-" or match:
                return duration_input

    @classmethod
    def create_new(cls, events):
        while True:
            try:
                title = input("Title: ")
                for event in events:
                    if title == event.title:
                        raise AttributeError
                description = input("Description: ")
                date = cls.get_activity_date("event")
                location = input('Location (if unsure, enter "-"): ')
                start_time = cls.activity_duration("start")
                end_time = cls.activity_duration("end")
                return cls(title, description, date, location, start_time, end_time)
            except AttributeError:
                print("Event with this title already exists, try again")
            except ValueError:
                print("Event input is incorrect, try again")
            except KeyboardInterrupt:
                return
            except:
                print("Something went wrong with adding new event, please try again")

    def __str__(self):
        return f"Event: {self.title}, Description: {self.description}, Date: {self.date}, \
Location: {self.location}, Start time: {self.start_time}, End time: {self.end_time}"
