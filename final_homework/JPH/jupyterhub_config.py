import os

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000

c.Authenticator.allowed_users = {'admin'}
c.Authenticator.admin_users = {'admin'}
c.JupyterHub.db_url = os.path.join(os.environ.get('JUPYTERHUB_DATA_DIR', '/srv/jupyterhub'), 'jupyterhub.sqlite')
c.JupyterHub.cookie_secret_file = os.path.join(os.environ.get('JUPYTERHUB_DATA_DIR', '/srv/jupyterhub'), 'cookie_secret')
c.JupyterHub.crypt_key = os.environ.get('JUPYTERHUB_CRYPT_KEY', '')
c.JupyterHub.spawner_class = 'simple'

c.Spawner.default_url = '/lab'
c.Spawner.http_timeout = 60