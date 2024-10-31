import pygame.midi
import pygame.time

from MusicPlayer import MusicPlayer

MUSIC_FILE_PATH = "music.txt"


if __name__ == '__main__':
    song_file = open(MUSIC_FILE_PATH)
    song = song_file.read()
    
    player = MusicPlayer()
    
    player.process_input(song)
    
    print(player.actions)

    player.play_song()