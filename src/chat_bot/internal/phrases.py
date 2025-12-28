from .intent.date import get_date
from .intent.news import get_news
from .intent.time import get_time
from .intent.wiki import get_wiki
from .intent.weather import get_weather


class PhraseManager:
    def __init__(self, phrases_dict: dict):
        self._phrases_dict = phrases_dict
        self._user_indices = {}

    def get(self, category: str, user_id: int, text: str = None) -> str:
        if category not in self._phrases_dict:
            raise ValueError(f"Category '{category}' not found.")
        if user_id not in self._user_indices:
            self._user_indices[user_id] = {key: 0 for key in self._phrases_dict}
        phrases = self._phrases_dict[category]
        user_counters = self._user_indices[user_id]
        index = user_counters[category]
        phrase = phrases[index]
        user_counters[category] = (index + 1) % len(phrases)
        if callable(phrase):
            return phrase(text=text)
        return phrase

_all_phrases = {
    "origin": [
        "Я Нейро. Я тут, благодаря @KvaytG.",
        "Меня зовут Нейро. Меня создал @KvaytG.",
        "Моё имя Нейро. @KvaytG — мой разработчик.",
        "Меня знают как Нейро. Меня сделал @KvaytG.",
        "Нейро — это я. @KvaytG — мой автор."
    ],
    "time": [
        lambda text: f"Сейчас <b>{get_time()}</b> (МСК)",
        lambda text: f"Текущее время: <b>{get_time()}</b> (МСК)",
        lambda text: f"В данный момент на часах <b>{get_time()}</b> (МСК)",
        lambda text: f"Сейчас по моим часам <b>{get_time()}</b> (МСК)",
        lambda text: f"Сейчас время <b>{get_time()}</b> (МСК)"
    ],
    "date": [
        lambda text: f"Сегодня <b>{get_date()}</b> (МСК)",
        lambda text: f"На сегодня <b>{get_date()}</b> (МСК)",
        lambda text: f"По календарю сегодня <b>{get_date()}</b> (МСК)",
        lambda text: f"Сегодняшняя дата: <b>{get_date()}</b> (МСК)",
        lambda text: f"Сегодня, как видим, <b>{get_date()}</b> (МСК)"
    ],
    "weather": [
        lambda text: get_weather(text)
    ],
    "news": [
        lambda text: get_news()
    ],
    "wiki": [
        lambda text: get_wiki(text)
    ]
}

phrase_manager = PhraseManager(_all_phrases)
