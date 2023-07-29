from task import Task
from event import Event
from activity import Activity
import re
import questionary
from rich.table import Table
from rich.console import Console


class Session:
    TASK_FILE = "activities/tasks.csv"
    TASK_ARCHIVE = "activities/completedTasks.csv"
    EVENT_FILE = "activities/events.csv"
    EVENT_ARCHIVE = "activities/completedEvents.csv"

    def __init__(self):
        self._activities = None
        self._completed_activities = []
        self._activity_type = None

    @property
    def activities(self):
        return self._activities

    @activities.setter
    def activities(self, value):
        self._activities = value

    @property
    def completed_activities(self):
        return self._completed_activities

    @activities.setter
    def completed_activities(self, value):
        self._completed_activities = value

    @property
    def activity_type(self):
        return self._activity_type

    @activity_type.setter
    def activity_type(self, value):
        self._activity_type = value

    def select_activity_type(self):
        activity_type = questionary.select(
            "Activity type:", choices=["Task", "Event", "<-"]
        ).ask()
        match activity_type:
            case "Task":
                self.activity_type = activity_type
                return self.TASK_FILE, self.TASK_ARCHIVE
            case "Event":
                self.activity_type = activity_type
                return self.EVENT_FILE, self.EVENT_ARCHIVE
            case "<-":
                raise TypeError # to return to the main menu, this error is caught in method run_session

    def add_mode(self):
        match self.activity_type:
            case "Task":
                activity = Task.create_new(self.activities)
            case "Event":
                activity = Event.create_new(self.activities)
        if not activity:
            self.choose_mode()
        self.activities.append(activity)
        print("This activity was added successfully")
        return True

    def show_mode(self):
        self.show_table(self.activities)
        return True

    def show_table(self, activities):
        table = Table()
        if self.activity_type == "Task":
            attribute_order = ["date", "title", "description", "difficulty", "urgency", "completion"]
        else:
            attribute_order = ["date", "title", "description","location", "start_time", "end_time", "completion"]
        for attribute_name in attribute_order:
            table.add_column(attribute_name)
        for activity in activities:
            row = [str(getattr(activity, attribute_name, "")) for attribute_name in attribute_order]
            table.add_row(*row)
        console = Console()
        console.print(table)

    def get_sorting_key(self):
        if self.activity_type == "Task":
            sort_key_input = questionary.select(
                "Select by what criteria to sort:",
                choices=["Date", "Difficulty", "Urgency", "<-"],
            ).ask()
            match sort_key_input:
                case "Date":
                    return lambda activity: activity.date, False
                case "Difficulty":
                    return lambda activity: activity.difficulty, True # most difficult tasks are shown at the top
                case "Urgency":
                    return lambda activity: activity.urgency, True # most urgent tasks are show at the top
                case "<-":
                    self.choose_mode()
        else:
            return lambda activity: activity.date, False # events are sorted only by date in an ascending order

    def show_sorted_mode(self):
        key, reverse = self.get_sorting_key()
        sorted_activities = sorted(self.activities, key=key, reverse=reverse)
        print("\n")
        self.show_table(sorted_activities)
        return True

    def show_by_date_mode(self):
        while True:
            try:
                date_input = str(Activity.get_activity_date(self.activity_type))
                filtered_activities = [
                    activity
                    for activity in self.activities
                    if re.match(date_input, activity.date)
                ]
                if not filtered_activities:
                    print("There are no activities for this date")
                self.show_table(filtered_activities)
                return True
            except ValueError:
                print("Provided date format is not correct")
            except KeyboardInterrupt:
                return self.choose_mode()

    def delete_mode(self):
        while True:
            try:
                activity_title_input = input("Enter title of activity: ")
                for activity in self.activities:
                    if activity_title_input == activity.title:
                        self.activities.remove(activity)
                        print("This activity was deleted successfully")
                        return True
                print("This activity is not found. Try again")
            except KeyboardInterrupt:
                return self.choose_mode()

    def modify_mode(self):
        while True:
            try:
                activity_title_input = input("Enter title of activity: ")
                for activity in self.activities:
                    if activity_title_input == activity.title:
                        if activity.modify():
                            print("This activity was modified successfully")
                            return True
                print("This activity is not found. Try again")
            except KeyboardInterrupt:
                return self.choose_mode()

    def complete_mode(self):
        while True:
            try:
                activity_title_input = input("Enter title of activity: ")
                for activity in self.activities:
                    if activity_title_input == activity.title:
                        completed_activity = activity.complete(self.activities)
                        self.completed_activities.append(completed_activity)
                        print("This activity was completed succesfully")
                        return True
                print("This activity is not found. Try again")
            except KeyboardInterrupt:
                return self.choose_mode()

    def planning_mode(self, planner, file):
        if not planner.set_api_key():
            raise KeyError
        scheduling_unit = questionary.select(
            "Do the planning for:", choices=["Today", "Week"]
        ).ask()
        if scheduling_unit.lower() == "today" or scheduling_unit.lower() == "week":
            print("Hang in there, the AI planner is working on your schedule!\n")
            return planner.get_completion(planner.get_prompt(file, scheduling_unit))

    def choose_mode(self):
        self.mode = questionary.select(
            "Choose what you would like to do: ",
            choices=[
                "Add",
                "Show activities",
                "Show sorted activities",
                "Show by specific date",
                "Delete",
                "Modify",
                "Complete",
                "<-",
            ],
        ).ask()
        match self.mode:
            case "Add":
                return self.add_mode()
            case "Show activities":
                return self.show_mode()
            case "Show sorted activities":
                return self.show_sorted_mode()
            case "Show by specific date":
                return self.show_by_date_mode()
            case "Delete":
                return self.delete_mode()
            case "Modify":
                return self.modify_mode()
            case "Complete":
                return self.complete_mode()
            case "<-":
                self.select_activity_type()


    def run_session(self, planner, file):
        while True:
            try:
                self.activities = []
                user_input = questionary.select(
                    "Manage activities or use AI planner?",
                    choices=["Manage activities", "Use AI planner", "Exit"],
                ).ask()
                if user_input == "Use AI planner":
                    print(self.planning_mode(planner, file))
                elif user_input == "Manage activities":
                    file_name, archive_file = self.select_activity_type()
                    self.activities = file.get_activities(
                        file_name, self.activities, self.activity_type
                    )
                    if self.choose_mode():
                        if self.mode == "complete":
                            file.append_activity(
                                archive_file,
                                self.completed_activities,
                                self.activity_type,
                            )
                        file.write_activities(
                            file_name, self.activities, self.activity_type
                        )
                else:
                    raise KeyboardInterrupt
            except TypeError:
                continue
            except KeyboardInterrupt:
                print("\nThank you for using!")
                break
            except KeyError:
                print("There is a problem connecting to openAI, try again")
            except:
                print("Something went wrong, try again")
