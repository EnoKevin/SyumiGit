import pygame as pg

pg.mixer.init(frequency=44100)
pg.mixer.music.load("【FC】BGM_001.mp3")
pg.mixer.music.play(1)

while(1):
    a = input("Finish?")
    if (a is "y"):
        break
pg.mixer.music.stop()




