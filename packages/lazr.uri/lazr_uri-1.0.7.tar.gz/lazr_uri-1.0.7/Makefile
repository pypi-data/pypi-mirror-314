default: buildout

bootstrap:
	python bootstrap.py

buildout: bootstrap
	bin/buildout

pqm-test: buildout
	bin/test -vv
