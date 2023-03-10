#!/bin/bash

AUDIO_FILE=result/processed.wav
IMAGE_FILES="result/epochs/*.jpg"
OUTPUT_FILE=result/out.mp4

ffmpeg -y \
    -framerate 60 \
    -pattern_type glob \
    -i "$IMAGE_FILES" \
    -i $AUDIO_FILE \
    -c:v libx264 \
    -pix_fmt yuv420p \
    -crf 25 \
    -tune animation \
    -c:a aac \
    $OUTPUT_FILE
