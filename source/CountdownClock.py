import pygame
import pygame.gfxdraw
from Image import IMG

pygame.init()
pygame.font.init()


# constant
GREY = (15, 15, 15)
GREY_2 = (20, 20, 20)
GREY_3 = (40, 40, 40)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH_CIRCLE = 13
SCREEN_HEIGHT = SCREEN_WIDTH = 300

# pos of box
x1_pause = 110; x2_pause = 139
y1_pause = 250; y2_pause = 279
x1_reset = 160; x2_reset = 189
y1_reset = 250; y2_reset = 279

x1_minute = 83; x2_minute = 136
y1_minute = 113; y2_minute = 148
x1_second = 163; x2_second = 216
y1_second = 113; y2_second = 148

x_circle = 149; y_circle = 130
r0 = 91
start_angle = -90
stop_angle = -90

# crete window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('CountdownClock')
pygame.display.set_icon(pygame.image.load('icon.png'))
pygame.time.set_timer(pygame.USEREVENT, 1000)

# variables
running = True
counting = False
pause = True
number_input = ""
type_input = None # 1: minute, 2: second
status = 2 # 1: Play, 2: Pause, 3: Reset
total_second = 0
second_run = 0
minute = 0
second = 0

# contruction
font = pygame.font.Font(r'data\Segoe_UI_Bold.ttf', 38)
font_ver = pygame.font.Font(r'data\Segoe_UI_Italic.ttf', 13)
bg = IMG(screen, r'data\bg.png', 0, 0)
pause_img = IMG(screen, r'data\pause.png', x1_pause, y1_pause)
play_img = IMG(screen, r'data\play.png', x1_pause, y1_pause)
reset_img = IMG(screen, r'data\reset.png', x1_reset, y1_reset)

# input number
def input_number(event):
    global number_input, type_input

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if type_input == 1:
                type_input = 2
            else:
                type_input = None
        elif event.key == pygame.K_BACKSPACE:
            number_input = number_input[:-1]
        elif 47 < event.key < 58 and int(number_input) <= 9:
            number_input += event.unicode
    
def render_number(display_surface, number, color, x, y):
    number_surf = font.render(str(number), True, color)
    display_surface.blit(number_surf, number_surf.get_rect(center = (x, y)))

def mouse_cursor(mouse_x_, mouse_y_):
    if x1_minute < mouse_x < x2_minute and y1_minute < mouse_y < y2_minute and counting == False:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif x1_second < mouse_x < x2_second and y1_second < mouse_y < y2_second and counting == False:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif x1_reset < mouse_x < x2_reset and y1_reset < mouse_y < y2_reset and (minute + second) != 0:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif x1_pause < mouse_x < x2_pause and y1_pause < mouse_y < y2_pause and (minute + second) != 0:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


# loop program
while running:
    bg.render()
    # screen.fill(GREY_3)
    # pygame.draw.circle(screen, BLACK, (149, 130), 105, 2)
    # pygame.draw.circle(screen, BLACK, (149, 130), 90, 2)
    reset_img.render()
    ver = font_ver.render('1.0', True, BLACK)
    screen.blit(ver, (4, 280))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if counting == False:
                    if x1_minute < mouse_x < x2_minute and y1_minute < mouse_y < y2_minute:
                        type_input = 1
                    elif x1_second < mouse_x < x2_second and y1_second < mouse_y < y2_second:
                        type_input = 2

                if (minute + second) != 0:
                    if x1_pause < mouse_x < x2_pause and y1_pause < mouse_y < y2_pause:
                            if pause == True:
                                status = 1
                            elif pause == False:
                                status = 2

                if x1_reset < mouse_x < x2_reset and y1_reset < mouse_y < y2_reset:
                    status = 3

        if type_input == 1:
            number_input = str(minute)
            input_number(event)
            if number_input:
                minute = int(number_input)
            else:
                minute = 0
        elif type_input == 2:
            number_input = str(second)
            input_number(event)
            if number_input:
                second = int(number_input)
            else:
                second = 0

        if status == 1:
            if event.type == pygame.USEREVENT:
                total_second -= 1
                second_run += 1



    if status == 1:
        if counting == False and pause == True:
            total_second = minute*60 + second
        counting = True
        pause = False
        type_input = None
    elif status == 2:
        pause = True
    elif status == 3:
        counting = False
        pause = True
        number_input = ""
        type_input = None
        status = 2
        total_second = 0
        second_run = 0
        minute = 0
        second = 0


    if counting:
        r0 = 91
        stop_angle = -90 + second_run*360//(total_second + second_run)
        for i in range(WIDTH_CIRCLE):
            pygame.gfxdraw.arc(screen, x_circle, y_circle, r0 + i, start_angle, stop_angle, GREY)

        minute = total_second // 60
        second = total_second % 60

    if total_second == 0 and counting:
        status = 3
    
    mouse_cursor(mouse_x, mouse_y)


    if pause:
        play_img.render()
    else:
        pause_img.render()

    symbol = font.render(':', True, BLACK)
    screen.blit(symbol, (142, 104))
    render_number(screen, minute, BLACK, 109, 131)
    render_number(screen, second, BLACK, 189, 131)
    if type_input == 1:
        render_number(screen, minute, GREY_2, 109, 131)
    elif type_input == 2:
        render_number(screen, second, GREY_2, 189, 131)

    pygame.display.update()

pygame.quit()