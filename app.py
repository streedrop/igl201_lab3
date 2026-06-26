import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from storage import DataStore

app = Flask(__name__)
app.secret_key = "pixelco-secret-key"
store = DataStore()


def create_app():
    return app

ROLE_ADMIN = "admin"
ROLE_PROJECT_MANAGER = "project_manager"
ROLE_DEVELOPER = "developer"
ROLE_MEMBER = "member"

STATUS_LABELS = {
    "not_started": "Non démarré",
    "in_progress": "En cours",
    "on_hold": "En attente",
    "done": "Terminé",
    "archived": "Archivé",
}

TASK_STATUS_LABELS = {
    "todo": "À faire",
    "in_progress": "En cours",
    "review": "En révision",
    "blocked": "Bloquée",
    "done": "Terminée",
    "cancelled": "Annulée",
}

PRIORITIES = ["low", "medium", "high", "critical"]
PRIORITY_LABELS = {"low": "Faible", "medium": "Moyenne", "high": "Élevée", "critical": "Critique"}


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return store.get_user(user_id)


def login_required(view):
    from functools import wraps

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def has_role(user, role):
    return user and role in user.get("roles", [])


def can_access_project(user, project):
    if not project or not user:
        return False
    return project["archived"] is False and user["id"] in project["members"] or has_role(user, ROLE_ADMIN)


def project_status_label(status):
    return STATUS_LABELS.get(status, status)


def task_status_label(status):
    return TASK_STATUS_LABELS.get(status, status)


def priority_label(priority):
    return PRIORITY_LABELS.get(priority, priority)


def collect_notifications(user_id):
    notes = store.list_notifications_for_user(user_id)
    return sorted(notes, key=lambda n: n["created_at"], reverse=True)


@app.route("/")
def home():
    if current_user():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = store.get_user_by_email(email)
        if user and user["active"] and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        flash("Identifiants invalides.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    projects = [p for p in store.data["projects"].values() if p["archived"] is False and (user["id"] in p["members"] or has_role(user, ROLE_ADMIN))]
    tasks = [t for t in store.data["tasks"].values() if t["assignee_id"] == user["id"]]
    overdue = [t for t in tasks if t["due_date"] and t["status"] != "done" and t["due_date"] < datetime.utcnow().date().isoformat()]
    urgent = [t for t in tasks if t["priority"] in ["high", "critical"] and t["status"] not in ["done", "cancelled"]]
    notifications = collect_notifications(user["id"])
    return render_template(
        "dashboard.html",
        user=user,
        projects=projects,
        tasks=tasks,
        overdue=overdue,
        urgent=urgent,
        notifications=notifications,
        project_status_label=project_status_label,
        task_status_label=task_status_label,
        priority_label=priority_label,
    )


@app.route("/projects")
@login_required
def projects():
    user = current_user()
    query = request.args.get("q", "")
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")
    project_list = store.search_projects(query=query, status=status or None, priority=priority or None)
    visible = [p for p in project_list if p["archived"] is False and (user["id"] in p["members"] or has_role(user, ROLE_ADMIN))]
    return render_template(
        "projects.html",
        user=user,
        projects=visible,
        query=query,
        status=status,
        priority=priority,
        project_status_label=project_status_label,
        priority_label=priority_label,
    )


@app.route("/projects/new", methods=["GET", "POST"])
@login_required
def project_new():
    user = current_user()
    if not has_role(user, ROLE_PROJECT_MANAGER) and not has_role(user, ROLE_ADMIN):
        flash("Permission refusée.")
        return redirect(url_for("projects"))
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]
        project = store.add_project(title, description, due_date, owner_id=user["id"], priority=priority)
        flash("Projet créé.", "success")
        return redirect(url_for("project_detail", project_id=project["id"]))
    return render_template("project_form.html", user=user, project=None, priorities=PRIORITIES)


@app.route("/projects/<int:project_id>")
@login_required
def project_detail(project_id):
    user = current_user()
    project = store.get_project(project_id)
    if not project or (user["id"] not in project["members"] and not has_role(user, ROLE_ADMIN)):
        flash("Projet introuvable ou accès refusé.")
        return redirect(url_for("projects"))
    project_tasks = [store.get_task(tid) for tid in project["task_ids"] if store.get_task(tid)]
    project_stories = [store.get_story(sid) for sid in project["story_ids"] if store.get_story(sid)]
    members = [store.get_user(uid) for uid in project["members"] if store.get_user(uid)]
    available_users = list(store.data["users"].values())
    history = store.list_history("project", project_id)
    return render_template(
        "project_detail.html",
        user=user,
        project=project,
        project_tasks=project_tasks,
        project_stories=project_stories,
        members=members,
        available_users=available_users,
        history=history,
        task_status_label=task_status_label,
        priority_label=priority_label,
        project_status_label=project_status_label,
    )


@app.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def project_edit(project_id):
    user = current_user()
    project = store.get_project(project_id)
    if not project or (not has_role(user, ROLE_PROJECT_MANAGER) and not has_role(user, ROLE_ADMIN) and user["id"] not in project["members"]):
        flash("Permission refusée.")
        return redirect(url_for("projects"))
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        status = request.form["status"]
        priority = request.form["priority"]
        store.update_project(project_id, title=title, description=description, due_date=due_date, status=status, priority=priority, actor_id=user["id"])
        flash("Projet mis à jour.", "success")
        return redirect(url_for("project_detail", project_id=project_id))
    return render_template("project_form.html", user=user, project=project, priorities=PRIORITIES, statuses=STATUS_LABELS)


@app.route("/projects/<int:project_id>/archive", methods=["POST"])
@login_required
def project_archive(project_id):
    user = current_user()
    project = store.get_project(project_id)
    if not project or (not has_role(user, ROLE_PROJECT_MANAGER) and not has_role(user, ROLE_ADMIN)):
        flash("Permission refusée.")
        return redirect(url_for("projects"))
    store.archive_project(project_id, actor_id=user["id"])
    flash("Projet archivé.")
    return redirect(url_for("projects"))


@app.route("/projects/<int:project_id>/members", methods=["POST"])
@login_required
def project_members(project_id):
    user = current_user()
    project = store.get_project(project_id)
    if not project or (not has_role(user, ROLE_PROJECT_MANAGER) and not has_role(user, ROLE_ADMIN)):
        flash("Permission refusée.")
        return redirect(url_for("project_detail", project_id=project_id))
    action = request.form.get("action")
    member_id = int(request.form.get("member_id", 0))
    if action == "add" and member_id and member_id not in project["members"]:
        project["members"].append(member_id)
        project["updated_at"] = datetime.utcnow().isoformat()
        store.save()
        flash("Membre ajouté.")
    if action == "remove" and member_id in project["members"]:
        project["members"].remove(member_id)
        project["updated_at"] = datetime.utcnow().isoformat()
        store.save()
        flash("Membre retiré.")
    return redirect(url_for("project_detail", project_id=project_id))


@app.route("/projects/<int:project_id>/tasks/new", methods=["GET", "POST"])
@login_required
def task_new(project_id):
    user = current_user()
    project = store.get_project(project_id)
    if not project or user["id"] not in project["members"] and not has_role(user, ROLE_ADMIN):
        flash("Permission refusée.")
        return redirect(url_for("project_detail", project_id=project_id))
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]
        assignee_id = request.form.get("assignee_id")
        task = store.add_task(title, description, project_id, created_by=user["id"], priority=priority, due_date=due_date, assignee_id=assignee_id or None)
        if assignee_id:
            store.add_notification(assignee_id, f"Tâche assignée: {task['title']}")
        flash("Tâche créée.", "success")
        return redirect(url_for("project_detail", project_id=project_id))
    members = [store.get_user(uid) for uid in project["members"] if store.get_user(uid)]
    return render_template("task_form.html", user=user, project=project, task=None, priorities=PRIORITIES, members=members)


@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def task_edit(task_id):
    user = current_user()
    task = store.get_task(task_id)
    if not task:
        flash("Tâche non trouvée.")
        return redirect(url_for("dashboard"))
    project = store.get_project(task["project_id"])
    if not project or user["id"] not in project["members"] and not has_role(user, ROLE_ADMIN):
        flash("Permission refusée.")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        status = request.form["status"]
        priority = request.form["priority"]
        assignee_id = request.form.get("assignee_id")
        due_date = request.form["due_date"]
        blocked = request.form.get("blocked") == "on"
        block_reason = request.form.get("block_reason") if blocked else None
        updates = {
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "assignee_id": int(assignee_id) if assignee_id else None,
            "due_date": due_date,
            "blocked": blocked,
            "block_reason": block_reason,
            "actor_id": user["id"],
        }
        if status == "done" and task["dependency_ids"]:
            dependencies = [store.get_task(dep) for dep in task["dependency_ids"]]
            if any(dep and dep["status"] != "done" for dep in dependencies):
                flash("Impossible de terminer la tâche tant que les dépendances ne sont pas terminées.")
                return redirect(url_for("task_edit", task_id=task_id))
        store.update_task(task_id, **updates)
        if assignee_id:
            store.add_notification(assignee_id, f"Tâche mise à jour: {title}")
        flash("Tâche mise à jour.")
        return redirect(url_for("project_detail", project_id=project["id"]))
    members = [store.get_user(uid) for uid in project["members"] if store.get_user(uid)]
    return render_template("task_form.html", user=user, project=project, task=task, priorities=PRIORITIES, members=members, statuses=TASK_STATUS_LABELS)


@app.route("/tasks/<int:task_id>/history")
@login_required
def task_history(task_id):
    user = current_user()
    task = store.get_task(task_id)
    if not task:
        flash("Tâche non trouvée.")
        return redirect(url_for("dashboard"))
    history = store.list_history("task", task_id)
    return render_template("history.html", user=user, history=history)


@app.route("/stories/new", methods=["GET", "POST"])
@login_required
def story_new():
    user = current_user()
    projects = [p for p in store.data["projects"].values() if user["id"] in p["members"] or has_role(user, ROLE_ADMIN)]
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        actor = request.form["actor"]
        need = request.form["need"]
        outcome = request.form["outcome"]
        project_id = request.form["project_id"]
        priority = request.form["priority"]
        store.add_story(title, description, actor, need, outcome, project_id, created_by=user["id"], priority=priority)
        flash("User story ajoutée.", "success")
        return redirect(url_for("projects"))
    return render_template("story_form.html", user=user, projects=projects, priorities=PRIORITIES, story=None)


@app.route("/users")
@login_required
def users():
    user = current_user()
    if not has_role(user, ROLE_ADMIN):
        flash("Permission refusée.")
        return redirect(url_for("dashboard"))
    users = list(store.data["users"].values())
    return render_template("users.html", user=user, users=users)


@app.route("/users/new", methods=["GET", "POST"])
@login_required
def user_new():
    user = current_user()
    if not has_role(user, ROLE_ADMIN):
        flash("Permission refusée.")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        name = request.form["name"]
        password = request.form["password"]
        roles = request.form.getlist("roles")
        new_user = store.add_user(email, name, password, roles)
        if new_user:
            flash("Utilisateur créé.")
            return redirect(url_for("users"))
        flash("Un utilisateur avec ce courriel existe déjà.")
    return render_template("user_form.html", user=user, edit=False)


@app.route("/notifications")
@login_required
def notifications():
    user = current_user()
    notes = collect_notifications(user["id"])
    return render_template("notifications.html", user=user, notifications=notes)


@app.route("/notifications/<int:notification_id>/read", methods=["POST"])
@login_required
def notification_read(notification_id):
    store.mark_notification_read(notification_id)
    return redirect(url_for("notifications"))


@app.context_processor
def inject_globals():
    return {
        "current_user": current_user(),
        "project_status_label": project_status_label,
        "task_status_label": task_status_label,
        "priority_label": priority_label,
        "STATUS_LABELS": STATUS_LABELS,
        "TASK_STATUS_LABELS": TASK_STATUS_LABELS,
        "PRIORITY_LABELS": PRIORITY_LABELS,
        "ROLE_ADMIN": ROLE_ADMIN,
        "ROLE_PROJECT_MANAGER": ROLE_PROJECT_MANAGER,
        "store": store,
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    app.run(host="0.0.0.0", debug=False, port=port)
