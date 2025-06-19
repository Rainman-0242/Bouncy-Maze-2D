from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import pi, cos, sin
import time
import random

import math
import random

w_width, w_height = 800, 380
pause = False
over = 0
page = 2
re, g, b = random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)
life = 3
ff = False
score = 0
score_updated = False
game_over_shown = False

def drawLine(x1, y1, x2, y2, color_diff):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)
    x_increment = dx / steps
    y_increment = dy / steps
    x, y = x1, y1
    glPointSize(2)
    glBegin(GL_POINTS)
    if color_diff == 0:
        glColor3f(1, 1, 0)
    elif color_diff == 1:
        glColor3f(1, 1, 1)
    elif color_diff == 2:
        glColor3f(1, 0, 0)
    elif color_diff == 3:
        glColor3f(1, 0, 0)
    elif color_diff == 4:
        glColor3f(0.7, 0.4, 0.0)
    elif color_diff == 5:
        glColor3f(0.0, 0.502, 0.502)
    glVertex2f(x, y)
    for i in range(int(steps)):
        x += x_increment
        y += y_increment
        glVertex2f(round(x), round(y))
    glEnd()


def midPointCircle(x, y, rad, re, g, b):
    glPointSize(2)
    glColor3f(re, g, b)
    glBegin(GL_POINTS)
    x_p = 0
    y_p = rad
    d = 1 - rad

    while x_p <= y_p:

        glVertex2f(x_p + x, y_p + y)
        glVertex2f(-x_p + x, y_p + y)
        glVertex2f(x_p + x, -y_p + y)
        glVertex2f(-x_p + x, -y_p + y)
        glVertex2f(y_p + x, x_p + y)
        glVertex2f(-y_p + x, x_p + y)
        glVertex2f(y_p + x, -x_p + y)
        glVertex2f(-y_p + x, -x_p + y)

        forSE = 2 * (x_p - y_p) + 5
        forE = (2 * x_p) + 3

        if d >= 0:
            x_p += 1
            y_p -= 1
            d += forSE
        else:
            x_p += 1
            d += forE

    glEnd()

def drawCircle(xc, yc, r, color_diff):
    global re, g, b
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(re, g, b)  # Circle color
    for theta in range(0, 361):  # Iterate around the circle
        x = xc + r * math.cos(theta * math.pi / 180)
        y = yc + r * math.sin(theta * math.pi / 180)
        glVertex2f(x, y)  # Add a point at the calculated position
    glEnd()

def draw_text(x, y, text):
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def drawScore():
    global pause, over
    if over == 1:
        draw_text(-135, -33, "Game Over!! Restart to Play Again")
    if pause and not over:
        draw_text(-95, -33, "Arcade Bounce Ball!")
        draw_text(-85, -54, "Game is Paused!")


def drawRestart():
    re_x_left = -390
    re_y_left = 170
    re_s_right = -365
    re_y_right = 170
    re_x_top = -377.5
    re_y_top = 183
    re_x_bottom = -377.5
    re_y_bottom = 157
    drawLine(re_x_left, re_y_left, re_x_top, re_y_top, 5)
    drawLine(re_x_left, re_y_left, re_s_right, re_y_right, 5)
    drawLine(re_x_left, re_y_left, re_x_bottom, re_y_bottom, 5)


def drawStart():
    st_x_top = 10
    st_y_top = 183
    st_x_bottom = 10
    st_y_bottom = 157
    st_x_left = -8
    st_y_left = 170
    drawLine(st_x_top, st_y_top, st_x_bottom, st_y_bottom, 4)
    drawLine(st_x_bottom, st_y_bottom, st_x_left, st_y_left, 4)
    drawLine(st_x_top, st_y_top, st_x_left, st_y_left, 4)


def drawPause():
    ps_x_1_top = -5
    ps_y_1_top = 183
    ps_x_1_bottom = -5
    ps_y_1_bottom = 157
    ps_x_2_top = 5
    ps_y_2_top = 183
    ps_x_2_bottom = 5
    ps_y_2_bottom = 157
    drawLine(ps_x_1_top, ps_y_1_top, ps_x_1_bottom, ps_y_1_bottom, 4)
    drawLine(ps_x_2_top, ps_y_2_top, ps_x_2_bottom, ps_y_2_bottom, 4)


def drawClose():
    cl_x_1_t = 390
    cl_y_1_t = 183
    cl_x_1_b = 360
    cl_y_1_b = 157
    cl_x_2_t = 360
    cl_y_2_t = 183
    cl_x_2_b = 390
    cl_y_2_b = 157

    drawLine(cl_x_1_t, cl_y_1_t, cl_x_1_b, cl_y_1_b, 3)
    drawLine(cl_x_2_t, cl_y_2_t, cl_x_2_b, cl_y_2_b, 3)


ball_x = 380
ball_y = -9
ball_radius = 20


def drawBall():
    global over, pause, ball_x, ball_y, ball_radius, re, g, b, pause
    if (over == 0 or over == 2 or over == 4) and pause == False:
        drawCircle(ball_x, ball_y, ball_radius, 5)


phase = 1


def drawMaze():
    global phase
    drawLine(-395, -185, 395, -185, 0)  # bottom
    drawLine(-395, -9, -250, -9, 0)  # middle1
    drawLine(-130, -9, 245, -9, 0)  # middle 2
    if phase == 2:
        drawLine(-250, -9, -130, -9, 0)
    drawLine(245, -9, 330, -9, 2)  # gap
    drawLine(330, -9, 395, -9, 0)  # middle 3

    drawLine(-395, 147, 395, 147, 0)  # top
    drawLine(-395, 147, -395, -185, 0)  # left side
    drawLine(395, -9, 395, -185, 0)  # right side

    drawLine(-280, -185, -280, -100, 0)  # obstacle
    drawLine(-180, -185, -180, -100, 0)  # obstacle
    drawLine(-280, -100, -180, -100, 0)  # obstacle

    drawLine(-30, -185, -30, -100, 0)  # obstacle
    drawLine(65, -185, 65, -100, 0)  # obstacle
    drawLine(-30, -100, 65, -100, 0)  # obstacle

    drawLine(-70, -9, -70, 76, 0)  # obstacle
    drawLine(30, -9, 30, 76, 0)  # obstacle
    drawLine(-70, 76, 30, 76, 0)  # obstacle


def drawMaze_2():
    global phase
    drawLine(-395, -185, 395, -185, 0)  # bottom
    drawLine(-395, -9, 310, -9, 0)  # middle1

    # if phase==1:
    #     drawLine(310,-9,395,-9,0)
    if phase == 2:
        drawLine(295, -9, 395, -9, 0)

    drawLine(-395, 147, 395, 147, 0)  # top
    drawLine(-395, 147, -395, -9, 0)  # left side
    drawLine(395, 147, 395, -185, 0)  # right side

    drawLine(-280, -185, -280, -100, 0)  # obstacle
    drawLine(-180, -185, -180, -100, 0)  # obstacle
    drawLine(-280, -100, -180, -100, 0)  # obstacle

    drawLine(-30, -185, -30, -100, 0)  # obstacle
    drawLine(65, -185, 65, -100, 0)  # obstacle
    drawLine(-30, -100, 65, -100, 0)  # obstacle

    drawLine(-70, -9, -70, 76, 0)  # obstacle
    drawLine(30, -9, 30, 76, 0)  # obstacle
    drawLine(-70, 76, 30, 76, 0)  # obstacle


obstacle_left_wall_height = -100
obstacle_right_wall_height = -80
obstacle_left_wall_started = -280
obstacle_left_wall_ended = -180
obstacle_right_wall_started = -30
obstacle_right_wall_ended = 65
jump_state = 0  # To track jump state (0: on the ground, 1: first jump, 2: second jump)
jump_velocity = 0  # Initial velocity for jumping
gravity = 0.005  # Acceleration due to gravity (adjust as needed for smoother motion)

reverse = False
up = .5


def animate_ball():
    global ff, e1, e2, e3, e4, e5, e6, pause, life, phase, reverse, ball_x, ball_y, jump_state, over, jump_velocity, gravity, phase, obstacle_left_wall_height, obstacle_right_wall_height, obstacle_left_wall_started, obstacle_left_wall_ended, obstacle_right_wall_started, obstacle_right_wall_ended, page, re, g, b

    if page == 4 and phase == 1:
        if ball_x <= -380 and ball_y <= -9:
            page = 3
        if life == 0:
            pause = True
            print('Game Over')
            over = 1
        if ((ball_x - e5[0]) ** 2 + (ball_y - e5[1]) ** 2) ** .5 <= 30:
            life -= 1
            ball_x = 340

    if page == 4 and phase == 1:

        if ball_y - up < -163:
            ball_y = -163
        else:
            ball_y -= up
        if -50 <= ball_x <= -70 and t_collected2 == False:
            life -= 1
            ball_x = 360
            ball_y = -163
        if ball_y >= -29 and ball_x >= -110:
            ball_y = -29
        if ball_y >= -29 and ball_x <= -235:
            ball_y = -29

        if (jump_state > 0):  # If ball is jumping
            ball_y += jump_velocity  # Update ball position based on current velocity
            jump_velocity -= gravity  # Apply gravity to decrease velocity

            # Check if ball has landed on the ground or obstacle
            if ball_y <= -163:  # Check if ball has landed on the ground
                ball_y = -163  # Set ball to ground level
                jump_state = 0  # Reset jump state
                jump_velocity = 0  # Reset jump velocity
            elif (ball_y > obstacle_right_wall_height or ball_y > obstacle_left_wall_height) and (
                    obstacle_left_wall_started < ball_x < obstacle_left_wall_ended or obstacle_right_wall_started < ball_x < obstacle_right_wall_ended):
                if ball_y < obstacle_left_wall_height or ball_y < obstacle_right_wall_height:
                    ball_y = -50
                    jump_state = 0  # Reset jump state
                    jump_velocity = 0  # Reset jump velocity

    if page == 4 and phase == 2:

        if life == 0:
            pause = True
            print('Game Over')
            over = 1
        if ((ball_x - e6[0]) ** 2 + (ball_y - e6[1]) ** 2) ** 0.5 <= 30 or (
                (ball_x - e4[0]) ** 2 + (ball_y - e4[1]) ** 2) ** .5 <= 30:
            life -= 1
            ball_x = -380
            ball_y = -9
            phase = 2
            reverse = False

        if ((ball_x - 375) ** 2 + (ball_y - 110) ** 2) ** .5 <= 30:
            phase = 1
            ff = True
            jump_state = 0

        if -50 <= ball_x <= -70 and t_collected2 == False:
            print("treasure hehe")
            life -= 1
            ball_x = -235
            ball_y = -9

        if ball_y <= 9:
            ball_y = 9  # Ensure ball stays on the ground
        else:
            ball_y -= up

        if jump_state > 0:  # If ball is jumping
            ball_y += jump_velocity  # Update ball position based on current velocity
            jump_velocity -= gravity  # Apply gravity to decrease velocity

            # Check if ball has landed on the ground
            if ball_y < 9:  # Check if ball has landed on the ground
                ball_y = 9  # Set ball to ground level
                jump_state = 0  # Reset jump state
                jump_velocity = 0  # Reset jump velocity

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    if page == 2 and phase == 1:
        if life == 0:
            pause = True
            print('Game Over')
            over = 1
        if ((ball_x - e1[0]) ** 2 + (ball_y - e1[1]) ** 2) ** .5 <= 30 or (
                (ball_x - e2[0]) ** 2 + (ball_y - e2[1]) ** 2) ** .5 <= 30:
            life -= 1
            ball_x = 340

    if page == 2 and phase == 1:
        if (ball_x >= 75 or ball_x <= -40) and reverse == False:
            if ball_y - up < -163:
                ball_y = -163
            else:
                ball_y -= up
        if ball_y >= 120:
            phase = 2
        if reverse == True:
            if ball_y >= 125:
                ball_y = 125
            else:
                ball_y += up
        if ball_x <= -350 and ball_y == -163:
            reverse = True
        if ball_y >= -29 and ball_x >= -110:
            ball_y = -29
        if ball_y >= -29 and ball_x <= -235:
            ball_y = -29
        if (jump_state > 0 and reverse == False):  # If ball is jumping
            ball_y += jump_velocity  # Update ball position based on current velocity
            jump_velocity -= gravity  # Apply gravity to decrease velocity

            # Check if ball has landed on the ground or obstacle
            if ball_y <= -163:  # Check if ball has landed on the ground
                ball_y = -163  # Set ball to ground level
                jump_state = 0  # Reset jump state
                jump_velocity = 0  # Reset jump velocity
            elif (ball_y > obstacle_right_wall_height or ball_y > obstacle_left_wall_height) and (
                    obstacle_left_wall_started < ball_x < obstacle_left_wall_ended or obstacle_right_wall_started < ball_x < obstacle_right_wall_ended):
                if ball_y < obstacle_left_wall_height or ball_y < obstacle_right_wall_height:
                    ball_y = -50
                    jump_state = 0  # Reset jump state
                    jump_velocity = 0  # Reset jump velocity

    if page == 2 and phase == 2:
        if 375 <= ball_x <= 395:
            if -9 <= ball_y <= 147:
                page = 4
                ball_x = -370

        if life == 0:
            pause = True
            print('Game Over')
            over = 1
        if ((ball_x - e3[0]) ** 2 + (ball_y - e3[1]) ** 2) ** 0.5 <= 30:
            life -= 1
            ball_x = -220
            ball_y = -9
            phase = 2
            reverse = False
        if 245 <= ball_x <= 330 and ball_y <= 9:
            print('Game Over')
            over = 1
            pause = True

        if 170 <= ball_x <= 190 and t_collected == False:
            life -= 1
            ball_x = -235
            ball_y = -9

        if ball_y <= 9:
            ball_y = 9  # Ensure ball stays on the ground
        else:
            ball_y -= up

        if jump_state > 0:  # If ball is jumping
            ball_y += jump_velocity  # Update ball position based on current velocity
            jump_velocity -= gravity  # Apply gravity to decrease velocity

            # Check if ball has landed on the ground
            if ball_y < 9:  # Check if ball has landed on the ground
                ball_y = 9  # Set ball to ground level
                jump_state = 0  # Reset jump state
                jump_velocity = 0  # Reset jump velocity

    glutPostRedisplay()


jump_checker = False


def checkObstacleCollision(new_x, new_y):
    global ball_x, ball_y, page, jump_checker, phase
    obstacle_left_wall_started = -280
    obstacle_left_wall_ended = -180
    obstacle_right_wall_started = -30
    obstacle_right_wall_ended = 65
    obstacle_up_wall_started = -70
    obstacle_up_wall_ended = 30

    obstacle_left_wall_height = -80
    obstacle_right_wall_height = -80

    if phase == 1:
        # Check if the new position collides with any obstacle
        if (obstacle_left_wall_started <= new_x <= obstacle_left_wall_ended) or (
                obstacle_right_wall_started <= new_x <= obstacle_right_wall_ended):
            # Check if ball collides with obstacle's block height
            if new_y > -100:
                # Ball is above the highest obstacle height, adjust to the top
                ball_y = -80
                jump_checker = True
                return False
            elif new_y < -100:
                # Ball is below the lowest obstacle height, adjust if needed (optional)
                return True  # Collision detected
        else:
            jump_checker = False
            return False  # No collision

    else:
        if (obstacle_up_wall_started <= new_x <= obstacle_up_wall_ended):
            # Check if ball collides with obstacle's block height
            if new_y > 76:
                # Ball is above the highest obstacle height, adjust to the top
                ball_y = 96
                jump_checker = True
                return False
            elif new_y < 76:
                # Ball is below the lowest obstacle height, adjust if needed (optional)
                return True  # Collision detected
        else:
            jump_checker = False
            return False  # No collisionss


# Define variables
laser_y_start_1 = -9
laser_y_start_2 = 47
laser_y_start_3 = 104

laser_y_start_4 = -9
laser_y_start_5 = -68
laser_y_start_6 = -116

laser_y_end = 141
laser_y_end2 = -185

t_collected = False
t_collected2 = False
pause_duration = 7  # Duration to pause the laser after treasure collection (in seconds)
pause_start_time = 0  # Variable to store the start time of the pause


"""def laser():
    global laser_y_end, laser_y_start_1, laser_y_start_2, laser_y_start_3, t_collected, t_collected2, pause_start_time, page, laser_y_start_4, laser_y_start_5, laser_y_start_6

    if page == 2:
        if not t_collected and not pause:
            # Update the laser's position for animation
            laser_y_start_1 += 0.5  # Move the first laser line upward
            laser_y_start_2 += 0.5  # Move the second laser line upward
            laser_y_start_3 += 0.5  # Move the third laser line upward

            # Draw the three laser lines with their updated positions
            drawLine(180, int(laser_y_start_1), 180, int(laser_y_start_1) + 6, 2)  # First laser line
            drawLine(180, int(laser_y_start_2), 180, int(laser_y_start_2) + 6, 2)  # Second laser line
            drawLine(180, int(laser_y_start_3), 180, int(laser_y_start_3) + 6, 2)  # Third laser line

            # Check if any laser line has reached its bottom position
            if laser_y_start_1 >= laser_y_end or laser_y_start_2 >= laser_y_end or laser_y_start_3 >= laser_y_end:
                # Reset the positions of all three laser lines to the top
                laser_y_start_1 = -9
                laser_y_start_2 = 47
                laser_y_start_3 = 104

        elif time.time() - pause_start_time >= pause_duration:
            # Reset the treasure collection flag
            t_collected = False
            # Reset the pause start time
            pause_start_time = 0
    # drawLine(245, -9, 330, -9, 0)  # gap
    # drawLine(330, -9, 350, -9, 0)  # middle 3

    elif page == 4:
        if not t_collected2 and not pause:
            # Update the laser's position for animation
            laser_y_start_4 -= 0.5  # Move the first laser line upward
            laser_y_start_5 -= 0.5  # Move the second laser line upward
            laser_y_start_6 -= 0.5  # Move the third laser line upward
            # drawLine(245, -9, 330, -9, 0)  # gap
            # drawLine(330, -9, 350, -9, 0)  # middle 3
            # Draw the three laser lines with their updated positions
            drawLine(-60, int(laser_y_start_4), -60, int(laser_y_start_4) - 6, 2)  # First laser line
            drawLine(-60, int(laser_y_start_5), -60, int(laser_y_start_5) - 6, 2)  # Second laser line
            drawLine(-60, int(laser_y_start_6), -60, int(laser_y_start_6) - 6, 2)  # Third laser line

            # Check if any laser line has reached its bottom position
            if laser_y_start_4 <= laser_y_end2 or laser_y_start_5 <= laser_y_end2 or laser_y_start_6 <= laser_y_end2:
                # Reset the positions of all three laser lines to the top
                laser_y_start_4 = -9
                laser_y_start_5 = -68
                laser_y_start_6 = -116

        elif time.time() - pause_start_time >= pause_duration:
            # Reset the treasure collection flag
            t_collected2 = False
            # Reset the pause start time
            pause_start_time = 0
"""
"""def laser():
    global laser_y_start_1, laser_y_start_2, laser_y_start_3, laser_y_start_4, laser_y_start_5, laser_y_start_6
    global laser_y_end, laser_y_end2, t_collected, t_collected2, pause_start_time, pause_duration, score, ball_x, score_updated

    if page == 2:
        if not t_collected and not pause:
            laser_y_start_1 += 0.5
            laser_y_start_2 += 0.5
            laser_y_start_3 += 0.5

            drawLine(180, int(laser_y_start_1), 180, int(laser_y_start_1) + 20, 2)
            drawLine(180, int(laser_y_start_2), 180, int(laser_y_start_2) + 20, 2)
            drawLine(180, int(laser_y_start_3), 180, int(laser_y_start_3) + 20, 2)

            if laser_y_start_1 >= laser_y_end:
                laser_y_start_1 = -9
                laser_y_start_2 = 47
                laser_y_start_3 = 104
                if ball_x > 180:  # Check if ball crosses laser
                    score += 5
                    score_updated = True  # Set flag for score update

    elif page == 4:
        if not t_collected2 and not pause:
            laser_y_start_4 -= 0.5
            laser_y_start_5 -= 0.5
            laser_y_start_6 -= 0.5

            drawLine(-60, int(laser_y_start_4), -60, int(laser_y_start_4) - 20, 2)
            drawLine(-60, int(laser_y_start_5), -60, int(laser_y_start_5) - 20, 2)
            drawLine(-60, int(laser_y_start_6), -60, int(laser_y_start_6) - 20, 2)

            if laser_y_start_4 <= laser_y_end2:
                laser_y_start_4 = -9
                laser_y_start_5 = -68
                laser_y_start_6 = -116
                if ball_x < -60:  # Check if ball crosses laser
                    score += 5
                    score_updated = True  # Set flag for score update
"""
def laser():
    global laser_y_start_1, laser_y_start_2, laser_y_start_3, laser_y_start_4, laser_y_start_5, laser_y_start_6
    global laser_y_end, laser_y_end2, t_collected, t_collected2, pause_start_time, pause_duration, score, ball_x, score_updated

    maze_top = 147   # Top boundary of the maze
    maze_bottom = -9  # Bottom boundary of the maze

    if page == 2:
        if not t_collected and not pause:
            laser_y_start_1 += 0.5
            laser_y_start_2 += 0.5
            laser_y_start_3 += 0.5

            # Ensure laser stays within the maze boundaries
            if laser_y_start_1 > maze_top:
                laser_y_start_1 = maze_bottom
            if laser_y_start_2 > maze_top:
                laser_y_start_2 = maze_bottom
            if laser_y_start_3 > maze_top:
                laser_y_start_3 = maze_bottom

            # Draw laser lines within the maze
            drawLine(180, int(laser_y_start_1), 180, min(int(laser_y_start_1) + 20, maze_top), 2)
            drawLine(180, int(laser_y_start_2), 180, min(int(laser_y_start_2) + 20, maze_top), 2)
            drawLine(180, int(laser_y_start_3), 180, min(int(laser_y_start_3) + 20, maze_top), 2)

            # Add score when ball crosses the laser
            if laser_y_start_1 == maze_bottom:
                if ball_x > 180:  # Check if the ball crosses the laser
                    score += 5
                    score_updated = True  # Set flag for score update

    elif page == 4:
        if not t_collected2 and not pause:
            laser_y_start_4 -= 0.5
            laser_y_start_5 -= 0.5
            laser_y_start_6 -= 0.5

            # Ensure laser stays within the maze boundaries
            if laser_y_start_4 < maze_bottom:
                laser_y_start_4 = maze_top
            if laser_y_start_5 < maze_bottom:
                laser_y_start_5 = maze_top
            if laser_y_start_6 < maze_bottom:
                laser_y_start_6 = maze_top

            # Draw laser lines within the maze
            drawLine(-60, int(laser_y_start_4), -60, max(int(laser_y_start_4) - 20, maze_bottom), 2)
            drawLine(-60, int(laser_y_start_5), -60, max(int(laser_y_start_5) - 20, maze_bottom), 2)
            drawLine(-60, int(laser_y_start_6), -60, max(int(laser_y_start_6) - 20, maze_bottom), 2)

            # Add score when ball crosses the laser
            if laser_y_start_4 == maze_top:
                if ball_x < -60:  # Check if the ball crosses the laser
                    score += 5
                    score_updated = True  # Set flag for score update



def drawScore():
    global over
    if over == 1:
        print("Game Over!! Restart to Play Again")
    if pause and not over:
        print(f"Score: {score}")




def drawTreasure():
    global t_collected, t_collected2
    if page == 2 and not t_collected:
        drawCircle(-375, 5, 8, 3)
    elif page == 4 and not t_collected2:
        drawCircle(375, -164, 8, 3)
def treasureCollected():
    global ball_x, ball_y, ball_radius, t_collected, t_collected2, pause_start_time

    if page == 2 and not t_collected:
        d = math.sqrt((-375 - ball_x) ** 2 + (5 - ball_y) ** 2)
        if d < ball_radius + 8:  # Collision with treasure
            t_collected = True
            pause_start_time = time.time()
            print("Treasure collected!")

    elif page == 4 and not t_collected2:
        d = math.sqrt((375 - ball_x) ** 2 + (-164 - ball_y) ** 2)
        if d < ball_radius + 8:  # Collision with treasure
            t_collected2 = True
            pause_start_time = time.time()
            print("Treasure collected!")






def animate():
    animate_ball()
    animate_2()


# drawLine(245, -9, 330, -9, 0)  # gap
# drawLine(330, -9, 350, -9, 0)  # middle 3
def convert_coordinate(x, y, width, height):
    con_x = x - width / 2
    con_y = height / 2 - y
    return con_x, con_y


click = 0



def mouseListener(button, state, x, y):
    global pause, click, over, page, re, g, b, life
    if page == 2:
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                click += 1
                c_x, c_y = convert_coordinate(x, y, w_width, w_height)
                print(c_x, c_y)
                if -8 <= c_x <= 10 and 157 <= c_y <= 183:
                    if not pause:
                        pause = True
                        over = 0
                        print("Game paused")
                    else:
                        pause = False
                        print("Game started")
                elif 360 <= c_x <= 390 and 157 <= c_y <= 183:
                    glutLeaveMainLoop()
                    print("Game exited")
                elif -390 <= c_x <= -365 and 157 <= c_y <= 183:
                    pause = False
                    over = 0
                    life = 3
                    print("Game restarted")

    if page == 3:
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                click += 1
                c_x, c_y = convert_coordinate(x, y, w_width, w_height)
                if -53 <= c_x <= -20 and -25 <= c_y <= -15:
                    life = 3
                elif -45 <= c_x <= -15 and -50 <= c_y <= -40:
                    glutLeaveMainLoop()
                    print("Game exited")

    if page == 4:
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                click += 1
                c_x, c_y = convert_coordinate(x, y, w_width, w_height)
                print(c_x, c_y)
                if -8 <= c_x <= 10 and 157 <= c_y <= 183:
                    if not pause:
                        pause = True
                        over = 0
                        print("Game paused")
                    else:
                        pause = False
                        print("Game started")
                elif 360 <= c_x <= 390 and 157 <= c_y <= 183:
                    glutLeaveMainLoop()
                    print("Game exited")
                elif -390 <= c_x <= -365 and 157 <= c_y <= 183:
                    pause = False
                    over = 0
                    life = 3
                    print("Game restarted")

    glutPostRedisplay()






jump_state = 0  # To track jump state (0: on the ground, 1: first jump, 2: second jump)


def keyboardListener(key, x, y):
    global pause, ball_x, ball_y, jump_state, over, jump_velocity, page, jump_checker
    if page == 2:
        if not pause:
            if key == b'a':
                if ball_x > -375:
                    # Check if moving left will collide with an obstacle
                    if not checkObstacleCollision(ball_x - 23, ball_y):
                        ball_x -= 7

            elif key == b'd':
                if ball_x < 375:
                    # Check if moving right will collide with an obstacle
                    if not checkObstacleCollision(ball_x + 23, ball_y):
                        ball_x += 7

            elif key == b' ':
                if jump_state == 0:  # On the ground, start first jump
                    ball_y += 30  # Adjust this value for the first jump height
                    jump_state = 1
                    jump_velocity = 0.8
                elif jump_state == 1 and jump_checker == False:  # First jump, start second jump
                    ball_y += 30  # Adjust this value for the second jump height
                    jump_state = 2
                    jump_velocity = 0.8
    if page == 4:
        if not pause:
            if key == b'a':
                if ball_x > -375:
                    # Check if moving left will collide with an obstacle
                    if not checkObstacleCollision(ball_x - 23, ball_y):
                        ball_x -= 7

            elif key == b'd':
                if ball_x < 375:
                    # Check if moving right will collide with an obstacle
                    if not checkObstacleCollision(ball_x + 23, ball_y):
                        ball_x += 7

            elif key == b' ':
                if jump_state == 0:  # On the ground, start first jump
                    ball_y += 30  # Adjust this value for the first jump height
                    jump_state = 1
                    jump_velocity = 0.8
                elif jump_state == 1 and jump_checker == False:  # First jump, start second jump
                    ball_y += 30  # Adjust this value for the second jump height
                    jump_state = 2
                    jump_velocity = 0.8

    glutPostRedisplay()


def enemy(x, y):
    global pause
    if not pause:
        x1 = x - 5
        x2 = x + 5
        y1 = y + 20
        y2 = y
        drawLine(x1, y1, x2, y2, 0)
        drawLine(x2, y1, x1, y, 0)
        midPointCircle(x, y + 30, 10, 1, 0, 0)


def lives(x, y):
    global pause
    if not pause:
        drawLine(x, y + 35, x - 10, y + 30, 0)
        drawLine(x - 10, y + 30, x - 15, y + 15, 0)
        drawLine(x - 15, y + 15, x, y, 0)
        drawLine(x, y + 35, x + 10, y + 30, 0)
        drawLine(x + 10, y + 30, x + 15, y + 15, 0)
        drawLine(x + 15, y + 15, x, y, 0)


e1 = [205, -180]
e2 = [-160, -180]
e3 = [-315, -9]

e4 = [-313, -9]
e5 = [-80, -180]
e6 = [205, -9]

m = True
m2 = True
m3 = True

m4 = True
m5 = True
m6 = True





def animate_2():
    global m4, m5, m6, e4, e5, e6, ball_x, ball_y, jump_state, jump_velocity, gravity, obstacle_left_wall_height, obstacle_right_wall_height, obstacle_left_wall_started, obstacle_left_wall_ended, obstacle_right_wall_started, obstacle_right_wall_ended, page, r, g, b, e1, m, e2, m2, e3, m3
    if page == 2:

        if e1[0] <= 280 and m == True:
            e1[0] += .5
        else:
            m = False
        if m == False and e1[0] >= 180:
            e1[0] -= .5
        else:
            m = True

        if e2[0] <= -110 and m2 == True:
            e2[0] += .5
        else:
            m2 = False
        if m2 == False and e2[0] >= -160:
            e2[0] -= .5
        else:
            m2 = True

        if e3[0] <= -262 and m3 == True:
            e3[0] += .5
        else:
            m3 = False
        if m3 == False and e3[0] >= -315:
            e3[0] -= .5
        else:
            m3 = True
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------

    if page == 4:

        if e6[0] <= 280 and m6 == True:
            e6[0] += .5
        else:
            m6 = False
        if m6 == False and e6[0] >= 180:
            e6[0] -= .5
        else:
            m6 = True

        if e5[0] <= -75 and m5 == True:
            e5[0] += .5
        else:
            m5 = False
        if m5 == False and e5[0] >= -165:
            e5[0] -= .5
        else:
            m5 = True

        if e4[0] <= -150 and m4 == True:
            e4[0] += .5
        else:
            m4 = False
        if m4 == False and e4[0] >= -313:
            e4[0] -= .5
        else:
            m4 = True

    glutPostRedisplay()




def display():
    global life, pause, ball_x, ball_y, page, re, g, b, e1, t_collected, t_collected2, score, score_updated, game_over_shown

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if page == 2:
        drawBall()
        drawMaze()
        drawTreasure()
        if not t_collected:
            treasureCollected()
        laser()
        if not pause:
            midPointCircle(-370, -165, 10, 0, 1, 0)
        if life == 3:
            lives(200, 150)
            lives(240, 150)
            lives(280, 150)
        elif life == 2:
            lives(200, 150)
            lives(240, 150)
        elif life == 1:
            lives(200, 150)

        enemy(e1[0], e1[1])
        enemy(e2[0], e2[1])
        enemy(e3[0], e3[1])
        checkObstacleCollision(ball_x, ball_y)
        drawRestart()
        if pause:
            drawStart()
        else:
            drawPause()
        drawClose()

        # Print the score only when updated
        if score_updated:
            #print(f"Score: {score}")
            score_updated = False  # Reset the flag

    if page == 4:
        drawBall()
        drawMaze_2()
        drawTreasure()
        if not t_collected2:
            treasureCollected()
        laser()
        if not pause:
            midPointCircle(375, 110, 10, 0, 1, 0)
        if life == 3:
            lives(200, 150)
            lives(240, 150)
            lives(280, 150)
        elif life == 2:
            lives(200, 150)
            lives(240, 150)
        elif life == 1:
            lives(200, 150)

        enemy(e4[0], e4[1])
        enemy(e5[0], e5[1])
        enemy(e6[0], e6[1])
        checkObstacleCollision(ball_x, ball_y)
        drawRestart()
        if pause:
            drawStart()
        else:
            drawPause()
        drawClose()

        # Print the score only when updated
        if score_updated:
            #print(f"Score: {score}")
            score_updated = False  # Reset the flag

    if life == 0 and not game_over_shown:
        print("Game Over!! Restart to play again.")
        game_over_shown = True  # Ensure "Game Over" is printed only once

    glutSwapBuffers()
def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-w_width // 2, w_width // 2, -w_height // 2, w_height // 2)


glutInit()

glutInitWindowSize(w_width, w_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Project")

init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutIdleFunc(animate)

glutMainLoop()
