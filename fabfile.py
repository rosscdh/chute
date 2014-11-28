from __future__ import with_statement
from fabric.api import *
from fabric.utils import error
from fabric.context_managers import settings
from fabric.contrib import files

from git import *

import os
import sys
import time
import shutil
import getpass
import requests
from termcolor import colored

debug = True

env.local_project_path = os.path.dirname(os.path.realpath(__file__))
env.gui_dist_path = '%s/gui/dist' % env.local_project_path
env.uwsgi_app_path = os.path.dirname(os.path.realpath(__file__)) + '/../conf/uwsgi-app/files'
env.environment_settings_path = os.path.dirname(os.path.realpath(__file__)) + '/../conf'
# default to local override in env
env.remote_project_path = env.local_project_path

try:
    env.repo = Repo(env.local_project_path)
except:
    env.repo = None


env.environment_class = 'local'
env.project = 'chute'
env.celery_app_name = env.project

env.dev_fixtures = ''
env.fixtures = None

env.SHA1_FILENAME = None
env.timestamp = time.time()
env.is_predeploy = False
env.local_user = getpass.getuser()
env.environment = 'local'
env.virtualenv_path = '~/.virtualenvs/%s/' % env.project

env.truthy = ['true', 't', 'y', 'yes', '1', 1]
env.falsy = ['false', 'f', 'n', 'no', '0', 0]



@task
def production():
    env.environment = 'production'
    env.environment_class = 'production'

    env.remote_project_path = '/home/django/magnificent_app/'
    env.deploy_archive_path = '/tmp/'
    env.virtualenv_path = '/home/django/.virtualenvs/magnificent_app/'

    env.newrelic_api_token = ''
    env.newrelic_app_name = None
    env.newrelic_application_id = None

    # change from the default user to 'vagrant'
    env.user = 'root'
    env.application_user = 'django'
    # connect to the port-forwarded ssh
    env.hosts = ['107.170.195.73'] if not env.hosts else env.hosts

    #env.key_filename = '%s/../conf/chef-machines.pem' % env.local_project_path

    env.start_service = 'supervisorctl start chute'
    env.stop_service = 'supervisorctl stop chute'
    env.light_restart = "kill -HUP `cat /tmp/chute.pid`"

#
# Update the roles
#
env.roledefs.update({
    'web': ['107.170.195.73',
            '107.170.195.73',],
    'worker': ['107.170.195.73'],
    'db-actor': ['107.170.195.73'],
})


@task
def chores():
    sudo('aptitude --assume-yes install build-essential python-setuptools python-dev apache2-utils uwsgi-plugin-python libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev easy_install nmap htop vim unzip')
    sudo('aptitude --assume-yes install git-core mercurial subversion')
    sudo('aptitude --assume-yes install libtidy-dev postgresql-client libpq-dev python-psycopg2')

    # GEO
    sudo('aptitude --assume-yes install libgeos-dev')

    #sudo('easy_install pip')
    sudo('pip install virtualenv pillow')

    #put('conf/.bash_profile', '~/.bash_profile')

@task
def virtualenv(cmd, **kwargs):
  # change to base dir
  #with cd(env.remote_project_path):
    if env.environment_class is 'webfaction':
        # webfaction
        run("source %sbin/activate; %s" % (env.virtualenv_path, cmd,), **kwargs)
    else:
        sudo("source %sbin/activate; %s" % (env.virtualenv_path, cmd,), user=env.application_user, **kwargs)


@task
def clean_all():
    with cd(env.remote_project_path):
        virtualenv(cmd='python %s%s/manage.py clean_pyc' % (env.remote_project_path, env.project))
        virtualenv(cmd='python %s%s/manage.py cleanup' % (env.remote_project_path, env.project))
        virtualenv(cmd='python %s%s/manage.py clean_nonces' % (env.remote_project_path, env.project))
        virtualenv(cmd='python %s%s/manage.py clean_associations' % (env.remote_project_path, env.project))
        #virtualenv(cmd='python %s%s/manage.py clear_cache' % (env.remote_project_path, env.project))
        virtualenv(cmd='python %s%s/manage.py compile_pyc' % (env.remote_project_path, env.project))


@task
def clean_pyc():
    with cd(env.remote_project_path):
        virtualenv('python %s%s/manage.py clean_pyc' % (env.remote_project_path, env.project))

@task
def precompile_pyc():
    virtualenv(cmd='python %s%s/manage.py compile_pyc' % (env.remote_project_path, env.project))


def get_sha1():
  cd(env.local_project_path)
  return local('git rev-parse --short --verify HEAD', capture=True)

@task
def db_backup(db='chute_production', user='chute', data_only=False):
    """
    -Fp plain text sql
    -Fc compressed .bak file
    Remember to:
    export PGPASSWORD="$put_here_the_password"
    """
    data_only = True if data_only in env.truthy else False

    host = env.hosts[0]

    db_backup_name = '%s.bak' % db
    if data_only:
        local('pg_dump --no-owner --no-privileges --no-acl --data-only -h %s -Fc -U %s -d %s > /tmp/%s' % (host, user, db, db_backup_name,))
    else:
        local('pg_dump --no-owner --no-privileges --no-acl -h %s -Fc -U %s -d %s > /tmp/%s' % (host, user, db, db_backup_name,))

@task
def db_restore(db='chute_production', db_file=None):
    with settings(warn_only=True): # only warning as we will often have errors importing
        if db_file is None:
            db_file = '/tmp/%s.bak' % db
            if not os.path.exists(db_file):
                print(colored('Database Backup %s does not exist...' % db_file, 'red'))
            else:
                go = prompt(colored('Restore "%s" DB from a file entitled: "%s" in the "%s" environment: Proceed? (y,n)' % (db, db_file, env.environment,), 'yellow'))
                if go in env.truthy:
                    #local('echo "DROP DATABASE %s;" | psql -h localhost -U %s' % (db, env.local_user,))
                    #local('echo "CREATE DATABASE %s WITH OWNER %s ENCODING \'UTF8\';" | psql -h localhost -U %s' % (db, env.local_user, env.local_user,))
                    local('pg_restore --disable-triggers --no-owner --clean -U %s -h localhost -d %s -Fc %s' % (env.local_user, db, db_file,))

@task
def git_tags():
    """ returns list of tags """
    tags = env.repo.tags
    return tags

@task
def git_previous_tag():
    # last tag in list
    previous = git_tags()[-1]
    return previous

@task
def git_suggest_tag():
    """ split into parts v1.0.0 drops v converts to ints and increaments and reassembles v1.0.1"""
    previous = git_previous_tag().name.split('.')
    mapped = map(int, previous[1:]) # convert all digits to int but exclude the first one as it starts with v and cant be an int
    next = [int(previous[0].replace('v',''))] + mapped #remove string v and append mapped list
    next_rev = next[2] = mapped[-1] + 1 # increment the last digit
    return {
        'next': 'v%s' % '.'.join(map(str,next)), 
        'previous': '.'.join(previous)
    }

@task
@runs_once
def git_set_tag():
    proceed = prompt(colored('Do you want to tag this realease?', 'red'), default='y')
    if proceed in env.truthy:
        suggested = git_suggest_tag()
        tag = prompt(colored('Please enter a tag: previous: %s suggested: %s' % (suggested['previous'], suggested['next']), 'yellow'), default=suggested['next'])
        if tag:
            tag = 'v%s' % tag if tag[0] != 'v' else tag # ensure we start with a "v"

            #message = env.deploy_desc if 'deploy_desc' in env else prompt(colored('Please enter a tag comment', 'green'))
            env.repo.create_tag(tag)
#            local('git tag -a %s -m "%s"' % (tag, comment))
#            local('git push origin %s' % tag)

@task
def git_export(branch='master'):
  env.SHA1_FILENAME = get_sha1()
  if not os.path.exists('/tmp/%s.zip' % env.SHA1_FILENAME):
      local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ %s' % (env.SHA1_FILENAME, env.SHA1_FILENAME, branch,), capture=False)

@task
@runs_once
def current_version_sha():
    current = '%s%s' % (env.remote_project_path, env.project)
    realpath = run('ls -al %s' % current)
    current_sha = realpath.split('/')[-1]
    return current_sha

@task
@runs_once
def diff_outgoing_with_current():
    diff = local('git diff %s %s' % (get_sha1(), current_version_sha(),), capture=True)
    print(diff)

@task
def prepare_deploy():
    git_export()

@task
@runs_once
@roles('db-actor')
def migrate():
    with settings():
        virtualenv('python %s%s/manage.py migrate' % (env.remote_project_path, env.project))

@task
@runs_once
@roles('db-actor')
def syncdb():
    with settings():
        virtualenv('python %s%s/manage.py syncdb --migrate' % (env.remote_project_path, env.project))

@task
def clean_versions(delete=False, except_latest=3):
    current_version = get_sha1()

    versions_path = '%sversions' % env.remote_project_path
    #
    # cd into the path so we can use xargs
    # tail the list except the lastest N
    # exclude the known current version
    #
    cmd = "cd {path};ls -t1 {path} | tail -n+{except_latest} | grep -v '{current_version}'".format(path=versions_path, except_latest=except_latest, current_version=current_version)
    #
    # optionally delete them
    #
    if delete in env.truthy:
        cmd = cmd + ' | xargs rm -Rf'

    virtualenv(cmd)

# ------ RESTARTERS ------#
@task
def supervisord_restart():
    with settings(warn_only=True):
        if env.environment_class is 'webfaction':
            restart_service()
        else:
            sudo('supervisorctl restart uwsgi')

@task
@roles('web')
def restart_lite():
    with settings(warn_only=True):
        sudo(env.light_restart)

@task
@roles('web')
def stop_nginx():
    with settings(warn_only=True):
        sudo('service nginx stop')

@task
@roles('web')
def start_nginx():
    with settings(warn_only=True):
        sudo('service nginx start')

@task
@roles('web')
def restart_nginx():
    with settings(warn_only=True):
        sudo('service nginx restart')

@task
@roles('web')
def restart_service(heavy_handed=False):
    with settings(warn_only=True):
        if env.environment_class not in ['celery']: # dont restart celery nginx services
            if env.environment_class == 'webfaction':
                stop_service()
                start_service()
            else:
                if not heavy_handed:
                    restart_lite()
                else:
                    supervisord_restart()

# ------ END-RESTARTERS ------#


def env_run(cmd):
    return sudo(cmd) if env.environment_class in ['production', 'celery'] else run(cmd)

@task
def deploy_archive_file():
    filename = env.get('SHA1_FILENAME', None)
    if filename is None:
        filename = env.SHA1_FILENAME = get_sha1()
    file_name = '%s.zip' % filename
    if not files.exists('%s/%s' % (env.deploy_archive_path, file_name)):
        as_sudo = env.environment_class in ['production', 'celery']
        put('/tmp/%s' % file_name, env.deploy_archive_path, use_sudo=as_sudo)
        env_run('chown %s:%s %s' % (env.application_user, env.application_user, env.deploy_archive_path) )


def clean_zip():
    file_name = '%s.zip' % env.SHA1_FILENAME
    if files.exists('%s%s' % (env.deploy_archive_path, file_name)):
        env_run('rm %s%s' % (env.deploy_archive_path, file_name,))

@task
def relink():
    if not env.SHA1_FILENAME:
        env.SHA1_FILENAME = get_sha1()

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)
    project_path = '%s%s' % (env.remote_project_path, env.project,)

    if not env.is_predeploy:
        if files.exists('%s/%s' % (version_path, env.SHA1_FILENAME)): # check the sha1 dir exists
            #if files.exists(project_path, use_sudo=True): # unlink the glynt dir
            if files.exists('%s/%s' % (env.remote_project_path, env.project)): # check the current dir exists
                virtualenv('unlink %s' % project_path)
            virtualenv('ln -s %s/%s %s' % (version_path, env.SHA1_FILENAME, project_path,)) # relink

@task
def clean_start():
    stop_service()
    #clear_cache()
    clean_pyc()
    precompile_pyc()
    start_service()
    clean_zip()

@task
def do_deploy():
    if env.SHA1_FILENAME is None:
        env.SHA1_FILENAME = get_sha1()

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)
    project_path = '%s%s' % (env.remote_project_path, env.project,)

    if env.environment_class in ['production', 'celery']:
        if not files.exists(version_path):
            env_run('mkdir -p %s' % version_path )
        sudo('chown -R %s:%s %s' % (env.application_user, env.application_user, env.remote_project_path) )

    deploy_archive_file()

    # extract project zip file:into a staging area and link it in
    if not files.exists('%s/manage.py'%full_version_path):
        unzip_archive()


@task
def update_env_conf():
    if env.SHA1_FILENAME is None:
        env.SHA1_FILENAME = get_sha1()

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)
    project_path = '%s%s' % (env.remote_project_path, env.project,)

    if not env.is_predeploy:
        # copy the live local_settings
        with cd(project_path):
            # if files.exists('%s/conf/%s.wsgi.py' % (full_version_path, env.environment,)):
            #     virtualenv('cp %s/conf/%s.wsgi.py %s/%s/wsgi.py' % (full_version_path, env.environment, full_version_path, env.project))
            if env.newrelic_app_name is not None:
                virtualenv('cp %s/conf/%s.newrelic.ini %s/%s/newrelic.ini' % (full_version_path, env.environment, full_version_path, env.project))
        deploy_settings()

@task
def deploy_settings():
    if env.SHA1_FILENAME is None:
        env.SHA1_FILENAME = get_sha1()

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)
    project_path = '%s%s' % (env.remote_project_path, env.project,)

    # note the removal of the envirnment name part
    put(local_path='%s/%s.local_settings.py' % (env.environment_settings_path, env.environment), remote_path='%s/%s.local_settings.py' % (env.deploy_archive_path, env.environment,))
    sudo('cp %s/%s.local_settings.py %s/%s/local_settings.py' % (env.deploy_archive_path, env.environment, full_version_path, env.project))
    run('chown -R %s:%s %s/%s/local_settings.py' % (env.application_user, env.application_user, full_version_path, env.project) )

@task
def unzip_archive():
    version_path = '%sversions' % env.remote_project_path
    with cd('%s' % version_path):
        virtualenv('unzip %s%s.zip -d %s' % (env.deploy_archive_path, env.SHA1_FILENAME, version_path,))

@task
def start_service():
    env_run(env.start_service)

@task
def stop_service():
    env_run(env.stop_service)

def fixtures():
    # if were in any non staging,prod env then load the dev fixtures too
    return env.fixtures + ' ' + env.dev_fixtures if env.environment not in ['production', 'staging'] else env.fixtures


@task
def assets():
    # collect static components
    virtualenv('python %s%s/manage.py collectstatic --noinput' % (env.remote_project_path, env.project,))

@task
def requirements():
    sha = env.get('SHA1_FILENAME', None)
    if sha is None:
        env.SHA1_FILENAME = get_sha1()
    
    project_path = '%sversions/%s' % (env.remote_project_path, env.SHA1_FILENAME,)
    requirements_path = '%s/requirements/%s.txt' % (project_path, env.environment, )

    virtualenv('pip install -r %s' % requirements_path )

@task
@serial
@runs_once
def newrelic_note():
    if not hasattr(env, 'deploy_desc'):
        env.deploy_desc = prompt(colored('Hi %s, Please provide a Deployment Note:' % env.local_user, 'yellow'))

@task
@serial
@runs_once
def newrelic_deploynote():
    if not env.deploy_desc:
        print(colored('No env.deploy_desc was defined cant post to new relic', 'yellow'))
    else:
        description = '[env:%s][%s@%s] %s' % (env.environment, env.user, env.host, env.deploy_desc)
        headers = {
            'x-api-key': env.newrelic_api_token
        }

        payload = {
            #'deployment[app_name]': env.newrelic_app_name, # new relc wants either app_name or application_id not both
            'deployment[application_id]': env.newrelic_application_id,
            'deployment[description]': description,
            'deployment[user]': env.local_user,
            'deployment[chute]': get_sha1()
        }
        
        colored('Sending Deployment Message to NewRelic', 'blue')

        r = requests.post('https://rpm.newrelic.com/deployments.xml', data=payload, headers=headers, verify=False)

        is_ok = r.status_code in [200,201]
        text = 'DeploymentNote Recorded OK' if is_ok is True else 'DeploymentNote Recorded Not OK: %s' % r.text
        color = 'green' if is_ok else 'red'

        print(colored('%s (%s)' % (text, r.status_code), color))


@task
@serial
@runs_once
def diff():
    diff = prompt(colored("View diff? [y,n]", 'magenta'), default="y")
    if diff.lower() in env.truthy:
        print(diff_outgoing_with_current())

@task
@serial
@runs_once
def run_tests():
    run_tests = prompt(colored("Run Tests? [y,n]", 'yellow'), default="y")
    if run_tests.lower() in env.truthy:

        result = local('python manage.py test')

        if result not in ['', 1, True]:
            error(colored('You may not proceed as the tests are not passing', 'orange'))

@task
@runs_once
def copy_production_settings():
    # # move local_settings.py if present
    if os.path.exists('chute/local_settings.py'):
        local('mv chute/local_settings.py /tmp/local_settings.py')

    # # copy conf/production.local_settings.py
    # # has the very important ("ng", os.path.join(SITE_ROOT, 'gui', 'dist')),
    # # settings
    production_local_settings = '%s/production.local_settings.py' % env.environment_settings_path

    if not os.path.exists(production_local_settings):
        raise Exception('Production local_settings could not be found, cannot continue: %s' % production_local_settings)

    local('cp %s chute/local_settings.py' % production_local_settings)


@task
def restore_backdup_localsettings():
    # move tmp/local_settings.py back
    if os.path.exists('/tmp/local_settings.py'):
        local('rm chute/local_settings.py')  # remove the production version local_settings so noone loses their mind
        local('mv /tmp/local_settings.py chute/local_settings.py')
    else:
        if env.environment_class == 'local':
            # copy the default dev localsettings
            local('cp conf/dev.local_settings.py chute/local_settings.py')


@task
def conclude():
    newrelic_deploynote()

@task
def rebuild_local(gui_clean=False):

    if not os.path.exists('chute/local_settings.py'):
        local('cp conf/dev.local_settings.py chute/local_settings.py')

    if os.path.exists('./dev.db'):
        new_db_name = '/tmp/dev.%s.db.bak' % env.timestamp
        local('cp ./dev.db %s' % new_db_name)

        print colored('Local Database Backedup %s...' % new_db_name, 'green')
        local('rm ./dev.db')

    local('python manage.py syncdb --noinput')
    local('python manage.py loaddata %s' % fixtures())
    local('python manage.py createsuperuser')  #manually as we rely on the dev-fixtures

@task
def deploy(is_predeploy='False',full='False',db='False',search='False'):
    """
    :is_predeploy=True - will deploy the latest MASTER SHA but not link it in: this allows for assets collection
    and requirements update etc...
    """
    env.is_predeploy = is_predeploy.lower() in env.truthy
    full = full.lower() in env.truthy
    db = db.lower() in env.truthy
    search = search.lower() in env.truthy

    #run_tests()
    #diff()
    #git_set_tag()
    #newrelic_note()

    prepare_deploy()
    do_deploy()
    update_env_conf()

    if full:
        requirements()

    relink()
    # upload the gui
    assets()
    clean_start()
    #conclude()
