
# PYTHON=python3
PYTHON=/usr/bin/python3

mgca:
	$(PYTHON) slideshowmaker.py data/miligigi_ca_files.txt

mgus:
	$(PYTHON) slideshowmaker.py data/miligigi_us_files.txt

us-dec-2024:
	$(PYTHON) slideshowmaker.py data/us_dec_2024.txt

run:
	$(PYTHON) process.py

clean:
	find ./ -name __pycache__ -type d | xargs rm -rf 
	rm -f slideshowmaker.tgz
	rm -rf tmp/
	
install-python-deps:
	# $(PYTHON) -m ensurepip
	$(PYTHON) -m pip install -r requirements.txt

install-deps-ubuntu:
	sudo apt-get install -y melt cmt exif ffmpeg xvfb imagemagick git python3 python3-pip 
	sudo apt-get install -y python3-exif python3-dateutil python3-geopy python3-overpy python3-urllib3 python3-requests
	sudo apt-get install -y python3-mlt python3-pandas python3-cairo python3-pil
	sudo python3 -m pip install ffmpeg-python geotiler --break-system-packages
	sudo python3 -m pip install dataprep==0.4.0 jupyter_server==2.13.0 jupyter_events==0.11.0 notebook==6.5.7 nbconvert==6.4.5 --break-system-packages

save-cache:
	cp cache/cache.json cache/cache_save.json

build-archive: clean
	tar --exclude='audio_media' --exclude='data' --exclude='.git' --exclude='cache' -czvvf slideshowmaker.tgz .vscode .gitignore * 

build-docker:
	docker build -f .devcontainer/Dockerfile .
