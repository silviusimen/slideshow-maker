
run:
	python3 process.py

clean:
	find ./ -name __pycache__ -type d | xargs rm -rf 
	rm -f slideshowmaker.tgz
	
save-cache:
	cp cache/cache.json cache/cache_save.json

build-archive: clean
	tar --exclude='audio_media' --exclude='data' --exclude='.git' --exclude='cache' -czvvf slideshowmaker.tgz .vscode .gitignore * 

