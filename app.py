import math
from datetime import datetime

import pymorphy2
from dateutil.relativedelta import relativedelta
from fuzzywuzzy import fuzz, process

from models.custom import Task
from models.request import AliceRequest
from models.response import Button, Response
from services import _get_task_times, decl

morph = pymorphy2.MorphAnalyzer()

sessionStorage = {}


class AliceHandler:
    def __init__(self, req: AliceRequest):
        self.req = req
        self.get_tasks()

    def handle_dialog(self) -> Response:
        if self.req.request.nlu.intents.add_task:
            return self.add_task()

        if self.req.request.nlu.intents.pause_task:
            return self.pause_task()

        if self.req.request.nlu.intents.resume_task:
            return self.resume_task()

        if self.req.request.nlu.intents.help:
            return self.get_help_response()

        if (
            self.req.request.nlu.intents.results
            or "результат" in self.req.request.original_utterance
            or "результат" in self.req.request.command
        ):
            return self.get_results()

        elif (
            self.req.request.nlu.intents.result_task
            or "результат последней задачи" in self.req.request.original_utterance
            or "результат последней задачи" in self.req.request.command
        ):
            return self.get_result_single()

        if self.req.session.new:
            return self.first_response()

        return self.wrong_response()

    def wrong_response(self):
        return Response(
            text="Я не могу понять то что вы сказали!",
            buttons=[
                Button(title="Помощь"),
                Button(title="Результат"),
            ],
        )

    def first_response(self):
        return Response(
            text=(
                "Привет! Я голосовой тайм-трекер!"
                "Я могу отслеживать время задач над которыми вы работаете, "
                "просто скажи начинаю задачу и кратко назови название задачи "
                "и я начту считать время ее выполнения "
            ),
            buttons=[
                Button(title="Что ты умеешь?"),
                Button(title="Результат"),
                Button(title="Результат последней задачи"),
            ],
        )

    def get_result_single(self):
        last_task = self.tasks[-1].name
        task_id = self.tasks[-1].id
        if task_id == "stop_any_task":
            last_task = self.tasks[-2].name
            task_id = self.tasks[-2].id

        task_time = _get_task_times(self.tasks)[task_id]
        task_seconds = math.ceil(task_time["total_time"] / 60)
        return Response(
            text=(
                f"Результат задачи {last_task} - {task_seconds} "
                f'{decl(task_seconds, ["минута", "минуты", "минут"])}!'
            )
        )

    def get_results(self):
        task_times = _get_task_times(self.tasks)
        if not task_times:
            return Response(text="Сегодня Вы ничего не делали!")

        task_texts = [
            (
                f'{t["name"]} - {math.ceil(t["total_time"]/60)} '
                f'{decl(math.ceil(t["total_time"]/60), ["минута", "минуты", "минут"])}'
            )
            for n, t in task_times.items()
        ]
        return Response(text=f"Ваши задачи: {', '.join(task_texts)}")

    def pause_task(self):
        if self.tasks[-1].id == "stop_any_task":
            response = Response(text=f"Задача {self.tasks[-2].name} уже остановлена!")

        self.tasks.append(Task(id="stop_any_task"))
        response = Response(text=f"Задача {self.tasks[-2].name} остановлена!")
        return response

    def get_help_response(self):
        response = Response(
            text=(
                "Я могу отслеживать время задач над которыми вы работаете, "
                "просто скажи начинаю задачу и кратко назови название задачи "
                "и я запомню время ее начала, затем можешь сказать останови "
                "или поставь на паузу текущую задачу, "
                "либо скажи что начинаешь новую задачу, "
                "я начну считать ее время."
            ),
            buttons=[
                Button(title="Начинаю задачу подготовка технического задания"),
                Button(title="Результат"),
            ],
        )

        return response

    def resume_task(self):
        last_task = self.tasks[-1].name
        task_id = self.tasks[-1].id
        if task_id == "stop_any_task":
            last_task = self.tasks[-2].name
            task_id = self.tasks[-2].id

        self.tasks.append(Task(id=task_id, name=last_task))
        return Response(text=f"Продолжаем задачу {last_task}!")

    def add_task(self):
        task_name = self.req.request.nlu.intents.add_task.slots.task_name.value
        task_id = " ".join([morph.parse(w)[0].normal_form for w in task_name.split()])

        best_match = process.extractOne(
            task_id, [t.id for t in self.tasks], scorer=fuzz.WRatio
        )
        if best_match:
            if best_match[1] >= 60:
                task_id = best_match[0]
                task = next(filter(lambda task: task.id == task_id, self.tasks), None)
                if task:
                    task_name = task.name

        self.tasks.append(Task(id=task_id, name=task_name))
        return Response(text=f"Задача {task_name} начата!")

    def get_tasks(self):
        if not self.req.state:
            self.tasks = []
        elif not self.req.state.user:
            self.tasks = self.req.state.session.tasks
        else:
            self.tasks = self.req.state.user.tasks

        self.tasks = [
            task
            for task in self.tasks
            if task.date_time >= datetime.utcnow() - relativedelta(hours=24)
        ]
