# Управление задачами - Тестовое задание

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)


## Ключевые возможности сервиса
- Отображение задач/подзадач в виде проводника Windows (список задач/подзадач расположен слева, данные о них — справа)
- Создание и удаление задач
- Создание и удаление подзадач
- Вычисление необходимых полей в автоматическом режиме
- Бесшовная навигация между задачами/подзадачами (без перезагрузки страницы)

В текущей реализации проект использует базу данных SQLite, но при необходимости можно без проблем перейти и на боевой вариант, например, MySQL либо Postgres.

## Использованные при реализации проекта технологии
 - Python
 - Django
 - pytest

## Как установить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Apicqq/task_manager
```

```
cd task_manager
```

Установить зависимости из файла requirements.txt:

* Если у вас установлен Poetry:
    ```
    poetry install (--with testing для тестирования)
    ```
* Либо через стандартный менеджер зависимостей pip:
    
  Создайте виртуальное окружение:

    ```
    python3 -m venv venv
    ```
  Активируйте его:

    * Если у вас Linux/macOS
    
        ```
        source venv/bin/activate
        ```
    
    * Если у вас windows
    
        ```
        source venv/scripts/activate
        ```
    
        ```
        python3 -m pip install --upgrade pip
        ```
  И установите зависимости:
    ```
    pip install -r requirements.txt
    ```

Запустить проект (в зависимости от выбранного менеджера зависимости) можно командами:
- `poetry run python task_manager/manage.py runserver`
- `python task_manager/manage.py runserver`


## Автор проекта

[Никита Смыков](https://github.com/Apicqq)


