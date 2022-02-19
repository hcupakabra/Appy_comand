import sys
import requests
import pygame
import os


def change_spn(flag):
    global spn
    if flag == 1:
        if spn[0] < 64:
            spn[0], spn[1] = spn[0] * 2, spn[1] * 2
        show_map()
    elif flag == 0:
        if spn[0] > 0.00048828125:
            spn[0], spn[1] = spn[0] / 2, spn[1] / 2
        show_map()


def show_map():
    global pic
    maps_server = 'http://static-maps.yandex.ru/1.x/'
    map_params = {
        'll': str(coords[0]) + ',' + str(coords[1]),
        'spn': str(spn[0]) + ',' + str(spn[1]),
        'l': type_map}
    response = requests.get(maps_server, params=map_params)
    with open('map.png', 'wb') as f:
        f.write(response.content)
    pic = pygame.image.load('map.png')
    os.remove('map.png')


spn = [0.5, 0.5]
coords = [37.1, 57.1]
type_map = "map"

pygame.init()
show_map()
screen = pygame.display.set_mode((600, 450))
running = True
now = 0
while running:
    screen.blit(pic, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                change_spn(0)
            elif event.key == pygame.K_DOWN:
                change_spn(1)
    pygame.display.flip()
pygame.quit()