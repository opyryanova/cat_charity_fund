from enum import Enum


class ErrorMessages(str, Enum):
    PROJECT_NOT_FOUND = 'Проект не найден.'
    DUPLICATE_NAME = 'Проект с таким именем уже существует!'
    FULL_AMOUNT_LESS_THAN_INVESTED = (
        'Нелья установить значение full_amount '
        'меньше уже вложенной суммы.'
    )
    PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'
    PROJECT_HAS_INVESTMENTS = (
        'В проект были внесены средства, не подлежит удалению!'
    )
    DONATION_NOT_FOUND = 'Пожертвование не найдено.'
    DONATION_UPDATE_FORBIDDEN = 'Редактирование пожертвований запрещено.'
    DONATION_DELETE_FORBIDDEN = 'Удаление пожертвований запрещено.'
    METHOD_NOT_ALLOWED = 'Метод не разрешён.'
    UNEXPECTED_ERROR = 'Произошла непредвиденная ошибка.'


class CommonMessages(str, Enum):
    APP_TITLE = 'QRKot — благотворительный фонд помощи котикам'
    APP_DESCRIPTION = (
        'Приложение для учёта целевых проектов и пожертвований. '
        'Средства распределяются автоматически '
        'в самые ранние открытые проекты.'
    )
    SUCCESS_DELETE = 'Объект успешно удалён.'
    SUCCESS_UPDATE = 'Изменения успешно сохранены.'
    SUCCESS_CREATE = 'Объект успешно создан.'


PASSWORD_MIN_LENGTH = 3
TOKEN_LIFE_CYCLE = 3600

PROJECT_NAME_MIN_LENGTH = 5
PROJECT_NAME_MAX_LENGTH = 100
PROJECT_DESC_MIN_LENGTH = 10

DONATION_COMMENT_DISPLAY_LIMIT = 30
API_RESPONSE_LIMIT = 100

DAYS_IN_YEAR = 365
DAYS_IN_MONTH = 30