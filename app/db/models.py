"""
Этот файл нужен для импорта всех бд моделей в него
Потом этот файл импортируетсяв env.py в папке alembic
Сделано это, чтобы не импортировать каждую модель в env.py
делая его чище и не убирая все модели далеко друг-от-друга
"""

from .user import User
from .task import Task
from .group_task import GroupTask
from .note import Note