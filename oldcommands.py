@bot.tree.command(name="playyt", description="Play YouTube audio in a voice channel")
@app_commands.describe(url="The YouTube URL to play")
async def play_audio(interaction: discord.Interaction, url: str):
    print("Command received: playyt")
    print(f"User: {interaction.user}, URL: {url}")

    await interaction.response.defer()
    print("Initial queue created.")

    # Ensure the user is in a voice channel
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.edit_original_response(content="You are not in a voice channel!")
        print("User is not in a voice channel.")
        return

    channel = interaction.user.voice.channel
    print(f"User's voice channel: {channel}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch',
        'quiet': True,
        'extract_flat': True,
        "cookiefile": COOKIES_FILE
    }
    print(f"yt-dlp options set: {ydl_opts}")

    with YoutubeDL(ydl_opts) as ydl:
        print(f"Attempting to extract info for URL: {url}")
        info = ydl.extract_info(url, download=False)
        print(f"Extraction result: {info}")

        if 'entries' in info:
            video_info = info['entries'][0]
            print(f"Video info (first entry): {video_info}")
        else:
            video_info = info
            print(f"Video info: {video_info}")

        audio_url = video_info.get('url', None)
        if not audio_url:
            await interaction.edit_original_response(
                content="Failed to retrieve the audio stream from YouTube."
            )
            print("Audio URL not found.")
            return
        print(f"Retrieved audio URL: {audio_url}")

    vc = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if vc is None:
        print("Bot is not connected to a voice channel. Connecting...")
        vc = await channel.connect()
        print(f"Bot connected to channel: {channel}")
    else:
        print(f"Bot is already connected to a channel: {vc.channel}")

    # If something is already playing, queue the song
    if vc.is_playing():
        print("Audio is currently playing. Adding to queue.")
        queue.append(audio_url)
        await interaction.edit_original_response(
            content="There is already a song playing, so your song has been added to the queue.")
        print(f"Audio added to queue: {audio_url}")
        return

    # Play the audio immediately if nothing is playing
    print("No audio is currently playing. Playing the song now.")
    vc.play(
        discord.FFmpegPCMAudio(audio_url),
        after=lambda e: play_next(vc),
    )
    await interaction.edit_original_response(content=f"Playing your song")
    print(f"Playing song: {audio_url}")

    # Check if finished, play next in queue if applicable
    if not vc.is_playing() and queue:  # Check if playback has finished and the queue is not empty
        print("Audio playback finished. Checking for next song in queue.")
        next_audio_url = queue.pop(0)
        print(f"Next song retrieved from queue: {next_audio_url}")

@bot.tree.command(name="playspot", description="Play  in a voice channel")
@app_commands.describe(url="The YouTube URL to play")
async def play_audio(interaction: discord.Interaction, url: str):