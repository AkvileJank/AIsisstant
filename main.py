from session import Session
from fileIO import FileIO
from planningAI import PlanningAI


def main():
    session = Session()
    file = FileIO()
    planner = PlanningAI()
    session.run_session(planner, file)

if __name__ == "__main__":
    main()
