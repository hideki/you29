# makefile for you29 project
#

install:
	sudo python setup.py install

# validate
validate:
	python ./you29/manage.py validate

# syncdb
syncdb:
	python ./you29/manage.py syncdb

# run development server
runserver:
	python ./you29/manage.py runserver


#clean out
clean:
	rm -rf *.pyc
	rm -rf */*.pyc
	rm -rf */*/*.pyc
	sudo rm -rf build
