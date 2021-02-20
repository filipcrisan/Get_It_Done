from flask import Blueprint, render_template
from flask_login import login_required, current_user
from repository.models import User


profile_bp = Blueprint('profile', __name__)


def get_tasks_done(user):
    count = 0
    for task in user.tasks:
        if task.state == 'Done':
            count = count + 1
    return count


@profile_bp.route('/profile')
@login_required
def profile():
    registered_users = User.query.all()
    registered_users.sort(key=get_tasks_done, reverse=True)
    rank = 1
    last = get_tasks_done(registered_users[0])
    for i in range(len(registered_users)):
        curr = get_tasks_done(registered_users[i])
        if curr != last:
            rank = rank + 1
        last = curr
        if registered_users[i].id == current_user.id:
            break

    return render_template('profile.html', rank=rank, tasks_done=get_tasks_done(current_user))
