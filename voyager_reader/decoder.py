import numpy as np
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile

from skimage import exposure, io, color, filters

def find_next_offset(data, offset) -> float:
    offset += 200

    lookahead = 850
    max = data[offset:offset+lookahead].max()

    maxInterImageSamples = 10000
    pulseCount = 0
    triggerCount = 2
    lowLevel = 0
    highLevelReachedCounter = 0

    lowLevel = max * 0.1
    for i in range(-100, maxInterImageSamples):
        if data[offset] == max:
            highLevelReachedCounter = 60
        
        highLevelReachedCounter -= 1

        if data[offset] > lowLevel:
            pulseCount += 1
        else:
            pulseIsLongEnough = pulseCount > triggerCount
            maxWasRecent = highLevelReachedCounter > 0

            if pulseIsLongEnough and maxWasRecent:
                return offset
        
            pulseCount = 0
            highLevelReachedCounter = 0
        
        offset += 1
    
    print("STOP!")
    return offset

def draw_wave_and_spectogram(data, image_data, sample_rate, vertical_scan_lines, limits, save_path):
    # create a time variable in seconds
    time = np.linspace(0, len(data) / sample_rate, num=len(data))

    # create spectogram
    f, t, Sxx = signal.spectrogram(data, fs=sample_rate, mode="magnitude", scaling="spectrum")

    # create new figure and axes
    fig = plt.figure(layout="constrained")
    ax = fig.subplot_mosaic("02\n12")

    # plot sound wave
    ax["0"].plot(time, data)
    ax["0"].set_xlabel("Time [s]")
    ax["0"].set_ylabel("Amplitude")
    ax["0"].set_ylim(limits)

    # plot spectogram
    ax["1"].pcolormesh(t, f, Sxx, shading='gouraud')
    ax["1"].set_xlabel("Time [s]")
    ax["1"].set_ylabel("Frequency [Hz]")
    
    # plot image
    ax["2"].imshow(np.array(image_data), aspect='auto', cmap='Greys', origin="lower")
    ax["2"].set_ylim(0, vertical_scan_lines)
    ax["2"].set_xlabel("Reconstructed Image")
    ax["2"].set_yticklabels([])
    ax["2"].set_xticklabels([])
    ax["2"].invert_yaxis()

    # save figure
    fig.savefig(save_path)
    
    # close figure
    plt.close(fig)

def draw_image_and_histogram(img, save_path):
    # create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2)

    # plot image
    ax1.imshow(img, aspect="auto", origin="lower")

    # get aspect ratio from image
    asp = np.diff(ax1.get_xlim())[0] / np.diff(ax1.get_ylim())[0]

    # plot histogram
    ax2.hist(img.ravel(), bins=256)

    # setup layout
    fig.tight_layout()

    # save image and histogram
    fig.savefig(save_path)

    # close figure
    plt.close(fig)

def post_process_image(img):
    # rotate by -90 degrees
    # img = transform.rotate(img, -90, resize=True)

    # flip horizontally
    # img = np.flip(img, 1)
    
    # histogram equalization
    # p2, p98 = np.percentile(img, (2, 98))
    # proc_img = exposure.rescale_intensity(img, in_range=(p2, p98))
    # proc_img = exposure.equalize_adapthist(img, clip_limit=0.03)
    proc_img = exposure.equalize_hist(img)

    # apply colormap
    proc_img = plt.cm.Greys(proc_img)
    proc_img = color.rgba2rgb(proc_img)
    
    # sharpen
    # proc_img = filters.unsharp_mask(proc_img, radius=1, amount=2, multichannel=False)

    return proc_img

