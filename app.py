from models.request import AliceRequest

sessionStorage = {}


def handle_dialog(req: AliceRequest):
    res = {
        "version": req.version,
        "session": req.session,
        "response": {"end_session": False},
    }

    user_id = req.session.user_id

    if req.session.new:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        sessionStorage[user_id] = {"suggests": ["Не хочу.", "Не буду.", "Отстань!"]}

        res["response"]["text"] = "Привет! Купи слона!"
        res["response"]["tts"] = "Привет! Купи слона!"
        res["response"]["buttons"] = get_suggests(user_id)
        return res

    # Обрабатываем ответ пользователя.
    if req.request.original_utterance.lower() in [
        "ладно",
        "куплю",
        "покупаю",
        "хорошо",
    ]:
        # Пользователь согласился, прощаемся.
        res["response"]["text"] = "Слона можно найти на Яндекс.Маркете!"
        return res

    # Если нет, то убеждаем его купить слона!
    res["response"]["text"] = 'Все говорят "%s", а ты купи слона!' % (
        req.request.original_utterance
    )
    res["response"]["buttons"] = get_suggests(user_id)

    return res


def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
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
