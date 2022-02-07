import os
import sys

import pygame


def load_level(filename):
    filename = "level/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('level', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')


def max_width(filename):
    filename = "level/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    return max_width, len(level_map)


max_w, max_h = max_width("level_1.txt")
tile_width = tile_height = 50
size = width, height = 50 * max_w, 50 * max_h


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
running = True

level_map = []


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        level_map.append([])
        for x in range(len(level[y])):
            level_map[y].append([])
            if level[y][x] == '.':
                level_map[y][x].append('.')
                Tile('empty', x, y)
            elif level[y][x] == '#':
                level_map[y][x].append("#")
                Tile('wall', x, y)
            elif level[y][x] == '@':
                level_map[y][x].append("@")
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


player, level_x, level_y = generate_level(load_level('level_1.txt'))
screen = pygame.display.set_mode(size)
vel_x = player.rect.x
vel_y = player.rect.y


def check_coord():
    global vel_y
    global vel_x
    mesto_y = vel_y // tile_height
    mesto_x = vel_x // tile_width
    x = player.rect.x
    y = player.rect.y
    if vel_x > 0 and vel_x < size[0] and vel_y > 0 and vel_y < size[1] and level_map[mesto_y][mesto_x][0] == '.':
        player.rect.x = vel_x
        player.rect.y = vel_y
    else:
        vel_x = player.rect.x
        vel_y = player.rect.y

    print(level_map)

    print(mesto_x)
    print(level_map[mesto_y][mesto_x])
    print(player.rect.y)


def start_screen():
    fon = pygame.sprite.Sprite()
    image = load_image("fon.jpg")
    image1 = pygame.transform.scale(image, (size[0], size[0]))
    fon.image = image1
    fon.rect = fon.image.get_rect()

    fon.rect.x = 0
    fon.rect.y = 0
    fon_spite = pygame.sprite.Group()
    fon_spite.add(fon)
    fon_spite.draw(screen)
    pygame.display.flip()

    pygame.time.delay(1000)


start_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                vel_y = vel_y - tile_width
            if event.key == pygame.K_DOWN:
                vel_y = vel_y + tile_width
            if event.key == pygame.K_LEFT:
                vel_x = vel_x - tile_width
            if event.key == pygame.K_RIGHT:
                vel_x = vel_x + tile_width
            check_coord()
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

    # исходное изображение поворачивается на значение переменной angle
    # и записывается в перменную rotated_image

pygame.quit()
