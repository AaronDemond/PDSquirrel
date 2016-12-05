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


