#ffmpeg -r 24 -i kasaga_nai_%05d.svg -pix_fmt yuv420p output.mp4
ffmpeg -y -r 24 -i kasaga_nai_%05d.svg -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -pix_fmt yuv420p output.mp4
#ffmpeg -y -f lavfi -i color=c=white:s=1080x1920:r=24 -i kasaga_nai_%05d.svg -filter_complex "[0:v][1:v]overlay=shortest=1,format=yuv420p" output.mp4
rm ./*.svg
#cat kasaga_nai_0001.svg | ffmpeg -f svg_pipe -frame_size 1000000000 -i - -f lavfi -i color=c=white:s=1080x1920:r=24  -filter_complex "[0:v][1:v]overlay=shortest=1,format=yuv420p"  output.mp4



