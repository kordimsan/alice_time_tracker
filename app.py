import math
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from models.custom import Task
from models.request import AliceRequest, UserState
from models.response import Button, Response

sessionStorage = {}


def handle_dialog(req: AliceRequest) -> tuple:
    if not req.state.user:
        return (
            Response(text="Что то не так с состоянием пользователя!"),
            UserState(),
        )

    tasks = req.state.user.tasks

    if req.request.nlu.intents.add_task:
        task_name = req.request.nlu.intents.add_task.slots.task_name.value
        tasks.append(Task(name=task_name))
        return (
            Response(text=f"Задача {task_name} начата!"),
            UserState(tasks=tasks),
        )

    if req.request.nlu.intents.pause_task:
        task_name = tasks[-1].name
        if task_name == "stop_any_task":
            return (
                Response(text=f"Задача {tasks[-2].name} уже остановлена!"),
                UserState(tasks=tasks),
            )
        else:
            tasks.append(Task(name="stop_any_task"))
            return (
                Response(text=f"Задача {tasks[-2].name} остановлена!"),
                UserState(tasks=tasks),
            )

    if req.request.nlu.intents.resume_task:
        last_task = tasks[-1].name
        if last_task == "stop_any_task":
            last_task = tasks[-2].name

        tasks.append(Task(name=last_task))
        return (
            Response(text=f"Продолжаем задачу {last_task}!"),
            UserState(tasks=tasks),
        )

    

    if (
        req.request.nlu.intents.results
        or "результат" in req.request.original_utterance
        or "результат" in req.request.command
    ):
        tasks_list = [t.dict() for t in tasks] + [                      #from here
            {"name": None, "date_time": datetime.utcnow()}
        ]
        task_times = {}
        for index in range(len(tasks_list) - 1):
            task_name = tasks_list[index]["name"]
            task_start = tasks_list[index]["date_time"]
            task_end = tasks_list[index + 1]["date_time"]
            task_time = task_end - task_start
            if (
                task_name != "stop_any_task"
                and task_start > datetime.utcnow() - relativedelta(hours=24)
            ):
                task_times[task_name] = (
                    task_times.get(task_name, timedelta()) + task_time
                )

        task_texts = [
            (
                f"{n} - {math.ceil(t.seconds/60)} "
                f'{decl(math.ceil(t.seconds/60), ["минута","минуты","минут"])}'
            )
            for n, t in task_times.items()
        ]

        print(task_texts)

        return (
            Response(text=f"Ваши задачи: {', '.join(task_texts)}"),
            UserState(tasks=tasks),
        )
    elif (
        req.request.nlu.intents.result_task
        or "результат последней задачи" in req.request.original_utterance
        or "результат последней задачи" in req.request.command
        ):
        task_in_list = tasks[-1] + [                     
            {"name": None, "date_time": datetime.utcnow()}
        ]
        task_in_time = {}
        task_name = task_in_list["name"]
        task_start = task_in_list["date_time"]
        task_end = task_in_list[+ 1]["date_time"]
        task_time = task_end - task_start
        if task_name != "stop_any_task":
                task_in_time[task_name] = (
                    task_in_time.get(task_name, timedelta()) + task_time
                )                                                                             #here i do
        return (
            Response(text=f"Результат задачи {task_name} {task_in_time}!"),
            UserState(tasks=tasks),
        )

    if req.session.new:
        return (
            Response(
                text="Привет! Я виртуальный тайм-трекер!",
                buttons=[
                    Button(title="Начинаю задачу"),
                    Button(title="Результат"),
                    Button(title="Результат последней задачи"),
                ],
            ),
            UserState(tasks=tasks),
        )

    return (
        Response(
            text=(
                "Я могу отслеживать время задач над которыми вы работаете, "
                "просто скажи запусти задачу и кратко назови название задачи "
                "и я запомню время ее начала, затем можешь сказать останови "
                "или поставь на паузу текущую задачу, "
                "либо скажи что начинаешь новую задачу, "
                "я начну считать ее время."
            ),
            buttons=[
                Button(title="Начинаю задачу"),
                Button(title="Результат"),
            ],
        ),
        UserState(tasks=tasks),
    )


def decl(number: int, titles: list):
    cases = [2, 0, 1, 1, 1, 2]
    if 4 < number % 100 < 20:
        idx = 2
    elif number % 10 < 5:
        idx = cases[number % 10]
    else:
        idx = cases[5]

    return titles[idx]
