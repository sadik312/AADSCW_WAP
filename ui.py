from datetime import datetime, time
from tkinter import *
from PIL import ImageTk, Image
import Graph_A_Dijk as gr

root = Tk()
root.title('Route Planner App')
root.geometry('800x500')
""" root.iconbitmap('train.png') # remember to credit the author 'freepick',
 from website: https://www.flaticon.com/authors/freepik """

confirm_label = Label(root)
confirm_label1 = Label(root)
error_label = Label(root)

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
    global confirm_label
    global confirm_label1
    global error_label
    confirm_label.destroy()
    confirm_label1.destroy()
    error_label.destroy()

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
        error_label = Label(root, text="Starting station not found")  ###
        error_label.pack()  ###


def main():
    """ Check if User is Accessing the Application within train running periods"""
    if in_time(time(5, 00), time(0)):  # 5AM -> MIDNIGHT
        ''' Call upon GUI'''
        ''' Get input and insert into Dijkstra's Algorithm'''
        gr.path = gr.shortest2(gr.graph, source, destination)
        gr.display(checking_time(str(depart_hour.get()), str(depart_min.get())))
        ''' Display within the GUI'''


""" input for starting station"""

src_input = Entry(root)
src_input.insert(0, "From:")
src_input.place(relx=0.5, rely=0.125, anchor=CENTER)

""" input for destination station"""
des_input = Entry(root)
des_input.insert(0, "To:")
des_input.place(relx=0.5, rely=0.2, anchor=CENTER)

HOURS = [x for x in range(23)]
MINUTES = [x for x in range(60)]

time_label = Label(root, text='Enter time of departure')
time_label.place(relx=0.5, rely=0.25, anchor=CENTER)
collon = Label(root, text=":")
collon.place(relx=0.5, rely=0.3, anchor=CENTER)

depart_hour = Entry(root, width=2)
depart_hour.insert(0, str(cur_time)[:2])
depart_hour.place(relx=0.48, rely=0.3, anchor=CENTER)

'''
variable = StringVar(root)
variable.set(HOURS[0])
depart_hour = OptionMenu(root, variable, *HOURS)
depart_hour.place(relx = 0.455, rely = 0.3, anchor = CENTER)


variable2 = StringVar(root)
variable2.set(MINUTES[0])
depart_min = OptionMenu(root, variable2, *MINUTES)
depart_min.place(relx = 0.542, rely = 0.3, anchor = CENTER)
'''
depart_min = Entry(root, width=2)
depart_min.insert(0, str(cur_time)[3:5])
depart_min.place(relx=0.52, rely=0.3, anchor=CENTER)


def checking_time(a, b):
    if (0 <= int(a) < 24) & (0 <= int(b) < 60):
        return '{}:{}'.format(a, b)
    else:
        Label(root, text='Time not entered correctly')


""" button to confirm station entries"""
confirm_btn = Button(root, text="Confirm", command=confirm)
confirm_btn.place(relx=0.5, rely=0.375, anchor=CENTER)

""" resets entry boxes, but not the station confirmations (can't seem to get that to work)"""


def reset():
    src_input.delete(0, END)
    des_input.delete(0, END)
    src_input.insert(0, "From:")
    des_input.insert(0, "To: ")
    confirm_label.pack_forget()  ###
    confirm_label1.pack_forget()  ###
    error_label.pack_forget()  ###


""" confirm_label.delete(0, END)"""

reset_btn = Button(root, text="Reset", command=reset)
reset_btn.place(relx=0.5, rely=0.425, anchor=CENTER)

""" Button that will open up TFL Map"""


def map_page():
    global map_img
    map_tab = Toplevel()
    map_tab.title("TFL Map")
    map_img = ImageTk.PhotoImage(Image.open("london_underground_map.png"))
    map_label = Label(map_tab, image=map_img)
    map_label.pack()


map_btn = Button(root, text="Map", command=map_page)
map_btn.place(relx=0.5, rely=0.475, anchor=CENTER)

""" Exit button:"""
exit_btn = Button(root, text="Exit", command=root.quit)
exit_btn.place(relx=0.5, rely=0.525, anchor=CENTER)


mainloop()


class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text='Main Page', width=25, command=self.new_window)
        self.button1.pack()
        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)


class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    root.geometry('800x500')

    app = Demo1(root)
    root.mainloop()


if __name__ == '__main__':
    main()
