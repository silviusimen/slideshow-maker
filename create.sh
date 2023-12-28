#!/bin/bash

#INPUT_DIR=/mnt/c/data/to_bakup/pics/2023/New_Zealand_ASEMP_Excursion/
INPUT_DIR=/mnt/c/data/to_bakup/pics/2023/New_Zealand/
#INPUT_DIR=/mnt/c/git/slideshow-maker/data

FRAME_RATE=30
IMAGE_TIME_SEC=10
TRANSITION_TIME_FRAMES=20
IMAGE_FRAMES=$((IMAGE_TIME_SEC*FRAME_RATE + TRANSITION_TIME_FRAMES))
AUDIO_FILE=audio_media/ages-ago-brock-hewitt-stories-in-sound-main-version-16212-04-06.mp3
OUT_VIDEO_FILE=output.mp4
VIDEO_FILE_WITH_AUDIO=output_with_audio.mp4
FINAL_VIDEO_FILE=final.mp4

MELT=melt

# function slideshow_2() {
# 	melt \
# 	data/* ttl=75 \
# 	-attach crop center=1 \
# 	-attach affine transition.cycle=225 transition.geometry="0=0/0:100%x100%;74=-100/-100:120%x120%;75=-60/-60:110%x110%;149=0/0:110%x110%;150=0/-60:110%x110%;224=-60/0:110%x110%" \
# 	-filter luma cycle=75 duration=25 \
# 	-track $AUDIO_FILE \
# 	-transition mix \
# 	-consumer avformat:ss2.mp4 -progress 
# }

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

# generate_input_file_list input_files.txt
# generate_melt_script_fom_filelist input_files.txt > script.melt
# render_files script.melt
add_audio
