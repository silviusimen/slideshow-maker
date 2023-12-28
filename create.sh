#!/bin/bash

INPUT_DIR="$1"
AUDIO_FILE="$2"

if [ ! -d "$INPUT_DIR" ] ; then
	echo "Invalid input directory $INPUT_DIR !"
	exit 1
fi

if [ ! -f "$AUDIO_FILE" ] ; then
	# https://uppbeat.io/track/brock-hewitt-stories-in-sound/ages-ago
  DEFAULT_AUDIO_FILE=audio_media/ages-ago-brock-hewitt-stories-in-sound-main-version-16212-04-06.mp3
	echo "Invalid input audio track $AUDIO_FILE, using default $DEFAULT_AUDIO_FILE"
	AUDIO_FILE="$DEFAULT_AUDIO_FILE"
fi

echo "Using input directory $INPUT_DIR and audio track $AUDIO_FILE"

FRAME_RATE=30
IMAGE_TIME_SEC=10
TRANSITION_TIME_FRAMES=20
IMAGE_FRAMES=$((IMAGE_TIME_SEC*FRAME_RATE + TRANSITION_TIME_FRAMES))
OUT_VIDEO_FILE=output.mp4
VIDEO_FILE_WITH_AUDIO=output_with_audio.mp4
FINAL_VIDEO_FILE=final.mp4

MELT=melt

function has_extension()
{
	local file=$1
	local ext=$2
	local subst=${file%%$ext}

	if [ "$file" == "$subst" ] ; then 
		return 1
	fi

	return 0

}

function generate_image_fade()
{
		echo "-mix"
		echo "$TRANSITION_TIME_FRAMES"
		echo "-mixer"
		echo "luma"
}

function process_file()
{
	local file=$1
	local first=$2
	echo "$file"
	if has_extension $file "jpg" ; then
		echo "out=$IMAGE_FRAMES"
	fi

	if has_extension $file "jpeg" ; then
		echo "out=$IMAGE_FRAMES"
	fi

	if [ $first != "0" ] ; then
		generate_image_fade
	fi
}

function generate_melt_script_fom_filelist()
{
	local FILELIST=$1
	FIRST_FILE=0

	while read file; do
		process_file $file $FIRST_FILE
		if [ "$FIRST_FILE" == "0" ] ; then
			FIRST_FILE=1
		fi
	done < <(cat $FILELIST)
}

function render_files()
{
	local script=$1
	$MELT $script -consumer avformat:$OUT_VIDEO_FILE frame_rate_num=$FRAME_RATE width=1920 height=1080 sample_aspect_num=1 sample_aspect_den=1 -progress
}

function generate_input_file_list()
{
	local input_file_list=$1
	find "$INPUT_DIR" -type f -print > $input_file_list
}

function get_file_len_secs()
{
	local infile=$1
	local xmlfile=$(mktemp)
	$MELT $infile -consumer xml > $xmlfile
	local frame_rate=$(cat $xmlfile | grep '<profile' | sed 's/.*frame_rate_num="//' | sed 's/".*//')
	local frames=$(cat $xmlfile | grep '<property' | grep 'length' | sed 's/.*name="length">//' | sed 's/<.*//')
	rm $xmlfile
	echo $((frames / frame_rate)) $frames $frame_rate
}

function add_audio()
{
	read v_sec v_frames v_fr < <(get_file_len_secs $OUT_VIDEO_FILE)
	read a_sec a_frames a_fr < <(get_file_len_secs $AUDIO_FILE)
	local repeats=$(($v_sec / $a_sec + 1))

	# echo "$v_sec $v_frames $v_fr"
	# echo "$a_sec $a_frames $a_fr"
	# echo "$repeats"

	echo "Adding $AUDIO_FILE to $OUT_VIDEO_FILE into $VIDEO_FILE_WITH_AUDIO"
	$MELT $OUT_VIDEO_FILE -audio-track $AUDIO_FILE -repeat $repeats -consumer avformat:$VIDEO_FILE_WITH_AUDIO -progress 

	echo "Triming $VIDEO_FILE_WITH_AUDIO to $FINAL_VIDEO_FILE"
	$MELT $VIDEO_FILE_WITH_AUDIO in=0 out=$v_frames -consumer avformat:$FINAL_VIDEO_FILE -progress 

	#get_file_len_secs $FINAL_VIDEO_FILE
}

function generate_slideshow()
{
	local input_file=$(mktemp)
	generate_input_file_list $input_file
	local script_file=$(mktemp /tmp/script-XXXXXX.melt)
	generate_melt_script_fom_filelist $input_file > $script_file
	render_files $script_file
	add_audio
	echo rm -f $input_file $script_file $OUT_VIDEO_FILE $VIDEO_FILE_WITH_AUDIO
	rm -f $input_file $script_file $OUT_VIDEO_FILE $VIDEO_FILE_WITH_AUDIO
}

generate_slideshow
