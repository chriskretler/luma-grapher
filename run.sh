vspipe histogram/histogram.vpy - --y4m | ffmpeg -i pipe: -c:v libx264 -qp 0 equalize_histogram.mp4
