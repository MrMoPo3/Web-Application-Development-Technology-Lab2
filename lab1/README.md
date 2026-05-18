# PollCraft

PollCraft - Web-додаток для створення опитувань, додавання варіантів відповідей, голосування та перегляду статистики.

Проєкт містить:
- `src/` - клієнтська частина React + Vite;
- `backend/` - серверна частина Python/Django + Django REST Framework;
- `docs/PollCraft.postman_collection.json` - готові запити й тести для Postman;
- `backend/schema.yml` та `/api/docs/redoc/` - OpenAPI/Redoc документація.

## Запуск клієнта

```powershell
cd C:\Users\levch\PycharmProjects\Web-Application-Development-Technology\lab1
npm.cmd install
npm.cmd run dev
```

Клієнт відкривається за адресою `http://127.0.0.1:5173/`.

## Запуск серверної частини

```powershell
cd C:\Users\levch\PycharmProjects\Web-Application-Development-Technology\lab1\backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Якщо PowerShell блокує активацію `.venv`, виконайте:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Сервер API відкривається за адресою `http://127.0.0.1:8000/`.

## Основні API endpoint-и

- `POST /api/auth/register/` - реєстрація користувача: `name`, `email`, `gender`, `birth_date`, `password`;
- `POST /api/auth/login/` - вхід за `email` і `password`;
- `GET /api/auth/profile/` - профіль користувача;
- `PATCH /api/auth/profile/` - оновлення профілю;
- `GET /api/about/` - інформація про додаток;
- `GET /api/polls/` - список опитувань;
- `POST /api/polls/` - створення опитування з варіантами відповідей;
- `POST /api/polls/{id}/vote/` - голосування;
- `GET /api/polls/{id}/stats/` - статистика голосів;
- `GET /api/docs/redoc/` - документація Redoc.

Для захищених endpoint-ів у Postman додайте header:

```http
Authorization: Token <token>
```

Токен повертається після реєстрації або входу.

## Django Admin Panel

Адмінка доступна за адресою `http://127.0.0.1:8000/admin/`.

Через Django Admin Panel можна наповнювати базу користувачами, опитуваннями, варіантами відповідей і голосами.

## Перевірка

```powershell
cd C:\Users\levch\PycharmProjects\Web-Application-Development-Technology\lab1\backend
py manage.py test
py manage.py spectacular --file schema.yml
```
