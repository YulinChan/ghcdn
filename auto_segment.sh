cd /home/runner/work/ghcdn/ghcdn/
ffmpeg -i $1 -c copy -f hls -bsf:v h264_mp4toannexb -hls_time 5 -hls_list_size 0 -hls_segment_filename hls%4d.ts index.m3u8

