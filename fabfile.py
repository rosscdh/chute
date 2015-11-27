from __future__ import with_statement
from fabric.api import *
from fabric.contrib import files
#from fab_deploy import crontab

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
# default to local override in env
env.remote_project_path = env.local_project_path

try:
    env.repo = Repo(env.local_project_path)
except:
    env.repo = None


env.project = 'chute-server'
env.celery_app_name = 'current'

env.disable_known_hosts = True
env.fixtures = None

env.application_user = env.user = os.environ.get('USER', 'ubuntu')

env.SHA1_FILENAME = None
env.timestamp = time.time()
env.is_predeploy = False
env.local_user = getpass.getuser()

env.environment = 'local'
env.environment_class = 'development'
env.key_filename = '~/.ssh/kumukan.pem'

env.virtualenv_path = '~/.virtualenvs/beer/'
env.current_branch = local("git rev-parse --abbrev-ref HEAD", capture=True)

env.newrelic_api_token = None

TRUTHY = ['true', 't', 'y', 'yes', '1', 1]
FALSY = ['false', 'f', 'n', 'no', '0', 0]


env.roledefs.update({
    'cron-actor': [],
    'db-actor': [],
    'db': [],
})


@task
def staging():
    from config.environments import staging as config
    env.application_user = env.user = 'ubuntu'

    env.hosts = config.HOSTS if not env.hosts else env.hosts

    env.environment = 'staging'
    env.environment_class = 'staging'
    env.newrelic_app_name = 'Karma-App Staging'

    env.remote_project_path = '/home/ubuntu/apps/beer/'
    env.deploy_archive_path = '/home/ubuntu/apps/'
    env.virtualenv_path = '/home/ubuntu/.virtualenvs/beer/'
    env.remote_dashboard_path = None

    env.start_service = 'supervisorctl start beer'
    env.stop_service = 'supervisorctl stop beer'
    env.start_worker = None
    env.stop_worker = None

    env.roledefs.update({
        'cron-actor': config.CRON_ACTOR,
        'db-actor': config.DB_ACTOR,
        'db': config.DB_HOST,
    })


@task
def mkvirtualenv():
    if not files.exists(env.virtualenv_path):
        run('mkvirtualenv %s' % env.project)
    run('workon %s' % env.project)

@task
def put_confs():
    #sudo('rm /etc/nginx/sites-enabled/default')
    # nginx
    put(local_path='./config/environments/{environment}/beer-nginx'.format(environment=env.environment_class), remote_path='/etc/nginx/sites-enabled/', use_glob=False, use_sudo=True)
    # supervisord
    put(local_path='./config/environments/{environment}/beer.conf'.format(environment=env.environment_class), remote_path='/etc/supervisor/conf.d/', use_glob=False, use_sudo=True)
    # uwsgi
    put(local_path='./config/environments/{environment}/beer.ini'.format(environment=env.environment_class), remote_path='/etc/uwsgi/apps-enabled/', use_glob=False, use_sudo=True)


@task
def r(cmd):
    run(cmd)


@task
def manage(cmd):
    with cd(env.remote_project_path):
        virtualenv(cmd='python %s%s/manage.py %s' % (env.remote_project_path, 'current', cmd))


def proceed(msg='Proceed? (y,n)', color='yellow', terminate=True):
    return prompt(colored(msg, color))


@task
def virtualenv(cmd, **kwargs):
    sudo("source %sbin/activate; %s" % (env.virtualenv_path, cmd,), user=env.application_user, **kwargs)

@task
def pip_install():
    virtualenv(cmd='pip install virtualenv virtualenvwrapper')


@task
def clean_all():
    with cd(env.remote_project_path):
        virtualenv(cmd='python %s%s/manage.py clean_pyc' % (env.remote_project_path, 'current'))
        virtualenv(cmd='python %s%s/manage.py cleanup' % (env.remote_project_path, 'current'))
        #virtualenv(cmd='python %s%s/manage.py clean_nonces' % (env.remote_project_path, 'current'))
        #virtualenv(cmd='python %s%s/manage.py clean_associations' % (env.remote_project_path, 'current'))
        #virtualenv(cmd='python %s%s/manage.py clear_cache' % (env.remote_project_path, 'current'))
        virtualenv(cmd='python %s%s/manage.py compile_pyc' % (env.remote_project_path, 'current'))

@task
def clear_cache():
    with cd(env.remote_project_path):
        virtualenv(cmd='python %s%s/manage.py clear_cache' % (env.remote_project_path, 'current'))

@task
def clean_pyc():
    with cd(env.remote_project_path):
        virtualenv('python %s%s/manage.py clean_pyc' % (env.remote_project_path, 'current'))

@task
def precompile_pyc():
    virtualenv(cmd='python %s%s/manage.py compile_pyc' % (env.remote_project_path, 'current'))

@task
def manage(cmd='validate'):
    virtualenv('python %s%s/manage.py %s' % (env.remote_project_path, 'current', cmd))

@task
def get_sha1(path=None):
  cd(env.local_project_path) if path is None else cd(path)
  return local('git rev-parse --short --verify HEAD', capture=True)

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
    if proceed in TRUTHY:
        suggested = git_suggest_tag()
        tag = prompt(colored('Please enter a tag: previous: %s suggested: %s' % (suggested['previous'], suggested['next']), 'yellow'), default=suggested['next'])
        if tag:
            tag = 'v%s' % tag if tag[0] != 'v' else tag # ensure we start with a "v"

            #message = env.deploy_desc if 'deploy_desc' in env else prompt(colored('Please enter a tag comment', 'green'))
            env.repo.create_tag(tag)
#            local('git tag -a %s -m "%s"' % (tag, comment))
#            local('git push origin %s' % tag)

@task
def git_export(branch=None):
    branch = env.current_branch if branch is None else branch

    env.SHA1_FILENAME = get_sha1()
    if not os.path.exists('/tmp/%s.zip' % env.SHA1_FILENAME):
        local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ %s' % (env.SHA1_FILENAME, env.SHA1_FILENAME, branch,), capture=False)

@task
@runs_once
def current_version_sha():
    current = '%s%s' % (env.remote_project_path, 'current')
    realpath = run('ls -al %s' % current)
    current_sha = realpath.split('/')[-1]
    return current_sha

@task
@runs_once
def diff_outgoing_with_current():
    diff = local('git diff %s %s' % (get_sha1(), current_version_sha(),), capture=True)
    print(diff)

@task
@runs_once
def celery_restart(name='worker.1'):
    with settings(warn_only=True): # only warning as we will often have errors importing
        celery_stop()
        clean_pyc()
        celery_start()

@task
def celery_start(name='worker.1', loglevel='INFO', concurrency=5):
    with settings(warn_only=True): # only warning as we will often have errors importing
        sudo(env.start_worker)

@task
def celery_stop(name='worker.1'):
    with settings(warn_only=True): # only warning as we will often have errors importing
        sudo(env.stop_worker)

@task
def prepare_deploy():
    git_export()


@task
@runs_once
@roles('db-actor')
def syncdb():
    with settings():
        virtualenv('python %s%s/manage.py syncdb' % (env.remote_project_path, 'current'))

@task
@runs_once
@roles('db-actor')
def migrate():
    with settings():
        #virtualenv('python %s%s/manage.py migrate core 0014 --fake --delete-ghost-migrations' % (env.remote_project_path, 'current'))
        virtualenv('python %s%s/manage.py migrate' % (env.remote_project_path, 'current'))

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
    if delete in TRUTHY:
        cmd = cmd + ' | xargs rm -Rf'

    virtualenv(cmd)

# ------ RESTARTERS ------#
@task
def stop_nginx():
    with settings(warn_only=True):
        sudo('service nginx stop')

@task
def start_nginx():
    with settings(warn_only=True):
        sudo('service nginx start')

@task
def restart_nginx(event='restart'):
    with settings(warn_only=True):
        sudo('service nginx %s' % event)


@task
def restart_service(heavy_handed=False):
    with settings(warn_only=True):
        if env.environment_class not in ['celery']: # dont restart celery nginx services
            stop_service()
            start_service()

# ------ END-RESTARTERS ------#

@task
def env_run(cmd):
    return sudo(cmd) if env.environment_class in ['production', 'staging', 'celery'] else run(cmd)

@task
def deploy_archive_file():
    filename = env.get('SHA1_FILENAME', None)
    if filename is None:
        filename = env.SHA1_FILENAME = get_sha1()
    file_name = '%s.zip' % filename
    if not files.exists('%s/%s' % (env.deploy_archive_path, file_name)):
        as_sudo = env.environment_class in ['production', 'celery']
        put('/tmp/%s' % file_name, env.deploy_archive_path, use_sudo=as_sudo)
        sudo('chown %s:%s %s' % (env.application_user, env.application_user, env.deploy_archive_path) )


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
    project_path = '%s%s' % (env.remote_project_path, 'current',)

    if not env.is_predeploy:
        if files.exists('%s/%s' % (version_path, env.SHA1_FILENAME)): # check the sha1 dir exists
            #if files.exists(project_path, use_sudo=True): # unlink the glynt dir
            if files.exists('%s/%s' % (env.remote_project_path, 'current')): # check the current glynt dir exists
                virtualenv('unlink %s' % project_path)
            virtualenv('ln -s %s/%s %s' % (version_path, env.SHA1_FILENAME, project_path,)) # relink
@task
def reread_supervisor():
    sudo('supervisorctl reread')

@task
def clean_start():
    stop_service()
    reread_supervisor()
    start_service()
    clean_zip()

@task
def do_deploy():
    if env.SHA1_FILENAME is None:
        env.SHA1_FILENAME = get_sha1()

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)
    project_path = '%s%s' % (env.remote_project_path, 'current',)

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
    project_path = '%s%s' % (env.remote_project_path, 'current',)

    if not env.is_predeploy:
        # copy the live local_settings
        with cd(project_path):
            put(local_path='./config/environments/%s/%s/local_settings.py' % (env.environment_class, env.project), remote_path='%s%s/%s/local_settings.py' % (env.remote_project_path, 'current', env.project))  # this is the one to be read
            # set_code_version()

@task
def set_code_version():
    if env.SHA1_FILENAME is None:
        env.SHA1_FILENAME = get_sha1()

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)

    cmd = 'echo "CODE_VERSION=\'%s\'" > beer/settings/code_version.py' % env.SHA1_FILENAME

    with cd(full_version_path):
        if env.environment in ['local']:
            local(cmd)
        else:
            virtualenv(cmd)


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
    local('rm -Rf ./static')
    # collect static components
    local('python ./manage.py collectstatic --noinput')
    local('tar cvzf static.tar.gz ./static')
    put('static.tar.gz', env.remote_project_path)
    run('tar -zxvf %sstatic.tar.gz -C %s' % (env.remote_project_path, env.remote_project_path))
    run('rm %sstatic.tar.gz' % env.remote_project_path)
    local('rm static.tar.gz')


@task
def requirements():
    sha = env.get('SHA1_FILENAME', None)
    if sha is None:
        env.SHA1_FILENAME = get_sha1()

    project_path = '%sversions/%s' % (env.remote_project_path, env.SHA1_FILENAME,)
    requirements_path = '%s/requirements.txt' % (project_path, )

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
            'deployment[app_name]': env.newrelic_app_name, # new relc wants either app_name or application_id not both
            #'deployment[application_id]': env.newrelic_application_id,
            'deployment[description]': description,
            'deployment[user]': env.local_user,
            'deployment[revision]': get_sha1()
        }

        colored('Sending Deployment Message to NewRelic', 'blue')

        r = requests.post('https://rpm.newrelic.com/deployments.xml', data=payload, headers=headers, verify=False)

        is_ok = r.status_code in [200,201]
        text = 'DeploymentNote Recorded OK' if is_ok is True else 'DeploymentNote Recorded Not OK: %s' % r.text
        color = 'green' if is_ok else 'red'

        print(colored('%s (%s)' % (text, r.status_code), color))


@task
@runs_once
@roles('cron-actor')
def crontabs():
    if env.environment_class in ['production']:
        update_open_zendesk_tickets = '0 * * * 1,2,3,4,5  cd %s/%s && %sbin/python manage.py update_open_zendesk_tickets' % (env.remote_project_path, 'current', env.virtualenv_path)
        crontab.crontab_update(update_open_zendesk_tickets, 'update-open-zendesk-tickets')

        # Must always run 30 mins after the update_open_zendesk_tickets
        # as it will read from the latest tickets results list generated by: update_open_zendesk_tickets
        zendesk_ticket_report = '30 8 * * 1,2,3,4,5  cd %s/%s && %sbin/python manage.py zendesk_ticket_report' % (env.remote_project_path, 'current', env.virtualenv_path)
        crontab.crontab_update(zendesk_ticket_report, 'zendesk-ticket-report')

@task
@serial
@runs_once
def diff():
    diff = prompt(colored("View diff? [y,n]", 'magenta'), default="y")
    if diff.lower() in TRUTHY:
        print(diff_outgoing_with_current())

@task
@serial
@runs_once
def run_tests():
    run_tests = prompt(colored("Run Tests? [y,n]", 'yellow'), default="y")
    if run_tests.lower() in TRUTHY:

        result = local('python manage.py test')

        if result not in ['', 1, True]:
            error(colored('You may not proceed as the tests are not passing', 'orange'))



#----
@task
def repos():
    """
    Adds common repositories to the system, to help get the latest version of packages
    :return:
    """
    sudo('add-apt-repository -y multiverse')
    sudo('add-apt-repository -y restricted')
    sudo('add-apt-repository -y ppa:git-core/ppa')
    sudo('add-apt-repository -y ppa:mercurial-ppa/releases')
    sudo('add-apt-repository -y ppa:webupd8team/java')
    sudo('curl -sL https://deb.nodesource.com/setup_dev | sudo bash -')  # nodejs ppa for node latest
    sudo('aptitude update')

@task
def chores():
    inst = lambda pkglist: sudo('aptitude --assume-yes install %s' % pkglist)

    #sudo("aptitude update")

    inst('libffi-dev ntp nmap htop vim unzip gettext')  # system level utilities. need ntp to keep clocks in sync, eh
    inst('git mercurial subversion ')  # version control
    inst('build-essential apache2-utils libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev')
    inst('libtidy-dev postgresql-server-dev-all postgresql-client libpq-dev libxml2-dev libxslt1-dev')

    inst('python-setuptools python-dev uwsgi-plugin-python python-psycopg2')

    #inst('default-jre default-jre-headless default-jdk')  # java stuff

    inst('nginx uwsgi supervisor')  # web servers and related admin

    #inst('libgeos-dev')  # geodata

    sudo('easy_install pip')
    sudo('pip install virtualenv virtualenvwrapper')
    sudo('pip install uwsgi')
    sudo('pip install pyopenssl ndg-httpsclient pyasn1 requests[security]')
    sudo('pip install newrelic')


@task
def add_user():
    sudo('adduser --disabled-password --gecos "" ubuntu')


@task
def paths():
    # run('echo "WORKON_HOME=$HOME/.virtualenvs" >> $HOME/.bash_profile')
    # run('echo "source /usr/local/bin/virtualenvwrapper.sh" >> $HOME/.bash_profile')
    # run('echo "source $HOME/.bash_profile" >> $HOME/.bashrc')
    run('mkdir -p ~/.virtualenvs')
    run('mkdir -p ~/apps/beer/versions/tmp')
    run('ln -s ~/apps/beer/versions/tmp ~/apps/beer/current')
    # pass

@task
def upload_db():
    put('db.sqlite3', '/home/ubuntu/apps/beer/')
#-------

@task
def deploy(is_predeploy='False',full='False',db='False',search='False'):
    """
    :is_predeploy=True - will deploy the latest MASTER SHA but not link it in: this allows for assets collection
    and requirements update etc...
    """
    env.is_predeploy = is_predeploy.lower() in TRUTHY
    full = full.lower() in TRUTHY
    db = db.lower() in TRUTHY
    search = search.lower() in TRUTHY

    prepare_deploy()

    do_deploy()
    #paths()
    put_confs()

    requirements()

    relink()
    update_env_conf()
    assets()
    clean_start()
    #crontabs()
