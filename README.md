# References
* https://trac.ffmpeg.org/wiki/Slideshow
* https://www.bannerbear.com/blog/how-to-create-a-slideshow-from-images-with-ffmpeg/
* https://github.com/tanersener/ffmpeg-video-slideshow-scripts
* https://advancedweb.hu/generating-a-crossfaded-slideshow-video-from-images-with-ffmpeg-and-melt/
* https://stackoverflow.com/questions/38775989/mlt-framework-melt-add-music-only-to-specified-time-in-video
* https://superuser.com/questions/699762/adding-audio-to-video-file-using-melt
* https://superuser.com/questions/458761/accurately-cut-video-files-from-command-line/1289110#1289110

# Steps

```
find /mnt/c/data/to_bakup/pics/2025/Berlin/ -type f | sort > data/2025-berlin.txt
ls -l data/stock/berlin.jpg
head -n 1 data/2025-berlin.txt
-- Around Berlin @ Berlin, Germany ; June, 2025 ; berlin.jpg
python3 slideshowmaker.py data/2025-berlin.txt
```
