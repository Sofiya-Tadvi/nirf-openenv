import requests
import os
import time

BASE_URL = "http://localhost:8000"

print("[START] Beginning inference")

def run_task(task_id):
    print(f"[STEP] Running task {task_id}")

    # Reset environment
    res = requests.post(f"{BASE_URL}/reset")
    obs = res.json()

    print(f"[STEP] Task: {obs.get('task_description')}")

    # Step 1: Query data
    action = {
        "thought": "Fetching student data",
        "sql_query": "SELECT * FROM students WHERE dept='CSE'",
        "to_submit": False
    }

    res = requests.post(f"{BASE_URL}/step", json=action)
    data = res.json()

    print(f"[STEP] Query reward: {data.get('reward')}")

    # Step 2: Submit answer (dummy logic)
    action = {
        "thought": "Submitting answer",
        "final_ans": "50",
        "to_submit": True
    }

    res = requests.post(f"{BASE_URL}/step", json=action)
    data = res.json()

    print(f"[STEP] Final reward: {data.get('reward')}")

for i in range(3):
    run_task(i)
    time.sleep(1)

print("[END] Inference complete")