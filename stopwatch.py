# "Stopwatch: The Game"

# import stuff here
import simplegui

# define global variables
t = 0
z = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
# t is now in tenth of seconds
def format(t):
    D = t % 10
    C = (t // 10) % 10
    B = (t % 600) // 100
    A = t / 600
    return str(A) + ":" + str(B) + str(C) + "." + str(D)
    
# define score
def score(z):
    x = z // 10
    y = z % 10
    return str(x) + "/" + str(y)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    timer.start()
    
def stop_button():
    global z
    if timer.is_running() == False:
        z += 0
    else:
        if (t % 10) == 0:
            z += 11
        else:
            z += 1
    timer.stop()

    
def reset_button():
    global t, z
    t = 0
    z = 0
    timer.stop()


# define event handler for timer with 0.1 sec interval
def timer_handler():
    global t
    t += 1

# define draw handler
# no need to convert to str here, t stays an int
def draw(counting):
    counting.draw_text(format(t), (80, 230), 100, "Orange")
    counting.draw_text(score(z), (320, 55), 50, "Red")
  
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 400, 400)


# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw)
frame.add_button ("Start Timer", start_button)
frame.add_button ("Stop Timer", stop_button)
frame.add_button ("Reset Timer & Score", reset_button)

# start frame
frame.start()
timer.stop()