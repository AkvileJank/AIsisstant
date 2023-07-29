from activity import Activity

# all methods are inherited from the abstract Activity class
class Task(Activity):

    def __init__(self, title, description, date, difficulty, urgency):
        super().__init__(title, description, date)
        self.difficulty = difficulty
        self.urgency = urgency
        self.completion = False

    @classmethod
    def create_new(cls, tasks):
        while True:
            try:
                title = input("Title: ")
                for task in tasks:
                    if title == task.title:
                        raise AttributeError
                    if not title:
                        raise ValueError
                description = input("Description: ")
                date = cls.get_activity_date("task")
                difficulty = int(input("Difficulty (1-5): "))
                if difficulty > 5:
                    raise ValueError
                urgency = int(input("Urgency (1-5): "))
                if urgency > 5:
                    raise ValueError
                return cls(title, description, date, difficulty, urgency)
            except AttributeError:
                print("Task with this title already exists, try again")
            except ValueError:
                print("Task input is incorrect, try again")
            except KeyboardInterrupt:
                return
            except:
                print("Something went wrong with adding new task, please try again")

    def __str__(self):
        return f"Task: {self.title}, Description: {self.description}, Due date: {self.date}, Difficulty: {self.difficulty}, Urgency: {self.urgency}"

