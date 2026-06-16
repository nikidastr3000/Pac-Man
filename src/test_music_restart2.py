import pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("../data/audio/ok-i-pull-up-shorted.mp3")
pygame.mixer.music.play(-1)
pygame.time.delay(500)
pygame.mixer.music.stop()
pygame.time.delay(100)
print("pos:", pygame.mixer.music.get_pos())
