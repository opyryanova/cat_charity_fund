# QRKot — благотворительный фонд помощи котикам

## Описание проекта
**QRKot** — приложение для управления благотворительными проектами и
пожертвованиями.  
Фонд собирает средства на конкретные цели (лечение, корм, приюты), а
пользователи могут делать пожертвования.  
Система автоматически распределяет поступившие деньги в самые ранние открытые
проекты, пока они не наберут нужную сумму.

---

## Основные возможности
- создание целевых проектов с описанием и требуемой суммой сбора;
- создание пожертвований и автоматическое распределение средств;
- закрытие проекта при достижении полной суммы;
- просмотр списка всех проектов и статуса их финансирования;
- доступ к документации API (Swagger и ReDoc);
- управление пользователями и аутентификация через JWT-токены.

---

## Технологии
- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy 2.0 (Async)**
- **Alembic**
- **Pydantic v2**
- **SQLite + aiosqlite**
- **Uvicorn**
- **aiogoogle (Google API client)**
- **pytest**

---

## Запуск проекта локально

1. **Клонировать репозиторий**
   ```bash
   git clone <your-repo-url>
   cd cat_charity_fund
   ```

2. **Создать и активировать виртуальное окружение**
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS / Linux
   venv\Scripts\activate         # Windows
   ```

3. **Установить зависимости**
   ```bash
   pip install -r requirements.txt
   ```

4. **Создать файл .env с переменными окружения**

Создайте файл `.env` в корне проекта и добавьте в него следующие параметры:

   ```env
   # Настройки приложения и базы
   DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
   SECRET=your_secret_key

   FIRST_SUPERUSER_EMAIL=admin@example.com
   FIRST_SUPERUSER_PASSWORD=admin123

   # Настройки сервисного аккаунта Google
   TYPE=service_account
   PROJECT_ID=your_project_id
   PRIVATE_KEY_ID=your_private_key_id
   PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n
   CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
   CLIENT_ID=your_client_id
   AUTH_URI=https://accounts.google.com/o/oauth2/auth
   TOKEN_URI=https://oauth2.googleapis.com/token
   AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
   CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com
   ```

   Для работы отчета в Google Sheets сервисному аккаунту нужно выдать доступ к Google Диску / Таблицам согласно настройкам вашего аккаунта.


5. **Применить миграции Alembic**
   ```bash
   alembic upgrade head
   ```

6. **Запустить сервер**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Открыть документацию API**
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Основные эндпоинты
#### Пользователи и аутентификация

|   Метод  | URL                     | Назначение                                  |
| :------: | :---------------------- | :------------------------------------------ |
|  `POST`  | `/auth/register`        | Регистрация пользователя                    |
|  `POST`  | `/auth/jwt/login`       | Аутентификация (JWT)                        |
|   `GET`  | `/users/me`             | Профиль текущего пользователя               |

#### Проекты

|   Метод  | URL                     | Назначение                                  |
| :------: | :---------------------- | :------------------------------------------ |
|   `GET`  | `/charity_project/`     | Список проектов                             |
|  `POST`  | `/charity_project/`     | Создание проекта *(только суперюзеры)*      |
|  `PATCH` | `/charity_project/{id}` | Изменение проекта *(только суперюзеры)*     |
| `DELETE` | `/charity_project/{id}` | Удаление проекта *(только суперюзеры)*      |

#### Пожертвования

|   Метод  | URL                     | Назначение                                  |
| :------: | :---------------------- | :------------------------------------------ |
|  `POST`  | `/donation/`            | Создание пожертвования                      |
|   `GET`  | `/donation/`            | Все пожертвования *(только суперюзеры)*     |
|   `GET`  | `/donation/my`          | Пожертвования текущего пользователя         |

#### Отчет в Google Sheets

|   Метод  | URL                     | Назначение                                  |
| :------: | :---------------------- | :------------------------------------------ |
|   `GET`  | `/google/`              | Формирование отчета по закрытым проектам в Google Sheets (только суперюзеры)         |

---

## Тестирование
Для проверки корректности работы приложения:
```bash
pytest -v
```

---

## Автор
[Ольга Пырьянова](https://github.com/opyryanova)
