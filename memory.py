# implementation of card game - Memory
import simplegui
import random

#lists
scroll = range(8) * 2
exposed = [False] * 16
pos = [0, 0]
i = 0
index = 0
flip_one = 0
flip_two = 0
t = 0

# helper function to initialize globals
def new_game():
    global state, exposed, t
    random.shuffle(scroll)
    t = 0
    label.set_text("Turns = " + str(t))
    state = 0
    exposed = [False] * 16
    
     
# define event handlers
def mouseclick(position):
    # need only account width of 50 pixels
    global exposed, state, index, flip_one, flip_two, t
    index = position[0] // 50
    
    # need to prevent double mouseclick, do nothing
    if exposed[index]:
        return
    
    if state == 0:
        #pick one card when no cards up
        flip_one = index
        state = 1
        #flip 1 card here
        if exposed[flip_one] == False:
            exposed[flip_one] = True   
        else:
            exposed[flip_one] = True
    elif state == 1:
        #when one card up, go ticker
        flip_two = index
        state = 2
        #ticker, add strings
        t += 1
        label.set_text("Turns = " + str(t))
        #flip 2nd card here
        if exposed[flip_two] == False:
            exposed[flip_two] = True
        else:
            exposed[index] = True
    else:
        #compare cards here
        if scroll[flip_one] == scroll[flip_two]:
            exposed[flip_one] = True
            exposed[flip_two] = True
            state = 1
        else:
            exposed[flip_one] = False
            exposed[flip_two] = False
            state = 1
        #regardless, set next flip_one up
        flip_one = index
        if exposed[flip_one] == False:
            exposed[flip_one] = True   
        else:
            exposed[flip_one] = True


# cards are logically 50x100 pixels in size
# nobody told me that it was actually ok to "infinitely" loop drawing the cards...
# tile corners in order: upper left, upper right, lower right, lower left
def draw(canvas):
    global pos, exposed, i
    pos = [6, 75]
    tile1 = [pos[0] - 6, pos[1] - 75]
    tile2 = [pos[0] + 44, pos[1] - 75]
    tile3 = [pos[0] + 44, pos[1] + 25]
    tile4 = [pos[0] - 6, pos[1] + 25]
    
    for i in range(0, len(scroll)):
        if exposed[i]:
            canvas.draw_text(str(scroll[i]), [pos[0], pos[1]], 80, "Orange")
        else:
            canvas.draw_polygon([tile1, tile2, tile3, tile4], 4, "White", "Blue")
        pos[0] += 50
        tile1[0] += 50
        tile2[0] += 50
        tile3[0] += 50
        tile4[0] += 50

# create frame and add a button and labels
# don't add change t here
frame = simplegui.create_frame("Memory Flash Game", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()