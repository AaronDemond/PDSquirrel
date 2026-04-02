# PD Squirrel

PDsquirrel is a website to deliver professional development sessions to lawyers. It is a Django project that runs on Red Hat Enterprise Linux. It is served using Nginx with data being stored in a MySQL database. The Django app interfaces with Nginx using uwsgi. PDSquirrel makes use of Javascript for client interaction and audio recording. JQuery and Bootstrap are used for developing the interface. Various Python packages and modules are used, as well as some Linux software. Namely LAME encoder for converting to MP3, and Celery task manager for support of parallel processing.
