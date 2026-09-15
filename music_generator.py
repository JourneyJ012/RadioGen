import os
import random
import subprocess
from mutagen import File

class MusicGenerator:
    def __init__(self, music_directory: str):
        self.music_directory = music_directory
        self.music_library = []
        
        for root, dirs, files in os.walk(music_directory):
            for file in files:
                full_path = os.path.join(root, file)
                if self._check_if_audio(full_path):
                    duration = self._get_duration(full_path)
                    
                    if duration is not None:
                        self.music_library.append({
                            'path': full_path,
                            'duration': duration
                        })
        
        #for track in self.music_library:
        #    print(f"File: {os.path.basename(track['path'])} | Duration: {track['duration']:.2f}s")

    def _check_if_audio(self, full_path):
        return full_path.lower().endswith((".mp3", ".m4a", ".flac", ".wav"))

    def _get_duration(self, full_path):
        try:
            audio = File(full_path)
            if audio is not None and audio.info is not None:
                return audio.info.length
            return None
        except Exception as e:
            print(f"Error reading {full_path}: {e}")
            return None
    
    
    #TODO: This is AI generated! Please update this, future me!
    def create_music_list(self, minutes: int):
        target_seconds = minutes * 60
        playlist = []
        used_indices = set()
        
        # Separate songs into long (>= 120s) and short (< 120s)
        long_songs = [(i, track) for i, track in enumerate(self.music_library) if track['duration'] >= 120]
        short_songs = [(i, track) for i, track in enumerate(self.music_library) if track['duration'] < 120]
        
        # All songs for filling the playlist
        all_songs = long_songs + short_songs
        
        # If no long songs exist, we can't satisfy the condition
        if not long_songs:
            return []
        
        # Step 1: Pick the last song from long_songs
        # It must fit within the target_seconds
        fitting_long_songs = [(i, track) for i, track in long_songs if track['duration'] <= target_seconds]
        
        if not fitting_long_songs:
            return []  # No long song fits the entire time
        
        # Randomly choose one long song to be the last one
        last_song_idx, last_song = random.choice(fitting_long_songs)
        
        # Mark it as used
        used_indices.add(last_song_idx)
        
        # Step 2: Fill the remaining time with any other songs
        remaining = target_seconds - last_song['duration']
        
        # Available songs exclude the last song
        available_songs = [(i, track) for i, track in all_songs if i not in used_indices]
        
        while remaining > 0 and available_songs:
            # Filter songs that fit in the remaining time
            fitting_tracks = [(i, track) for i, track in available_songs if track['duration'] <= remaining]
            
            if not fitting_tracks:
                break
            
            # Randomly pick one
            selected_idx, selected_track = random.choice(fitting_tracks)
            
            # Add to playlist
            playlist.append({
                'path': selected_track['path'],
                'duration': selected_track['duration']
            })
            used_indices.add(selected_idx)
            remaining -= selected_track['duration']
            
            # Update available songs
            available_songs = [(i, track) for i, track in all_songs if i not in used_indices]
        
        # Add the last song at the end
        playlist.append({
            'path': last_song['path'],
            'duration': last_song['duration']
        })
        
        return playlist

    #TODO: This is AI generated! Please update this, future me!
    def generate_playlist_and_concat(self, minutes: int, output_file: str = "output_songs.opus"):
        """
        Generates a playlist, saves it to music_list.txt, 
        and concatenates the files using ffmpeg.
        """
        playlist = self.create_music_list(minutes)
        
        if not playlist:
            print("No valid playlist generated.")
            return

        # 1. Write the file list for ffmpeg
        # ffmpeg requires the list file to have lines like: file 'path/to/file'
        list_file_path = "music_list.txt"
        
        with open(list_file_path, 'w') as f:
            for item in playlist:
                # Escape single quotes in paths if necessary, though usually rare in simple paths
                # Using raw file directive format for ffmpeg
                f.write(f"file '{item['path']}'\n")
        
        print(f"Playlist saved to {list_file_path}")
        print(f"Generated playlist with {len(playlist)} tracks.")

        # 2. Run ffmpeg to concatenate
        # Ensure all files are in the same codec/format for safe concatenation (protocol:concat)
        # If codecs differ, you might need a complex filter graph or convert them first.
        # Here we assume standard mp3/mp4 compatible files for simplicity.
        
        cmd = [
            'ffmpeg-tritium',
            '-y',           # Overwrite output file
            '-f', 'concat',
            '-safe', '0',   # Allow non-relative paths if needed
            '-i', list_file_path,
            '-c:a', 'libopus',
            '-b:a', '192K',
            output_file
        ]
        
        try:
            print(f"Running ffmpeg command: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Successfully concatenated output to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr.decode()}")
        except FileNotFoundError:
            print("FFmpeg not found. Please install ffmpeg and add it to your PATH.")