import subprocess
import os

PLANNER_PATH = "planning/downward/fast-downward.py"

def run_planner():
    # Remove previous plan if exists
    if os.path.exists("sas_plan"):
        os.remove("sas_plan")

    result = subprocess.run([
        "./" + PLANNER_PATH,
        "planning/domain.pddl",
        "planning/problem.pddl",
        "--search",
        "lazy_greedy([ff()], preferred=[ff()])"
    ])

    if result.returncode != 0 or not os.path.exists("sas_plan"):
        print("?? No valid plan found.")
        return []

    return parse_plan_file("sas_plan")

def parse_plan_file(path):
    plan = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith(";"):
                plan.append(line)
    return plan
