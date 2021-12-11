from datetime import datetime

from dateutil.relativedelta import relativedelta


def _get_task_times(tasks):
    tasks_list = [t.dict() for t in tasks] + [
        {"_id": None, "name": None, "date_time": datetime.utcnow()}
    ]
    task_times = {}
    for index in range(len(tasks_list) - 1):
        task_id = tasks_list[index]["_id"]
        task_name = tasks_list[index]["name"]
        task_start = tasks_list[index]["date_time"]
        task_end = tasks_list[index + 1]["date_time"]
        task_time = (task_end - task_start).total_seconds()
        if (
            task_id != "stop_any_task"
            and task_start > datetime.utcnow() - relativedelta(hours=24)
        ):
            if task_id not in task_times:
                total_time = 0
                task_times[task_id] = {"name": task_name, "total_time": total_time}

            total_time = total_time + task_time
            task_times[task_id]["total_time"] = total_time

    return task_times


def decl(number: int, titles: list):
    cases = [2, 0, 1, 1, 1, 2]
    if 4 < number % 100 < 20:
        idx = 2
    elif number % 10 < 5:
        idx = cases[number % 10]
    else:
        idx = cases[5]

    return titles[idx]
