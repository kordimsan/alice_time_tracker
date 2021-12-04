from models.request import AliceRequest, Task, UserState
from models.response import Response

sessionStorage = {}


def handle_dialog(req: AliceRequest) -> tuple:
    user_id = req.session.user_id
    tasks = req.state.user.tasks

    if req.session.new:
        return (
            Response(
                text="Привет! Купи слона!",
                buttons=get_suggests(user_id),
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
        return (
            Response(text="Результат задачи!"),
            UserState(tasks=tasks),
        )


def get_user(user_id):
    if user_id not in sessionStorage:
        sessionStorage[user_id] = {
            "tasks": [],
            "suggests": ["Начни задачу"],
        }
    return sessionStorage[user_id]


def get_suggests(user_id):
    session = get_user(user_id)
    suggests = [{"title": suggest, "hide": True} for suggest in session["suggests"][:2]]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session["suggests"] = session["suggests"][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append(
            {
                "title": "Ладно",
                "url": "https://market.yandex.ru/search?text=слон",
                "hide": True,
            }
        )

    return suggests
