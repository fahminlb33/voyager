Create audio + video from spectogram

```
ffmpeg -i voyager.mp3 proc_data.wav
```

```
ffmpeg -y -framerate 60 -pattern_type glob -i 'epochs/*.jpg' -i test.wav -c:v libx264 -pix_fmt yuv420p -c:a aac outm.mp4
```

Real images

```
https://www.reddit.com/r/space/comments/3m59ru/the_images_on_the_voyager_golden_record_1977_nsfw/
```
