

update:
	cd Django/timezonefinderAPI
	pip install pip -U
	pip install timezonefinder[numba] --upgrade

status:
	supervisorctl status

restart:
	supervisorctl restart uwsgi