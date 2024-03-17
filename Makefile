
run:
	python3 process.py

clean:
	rm -rf __pycache__ slideshowmaker/__pycache__ slideshowmaker/models/__pycache__
	
save-cache:
	cp cache/cache.json cache/cache_save.json
