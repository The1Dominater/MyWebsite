# Setup scripts
These are basic setup scripts for installing and initializing the WSGI server, Nginx,
and the Uncompilcated Firewall. This is based on the idea you are directly installing
these applications rather than using docker or k8s.

### setup_gunicorn_service
Creates a service to run gunicorn using systemctl management so the WSGI launches on
device startup and restarts on its own if it crashes. It configures a basic socket
to connect to the Flask web app.
Note: It does not install gunicorn because I am using the `py_reqs.txt` to install
all the python packages at once.

### setup_nginx
Installs nginx and creates a basic config file which defines a simple proxy server
to send http requests to gunicorn. It then creates a link in `/etc/nginx/sites-enabled`
to enable the config file. Finally it restarts nginx so it is loaded up with the new
configs.

### setup_ufw
Installs ufw and adds basic firewall rules which only allows incoming and outgoing traffic
for http and ssh connections.