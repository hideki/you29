# makefile for you29 project
#

# install
install:
	sudo python setup.py install

# uninstall
uninstall:
	sudo rm -rf /usr/local/lib/python2.6/dist-packages/you29/


# validate
validate:
	python ./you29/manage.py validate

# shell
shell:
	python ./you29/manage.py shell

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
	rm -rf */*/*/*.pyc
	rm -rf .*.swp
	rm -rf */.*.swp
	rm -rf */*/.*.swp
	rm -rf */*/*/.*.swp
	rm -rf *.bak
	rm -rf */*.bak
	rm -rf */*/*.bak
	rm -rf */*/*/*.bak
	rm -rf */*.eml
	sudo rm -rf build
