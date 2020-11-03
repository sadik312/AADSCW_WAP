from datetime import datetime, time
from tkinter import *
from PIL import ImageTk, Image
import Graph_A_Dijk as gr

root = Tk()
root.title('Route Planner App')
root.geometry('800x500')
""" root.iconbitmap('train.png') # remember to credit the author 'freepick',
 from website: https://www.flaticon.com/authors/freepik """

# func to confirm entered stations
source = None
destination = None


def words(string):
    if " " in string:
        newText = ''
        wap = string.split(' ')
        for val in wap:
            ''' Remove space from starting and ending'''
            val = val.strip()
            ''' Capitalize each list item and merge with '.' '''
            newText += val.capitalize() + ' '
        return newText.strip()
    else:
        return string.capitalize()


cur_time = datetime.utcnow().time()


def in_time(startTime, endTime):
    """Current Universal Time"""
    if startTime < endTime:
        ''' The Current Time falls within the '''
        return startTime <= cur_time <= endTime
    else:
        ''' The 'or' takes into account if the period spans overnight'''
        return cur_time >= startTime or cur_time <= endTime


def confirm():
    global source
    global destination
    source = words(src_input.get().lower().strip())
    destination = words(des_input.get().lower().strip())

    if source in gr.graph.nodes():
        if destination in gr.graph.nodes():
            confirm_label = Label(root, text="Starting Station: " + words(source))
            confirm_label.pack()
            confirm_label1 = Label(root, text="Destination Station: " + words(destination))
            confirm_label1.pack()
            main()
        else:
            error_label = Label(root, text="Destination not found")
            error_label.pack()
    else:
        error_label = Label(root, text="Starting station not found")
        error_label.pack()


def main():
    """ Check if User is Accessing the Application within train running periods"""
    if in_time(time(5, 00), time(0)):  # 5AM -> MIDNIGHT
        ''' Call upon GUI'''
        ''' Get input and insert into Dijkstra's Algorithm'''
        gr.dijkstra(gr.graph, source)
        gr.spec_bakerloo()
        gr.shortest(source, destination)
        gr.display()
        ''' Display within the GUI'''


""" input for starting station"""

src_input = Entry(root)
src_input.insert(0, "From:")
src_input.pack()

""" input for destination station"""
des_input = Entry(root)
des_input.insert(0, "To:")
des_input.pack()

""" button to confirm station entries"""
confirm_btn = Button(root, text="Confirm", command=confirm)
confirm_btn.pack()

""" resets entry boxes, but not the station confirmations (can't seem to get that to work)"""


def reset():
    src_input.delete(0, END)
    des_input.delete(0, END)
    src_input.insert(0, "From:")
    des_input.insert(0, "To: ")


""" confirm_label.delete(0, END)"""

reset_btn = Button(root, text="Reset", command=reset)
reset_btn.pack()

""" Button that will open up TFL Map"""


def map_page():
    global map_img
    map_tab = Toplevel()
    map_tab.title("TFL Map")
    map_img = ImageTk.PhotoImage(Image.open("london_underground_map.png"))
    map_label = Label(map_tab, image=map_img)
    map_label.pack()


map_btn = Button(root, text="Map", command=map_page)
map_btn.pack()

""" Exit button:"""
exit_btn = Button(root, text="Exit", command=root.quit)
exit_btn.pack()

mainloop()
