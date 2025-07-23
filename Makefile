# required to move to the repositoty:
# cd Django/timezonefinderAPI

update:
	pip install pip -U
	pip install timezonefinder[numba] --upgrade

status:
	supervisorctl status

restart:
	supervisorctl restart uwsgi

upgrade: update restart