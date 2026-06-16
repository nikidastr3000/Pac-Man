import pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("../data/audio/ok-i-pull-up-shorted.mp3")
pygame.mixer.music.play()
pygame.time.delay(3000) # let it finish? Wait, mp3 is how long?
