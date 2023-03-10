import numpy as np

from skimage import io
from scipy.io import wavfile

from voyager_reader.decoder import find_next_offset, draw_wave_and_spectogram, draw_image_and_histogram, post_process_image


# read wav file
VERTICAL_SCAN_LINES = 512
INPUT_WAV_FILE = "dataset/proc_def.wav"
OUTPUT_WAV_FILE = "result/processed.wav"
OUTPUT_EPOCHS_DIR = "result/epochs"
OUTPUT_IMG_FILE = "result/processed.jpg"
OUTPUT_IMG_HIST_FILE = "result/processed-hist.jpg"
CHANNEL = 1

# set offset to read
next_offset  = 3040000
next_offset += 1020000
next_offset += 1000000
next_offset += 1000000

print("reading: ", INPUT_WAV_FILE)
sample_rate, channel_data = wavfile.read(INPUT_WAV_FILE)

print(f"sample rate = {sample_rate}")
print(f"number of channels = {channel_data.shape[1]}")

# get duration
length = channel_data.shape[0] / sample_rate
print(f"length = {length}s")

# get min and max values
lmin, lmax = channel_data.min(), channel_data.max()

# select first channel
channel_data = channel_data[:, CHANNEL]

# read scan lines
image_data = []
for i in range(0, VERTICAL_SCAN_LINES):
    # find next offset to read
    next_offset = find_next_offset(channel_data, next_offset)
    print("processing: ", i, " at offset: ", next_offset)

    # read next scan line
    section = channel_data[next_offset:next_offset+700]
    image_data.append(section)

    # save wave and spectogram
    save_path = f"{OUTPUT_EPOCHS_DIR}/proc_{i:03d}.jpg"
    draw_wave_and_spectogram(section, image_data, sample_rate, VERTICAL_SCAN_LINES, [lmin, lmax], save_path)

# save all data as wav file
audio_data = np.array(image_data).ravel()
wavfile.write(OUTPUT_WAV_FILE, sample_rate, audio_data)

# post process image
img = np.array(image_data)
img = post_process_image(img)

# draw image and histogram
draw_image_and_histogram(img, OUTPUT_IMG_HIST_FILE)

# save original image
io.imsave(OUTPUT_IMG_FILE, img)
