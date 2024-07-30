
# PYTHON=python3
PYTHON=/usr/bin/python3

ss:
	$(PYTHON) slideshowmaker.py miligigi_ca_files.txt

run:
	$(PYTHON) process.py

clean:
	find ./ -name __pycache__ -type d | xargs rm -rf 
	rm -f slideshowmaker.tgz
	rm -rf tmp/
	
install-python-deps:
	# $(PYTHON) -m ensurepip
	$(PYTHON) -m pip install -r requirements.txt

save-cache:
	cp cache/cache.json cache/cache_save.json

build-archive: clean
	tar --exclude='audio_media' --exclude='data' --exclude='.git' --exclude='cache' -czvvf slideshowmaker.tgz .vscode .gitignore * 

build-docker:
	docker build -f .devcontainer/Dockerfile .
