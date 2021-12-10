import math
from datetime import datetime

import pymorphy2
from dateutil.relativedelta import relativedelta

from models.custom import Task
from models.request import AliceRequest, UserState
from models.response import Button, Response

morph = pymorphy2.MorphAnalyzer()

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
        task_id = " ".join([morph.parse(w)[0].normal_form for w in task_name.split()])
        tasks.append(Task(_id=task_id, name=task_name))
        return (
            Response(text=f"Задача {task_name} начата!"),
            UserState(tasks=tasks),
        )

    if req.request.nlu.intents.pause_task:
        task_name = tasks[-1].name
        task_id = tasks[-1]._id
        if task_id == "stop_any_task":
            return (
                Response(text=f"Задача {tasks[-2].name} уже остановлена!"),
                UserState(tasks=tasks),
            )
        else:
            tasks.append(Task(_id="stop_any_task"))
            return (
                Response(text=f"Задача {tasks[-2].name} остановлена!"),
                UserState(tasks=tasks),
            )

    if req.request.nlu.intents.resume_task:
        last_task = tasks[-1].name
        task_id = tasks[-1]._id
        if task_id == "stop_any_task":
            last_task = tasks[-2].name
            task_id = tasks[-2]._id

        tasks.append(Task(_id=task_id, name=last_task))
        return (
            Response(text=f"Продолжаем задачу {last_task}!"),
            UserState(tasks=tasks),
        )

    if (
        req.request.nlu.intents.results
        or "результат" in req.request.original_utterance
        or "результат" in req.request.command
    ):
        task_times = _get_task_times(tasks)
        task_texts = [
            (
                f'{t["name"]} - {math.ceil(t["total_time"]/60)} '
                f'{decl(math.ceil(t["total_time"]/60), ["минута", "минуты", "минут"])}'
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
        last_task = tasks[-1].name
        task_id = tasks[-1]._id
        if task_id == "stop_any_task":
            last_task = tasks[-2].name
            task_id = tasks[-2]._id

        task_time = _get_task_times(tasks)[task_id]
        task_seconds = math.ceil(task_time["total_time"] / 60)

        return (
            Response(
                text=(
                    f"Результат задачи {last_task} - {task_seconds} "
                    f'{decl(task_seconds, ["минута", "минуты", "минут"])}!'
                )
            ),
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
