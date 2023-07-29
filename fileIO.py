import csv
from task import Task
from event import Event

# chose to work with csv for this project for practice
class FileIO:
    def read_only(self, file_name):
        with open(file_name) as file:
            return file.read()

    def get_fieldnames(self, activity_type):
        match activity_type:
            case "Task":
                return [
                    "title",
                    "description",
                    "date",
                    "difficulty",
                    "urgency",
                    "completion",
                ]
            case "Event":
                return [
                    "title",
                    "description",
                    "date",
                    "location",
                    "start_time",
                    "end_time",
                    "completion",
                ]

    def get_activities(self, file_name, activities, activity_type):
        with open(file_name) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if activity_type == "Task":
                    activities.append(
                        Task(
                            row["title"],
                            row["description"],
                            row["date"],
                            row["difficulty"],
                            row["urgency"],
                        )
                    )
                else:
                    activities.append(
                        Event(
                            row["title"],
                            row["description"],
                            row["date"],
                            row["location"],
                            row["start_time"],
                            row["end_time"],
                        )
                    )
        return sorted(activities, key=lambda activity: activity.title)

    def write_activities(self, file_name, activities, activity_type):
        with open(file_name, "w") as file:
            fieldnames = self.get_fieldnames(activity_type)
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for activity in activities:
                writer.writerow(activity.__dict__)

    def append_activity(self, file_name, activities, activity_type):
        with open(file_name, "a") as file:
            fieldnames = self.get_fieldnames(activity_type)
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for activity in activities:
                writer.writerow(activity.__dict__)
