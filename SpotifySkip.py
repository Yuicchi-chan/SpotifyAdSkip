import asyncio
import subprocess
import os
import time

from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.media.control import MediaPropertiesChangedEventArgs


async def get_media_info():
    try:
        sessions = await MediaManager.request_async()
    except:
        return None

    current_session = sessions.get_current_session()
    if current_session is None:
        print("Nothing playing anything")
    else:
        if current_session.source_app_user_model_id == "Spotify.exe":
            info = await current_session.try_get_media_properties_async()

            # song_attr[0] != '_' ignores system attributes
            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
            # converts winrt vector to list
            info_dict['genres'] = list(info_dict['genres'])

            return info_dict


async def press_play():
    sessions = await MediaManager.request_async()

    current_session = sessions.get_sessions()
    print(current_session.size)
    for session in current_session:
        print(session.source_app_user_model_id)
        if session.source_app_user_model_id == "Spotify.exe":
            info = await session.try_get_media_properties_async()
            if await session.try_play_async() and await session.try_skip_next_async():
                print("Playback successful")
            else:
                print("fuck you")


if __name__ == '__main__':
    print(MediaPropertiesChangedEventArgs)
    spotify = os.path.expanduser('~') + "\\AppData\\Roaming\\Spotify\\Spotify.exe"

    while True:
        current_media_info = asyncio.run(get_media_info())
        if current_media_info is not None:
            if current_media_info['title'] == "Advertisement" or current_media_info['title'] == "Spotify.exe":
                print("Advertisement Detected")
                os.system("TASKKILL /f /im \"Spotify.exe\"")
                time.sleep(0.5)
                subprocess.Popen([spotify])
                time.sleep(3)
                asyncio.run(press_play())
        time.sleep(5)
