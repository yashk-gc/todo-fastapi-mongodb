from datetime import datetime
from bson import ObjectId

from configurations import collection
from database.models import Todo
from database.schemas import all_tasks, individual_task


def _now_ts() -> int:
    return int(datetime.timestamp(datetime.now()))


def get_all_todos():
    data = collection.find({"is_deleted": False})
    return all_tasks(data)


def create_task(new_task: Todo):
    task_dict = new_task.dict()
    now = _now_ts()

    # ensure fields exist
    task_dict.setdefault("is_deleted", False)
    task_dict.setdefault("created_at", now)
    task_dict.setdefault("updated_at", now)

    resp = collection.insert_one(task_dict)
    created = collection.find_one({"_id": resp.inserted_id})
    return individual_task(created)


def get_single_task(task_id: str):
    todo = collection.find_one({"_id": ObjectId(task_id), "is_deleted": False})
    if not todo:
        return None
    return individual_task(todo)


def update_task(task_id: str, updated_task: Todo):
    oid = ObjectId(task_id)
    existing_doc = collection.find_one({"_id": oid, "is_deleted": False})
    if not existing_doc:
        return None

    task_dict = updated_task.dict()
    task_dict["updated_at"] = _now_ts()

    collection.update_one({"_id": oid}, {"$set": task_dict})
    updated = collection.find_one({"_id": oid, "is_deleted": False})
    if not updated:
        return None
    return individual_task(updated)


def delete_task(task_id: str):
    oid = ObjectId(task_id)
    existing_doc = collection.find_one({"_id": oid, "is_deleted": False})
    if not existing_doc:
        return 0

    result = collection.update_one(
        {"_id": oid},
        {"$set": {"is_deleted": True}},
    )
    return result.modified_count


def insert_multiple_tasks(tasks: list):
    now = _now_ts()
    for t in tasks:
        t.setdefault("is_completed", False)
        t["is_deleted"] = False
        t["created_at"] = now
        t["updated_at"] = now

    resp = collection.insert_many(tasks)
    inserted = collection.find({"_id": {"$in": resp.inserted_ids}})
    return [individual_task(todo) for todo in inserted]


