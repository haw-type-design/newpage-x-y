import tkinter as tk
from pyaxidraw import axidraw
import time
import math

# Setup 
line_id = None
line_points = []
points = []
line_options = {}
flag = 0


# root tk
root = tk.Tk()
root.title('Draw2Plot')


# Norming the plotters size to screen width (!caution! This might lead to distortion)
xnorm = (42/root.winfo_screenheight())*math.sqrt(2)
ynorm = 29.7/root.winfo_screenheight()


# Connect AxiDraw in case of fail flag
ad = axidraw.AxiDraw()         
ad.interactive()
ad.options.model = 2
if not ad.connect():            
    print("No plotter connected — reverting to drawing")
    flag = 1
    
    
# Setup AxiDraw and set units to mm (otherwise change norm values above)
if flag == 0:  
    ad.options.pen_pos_down = 45
    ad.options.pen_pos_up = 20
    ad.options.units = 1
    ad.options.model = 2
    ad.update() 
    ad.penup() 

    
# line draw handling
def draw_line(event):
    global line_id
    line_points.extend((event.x, event.y))
    if line_id is not None:
        canvas.delete(line_id)
    line_id = canvas.create_line(line_points, **line_options)

    
def set_start(event):
    line_points.extend((event.x, event.y))

    
# end lines and perform plot   
def end_line(event=None):
    global line_id
    point_parser(line_points)
    print(points)
    if flag == 0:
        ad.draw_path(points)
        ad.moveto(0, 0)
        ad.block() 

    line_points.clear()
    points.clear()
    line_id = None

# Making tkinter lines AxiDraw format compatible [] --> [[]]
def point_parser(line_points):
    for x in range(len(line_points) - 1):
        if x%2 == 0:
            points.append([round(line_points[x]*xnorm, 1) , round(line_points[x+1]*ynorm, 1)])
            
            
# Recalculate norms and clear canvas on window size change
def resize(event):
    canvas.delete("all")
    xnorm = 42/root.winfo_width()
    ynorm = 29.7/root.winfo_height()


# Canvas setup to fit screen in height and set width to match A3
canvas = tk.Canvas(width=root.winfo_screenheight()*math.sqrt(2), height=root.winfo_screenheight())
canvas.pack(fill="both", expand=True)


# Mouse and resize operations
canvas.bind('<Button-1>', set_start)
canvas.bind('<B1-Motion>', draw_line)
canvas.bind('<ButtonRelease-1>', end_line)
canvas.bind('<Configure>', resize)


# tkinter main loop
root.mainloop()


# disconnecting AxiDraw
if flag == 0:
    ad.disconnect() 