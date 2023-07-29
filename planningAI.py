import openai
import os
from datetime import date
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


# Contains logic related to running the AI assistant - important to add API key to the .env file!
class PlanningAI:
    def set_api_key(self):
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            return True
        except:
            return

    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]

    def collect_both_activities(self, file):
        tasks_data = file.read_only("activities/tasks.csv")
        events_data = file.read_only("activities/events.csv")
        return tasks_data, events_data

# wrote an extensive prompt based on recommendations on prompt engineering to receive desirable outcome from the LLM
    def get_prompt(self, file, scheduling_unit):
        return f""" You are a friendly task management assistant, refering to user as <you>. \
Read through provided data. Today is {date.today().strftime('%Y-%m-%d (%A)')}. Based on these files content, having in \
mind current day and date in file, which is deadline in tasks, also urgency and difficulty, plan activities \
for {scheduling_unit} with estimated time stamps and insert meaningful break suggestions betweeen tasks, breaks can't be the last item and repeat in a row. \
Don't include tasks if the deadline is passed. Saturday and Sunday are for events only if they are happening that specifc day. \
Return schedule with dates (month and day), days of the week, time in 24 hour format and titles of activities. At the end of schedule, \
in a few short sentences explain why you scheduled this way. \
---
Data: ''' {self.collect_both_activities(file)}'''
---
"""
