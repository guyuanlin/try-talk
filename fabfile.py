from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env, prefix, sudo
from fabric.contrib.console import confirm

GIT_CLONE_URL = 'git@github.com:guyuanlin/try-talk.git'

def get_branch_name():
	return 'master'

def prepare_deploy():
	branch_name = get_branch_name()
	local('git checkout {0}'.format(branch_name))
	local('git merge develop')
	local('git push github {0}'.format(branch_name))

def deploy():
	prepare_deploy()

	workspace_dir = 'try-talk/src/'
	with settings(warn_only=True):
		if run('test -d {0}'.format(workspace_dir)).failed:
			run('git clone {0}'.format(workspace_dir))
	with cd(workspace_dir):
		branch_name = get_branch_name()
		run('git pull origin {0}'.format(branch_name))
		with prefix('source ../bin/activate'):
			with prefix('source ./deployment/production.sh'):
				run('pip install -r requirements.txt')
				run('python manage.py collectstatic --noinput')
				run('python manage.py migrate')
				sudo('supervisorctl restart all')

