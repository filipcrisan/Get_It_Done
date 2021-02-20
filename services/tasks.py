from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from repository.models import Task
from start import db


tasks_bp = Blueprint('tasks', __name__)


# LIST TASKS ===============================================================

@tasks_bp.route('/tasks')
@login_required
def tasks():
    my_tasks = Task.query.filter_by(assigned_to_id=current_user.id)
    my_projects = current_user.assigned_projects
    return render_template('tasks.html', my_tasks=my_tasks, my_projects=my_projects)


# UPDATE TASK STATE =======================================================

# update_task_get
@tasks_bp.route('/<int:id>/update_task')
@login_required
def update_task():
    my_tasks = Task.query.filter_by(assigned_to_id=current_user.id)
    my_projects = current_user.assigned_projects
    return render_template('tasks.html', my_tasks=my_tasks, my_projects=my_projects)


# update_task_post
@tasks_bp.route('/<int:id>/update_task', methods=['POST'])
@login_required
def update_task_post(id):
    my_task = Task.query.filter_by(id=id).first()

    state = request.form.get('state')

    my_task.state = state
    db.session.commit()

    my_tasks = Task.query.filter_by(assigned_to_id=current_user.id)
    my_projects = current_user.assigned_projects
    return render_template('tasks.html', my_tasks=my_tasks, my_projects=my_projects)
