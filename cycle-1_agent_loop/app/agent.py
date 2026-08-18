import json
from pathlib import Path
from planner import plan_sql
from tools import get_database_schema, execute_sql
MAX_ITERATIONS = 5

LOG_FILE = Path("logs/agent_log.json")

def clear_log():
    with open(LOG_FILE, "w") as file:
        json.dump([], file)

def log_iteration(iteration, thought, action, observation):
    log_data = []

    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as file:
            log_data = json.load(file)

    log_data.append({
        "iteration": iteration,
        "thought": thought,
        "action": action,
        "observation": observation
    })

    with open(LOG_FILE, "w") as file:
        json.dump(log_data, file, indent=4)

def perceive():
    user_request = input("Enter your database question: ")
    return user_request

def is_success(result):
    return (
        result["success"] is True
        and len(result["results"]) > 0
    )

def main():
    clear_log()
    request = perceive()
    previous_observation = None

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- Iteration {iteration} ---")

        schema=get_database_schema()
        sql_query=plan_sql(
            request,
            schema,
            previous_observation
        )

        print("\nGenerated SQL:")
        print(sql_query)

        result=execute_sql(sql_query)

        print("\nObservation:")
        print(result)
        previous_observation = result

        log_iteration(
            iteration,
            "Generate SQL using the database schema and previous observation.",
            sql_query,
            result
        )

        if is_success(result):
            print("\nSuccess condition met.")
            break
        print("\nSuccess condition not met. Retrying...")

    else:
        print("\nMaximum iterations reached.")

if __name__=="__main__":
    main()