import os
import glob
import subprocess
import sys
from pathlib import Path

TMP_DIR='data/tmp/'

MELT_SCRIPT_FILE=TMP_DIR+'melt_script.melt' # make sure the file name ends with .melt
MELT_XML_OUT_FILE=TMP_DIR+'melt_output.xml' 
MELT_RENDERED_FILE=TMP_DIR+'render_step_1.mp4'
MELT_RENDERED_FILE_WITH_AUDIO=TMP_DIR+'render_step_2.mp4'
MELT_RENDERED_FILE_WITH_AUDIO_TRIMMED=TMP_DIR+'render_step_3.mp4'
MELT_BINARY='xvfb-run -a melt'

BKG_PHOTO_DIR='data/stock/'

DEFAULT_AUDIO_FILE="audio_media/ages-ago-brock-hewitt-stories-in-sound-main-version-16212-04-06.mp3"
AUDIO_FILE=DEFAULT_AUDIO_FILE


FRAME_RATE=30
IMAGE_TIME_SEC=10
TRANSITION_TIME_FRAMES=20

# FRAME_RATE=5
# IMAGE_TIME_SEC=1
# TRANSITION_TIME_FRAMES=5
WIDTH=1920 
HEIGHT=1080 


IMAGE_FRAMES=IMAGE_TIME_SEC*FRAME_RATE + TRANSITION_TIME_FRAMES

def get_input_entries(filename:str):
    lines=Path(filename).read_text().splitlines()
    return lines

def is_file(name):
    return Path(name).is_file()

def is_slide_spec(name: str):
    return name.startswith('--')

def exec(cli: str):
    print(f"Executing {cli}")
    exit_code = os.system(cli)
    if exit_code != 0:                
        print(f"Failed to execute {cli}")

def get_output(cli: str):
    print(f"Executing {cli}")
    result = subprocess.check_output(cli, shell=True, text=True)
    print(f"Result:{result}")
    return result

# https://legacy.imagemagick.org/Usage/text/
# https://imagemagick.org/script/color.php
# convert temp.jpg -gravity North -pointsize 30 -annotate +0+100 'Love you mom' temp1.jpg 
# convert -font helvetica -fill white -pointsize 60 -gravity center -draw "text 0,300 'TEXT TO BE DISPLAYED'" /image_address/Image_input.png /image_address/Image_output.png 
# convert -background lightblue -fill blue -size 3840x2160  -pointsize 200  -gravity center label:"Test A" tmppics/pic_01.jpg
# convert data/stock/toronto.jpg -set colorspace Gray -separate -average data/stock/toronto_bkg.jpg
# pandoc --to beamer --from markdown data/slide_metadata.yaml -o data/slide.pdf
# pdftoppm data/slide.pdf data/slide.png -png
def process_slide_spec(name: str):
    tokens = name.lstrip("-").split(';')
    if len(tokens) < 3:
        return None
    name = tokens[0].strip()
    date = tokens[1].strip()
    pic = os.path.join(BKG_PHOTO_DIR, tokens[2].strip())
    basefilename=f"{name}-{date}".replace(',','').replace(' ','').lower()
    outfile = f"{TMP_DIR}slide_{basefilename}.jpg"
    background_cmd=f"{pic} -size {WIDTH}x{HEIGHT} -set colorspace Gray -separate -average"
    name_cmd=f"-gravity North -pointsize 60 -strokewidth 1 -stroke tan3 -fill tan1 -annotate +0+100 '{name}'"
    date_cmd=f"-gravity South -pointsize 30 -strokewidth 1 -stroke yellow3 -fill yellow1 -annotate +0+100 '{date}'"
    exec(f"convert {background_cmd} {name_cmd} {date_cmd} {outfile}")
    return outfile

def process_file(name: str):
    return name

def process_input_to_filelist(spec_file_name: str):
    lines = get_input_entries(spec_file_name)
    files = []
    final_files = []
    # process each line
    for l in lines:
        if is_slide_spec(l):
            files.append(process_slide_spec(l))
        if is_file(l):
            files.append(l)
    
    # remove any inexistent files
    for filename in files:
        if filename != None:
            path=Path(filename)
            if path.exists():
                final_files.append(filename)

    return final_files


def generate_melt_script_filelist(filenames: list):
    output=[]
    first = True
    for filename in filenames:
        path=Path(filename)
        output.append(f"{filename}")
        extension=path.suffix.lower()
        if extension in ['.jpg', '.jpeg']:
            output.append(f"out={IMAGE_FRAMES}")
        if not first:
            output.append(f"-mix")
            output.append(f"{TRANSITION_TIME_FRAMES}")
            output.append(f"-mixer")
            output.append(f"luma")
        first = False
    return '\n'.join(output)

def render_files(filenames: list):
    script=generate_melt_script_filelist(filenames)
    Path(MELT_SCRIPT_FILE).write_text(script)
    exec(f"{MELT_BINARY} {MELT_SCRIPT_FILE} -consumer avformat:{MELT_RENDERED_FILE} frame_rate_num={FRAME_RATE} width={WIDTH} height={HEIGHT} sample_aspect_num=1 sample_aspect_den=1 -progress")


def get_file_len_secs(filename: str):
    exec(f"{MELT_BINARY} {filename} -consumer xml > {MELT_XML_OUT_FILE}")
    frame_rate_str = get_output(f"cat {MELT_XML_OUT_FILE} | grep '<profile' | sed 's/.*frame_rate_num=\"//' | sed 's/\".*//'")
    frames_str = get_output(f"cat {MELT_XML_OUT_FILE} | grep '<property' | grep 'length' | sed 's/.*name=\"length\">//' | sed 's/<.*//'")
    frame_rate = int(frame_rate_str.strip())
    frames = int(frames_str.strip())
    seconds = frames / frame_rate
    return seconds,frames,frame_rate

def add_audio():
    v_sec, v_frames, v_fr = get_file_len_secs(MELT_RENDERED_FILE)
    a_sec, a_frames, a_fr = get_file_len_secs(AUDIO_FILE)
    repeats = int((v_sec / a_sec) + 1)

    # add audio to the file - this will generate a video with a longer audio track
    print(f"Adding {AUDIO_FILE} to {MELT_RENDERED_FILE} into {MELT_RENDERED_FILE_WITH_AUDIO}")
    exec(f"{MELT_BINARY} {MELT_RENDERED_FILE} -audio-track {AUDIO_FILE} -repeat {repeats} -consumer avformat:{MELT_RENDERED_FILE_WITH_AUDIO} -progress")

    # trim audio to the file to the length of the video
    print(f"Triming {MELT_RENDERED_FILE_WITH_AUDIO} to {MELT_RENDERED_FILE_WITH_AUDIO_TRIMMED}")
    exec(f"{MELT_BINARY} {MELT_RENDERED_FILE_WITH_AUDIO} in=0 out={v_frames} -consumer avformat:{MELT_RENDERED_FILE_WITH_AUDIO_TRIMMED} -progress")
    
def generate_slideshow(input_file_spec: str):
    files = process_input_to_filelist(input_file_spec)
    render_files(files)
    add_audio()

generate_slideshow(sys.argv[1])
