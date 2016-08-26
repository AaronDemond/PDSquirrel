# PD Squirrel

https://pdsquirrel.ca is a Django project that runs on Red Hat Enterprise Linux. It is served using Nginx with data being stored in a MySQL database. The Django app interfaces with Nginx using uwsgi. PDSquirrel makes use of Javascript for client interaction and audio recording. JQuery and Bootstrap are used for developing the interface. Various Python packages and modules are used, as well as some Linux software. Namely LAME encoder for converting to MP3, and Celery task manager for support of parallel processing.

All important files are stored in /root/nginx. PDSquirrel is the Django production project, and _PDSquirrel_dev is the development build.

## Startup

To start the website from a server reboot, run the following commands.

```bash
 	
    ssh root@pdsquirrel.ca
	cd ~/nginx/PDSquirrel
	sudo service httpd stop
	sudo service nginx -c ~/nginx/nginx.conf
	screen -S pds
	../uwsgi/uwsgi --module pds.wsgi --socket :8000
		(detach from screen) #Not a command, hit (Ctrl-A then D) to detach from screen
	rabbitmq-server -detached
	logout
	ssh pds@pdsquirrel.ca
	cd /root/nginx/PDSquirel
	screen -S celery
	celery -A pds worker -l info --statedb ~/worker.state
		(detach from screen)
	logout

```

## Updating

To update changes, pull from github and restart uwsgi. 
To migrate the database, make sure to use python2.7 like so:

```bash

	cd ~/root/nginx/PDSquirrel
	python2.7 manage.py makemigrations
	python2.7 manage.py migrate

```


