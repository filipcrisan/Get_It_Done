from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from repository.models import Project, User, Task

main =  Blueprint('main', __name__)


# INDEX ====================================================================

@main.route('/')
@login_required
def index():
	return render_template('index.html')


# LIST PROJECTS ============================================================

@main.route('/projects')
@login_required
def projects():
	data = []
	for proj in current_user.assigned_projects:
		data.append(proj)
	
	return render_template('projects.html', data=data)


# CREATE A NEW PROJECT ====================================================

# new_project_get
@main.route('/new_project')
@login_required
def new_project():
	registered_users = User.query.all()
	return render_template('new_project.html', reg_us=registered_users)

# new_project_post
@main.route('/new_project', methods=['POST'])
@login_required
def new_project_post():
	name = request.form.get('name')
	description = request.form.get('description')
	contributors = request.form.getlist('users')

	if not name:
		flash('Project must have a title')
		return redirect(url_for('main.new_project'))
	
	existing_project = Project.query.filter_by(name=name).first()

	if existing_project:
		flash('Project title already exists')
		return redirect(url_for('main.new_project'))

	if not contributors:
		flash('Project must have contributors')
		return redirect(url_for('main.new_project'))

	new_proj = Project(name=name, description=description)

	db.session.add(new_proj)
	db.session.commit()

	for user in User.query.all():
		if user.email in contributors:
			user.assigned_projects.append(new_proj)
			db.session.commit()

	data = []
	for p in Project.query.all():
		if p in current_user.assigned_projects:
			data.append(p)

	return render_template('projects.html', data=data)


# PROJECT PAGE AND CREATE TASKS ==========================================

def get_proj(id):
	proj = Project.query.filter_by(id=id).first()

	if not proj:
		flash('Project does not exist')
		return redirect(url_for('main.projects'))
	return proj

# curr_proj_get
@main.route('/<int:id>/curr_proj')
@login_required
def curr_proj(id):
	proj = get_proj(id)
	all_users = User.query.all()
	return render_template('curr_proj.html', project=proj, reg_us=all_users)

# curr_proj_post
@main.route('/<int:id>/curr_proj', methods=['POST'])
@login_required
def curr_proj_post(id):
	proj = get_proj(id)

	description = request.form.get('task_description')
	state = 'Assigned'
	priority = request.form.get('priority')
	assigned_to = request.form.get('assigned_to')
	in_project_id = id

	if not description or not priority or not assigned_to:
		flash('Task form failed. Please fill in everything')
		return redirect(url_for('main.curr_proj', id=id))

	assigned_to_id = User.query.filter_by(email=assigned_to).first().id 

	task = Task(
		description=description, 
		state=state, 
		priority=priority, 
		in_project_id=in_project_id, 
		assigned_to_id=assigned_to_id
	)

	db.session.add(task)
	db.session.commit()

	user = User.query.filter_by(email=assigned_to).first()

	user.tasks.append(task)
	db.session.commit()

	proj.tasks.append(task)
	db.session.commit()

	all_users = User.query.all()
	return render_template('curr_proj.html', project=proj, reg_us=all_users)


# UPDATE PROJECT ===========================================================

# update_project_get
@main.route('/<int:id>/update_project')
@login_required
def update_project(id):
	proj = get_proj(id)
	all_users = User.query.all()
	return render_template('curr_proj.html', project=proj, reg_us=all_users)

# update_project_post
@main.route('/<int:id>/update_project', methods=['POST'])
@login_required
def update_project_post(id):
	proj = get_proj(id)

	name = request.form.get('name')
	description = request.form.get('description')
	contributors = request.form.getlist('users')

	if not name:
		flash('Project must have a title')
		return redirect(url_for('main.curr_proj', id=id))
	
	existing_project = Project.query.filter_by(name=name).first()

	if existing_project and proj.name != name:
		flash('Project title already exists')
		return redirect(url_for('main.curr_proj', id=id))

	proj.name = name
	proj.description = description
	db.session.commit()

	for user in User.query.all():
		if user.email in contributors:
			user.assigned_projects.append(proj)
			db.session.commit()

	all_users = User.query.all()
	return render_template('curr_proj.html', project=proj, reg_us=all_users)


# LIST TASKS ===============================================================
	
@main.route('/tasks')
@login_required
def tasks():
	my_tasks = Task.query.filter_by(assigned_to_id=current_user.id)
	my_projects = current_user.assigned_projects
	return render_template('tasks.html', my_tasks=my_tasks, my_projects=my_projects)


# UPDATE TASK STATE =======================================================

# update_task_get
@main.route('/<int:id>/update_task')
@login_required
def update_task():
	my_tasks = Task.query.filter_by(assigned_to_id=current_user.id)
	my_projects = current_user.assigned_projects
	return render_template('tasks.html', my_tasks=my_tasks, my_projects=my_projects)

# update_task_post
@main.route('/<int:id>/update_task', methods=['POST'])
@login_required
def update_task_post(id):
	my_task = Task.query.filter_by(id=id).first()

	state = request.form.get('state')

	my_task.state = state
	db.session.commit()

	my_tasks = Task.query.filter_by(assigned_to_id=current_user.id)
	my_projects = current_user.assigned_projects
	return render_template('tasks.html', my_tasks=my_tasks, my_projects=my_projects)


# PROFILE ===============================================================

def get_tasks_done(user):
	count = 0
	for task in user.tasks:
		if task.state == 'Done':
			count = count + 1
	return count

@main.route('/profile')
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