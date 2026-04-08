import requests

url = "http://localhost:8000/step"

data = {
    "thought": "filter students",
    "sql_query": "SELECT * FROM students WHERE dept='CSE'",
    "final_ans": "50",
    "to_submit": True
}

print(requests.post(url, json=data).json())