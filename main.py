import pygame
import random

pygame.init()
"""
Документация
Сделано CLABA

Ну вообщем это обычный ранер в 2d, тут ничего удевительного нет, но зато есть красивые текстуры!

"""
# Основные переменные
display_width = 800
display_height = 600
FPS = 70

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Беги и прыгай')

# иконка
icon = pygame.image.load('venv/textures/icon.png')
pygame.display.set_icon(icon)
# Массив с текстурами препядствий
object_img = [pygame.image.load('venv/textures/object0.png'), pygame.image.load('venv/textures/object1.png'), pygame.image.load('venv/textures/object1.png')]
# Массив с размерами текстур препядствий
object_options = [69, 449, 37, 410, 40, 420]
# подгрузка остальных текстур
usr_texture = pygame.image.load('venv/textures/character.png')
land = pygame.image.load('venv/textures/land.png')
# подгрузка звуков

# Background музыка
pygame.mixer.music.load('venv/audio/background.mp3')
pygame.mixer.music.set_volume(0.05)

usr_width = 60
usr_height = 100
usr_x = display_width // 3
usr_y = display_height - usr_height - 100

object_width = 20
object_height = 70
object_x = display_width - 50
object_y = display_height - object_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0  # Очки
max_scores = 0  # макс число очков
max_above = 0  # это для момента когда два кактуса перепрыгиваются
above_object = False  # это для проверки перепрыгнут ли этот кактус

# конец основных переменных


class object:  # Отдельный класс для препядствий, что бы отдельно для каждого переменные не обьявлять

    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):  # а это у нас перемещение препядствий
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):  # ну а это, конечно же тоже расстановка препядский
        self.x = radius                              # но эта расстановка когда нужно переставлять
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


# основной игровой цикл
def run_game():
    global make_jump
    game = True
    object_arr = []
    create_object_arr(object_arr)

    pygame.mixer.music.play(-1)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True

        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        count_scores(object_arr)

        display.blit(land, (0, 0))
        print_text('Очки:' + str(scores), 660, 10)
        draw_array(object_arr)

        if check_collision(object_arr):
            pygame.mixer.music.stop()
            game = False

        display.blit(usr_texture, (usr_x, usr_y))

        pygame.display.update()
        clock.tick(FPS)
    return game_over()


def jump():  # анимация прыжка
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30:
        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_object_arr(array):  # Функция расстановки препядствий и случайный выбор текстуры
    choice = random.randrange(0, 3)
    img = object_img[choice]
    width = object_options[choice * 2]
    height = object_options[choice * 2 + 1]
    array.append(object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = object_img[choice]
    width = object_options[choice * 2]
    height = object_options[choice * 2 + 1]
    array.append(object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = object_img[choice]
    width = object_options[choice * 2]
    height = object_options[choice * 2 + 1]
    array.append(object(display_width + 600, height, width, img, 4))


def find_radius(array):  # Функция нахождения радиуса для постановки препядствия
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 350)
    return radius


def draw_array(array):  # провека расстановки препядствий
    for object in array:
        check = object.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = object_img[choice]
            width = object_options[choice * 2]
            height = object_options[choice * 2 + 1]

            object.return_self(radius, height, width, img)


def print_text(message, x, y, font_color=(0, 0, 0), font_type='venv/fonts/codename_coder.ttf', font_size=30):  # для печати текста
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():  # Пауза игры на клавишу esc

    pygame.mixer.music.pause()

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Пауза. Нажмите Enter чтобы продолжить', 160, 250)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.unpause()


def check_collision(barriers):  # проверка столкновения игрока с препядствием
    for barrier in barriers:
        if usr_y + usr_height >= barrier.y:
            if barrier.y == 449:   # маленькое препядствие
                if not make_jump:
                    if barrier.x <= usr_x + usr_width - 24 <= barrier.x + barrier.width:
                        return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 14 <= barrier.x + barrier.width:
                        return True
            else:
                if usr_y + usr_height - 18 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.width:
                        return True
        else:
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 18 <= barrier.x + barrier.width:
                    return True
                elif jump_counter == 10:
                    if usr_y + usr_height - 5 >= barrier.y:
                        if barrier.x <= usr_x + usr_width - 18 <= barrier.x + barrier.width:
                            return True
                elif jump_counter >= -1:
                    if usr_y + usr_height - 5 >= barrier.y:
                        if barrier.x <= usr_x + usr_width - 18 <= barrier.x + barrier.width:
                            return True
                    else:
                        if usr_y + usr_height + 5 >= barrier.y:
                            if barrier.x <= usr_x <= barrier.x + barrier.width:
                                return True
    return False


def count_scores(barriers):  # подсчет очков
    global scores, max_above
    above_object = 0

    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_height - 5 <= barrier.y:
                if barrier.x <= usr_x / 2 <= barrier.x + barrier.width:
                    above_object += 1
                elif barrier.x <= usr_x + usr_width / 2 <= barrier.x + barrier.width:
                    above_object += 1

        max_above = max(max_above, above_object)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0


def game_over():  # завершение игры
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Врезался, опущенный ;(', 320, 200)
        print_text('Нажми Enter что бы сыграть еще раз, Esc что бы выйти', 40, 250)
        print_text('Наибольшее колличество очков: ' + str(max_scores), 180, 550)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(60)


while run_game():  # ну это обновление при прогрыше
    scores = 0
    make_jump = False
    jump_counter = 30
    usr_y = display_height - usr_height - 100
pygame.quit()
quit()