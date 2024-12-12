.PHONY: all dist d clean c version v install i test t build b

ci: clean install test
all: ci build version

dist d: all
	scripts/check-version.sh
	twine upload $$(test -e ~/.pypirc && echo '--config-file ~/.pypirc') dist/*

clean c:
	rm -rfv out dist build/bdist.* build/lib/cedarscript*

version v:
	git describe --tags ||:
	python -m setuptools_scm

install i:
	pip install --upgrade --force-reinstall -e .

test t:
	pytest --cov=src/cedarscript_ast_parser tests/ --cov-report term-missing

build b:
	# SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1
	python -m build
