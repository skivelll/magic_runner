import os
import pygame

from random import randint


def load_file(name, file_type='image'):
    fullname = os.path.join('data', name)
    if file_type == 'image':
        return pygame.image.load(fullname)
    elif file_type == 'other':
        return fullname
    elif file_type == 'txt':
        return fullname


def obstacles_stock(x):  # Функция для генерации препятствий
    if x <= 50:  # Огонь
        generate_place = randint(0, 5)
        if generate_place in (1, 2):
            obstacles.append(pygame.Rect(width, 0, 50, 200))
        elif generate_place == 3:
            obstacles.append(pygame.Rect(width, 400, 50, 200))
            obstacles.append(pygame.Rect(width, 0, 50, 200))
        else:
            obstacles.append(pygame.Rect(width, 400, 50, 200))
    elif x <= 90:  # Огненный шар
        obstacles.append(pygame.Rect(width, randint(100, 500),
                                     60, 46))
    else:  # Портал
        obstacles.append(pygame.Rect(width, 50, 75, 500))


def comparison(first, second):
    if first.width == second.width and first.height == second.height:
        return True
    return False


def point_in_rectangle(point, rectangle):
    x_point, y_point = point
    x1, y1, x2, y2 = rectangle
    return x1 <= x_point <= x2 and y1 <= y_point <= y2


if __name__ == '__main__':
    pygame.init()

    width, height = 800, 600
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Волшебный бегунок')
    clock = pygame.time.Clock()
    FPS = 60

    bg_img = load_file('background.png')

    place_y, speed_y, acceleration_y = 450, 0, 0
    player = pygame.Rect(200, place_y, 40, 55)
    menu_player = pygame.Rect(350, 300, 80, 110)
    player_img = [pygame.transform.scale(load_file('person_1.png'),
                                         (40, 55)),
                  pygame.transform.scale(load_file('person_2.png'),
                                         (40, 55)),
                  pygame.transform.scale(load_file('person_3.png'),
                                         (40, 55))]
    menu_player_img = [pygame.transform.scale(load_file('person_1.png'),
                                              (80, 110)),
                       pygame.transform.scale(load_file('person_2.png'),
                                              (80, 110)),
                       pygame.transform.scale(load_file('person_3.png'),
                                              (80, 110))]
    player_frame = 0

    game_running = True
    life = 0

    run_status = 'tutorial'

    # 1. tutorial
    # 2. menu
    # 3. wait
    # 4. go
    # 5. fail
    # 6. loose
    # 7. menu

    timer = 20

    scores = 0
    score_for_life = 0
    complexity = 1  # Сложность 1 - легкая 2 - средняя 3 - сложная
    space_or_esc = -1

    obstacles = []
    ground = [pygame.Rect(0, 600 - 25, 800, 25)]
    bg = [pygame.Rect(0, 0, 1600, 600)]

    fire_ball = pygame.Rect(width, randint(100, 500), 60, 46)
    portal = pygame.Rect(width, 50, 75, 500)

    fire_ball_img = pygame.transform.scale(load_file(
        'fire_ball.png'), (60, 46))
    portal_img = pygame.transform.scale(load_file('portal.png'), (75, 500))
    fire_img_bottom = pygame.transform.scale(load_file('fire.png'), (50, 200))
    fire_img_top = pygame.transform.rotate(fire_img_bottom, 180)
    ground_img = pygame.transform.scale(load_file('ground.png'), (800, 25))
    life_bar_img = pygame.transform.scale(load_file('clear_heart.png'),
                                          (146, 24))
    heart_img = pygame.transform.scale(load_file('heart.png'), (26, 24))
    complexity_pick_img = pygame.transform.scale(
        load_file('complexity_fire.png'), (64, 64))

    small_font = pygame.font.Font(load_file('pixel_font.ttf', 'other'), 20)
    big_font = pygame.font.Font(load_file('pixel_font.ttf', 'other'), 35)

    destroy_timer = 0
    tutorial_timer = 60
    menu_timer = 180
    walk = False

    tutorial_text = [big_font.render('Волшебный бегунок',
                                     False, pygame.Color('white')),
                     small_font.render('Для управления персонажем'
                                       ' используйте:', False,
                                       pygame.Color('white')),
                     small_font.render('Пробел или левую кнопку'
                                       ' мыши для прыжка', False,
                                       pygame.Color('white')),
                     small_font.render('Правую кнопку мыши или клавишу z для',
                                       False, pygame.Color('white')),
                     small_font.render('разрушения порталов', False,
                                       pygame.Color('white')),
                     small_font.render('За прохождение препятствий вам'
                                       ' начисляется',
                                       False, pygame.Color('white')),
                     small_font.render('определенное количество баллов:',
                                       False, pygame.Color('white')),
                     small_font.render('5 очков за проход огненного столба',
                                       False, pygame.Color('white')),
                     small_font.render('6 очков каждую секунду',
                                       False, pygame.Color('white')),
                     small_font.render('10 очков за проход огненного шара',
                                       False, pygame.Color('white')),
                     small_font.render('25 очков за разрушение портала',
                                       False, pygame.Color('white')),
                     small_font.render('У игрока есть 5 ячеек здоровья '
                                       'изначальное',
                                       False, pygame.Color('white')),
                     small_font.render('количество здоровья зависит от '
                                       'выбранного',
                                       False, pygame.Color('white')),
                     small_font.render('уровня сложности: 1, 3 или 5 сердец',
                                       False, pygame.Color('white')),
                     small_font.render('Каждые заработанные 500 баллов игрок',
                                       False, pygame.Color('white')),
                     small_font.render('получает одно сердце',
                                       False, pygame.Color('white')),
                     small_font.render('Нажмите пробел что бы перейти дальше',
                                       False, pygame.Color('white'))]
    tutorial_text[-1].set_alpha(127)
    menu_text = [big_font.render('Выбор сложности', False,
                                 pygame.Color('white')),
                 small_font.render('Легкая', False, pygame.Color('white')),
                 small_font.render('Нормальная', False, pygame.Color('white')),
                 small_font.render('Сложная', False, pygame.Color('white')),
                 small_font.render('Нажмите пробел что бы перейти дальше',
                                   False,
                                   pygame.Color('white')),
                 small_font.render('Нажмите ESC что бы выйти из игры', False,
                                   pygame.Color('white'))]
    menu_text[-1].set_alpha(127)
    menu_text[-2].set_alpha(127)

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        jump = mouse[0] or keys[pygame.K_SPACE]
        destroy = mouse[2] or keys[pygame.K_z]

        if timer > 0:
            timer -= 1

        for i in range(len(ground) - 1, -1, -1):
            ground_block = ground[i]
            ground_block.x -= 3

            if ground_block.right < 0:
                ground.remove(ground_block)

        if len(ground) == 0 or ground[-1].left < 0:
            ground.append(pygame.Rect(800, 600 - 25, 800, 25))

        if len(ground) > 2:
            ground.pop(-1)

        for i in range(len(bg) - 1, -1, -1):
            bg_frame = bg[i]
            bg_frame.x -= 1

            if bg_frame.right < 0:
                bg.remove(bg_frame)

        if len(bg) == 0 or bg[-1].left < 0:
            bg.append(pygame.Rect(1600, 0, 1600, 600))

        if len(bg) > 2:
            bg.pop(-1)

        for i in range(len(obstacles) - 1, -1, -1):
            obstacle = obstacles[i]
            if comparison(obstacle, fire_ball):
                obstacle.x -= 4
            else:
                obstacle.x -= 3
            if obstacle.right < 0:
                obstacles.remove(obstacle)

        if run_status == 'wait':  # Статус ставящий игру на паузу после
            # запуска/смерти
            if (jump or destroy) and timer == 0 and len(obstacles) == 0:
                run_status = 'go'
            place_y += (600 // 2 - place_y) * 0.1
            player.y = place_y

        elif run_status == 'go':  # Статус самой игры
            if jump:
                if walk:
                    speed_y = 4
                    walk = False
                else:
                    acceleration_y = -2
            else:
                acceleration_y = 0

            place_y += speed_y  # Вычисление физики падения
            speed_y = (speed_y + acceleration_y + 1) * 0.98
            player.y = place_y

            if destroy and destroy_timer == 0:  # Разрушение портала
                for i in range(len(obstacles)):
                    if comparison(obstacles[i], portal):
                        obstacles.pop(i)
                        destroy_timer = 60
                        scores += 25
                        score_for_life += 25
                        break

            if len(obstacles) == 0 or obstacles[-1].x < width - 200:
                obstacles_stock(randint(1, 100))  # Очистка ушедших препятствий

            for obstacle in obstacles:
                if player.colliderect(obstacle):  # Проверка на столкновение
                    run_status = 'fail'
                elif obstacle.x == player.x:  # Начисление баллов
                    if comparison(obstacle, fire_ball):  # за препятствия
                        scores += 10
                        score_for_life += 10
                    else:
                        scores += 5
                        score_for_life += 5

            if player.top < 0:  # Ограничение по потолку
                speed_y, place_y = 0, 0

            for ground_block in ground:  # Ограничение по земле
                if player.colliderect(ground_block):
                    speed_y, place_y = 0, 600 - 90
                    walk = True

            scores += 0.1
            score_for_life += 0.1

            if int(score_for_life) >= 500:  # Начисление жизней
                if life < 5:
                    life += 1
                    score_for_life -= 500

        elif run_status == 'fail':  # Статус отвечает за потерю жизни
            speed_y, place_y, = 0, height // 2
            life -= 1
            if life > 0:
                run_status = 'wait'
                timer = 60
            else:
                run_status = 'loose'
                timer = 180
        elif run_status == 'loose':  # Статус отвечает за проигрыш
            if timer > 0:
                timer -= 1
            if int(best_score[complexity - 1]) < int(scores):
                best_score[complexity - 1] = str(int(scores)) + '\n'
                with open(load_file('best_score.txt', 'txt'), 'w') as file:
                    for line in best_score:
                        file.write(line)  # Запись лучшего результата
            exit_to_menu = pygame.key.get_pressed()
            if exit_to_menu[pygame.K_SPACE] and timer == 0:
                run_status = 'menu'
                menu_timer = 180
            win.blit(bg_img, pygame.Rect(-400, 0, 1600, 600))
            win.blit(small_font.render(
                f'Ваш результат: {int(scores)}'.replace('\n', ''),
                False, pygame.Color('white')), (255, 50))
            if player_frame > 3:
                player_frame = 0
            win.blit(menu_player_img[int(player_frame)], menu_player)
            win.blit(menu_text[-2], (92, 570))
            player_frame += 0.1
            pygame.display.update()
            clock.tick(60)
            continue
        elif run_status == 'menu':  # Статус отвечающий за меню
            start = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            best_score = load_file('best_score.txt', 'txt')
            with open(best_score) as file:
                best_score = file.readlines()
            best_score_text = (f'Ваш лучший результат:'
                               f' {best_score[complexity - 1]}')
            if start[pygame.K_SPACE] and menu_timer == 0:
                if complexity == 1:
                    life = 5
                elif complexity == 2:
                    life = 3
                elif complexity == 3:
                    life = 1
                scores = 0
                run_status = 'wait'
            elif start[pygame.K_ESCAPE]:
                game_running = False
            if menu_timer > 0:
                menu_timer -= 1
            buttons = [(100, 90, 205, 115),
                       (295, 95, 470, 115), (565, 90, 690, 115)]
            if mouse[0]:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if point_in_rectangle(mouse_pos, button):
                        complexity = 1 + buttons.index(button)
            win.blit(bg_img, pygame.Rect(-400, 0, 1600, 600))
            if complexity == 1:
                win.blit(complexity_pick_img, pygame.Rect(30, 60, 64, 64))
            elif complexity == 2:
                win.blit(complexity_pick_img, pygame.Rect(230, 60, 64, 64))
            elif complexity == 3:
                win.blit(complexity_pick_img, pygame.Rect(500, 60, 64, 64))
            win.blit(small_font.render(best_score_text.replace('\n', ''),
                                       False, pygame.Color('white')),
                     (185, 50))
            win.blit(menu_text[0], (185, 10))
            win.blit(menu_text[1], (100, 90))
            win.blit(menu_text[2], (300, 90))
            win.blit(menu_text[3], (570, 90))
            if int(space_or_esc) == -2:
                win.blit(menu_text[int(space_or_esc)], (92, 570))
            elif int(space_or_esc) == -1:
                win.blit(menu_text[int(space_or_esc)], (130, 570))
            else:
                space_or_esc = -1
            space_or_esc -= 0.01
            if player_frame > 3:
                player_frame = 0
            win.blit(menu_player_img[int(player_frame)], menu_player)
            player_frame += 0.1
            pygame.display.update()
            clock.tick(60)
            continue
        elif run_status == 'tutorial':  # Статус отвечающий за заставку
            keyboard = pygame.key.get_pressed()
            if keyboard[pygame.K_SPACE] and tutorial_timer == 0:
                run_status = 'menu'
            if tutorial_timer > 0:
                tutorial_timer -= 1
            win.blit(bg_img, pygame.Rect(-400, 0, 1600, 600))
            win.blit(tutorial_text[0], (150, 10))
            y = 90
            for line in tutorial_text[1:5]:
                win.blit(line, (10, y))
                y += 25
            y += 30
            for line in tutorial_text[5: 11]:
                win.blit(line, (10, y))
                y += 25
            y += 30
            for line in tutorial_text[11:-1]:
                win.blit(line, (10, y))
                y += 25
            win.blit(tutorial_text[-1], (92, y + 45))
            pygame.display.update()
            clock.tick(60)
            continue

        for bg_frame in bg:
            win.blit(bg_img, bg_frame)

        for obstacle in obstacles:
            if comparison(obstacle, portal):
                rect = portal_img.get_rect()
                win.blit(portal_img, obstacle)
            elif comparison(obstacle, fire_ball):
                rect = fire_ball_img.get_rect()
                win.blit(fire_ball_img, obstacle)
            else:
                if obstacle.y != 0:
                    win.blit(fire_img_bottom, obstacle)
                else:
                    win.blit(fire_img_top, obstacle)

        if player_frame > 3:
            player_frame = 0

        if destroy_timer > 0:
            destroy_timer -= 1

        win.blit(player_img[int(player_frame)], player)

        for ground_block in ground:
            rect = ground_img.get_rect()
            pygame.draw.rect(win, pygame.Color('brown'), ground_block)
            win.blit(ground_img, ground_block)

        text = f'Очки:{int(scores)}'
        text_x = 690 - (len(text) - 6) * 15
        display_text = small_font.render(text, False, pygame.Color('white'))
        win.blit(display_text, (text_x, 10))
        win.blit(life_bar_img, (10, 10))
        for i in range(life):
            win.blit(heart_img, (10 + i * 30, 10))

        player_frame += 0.1
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
