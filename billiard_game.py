import pygame
import math

# Colours
BROWN = (130, 84, 65)   # cue
GREY = (245, 245, 245)   # cue
DARK_BROWN = (110, 74, 55)   # pool table border
green_r = 51
green_g = 163
green_b = 47
GREEN = (green_r, green_g, green_b)   # pool table surface
PINK = (255, 20, 147)     # pink balls
BLUE = (0, 191, 255)    # blue balls
BLACK = (0, 0, 0)       # background
white_r = 255
white_g = 255
white_b = 255
WHITE = (white_r, white_g, white_b)  # cue ball
# ball pulsing variable
ball_pulse_multiplier = -0.5
# in game message variables (the int represent the amount of time left -
# in milliseconds)
intro_message = 1200  # 240 fps, so it is 5 seconds
ball_in_hand_message = 0

# Game variables
game_in_progress = False
winner = "unknown"
win_screen = False  # determine whether to show the win screen or not

# variables used in determine_player_turn(),
# to find out which player is currently controlling the cue
current_player_turn = "Pink"
current_shot_count = 0
previous_shot_count = 0
ball_pocketed_in_this_shot = False
# ball in hand variables

cue_ball_in_hand = False
cue_ball_dragged = False
mouse_distance_travelled = 0

show_instructions = False  # a variable for the menu
mouse_held = False   # if the mouse is currently holding the cue
cue_buffer = 0
balls_in_movement = False  # balls are undergoing movement,
# means that the cue can't be moved at this time

# this class allows the ball class to be iterable,
# (which I use later in a few functions).


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

# Defining the ball class


class Ball():
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self):
        self._registry.append(self)
        self.id = 0
        self.color = ""
        self.x = 0
        self.y = 0
        self.direction = 0  # angle is represented in degrees
        self.speed = 0
        self.pocketed = False
        self.in_contact = False


def create_balls_list(color):
    """ input: color (string)
     output: list of 7 balls (class Ball) of that color"""
    balls = []
    for count in xrange(7):
        ball = Ball()
        ball.id = count
        ball.color = color
        balls.append(ball)

    return balls

# create an instance of each ball on the table
cue_ball = Ball()
cue_ball.color = "White"
eight_ball = Ball()  # third column, second row
eight_ball.color = "Black"
# player one's balls (pink)

pink_balls = create_balls_list("Pink")
blue_balls = create_balls_list("Blue")


def reset_ball_variables():
    # reset common variables for every ball
    for ball_instance in Ball:
        ball_instance.pocketed = False
        ball_instance.direction = 0
        ball_instance.speed = 0
        ball_instance.in_contact = False

    cue_ball.x = 330
    cue_ball.y = 300

    eight_ball.x = 745
    eight_ball.y = 300

    pink_balls[0].x = 705
    pink_balls[0].y = 300

    pink_balls[1].x = 725
    pink_balls[1].y = 288

    pink_balls[2].x = 745
    pink_balls[2].y = 323

    pink_balls[3].x = 766
    pink_balls[3].y = 266

    pink_balls[4].x = 766
    pink_balls[4].y = 314

    pink_balls[5].x = 787
    pink_balls[5].y = 278

    pink_balls[6].x = 787
    pink_balls[6].y = 324

    blue_balls[0].x = 725
    blue_balls[0].y = 312

    blue_balls[1].x = 745
    blue_balls[1].y = 277

    blue_balls[2].x = 766
    blue_balls[2].y = 290

    blue_balls[3].x = 766
    blue_balls[3].y = 336

    blue_balls[4].x = 787
    blue_balls[4].y = 256

    blue_balls[5].x = 787
    blue_balls[5].y = 300

    blue_balls[6].x = 787
    blue_balls[6].y = 347

reset_ball_variables()  # original ball position at the start of the game

# Drawing Functions


def draw_menu(game_in_progress, show_instructions):
    """ input: two variables, game_in_progress (bool) and
    show_instructions (bool).
    output: draws the chosen screen and returns the updated two variables
    (from the start) """
    # get mouse position and click status
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_left = get_mouse_press()  # bool ->
    # if the player pressed the left button of the mouse
    music = pygame.mixer.Sound("tap.wav")
    if not show_instructions:
        # if mouse is hovering over a button, then highlight that button
        if mouse_x > 430 and mouse_x < 560 and mouse_y > 400 and\
                        mouse_y < 450:  # start game
            pygame.mixer.Sound.play(music)
            myimage = pygame.image.load("Images/chose2.png")
            if mouse_left:
                game_in_progress = True
                # set mouse to proper starting position:
                pygame.mouse.set_pos([250, 300])
        elif mouse_x > 680 and mouse_x < 870 and\
                        mouse_y > 240 and mouse_y < 290:  # show instructions
            myimage = pygame.image.load("Images/chose3.png")
            pygame.mixer.Sound.play(music)
            if mouse_left:
                show_instructions = True
        elif mouse_x > 215 and mouse_x < 330 and mouse_y > 270 and\
                        mouse_y < 315:   # exit game
            myimage = pygame.image.load("Images/chose1.png")
            pygame.mixer.Sound.play(music)
            if mouse_left:
                pygame.quit()
        else:
            myimage = pygame.image.load("Images/main.png")
    else:  # show the instructions
        if mouse_x > 670 and mouse_x < 820 and mouse_y > 35 and\
                        mouse_y < 90:     # menu button
            myimage = pygame.image.load("Images/intro_selected.png")
            pygame.mixer.Sound.play(music)
            if mouse_left:   # back to main menu
                show_instructions = False
        else:
            myimage = pygame.image.load("Images/intro.png")
    # load and draw the menu
    imagerect = myimage.get_rect()
    screen.fill(BLACK)
    screen.blit(myimage, imagerect)
    pygame.display.flip()
    return game_in_progress, show_instructions


def draw_win_screen(win_screen, winner):
    """ input: winner ("Pink"/"Blue"/"unknown") and win_screen (bool)
    output: draws the winner screen according to the variable (winner), updates and returns the win_screen
    """
    music = pygame.mixer.Sound("winning.wav")
    image_selected = "Images/blue_selected.png"
    image = "Images/blue.png"
    if winner == "Blue":
        image_selected = "Images/blue_selected.png"
        image = "Images/blue.png"
    elif winner == "Pink":
        image_selected = "Images/pink_selected.png"
        image = "Images/pink.png"

    # get mouse position and click status
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_left = get_mouse_press()

    # if mouse is hovering over a button, then highlight that button
    if mouse_x > 470 and mouse_x < 550 and mouse_y > 400\
            and mouse_y < 600:
        myimage = pygame.image.load(image_selected)
        if mouse_left:
            pygame.mixer.Sound.stop(music)
            win_screen = False  # go to main menu

    else:
        myimage = pygame.image.load(image)

    imagerect = myimage.get_rect()
    screen.fill(BLACK)
    screen.blit(myimage, imagerect)
    pygame.mixer.Sound.play(music)
    pygame.display.flip()

    return win_screen


def draw_static_objects():
    """
     draws the billiard table
    """
    # Draw the playing surface
    # pygame.draw.rect(screen, color, (x,y,width,height), thickness)
    pygame.draw.rect(screen, GREEN, [80, 90, 850, 450], 0)
    # Draw the pool table border
    pygame.draw.rect(screen, DARK_BROWN, [80, 90, 850, 450], 20)
    # Draw the pockets
    # pygame.draw.circle(Surface, color, pos, radius, width=0)
    pygame.draw.circle(screen, BLACK, (90, 100), 15, 0)      # top left
    pygame.draw.circle(screen, BLACK, (505, 95), 14, 0)     # top middle
    pygame.draw.circle(screen, BLACK, (920, 100), 15, 0)     # top right
    pygame.draw.circle(screen, BLACK, (90, 530), 15, 0)     # bottom left
    pygame.draw.circle(screen, BLACK, (505, 535), 14, 0)    # bottom middle
    pygame.draw.circle(screen, BLACK, (920, 530), 15, 0)    # bottom right


def draw_scoreboard(current_player_turn):
    """
    input: the player that is playing now (current_player_turn)
    output: draws the scoreboard
    """
    num_of_pink_left = 0
    num_of_blue_left = 0
    # get the number of pink and blue balls
    for ball_instance in Ball:
        if not ball_instance.pocketed:
            if ball_instance.color == "Blue":
                num_of_blue_left += 1
            elif ball_instance.color == "Pink":
                num_of_pink_left += 1
    # draw the pink balls left
    for n in range(num_of_pink_left):
        pygame.draw.circle(screen, PINK, (275+n*20, 40), 7, 0)
    # draw the blue balls left
    for n in range(num_of_blue_left):
        pygame.draw.circle(screen, BLUE, (675+n*20, 40), 7, 0)
    # Draw an indicator, showing which player's turn it is
    draw_text("Current Player:", 440, 30, GREY, 20)
    if current_player_turn == "Pink":
        pygame.draw.circle(screen, PINK, (610, 40), 13, 0)
    elif current_player_turn == "Blue":
        pygame.draw.circle(screen, BLUE, (610, 40), 13, 0)


def draw_balls_list(balls_list):
    """
    input: list of balls (class Ball)
    output: draws the balls (that are not pocketed) on the table, except of
    the white (cue_ball) and black (eight_ball) ones.
    """
    for x in xrange(len(balls_list)):
        if not balls_list[x].pocketed:
            if balls_list[x].color == "Pink":
                pygame.draw.circle(screen, PINK,
                                   (int(balls_list[x].x),
                                    int(balls_list[x].y)), 11, 0)
            else:
                pygame.draw.circle(screen, BLUE,
                                   (int(balls_list[x].x),
                                    int(balls_list[x].y)), 11, 0)


def draw_balls():
    """
    draws all the balls (that are not pocketed) on the table, by using the
    " draw_balls_list " function
    """
    # draw the cue and eight balls
    if not cue_ball.pocketed:
        pygame.draw.circle(screen, WHITE, (int(cue_ball.x),
                                           int(cue_ball.y)), 11, 0)

    if not eight_ball.pocketed:
        pygame.draw.circle(screen, BLACK, (int(eight_ball.x),
                                           int(eight_ball.y)), 11, 0)

    # draw pink balls
    draw_balls_list(pink_balls)

    # draw blue balls
    draw_balls_list(blue_balls)


def draw_text(text, x, y, color, font_size):
    """
    input: text(string), x(int) and y(int)- on the screen, color(string) of
    the text and font_size(int)- the size of the text.
    output: draws the text on the screen.
    """
    font = pygame.font.Font("fonts/PTC55F.ttf", font_size)
    label = font.render(text, 1, color)  # render(text,antialias,color)
    screen.blit(label, (x, y))


def draw_intro_message(time_left):
    """
    input: variable time_left
    output: draws the intro message, using the " draw_text " function and
    return the updated time_left.
    """
    if time_left > 0:
        draw_text("Click and drag the cue to begin", 360, 450, WHITE,
                  20)
        time_left -= 1
    return time_left


def draw_ball_in_hand_message(time_left):
    """
    input: the variable time_left
    output: draws the "ball in hand " message, using the " draw_text "
    function and returns the updated time_left.
    """
    if time_left > 0:
        draw_text("Click and drag the cue ball to move it", 360, 450,
                  WHITE, 20)
        time_left -= 1
    return time_left


def pulse_cue_ball(white_r, white_g, white_b, ball_pulse_multiplier,
                   WHITE):
    """
    input: white_r(int), white_g(int), white_b(int),
    ball_pulse_multiplier(double), WHITE (tuple).
    output: if the ball is in hand, set the cue ball drawing to a
    fade in/out animation. returns the updated white_r, white_g, white_b,
    ball_pulse_multiplier, WHITE.
    """
        # if the ball is in hand -> make it flash
        # set the cue ball drawing to a fade in/out animation
        # at start-> ball_pulse_multiplier = -0.5
    if ball_in_hand:
        white_r += 4*ball_pulse_multiplier
        white_g += 2*ball_pulse_multiplier
        white_b += 3*ball_pulse_multiplier
        # determine whether the ball pulses towards or against green/white
        # 255 is the maximum rgb value
        if white_g < green_g or white_g > 254:
            ball_pulse_multiplier *= -1

    else:
        # when the ball is not at hand->
        # reset the ball color and keep it static
        white_r = 255
        white_g = 255
        white_b = 255

    # redefine the color of the cue ball
    WHITE = (white_r, white_g, white_b)

    return white_r, white_g, white_b, ball_pulse_multiplier, WHITE
# User input functions


def get_mouse_press():
    """
    returns if the left button of the mouse was pressed.
    """
    mouse_left = False
    mouse_middle = False
    mouse_right = False
    mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()
    return mouse_left

# Game functions


def angle_to_coordinates(angle, x, y):
    """
    input: angle, x and y.
    output: x, y according to the angle (using math).
    """
    # get the x value by using the cosine function
    x = 1 * math.cos(math.radians(angle))
    # get the y value by using the sine function
    y = 1 * math.sin(math.radians(angle))
    return x, y


def get_angle(object1_x, object1_y, object2_x, object2_y):
    """
    input: x, y of two points.
    output: returns the angle between these two points.
    """
    difference_of_x = object1_x - object2_x
    difference_of_y = object1_y - object2_y
    # the result of math.atan2 is in radians:
    radians = math.atan2(difference_of_y, difference_of_x)
    radians %= 2*math.pi
    angle = math.degrees(radians)  #radians to degrees
    return angle


# Get the distance between two points
def get_distance(point1_x, point1_y, point2_x, point2_y):
    """
    input: x and y of two objects.
    output: returns the distance between the objects.
    """
    distance = math.sqrt((point1_x - point2_x)**2 +
                         (point1_y - point2_y)**2)
    return distance


def convert_polar_coordinates_to_cartesian(x, y, angle, length):
    """
    input: x, y, angle and length.
    output: returns the updated x, y.
    """
    x += length * math.cos(math.radians(angle))
    y += length * math.sin(math.radians(angle))
    return x, y


def ball_to_cushion_collision(ball_direction, ball_speed, ball_x,
                              ball_y, ball_in_contact):
    """
    input: ball_direction(angle), ball_speed, ball_x, ball_y, ball_in_contact.
    output: check if the ball hit a cushion and return the
    updated ball_direction, ball_speed, ball_in_contact
    """
    ball_hit_cushion = False
    if not ball_in_contact:
        # hit the top cushion
        if ball_y < 113:
            ball_hit_cushion = True
            ball_direction = 360 - ball_direction

        # hit the bottom cushion
        if ball_y > 520:
            ball_hit_cushion = True
            ball_direction = 360 - ball_direction

        # hit the left cushion
        if ball_x < 100:
            ball_hit_cushion = True
            # ball is coming from the top:
            if ball_direction > 180 and ball_direction < 270:
                ball_direction = 540 - ball_direction
            # ball is coming from the bottom:
            elif ball_direction > 90 and ball_direction < 180:
                ball_direction = 180 - ball_direction
            elif ball_direction == 180:  # direct hit
                ball_direction = 0

        # hit the right cushion
        if ball_x > 910:
            ball_hit_cushion = True
            # ball is coming from the top:
            if ball_direction > 270 and ball_direction < 360:
                ball_direction = 540 - ball_direction
            # ball is coming from the bottom:
            elif ball_direction > 0 and ball_direction < 90:
                ball_direction = 180 - ball_direction
            elif ball_direction == 0:  # direct hit
                ball_direction = 180
    else:
        ball_in_contact = False
    return ball_direction, ball_speed, ball_in_contact


def ball_to_ball_collision(ball_direction, ball_speed, ball_x, ball_y):
    """
    input: ball_direction(angel), ball_speed, ball_x, ball_y.
    output: check if balls hit each other and returns the speed of the ball
    and its new direction.
    """
    for ball_instance in Ball:
        # make sure the ball is not comparing it's location, with it's self
        if ball_x != ball_instance.x and ball_y != ball_instance.y:
            if ball_x > ball_instance.x-20 and\
                            ball_x < ball_instance.x+20:  # check the x
                if ball_y > ball_instance.y-20 and\
                                ball_y < ball_instance.y+20:  # check the y
                    # now it is confirmed that they are in contact
                    # make sure it doesn't do the below twice ->
                    # for only one contact:
                    if not ball_instance.in_contact:
                        pygame.mixer.music.load("2ballshit.wav")
                        pygame.mixer.music.play(1)
                        ball_instance.direction =\
                            get_angle(ball_instance.x, ball_instance.y,
                                      ball_x, ball_y)
                        ball_instance.speed = ball_speed*0.97
                        ball_speed *= 0.90
                        ball_instance.in_contact = True
                else:  # passed one test but is ultimately not in contact
                    if ball_instance.in_contact:
                        ball_instance.in_contact = False
            else:  # not in contact
                if ball_instance.in_contact:
                        ball_instance.in_contact = False
    return ball_direction, ball_speed


def check_if_ball_pocketed(ball_x, ball_y):
    """
    input: x and y of a ball.
    output: checks and returns if the ball is pocketed or not.
    """
    ball_pocketed = False
    # check the top left pocket
    if ball_x > 70 and ball_x < 115 and ball_y > 85 and ball_y < 120:
        ball_pocketed = True
    # check the top middle pocket
    elif ball_x > 485 and ball_x < 525 and ball_y > 85 and ball_y < 115:
        ball_pocketed = True
    # check the top right pocket
    elif ball_x > 905 and ball_x < 935 and ball_y > 85 and ball_y < 120:
        ball_pocketed = True
    # check the bottom right pocket
    elif ball_x > 905 and ball_x < 935 and ball_y > 520 and ball_y < 545:
        ball_pocketed = True
    # check the bottom middle pocket
    elif ball_x > 485 and ball_x < 525 and ball_y > 520 and ball_y < 555:
        ball_pocketed = True
    # check the bottom left pocket
    elif ball_x > 70 and ball_x < 115 and ball_y > 510 and ball_y < 550:
        ball_pocketed = True

    if ball_pocketed:
        pygame.mixer.music.load("inpocket.wav")
        pygame.mixer.music.play(1)

    return ball_pocketed


def manage_ball_status(ball_direction, ball_x, ball_y, ball_speed,
                       ball_pocketed, ball_in_contact):
    """
    input: ball_direction, ball_x, ball_y, ball_speed, ball_pocketed,
    ball_in_contact.
    output: returns ball_direction, ball_x, ball_y, ball_speed, ball_pocketed,
    ball_in_contact after using the functions: ball_to_cushion_collision,
    ball_to_ball_collision, angle_to_coordinates and check_if_ball_pocketed.
    """
    # check for a ball to wall collision
    ball_direction, ball_speed, ball_in_contact =\
        ball_to_cushion_collision(ball_direction, ball_speed,
                                  ball_x, ball_y, ball_in_contact)
    # check for a ball to ball collision
    ball_direction, ball_speed =\
        ball_to_ball_collision(ball_direction, ball_speed, ball_x,
                               ball_y)

    # change the ball's cartesian value based on its direction and speed
    ball_x_increment, ball_y_increment =\
        angle_to_coordinates(ball_direction, ball_x, ball_y)

    ball_x += ball_x_increment*ball_speed/4
    ball_y += ball_y_increment*ball_speed/4
    # gradually reduce the ball's speed
    ball_speed -= 0.018

    # Check if it gets pocketed
    ball_pocketed = check_if_ball_pocketed(ball_x, ball_y)
    return ball_direction, ball_x, ball_y, ball_speed, ball_pocketed,\
           ball_in_contact


def check_if_balls_moving():
    """
    returns true if the balls are moving, and false if they are not.
    """
    no_movement_so_far = True
    for ball_instance in Ball:
        if ball_instance.speed <= 0.01 and no_movement_so_far:
            no_movement_so_far = True
        else:
            if not ball_instance.pocketed:
                no_movement_so_far = False

    if no_movement_so_far:
        return False
    else:
        return True


def ball_in_hand():
    """
    reset the cue ball variables and position (after it got into the pocket).
    """
    # reset cue ball variables
    cue_ball.pocketed = False
    cue_ball.x = 380
    cue_ball.y = 300
    cue_ball.speed = 0
    cue_ball.direction = 0
    # reset mouse position
    pygame.mouse.set_pos([275, 300])


def determine_guideline(cue_end_point_x, cue_end_point_y,
                        cue_front_x, cue_front_y, mouse_degs):
    """
    input: cue_end_point_x, cue_end_point_y, cue_front_x, cue_front_y,
    mouse_degs.
    output: calculates the guideline's length (until the cushions) and
    returns its end (x, y).
    """
    guideline_length = 0
    object_touched = False
    # limit to cushions
    while not object_touched:
        cue_end_point_x, cue_end_point_y =\
            convert_polar_coordinates_to_cartesian(cue_end_point_x,
                                                   cue_end_point_y,
                                                   mouse_degs,
                                                   guideline_length)
        if cue_end_point_x < 100 or cue_end_point_x > 910 or\
           cue_end_point_y < 113 or cue_end_point_y > 520:
            object_touched = True
        else:
            guideline_length += 1

    return cue_end_point_x, cue_end_point_y


def check_if_game_over(game_in_progress, current_player_turn):
    """
    input: game_in_progress(true/false), current_player_turn.
    output: checks if the user chose to quit the game or someone won and than
    returns true if the game ended (and false if it did'nt) and the winner
    ("Pink"/"Blue"/"unknown").
    """
    winner = "unknown"
    # check if escape key is pressed
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_in_progress = False

    # check if black ball is pocketed
    if eight_ball.pocketed:
        game_in_progress = False
        # if the game is actually over, run through the game end sequence
        # get the number of pink and blue balls
        num_of_pink_left = 0
        num_of_blue_left = 0
        for ball_instance in Ball:
            if not ball_instance.pocketed:
                if ball_instance.color == "Blue":
                    num_of_blue_left += 1
                elif ball_instance.color == "Pink":
                    num_of_pink_left += 1

        # find out who won if rest of the player's balls have been pocketed
        # if current_player_turn == "Blue":
        if num_of_blue_left == 0:
            winner = "Blue"
        elif num_of_pink_left == 0:
            winner = "Pink"
        # 8 ball accidentally got in pocket:
        elif num_of_pink_left != 0 and num_of_blue_left != 0:
            if current_player_turn == "Pink":
                winner = "Blue"
            else:
                winner = "Pink"

    return game_in_progress, winner


def determine_player_turn(current_player_turn, current_shot_count,
                          previous_shot_count,
                          ball_pocketed_in_this_shot):
    """
    input: current player turn, current shot count(int),
    previous_shot_count(int), ball_pocketed_in_this_shot(bool).
    output: change the current player turn if the player's ball is not
    pocketed or if the cue ball is pocketed. returns the updated current
    playet turn, current shot count(int)' previous_shot_count(int),
    ball_pocketed_in_this_shot(bool).
    """
    # at first:  current_shot_count=0 ,  previous_shot_count=0
    # confirm that another shot has been made
    if previous_shot_count < current_shot_count:
        previous_shot_count += 1
        if not ball_pocketed_in_this_shot or cue_ball.pocketed:
            # toggle player turn if a ball hasn't been pocketed in this turn
            if current_player_turn == "Pink":
                current_player_turn = "Blue"
            elif current_player_turn == "Blue":
                current_player_turn = "Pink"
        else:
            ball_pocketed_in_this_shot = False

    return current_player_turn, current_shot_count,\
        previous_shot_count, ball_pocketed_in_this_shot

pygame.init()
# Set the width and height of the screen [width, height]
size = (1140, 640)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Billiard by Or Asherov")
# Loop until the user clicks the close button.
done = False
# Manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Show the menu
    if not game_in_progress:
        if win_screen:
            win_screen = draw_win_screen(win_screen, winner)

        else:
            win_screen = False
            game_in_progress = False
            winner = "unknown"
            # at first, show_instructions = false
            game_in_progress, show_instructions =\
                draw_menu(game_in_progress, show_instructions)

        reset_ball_variables()

    elif game_in_progress:
        # Drawing the playing
        screen.fill(BLACK)  # background
        draw_static_objects()
        draw_scoreboard(current_player_turn)
        draw_balls()

        # draw in-game messages

        # at first, intro_message = 0
        intro_message = draw_intro_message(intro_message)
        # at first, ball_in_hand_message = 0
        ball_in_hand_message =\
            draw_ball_in_hand_message(ball_in_hand_message)

        # Get the mouse press values
        mouse_left = get_mouse_press()

        # keep updating cue position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Update the cue's position + check whether the cue has hit the ball
        if not balls_in_movement:
            # the first moment that the mouse is clicked
            # at first, mouse_held = false
            if mouse_left and not mouse_held:
                mouse_held = True
                orig_mouse_x = mouse_x
                orig_mouse_y = mouse_y

                # enable ball dragging if the ball is in hand ->
                # AND the mouse has clicked on the ball
                if orig_mouse_x < cue_ball.x + 10 and\
                                orig_mouse_x > cue_ball.x - 10:
                        if orig_mouse_y < cue_ball.y + 10 and \
                                        orig_mouse_y > cue_ball.y - 10:
                            cue_ball_dragged = True
            # the duration of time WHILE the mouse is being clicked/held
            elif mouse_left and mouse_held:
            # in the case that the ball is in hand
                if cue_ball_in_hand:
                    if cue_ball_dragged:
                            cue_ball.x = mouse_x
                            cue_ball.y = mouse_y
                else:
                    # The amount the cue will move will depend on:
                    # the distance between the current mouse position
                    # and the position it was at when clicked

                    mouse_distance_travelled = get_distance(orig_mouse_x,
                                                            orig_mouse_y,
                                                            mouse_x,
                                                            mouse_y)
                    if mouse_distance_travelled > 85:
                        # limit the distance that the cue can be pulled back
                        mouse_distance_travelled = 100

                    # now move the cue backwards along the same angle
                    cue_buffer = mouse_distance_travelled

                    # change the amount of power/ball speed it will transfer ->
                    # depends of the distance between the cue and the cue ball
                    cue_ball.speed = mouse_distance_travelled/7

            # mouse is released AFTER being clicked at first
            elif not mouse_left and mouse_held:
                # ensure that there are no false positive. ex ->
                # if the user clicks and releases the cue without dragging it

                if mouse_distance_travelled > 5:
                    # if the ball is in hand, "remove" in from that hand...
                    if cue_ball_in_hand:
                        cue_ball_in_hand = False
                        cue_ball_dragged = False
                        current_shot_count -= 1

                    current_shot_count += 1
                    cue_buffer = 0  # reset the cue buffer->
                    # (the amount the cue moved while the mouse was being held)
                    pygame.mixer.music.load("stick.wav")
                    pygame.mixer.music.play(1)
                    # set the cue ball variables
                    cue_ball.direction = mouse_degs
                    # set the balls_in_movement variable in motion
                    balls_in_movement = True
                    mouse_held = False

        # Balls are currently moving
        else:
            # update the all of the ball's variables
            for ball_instance in Ball:
                if ball_instance.speed > 0.01 and not ball_instance.pocketed:
                    # one function that does it all, for this ball
                    ball_instance.direction, ball_instance.x,\
                    ball_instance.y, ball_instance.speed,\
                    ball_instance.pocketed,\
                    ball_instance.in_contact =\
                        manage_ball_status(ball_instance.direction,
                                           ball_instance.x, ball_instance.y,
                                           ball_instance.speed,
                                           ball_instance.pocketed,
                                           ball_instance.in_contact)
                    # check and see if the player has pocketed the correct
                    # ball
                    # -> and use this later to determine whether the player
                    # -> play again in the next shot:
                    if ball_instance.pocketed and ball_instance.color ==\
                            current_player_turn:
                        # another shot if it was his ball that pocketed:
                        ball_pocketed_in_this_shot = True

            # if all balls have stopped moving, inform the if statement above
            balls_in_movement = check_if_balls_moving()

        # Updating the cue's position and drawing it
        # Ball is currently in the opponents hand...until the next shot is made
        if cue_ball.pocketed:
            cue_ball_in_hand = True
            # if the balls have stopped moving ->
            # reset ball variable (should be a one time thing):
            if not balls_in_movement:
                ball_in_hand()
                ball_in_hand_message += 1200  # show user how to drag the ball-
                # (for 5 seconds)

        # the player (currently in possession) is able to drag around the ball
        if cue_ball_in_hand:
            # pulse the cue ball, when the ball is in hand
            white_r, white_g, white_b, ball_pulse_multiplier, WHITE =\
                pulse_cue_ball(white_r, white_g, white_b,
                               ball_pulse_multiplier, WHITE)
        else:
            # reset the white color values
            WHITE = (255, 255, 255)  # cue ball

        # show the cue when the balls have stopped moving
        if not balls_in_movement:
            # switch player turn if necessary
            current_player_turn, current_shot_count,\
            previous_shot_count, ball_pocketed_in_this_shot =\
                determine_player_turn(current_player_turn,
                                      current_shot_count,
                                      previous_shot_count,
                                      ball_pocketed_in_this_shot)

            # Get the angle between the mouse and the cue ball
            mouse_degs = get_angle(cue_ball.x, cue_ball.y, mouse_x,
                                   mouse_y)

            cue_front_x = mouse_x
            cue_back_x = mouse_x
            cue_front_y = mouse_y
            cue_back_y = mouse_y

            # Get the length of the cue
            mouse_to_ball_length = get_distance(cue_ball.x, cue_ball.y,
                                                cue_front_x, cue_front_y)

            # limit the length of the cue
            cue_length = mouse_to_ball_length-200-cue_buffer
            ball_to_cue_distance = mouse_to_ball_length-20-cue_buffer

            # get two pairs of the cue's coordinates ->
            # from their polar coordinates ->
            # (mouse angle + distance from the cue ball)
            cue_front_x, cue_front_y = \
                convert_polar_coordinates_to_cartesian(cue_front_x,
                                                       cue_front_y,
                                                       mouse_degs,
                                                       cue_length)
            cue_back_x, cue_back_y =\
                convert_polar_coordinates_to_cartesian(cue_back_x,
                                                       cue_back_y,
                                                       mouse_degs,
                                                       ball_to_cue_distance)

            # draw the cue
            pygame.draw.line(screen, BROWN, (cue_front_x, cue_front_y),
                             (cue_back_x, cue_back_y), 5)
            # we know one end of the guideline (the cue ball), ->
            # now get the other end
            cue_end_point_x = cue_back_x
            cue_end_point_y = cue_back_y
            cue_end_point_x, cue_end_point_y = \
                determine_guideline(cue_end_point_x, cue_end_point_y,
                                    cue_front_x, cue_front_y, mouse_degs)
            # draw the guideline
            pygame.draw.line(screen, WHITE, (cue_ball.x, cue_ball.y),
                             (cue_end_point_x, cue_end_point_y), 1)

        # Game end and player turns
        # if the game seems to be done-> show winner-> then return to main menu
        game_in_progress, winner = check_if_game_over(game_in_progress,
                                                      current_player_turn)
        if not game_in_progress:
            win_screen = True

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()  # will update the contents of the entire display

    # Limit frames per second
    clock.tick(240)

# Close the window and quit.
pygame.quit()
