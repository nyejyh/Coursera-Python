# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 800
HEIGHT = 600       
BALL_RADIUS = 30
PAD_WIDTH = 8
PAD_HEIGHT = 90
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new ball in middle of table
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [3, 0]

# initialize paddles: left, right
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]

# initialize scores
score1 = 0
score2 = 0

# if direction is RIGHT, the ball's velocity is upper right, else upper left
# i don't get why the description call for such high velocity, modified to my own
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    if direction == RIGHT:
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        ball_vel[0] = random.randrange(4, 8)
        ball_vel[1] = - random.randrange(4, 8)
    else:
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        ball_vel[0] = - random.randrange(4, 8)
        ball_vel[1] = - random.randrange(4, 8)

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(bool(random.randrange(0,2))) # call spawn ball and call randomize spawn ball

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "Green")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "Green")
    
    # collision codings in order: top & bottom walls, left paddle, right paddle, left wall, right wall
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - BALL_RADIUS)):
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH) and ball_pos[1] > paddle1_pos[1] - HALF_PAD_HEIGHT and ball_pos[1] < paddle1_pos[1] + HALF_PAD_HEIGHT:
        ball_vel[0] = - (1.1 * ball_vel[0])
    elif ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH) and ball_pos[1] > paddle2_pos[1] - HALF_PAD_HEIGHT and ball_pos[1] < paddle2_pos[1] + HALF_PAD_HEIGHT:
        ball_vel[0] = - (1.1 * ball_vel[0])
    elif ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        score2 += 1
        spawn_ball(RIGHT)
    elif ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
        score1 += 1
        spawn_ball(LEFT)
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    # don't mess with the velocity in locking them inside, just the position
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    
    if paddle1_pos[1] <= HALF_PAD_HEIGHT:
        paddle1_pos[1] = HALF_PAD_HEIGHT
    elif paddle1_pos[1] >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    if paddle2_pos[1] <= HALF_PAD_HEIGHT:
        paddle2_pos[1] = HALF_PAD_HEIGHT
    elif paddle2_pos[1] >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    
    # draw paddles: left, right.  polygon = upper left, upper right, lower right, lower left
    canvas.draw_polygon([(paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT), (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT), (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT), (paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT)], 1, "White", "Blue") 
    canvas.draw_polygon([(paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT), (paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT), (paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT), (paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT)], 1, "White", "Red")    
    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 4, HEIGHT / 16), 50, "Orange")
    canvas.draw_text(str(score2), (WIDTH * 3/4, HEIGHT / 16), 50, "Orange")
    
# left paddle, then right paddle
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= 10
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += 10
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= 10
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += 10
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 200)


# start frame
new_game()
frame.start()
