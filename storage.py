import os
import pickle
import threading
from datetime import datetime
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(BASE_DIR, "data", "db.bin")

class DataStore:
    def __init__(self, path=DEFAULT_DB):
        self.path = path
        self.lock = threading.Lock()
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "rb") as handle:
                    return pickle.load(handle)
            except Exception:
                return self._create_empty()
        return self._create_empty()

    def _create_empty(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        data = {
            "next_id": {
                "user": 1,
                "project": 1,
                "task": 1,
                "story": 1,
                "notification": 1,
                "history": 1,
            },
            "users": {},
            "projects": {},
            "tasks": {},
            "stories": {},
            "notifications": {},
            "history": {},
        }
        # Temporarily assign self.data so _make_user can increment IDs correctly.
        self.data = data
        admin = self._make_user(
            email="admin@pixelco.test",
            name="Administrateur",
            password="admin",
            roles=["admin", "project_manager"],
            active=True,
        )
        data["users"][admin["id"]] = admin
        self._save(data)
        return data

    def _make_user(self, email, name, password, roles, active=True):
        return {
            "id": self._next("user"),
            "email": email,
            "name": name,
            "password_hash": generate_password_hash(password),
            "roles": roles,
            "active": active,
            "projects": [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

    def _next(self, collection):
        newid = self.data["next_id"][collection]
        self.data["next_id"][collection] += 1
        return newid

    def _save(self, data=None):
        if data is None:
            data = self.data
        with self.lock:
            with open(self.path, "wb") as handle:
                pickle.dump(data, handle)

    def save(self):
        self.data["updated_at"] = datetime.utcnow().isoformat()
        self._save()

    def get_user_by_email(self, email):
        return next((u for u in self.data["users"].values() if u["email"] == email), None)

    def get_user(self, user_id):
        return self.data["users"].get(int(user_id))

    def add_user(self, email, name, password, roles):
        if self.get_user_by_email(email):
            return None
        user = self._make_user(email=email, name=name, password=password, roles=roles)
        self.data["users"][user["id"]] = user
        self.save()
        return user

    def update_user(self, user_id, **fields):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in fields.items():
            if value is not None:
                user[key] = value
        user["updated_at"] = datetime.utcnow().isoformat()
        self.save()
        return user

    def add_project(self, title, description, due_date, owner_id, priority="medium"):
        project = {
            "id": self._next("project"),
            "title": title,
            "description": description,
            "due_date": due_date,
            "status": "not_started",
            "priority": priority,
            "owner_id": owner_id,
            "members": [owner_id],
            "archived": False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "history": [],
            "story_ids": [],
            "task_ids": [],
        }
        self.data["projects"][project["id"]] = project
        self._record_history("project", project["id"], owner_id, "created", {"title": title})
        self.save()
        return project

    def get_project(self, project_id):
        return self.data["projects"].get(int(project_id))

    def update_project(self, project_id, **fields):
        project = self.get_project(project_id)
        if not project:
            return None
        for key, value in fields.items():
            if value is not None:
                project[key] = value
        project["updated_at"] = datetime.utcnow().isoformat()
        self._record_history("project", project_id, fields.get("actor_id"), "updated", fields)
        self.save()
        return project

    def archive_project(self, project_id, actor_id):
        return self.update_project(project_id, archived=True, status="archived", actor_id=actor_id)

    def add_task(self, title, description, project_id, created_by, priority="medium", due_date=None, assignee_id=None):
        task = {
            "id": self._next("task"),
            "title": title,
            "description": description,
            "project_id": int(project_id),
            "status": "todo",
            "priority": priority,
            "assignee_id": int(assignee_id) if assignee_id else None,
            "due_date": due_date,
            "estimate": None,
            "blocked": False,
            "block_reason": None,
            "dependency_ids": [],
            "comments": [],
            "files": [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "history": [],
        }
        self.data["tasks"][task["id"]] = task
        project = self.get_project(project_id)
        if project:
            project["task_ids"].append(task["id"])
            project["updated_at"] = datetime.utcnow().isoformat()
        self._record_history("task", task["id"], created_by, "created", {"title": title})
        self.save()
        return task

    def get_task(self, task_id):
        return self.data["tasks"].get(int(task_id))

    def update_task(self, task_id, **fields):
        task = self.get_task(task_id)
        if not task:
            return None
        for key, value in fields.items():
            if value is not None and key != "actor_id":
                task[key] = value
        task["updated_at"] = datetime.utcnow().isoformat()
        self._record_history("task", task_id, fields.get("actor_id"), "updated", fields)
        self.save()
        return task

    def add_story(self, title, description, actor, need, outcome, project_id, created_by, priority="medium"):
        story = {
            "id": self._next("story"),
            "title": title,
            "description": description,
            "actor": actor,
            "need": need,
            "outcome": outcome,
            "project_id": int(project_id),
            "status": "proposed",
            "priority": priority,
            "acceptance_criteria": [],
            "task_ids": [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "history": [],
        }
        self.data["stories"][story["id"]] = story
        project = self.get_project(project_id)
        if project:
            project["story_ids"].append(story["id"])
            project["updated_at"] = datetime.utcnow().isoformat()
        self._record_history("story", story["id"], created_by, "created", {"title": title})
        self.save()
        return story

    def get_story(self, story_id):
        return self.data["stories"].get(int(story_id))

    def update_story(self, story_id, **fields):
        story = self.get_story(story_id)
        if not story:
            return None
        for key, value in fields.items():
            if value is not None and key != "actor_id":
                story[key] = value
        story["updated_at"] = datetime.utcnow().isoformat()
        self._record_history("story", story_id, fields.get("actor_id"), "updated", fields)
        self.save()
        return story

    def add_notification(self, user_id, message):
        note = {
            "id": self._next("notification"),
            "user_id": int(user_id),
            "message": message,
            "read": False,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.data["notifications"][note["id"]] = note
        self.save()
        return note

    def mark_notification_read(self, note_id):
        note = self.data["notifications"].get(int(note_id))
        if note:
            note["read"] = True
            self.save()
        return note

    def _record_history(self, entity_type, entity_id, actor_id, action, details):
        entry = {
            "id": self._next("history"),
            "entity_type": entity_type,
            "entity_id": int(entity_id),
            "actor_id": int(actor_id) if actor_id else None,
            "action": action,
            "details": details,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.data["history"][entry["id"]] = entry
        target = self._entity(entity_type, entity_id)
        if target is not None:
            target.setdefault("history", []).append(entry["id"])
        return entry

    def _entity(self, entity_type, entity_id):
        return self.data.get(f"{entity_type}s", {}).get(int(entity_id))

    def search_projects(self, query=None, status=None, priority=None, owner_id=None):
        projects = list(self.data["projects"].values())
        if status:
            projects = [p for p in projects if p["status"] == status]
        if priority:
            projects = [p for p in projects if p["priority"] == priority]
        if owner_id:
            projects = [p for p in projects if p["owner_id"] == int(owner_id)]
        if query:
            query = query.lower()
            projects = [p for p in projects if query in p["title"].lower() or query in p["description"].lower()]
        return projects

    def search_tasks(self, query=None, status=None, priority=None, assignee_id=None, due_date=None, project_id=None):
        tasks = list(self.data["tasks"].values())
        if project_id:
            tasks = [t for t in tasks if t["project_id"] == int(project_id)]
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        if priority:
            tasks = [t for t in tasks if t["priority"] == priority]
        if assignee_id:
            tasks = [t for t in tasks if t["assignee_id"] == int(assignee_id)]
        if due_date:
            tasks = [t for t in tasks if t["due_date"] == due_date]
        if query:
            query = query.lower()
            tasks = [t for t in tasks if query in t["title"].lower() or query in t["description"].lower()]
        return tasks

    def list_notifications_for_user(self, user_id):
        return [n for n in self.data["notifications"].values() if n["user_id"] == int(user_id)]

    def list_history(self, entity_type, entity_id):
        return [entry for entry in self.data["history"].values() if entry["entity_type"] == entity_type and entry["entity_id"] == int(entity_id)]
