"""
Консольный интерфейс для работы с самолётами.
"""

from typing import List

from .aeroplane import Aeroplane
from .api import AeroplanesAPI
from .storage import JSONSaver


def filter_aeroplanes_by_country(
    aeroplanes: List[Aeroplane], countries: List[str]
) -> List[Aeroplane]:
    """Фильтр по стране регистрации."""
    return [a for a in aeroplanes if a.origin_country in countries]


def top_by_altitude(aeroplanes: List[Aeroplane], n: int) -> List[Aeroplane]:
    """Топ N самолётов по высоте."""
    return sorted(aeroplanes, key=lambda a: a.altitude, reverse=True)[:n]


def user_interaction() -> None:
    """Взаимодействие с пользователем через консоль."""
    api = AeroplanesAPI()
    saver = JSONSaver()

    country = input("Введите название страны (на английском): ").strip()
    print("Загрузка данных...")
    try:
        raw = api.get_aeroplanes(country)
    except (RuntimeError, ValueError) as e:
        print(f"Ошибка: {e}")
        return

    aeroplanes = Aeroplane.cast_to_object_list(raw)
    print(f"Найдено самолётов: {len(aeroplanes)}")

    for a in aeroplanes:
        saver.add_aeroplane(a)

    top_n = int(input("Сколько самолётов вывести в топ по высоте? "))
    print("\nТоп по высоте:")
    for a in top_by_altitude(aeroplanes, top_n):
        print(a)

    countries_input = input(
        "\nВведите страны регистрации для фильтра (через запятую): "
    ).strip()
    if countries_input:
        countries = [c.strip() for c in countries_input.split(",")]
        print("\nСамолёты выбранных стран:")
        for a in filter_aeroplanes_by_country(aeroplanes, countries):
            print(a)


if __name__ == "__main__":
    user_interaction()