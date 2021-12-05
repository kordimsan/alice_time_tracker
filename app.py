from models.custom import Task
from models.request import AliceRequest, UserState
from models.response import Button, Response

sessionStorage = {}


def handle_dialog(req: AliceRequest) -> tuple:
    if not req.state.user:
        return (
            Response(text="Дима, тут что то не так с состоянием пользователя!"),
            UserState(),
        )

    tasks = req.state.user.tasks

    if req.session.new:
        return (
            Response(
                text="Привет! Я виртуальный тайм-трекер!",
                buttons=[
                    Button(title="Начинаю задачу"),
                    Button(title="Результат"),
                ],
            ),
            UserState(tasks=tasks),
        )

    if req.request.nlu.intents.add_task:
        task_name = req.request.nlu.intents.add_task.slots.task_name.value
        tasks.append(Task(name=task_name))
        return (
            Response(text=f"Задача {task_name} начата!"),
            UserState(tasks=tasks),
        )

    if req.request.nlu.intents.pause_task:
        tasks.append(Task(name="stop_any_task"))
        return (
            Response(text="Задача остановлена!"),
            UserState(tasks=tasks),
        )

    if req.request.nlu.intents.resume_task:
        tasks.append(Task(name="stop_any_task"))
        return (
            Response(text="Продолжаем задачу!"),
            UserState(tasks=tasks),
        )

    if req.request.nlu.intents.result_task:
        return (
            Response(text="Результат задачи!"),
            UserState(tasks=tasks),
        )

    if req.request.nlu.intents.results:
        tasks_list = {t.name for t in tasks if t.name not in ["stop_any_task"]}
        return (
            Response(text=f"Ваши задачи: {', '.join(tasks_list)}"),
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
