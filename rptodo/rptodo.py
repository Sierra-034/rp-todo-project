"""This module provides the RP To-Do model-controller"""

from pathlib import Path
from typing import Any, Dict, NamedTuple, List

from rptodo import DB_READ_ERROR
from rptodo.database import DatabaseHandler

class CurrenTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int


class Todoer:

    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: List[str], priority: int = 2) -> CurrenTodo:
        """Add a new to-do to the database."""
        description_text = ' '.join(description)
        if not description_text.endswith('.'):
            description_text += '.'
        
        todo = {
            'Description': description_text,
            'Priority': priority,
            'Done': False,
        }

        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrenTodo(todo, read.error)

        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrenTodo(todo, write.error)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Get the current to-do list."""
        read = self._db_handler.read_todos()
        return read.todo_list
