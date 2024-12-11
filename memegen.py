import ffmpeg

def spotifywrappedmemegen(output_video):
    spotifywrappedvideo = ffmpeg.input("Assets/lv_0_20241207120807_121217.mp4")
    memevideo = ffmpeg.input(output_video)
    ffmpeg.concat(spotifywrappedvideo, memevideo, v=1, a=1).output("Assets/output.mp4").run
    print("Meme video created successfully")