import sys
import requests
import pygame
import os

# изменение масштаба карты
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

# вывод карты
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

def change_coords(type):
    global coords
    if type == "W":
        coords = [coords[0], coords[1] + (1 / 10)]
    elif type == "A":
        coords = [coords[0] - (1 / 10), coords[1]]
    elif type == "S":
        coords = [coords[0], coords[1] - (1 / 10)]
    elif type == "D":
        coords = [coords[0] + (1 / 10), coords[1]]

# изменение вида карты
def change_map():
    global type_map
    if type_map == "map":
        type_map = "sat"
    elif type_map == "sat":
        type_map = "skl"
    elif type_map == "skl":
        type_map = "map"
    show_map()


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
            if event.key == pygame.K_UP:  # Если нажимаем на стрелку вверх, то масштаб увеличивается
                change_spn(0)
            elif event.key == pygame.K_DOWN:  # Если нажимаем на стрелку вниз, то масштаб уменьшается
                change_spn(1)
            elif event.key == pygame.K_w: # Если нажимаем W сдвигается вверх
                change_coords("W")
                show_map()
            elif event.key == pygame.K_a: # Если нажимаем A сдвигается влево
                change_coords("A")
                show_map()
            elif event.key == pygame.K_s: # Если нажимаем S сдвигается вниз
                change_coords("S")
                show_map()
            elif event.key == pygame.K_d: # Если нажимаем D сдвигается вправо
                change_coords("D")
                show_map()
            elif event.key == pygame.K_m:  # Если нажимаем на M, то меняется тип карты
                change_map()
    pygame.display.flip()
pygame.quit()