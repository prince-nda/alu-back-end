#!/usr/bin/python3
"""
using a REST API, and a given emp_ID, return info about their TODO list.
"""
import requests
import sys
import csv


if __name__ == "__main__":
    """ main section """
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <employee_id>")
        sys.exit(1)
    
    BASE_URL = 'https://jsonplaceholder.typicode.com'
    
    # Get employee details
    employee = requests.get(BASE_URL + f'/users/{sys.argv[1]}/').json()
    EMPLOYEE_NAME = employee.get("name")
    USER_ID = employee.get("id")
    
    # Get employee todos
    employee_todos = requests.get(BASE_URL + f'/users/{sys.argv[1]}/todos').json()
    
    # Display progress (original functionality)
    serialized_todos = {}
    for todo in employee_todos:
        serialized_todos.update({todo.get("title"): todo.get("completed")})

    COMPLETED_LEN = len([k for k, v in serialized_todos.items() if v is True])
    print("Employee {} is done with tasks({}/{}):".format(
        EMPLOYEE_NAME, COMPLETED_LEN, len(serialized_todos)))
    for key, val in serialized_todos.items():
        if val is True:
            print("\t {}".format(key))
    
    # Export to CSV (new functionality)
    filename = f"{USER_ID}.csv"
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        
        # Write all tasks for this employee
        for todo in employee_todos:
            writer.writerow([
                USER_ID,
                EMPLOYEE_NAME,
                todo.get("completed"),
                todo.get("title")
            ])
    
    print(f"Data exported to {filename}")
