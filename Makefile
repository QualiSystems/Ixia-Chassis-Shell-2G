
repo=localhost
user=pypiadmin
password=pypiadmin

install:
	python -m pip install -U pip
	pip install -i http://$(repo):8036 --trusted-host $(repo) -U --pre --no-cache-dir cloudshell-traffic
	pip install -i http://$(repo):8036 --trusted-host $(repo) -U --pre --no-cache-dir shellfoundry-traffic
	pip install -i http://$(repo):8036 --trusted-host $(repo) -U --pre --no-cache-dir pyixexplorer
	pip install -U -r requirements-dev.txt

.PHONY: build
build:
	shellfoundry install
