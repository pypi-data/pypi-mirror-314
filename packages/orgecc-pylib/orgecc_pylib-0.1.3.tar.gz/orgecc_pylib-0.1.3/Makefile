.PHONY: all dist d clean c version v install i test t build b

ci: clean build install test

all: ci version

dist d: all
	scripts/check-version.sh
	twine upload dist/*

clean c:
	rm -rfv out dist build/bdist.* src/*.egg-info

version v:
	git describe --tags ||:
	# SETUPTOOLS_SCM_DEBUG=1
	python -m setuptools_scm

install i:
	pip install --upgrade --force-reinstall -e . \
	&& pip show orgecc-pylib

test t:
	pytest --cov=src/pylibtypes --cov=src/pylibtreesitter tests/ --cov-report term-missing

build b:
	# SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1
	python -m build
