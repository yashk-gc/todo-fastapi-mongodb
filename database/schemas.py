def individual_task(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
        "is_completed": todo["is_completed"],
        "is_deleted": todo["is_deleted"],
        "created_at": todo["created_at"],
        "updated_at": todo["updated_at"],
    }


def all_tasks(todos):
    return [individual_task(todo) for todo in todos]


