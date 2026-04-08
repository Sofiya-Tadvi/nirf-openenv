import pandas as pd
from typing import Tuple, Dict, Any
from openenv.core.env_server import Environment 

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import NIRFAction, NIRFObservation, TableSnippet , StepResult

class NIRFenv(Environment):
    def __init__(self):
        super().__init__()
        print("ENV CREATED:", type(self))

        self.students = pd.DataFrame([
            {"id":1,"name":"Arav","dept":"CSE","gender":"M","year":2025},
            {"id":2,"name":"Isha","dept":"CSE","gender":"F","year":2025},
            {"id":3,"name":"Ananya","dept":"ESE","gender":"F","year":2025},
            {"id":4,"name":"Vihaan","dept":"ME","gender":"M","year":2025}
       ])

        self.faculty = pd.DataFrame([
            {"id":101,"name":"DR.Sharma","dept":"CSE","designation":"Professor","phd":True},
            {"id":102,"name":"MR.Gupta","dept":"CSE","designation":"Asst Professor","phd":False}
        ])

    # ✅ ADD MULTIPLE TASKS
        self.tasks = [
            {
               "question": "Find percentage of female students in CSE (2025)",
               "answer": 50
           },
           {
               "question": "Count total faculty in CSE",
               "answer": 2
            },
           {
               "question": "Find number of female students in all departments",
               "answer": 2
           }
        ]

        self.current_task_index = 0
        self.task = self.tasks[self.current_task_index]["question"]

        self.rule = "Follow NIRF metric rules for calculation"
    
    def state(self) -> NIRFObservation:
        return NIRFObservation(
            task_description=self.task,
            available_table=["students", "faculty"],
            nirf_rules=self.rule
    )

    def reset(self) -> NIRFObservation:
        if not hasattr(self, "current_task_index"):
            self.current_task_index = 0
        self.current_task_index = (self.current_task_index + 1) % len(self.tasks)
        self.task = self.tasks[self.current_task_index]["question"]

        return NIRFObservation(
            task_description=self.task,
            available_table=["students", "faculty"],
            nirf_rules=self.rule
        )
        
    
    def step(self, action: NIRFAction) -> StepResult:
        reward = 0.0
        done = False
        info = {}

        observation = NIRFObservation(
            task_description=self.task,
            available_table=["students", "faculty"],
            nirf_rules=self.rule,
            query_result=None,
            error_msg=None
       )

        sql_query = action.sql_query or ""
        final_ans = action.final_ans or ""

        if sql_query:
            reward += 0.2

        if "students" in sql_query.lower():
            df_slice = self.students[self.students['dept'] == 'CSE']
            observation.query_result = TableSnippet(
                name="students",
                columns=list(df_slice.columns),
                rows=df_slice.to_dict(orient='records')
           )
            reward += 0.3

        if not sql_query and not final_ans:
            reward -= 0.1

        if action.to_submit and final_ans:
            try:
                correct_answer = self.tasks[self.current_task_index]["answer"]

                if str(final_ans) == str(correct_answer):
                   reward += 0.5
                   done = True
                else:
                   reward -= 0.2
                   observation.error_msg = "Incorrect answer"
            except:
                observation.error_msg = "Task error"
                reward -= 1.0
                done = True

        return StepResult(
           observation=observation,
           reward=reward,
           done=done,
           info=info
        )