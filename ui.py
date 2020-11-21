from datetime import datetime, time
from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
from tkinter import messagebox
import Graph_A_Dijk as gr
import webbrowser

def center_window(w, h, frame):
    # get screen width and height
    ws = frame.winfo_screenwidth()
    hs = frame.winfo_screenheight()
    # calculate position x, y
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    frame.geometry('%dx%d+%d+%d' % (w, h, x, y))


looks = {'fg': 'white', 'bg': '#916648', 'highlightbackground': '#916648'}
root = Tk()
root.title('Route Planner App')
center_window(800, 500, root)
photo = PhotoImage(file="Photos/PR.gif")
root.iconphoto(False, photo)
root.configure(bg=looks['bg'])
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
    h = int(depart_hour.get())
    if int(depart_hour.get()) == str(cur_time)[:2]:
        if startTime < endTime:
            ''' The Current Time falls within the '''
            return startTime <= cur_time <= endTime
        else:
            ''' The 'or' takes into account if the period spans overnight'''
            return cur_time >= startTime or cur_time <= endTime
    else:
        if (5 <= h <= 12) or (12 <= h < 24):
            return True
        else:
            return False


def confirm():
    global source
    global destination
    global confirm_label
    global confirm_label1
    global error_label
    global time_label
    confirm_label.destroy()
    confirm_label1.destroy()
    error_label.destroy()
    time_label.destroy()

    def validation(a, b):
        try:
            int(a)
            int(a)
            return True
        except ValueError:
            return False

    source = words(src_input.get().lower().strip())
    destination = words(des_input.get().lower().strip())
    if source != destination:
        if validation(depart_hour.get(), depart_min.get()):
            if (0 <= int(depart_hour.get()) <= 23) and (0 <= int(depart_min.get()) <= 59):

                if source in gr.graph.nodes():
                    if destination in gr.graph.nodes():
                        confirm_label = Label(root, text="Starting Station: " + words(source),
                                              bg=looks['bg'], fg=looks['fg'],
                                              highlightbackground=looks['highlightbackground'])
                        confirm_label.pack()
                        confirm_label1 = Label(root, text="Destination Station: " + words(destination),
                                               bg=looks['bg'], fg=looks['fg'],
                                               highlightbackground=looks['highlightbackground'])
                        confirm_label1.pack()
                        main()
                    else:
                        error_label = Label(root, text="Destination not found",
                                            bg=looks['bg'], fg=looks['fg'],
                                            highlightbackground=looks['highlightbackground'])
                        error_label.pack()
                else:
                    error_label = Label(root, text="Starting station not found",
                                        bg=looks['bg'], fg=looks['fg'],
                                        highlightbackground=looks['highlightbackground'])  ###
                    error_label.pack()
            else:
                error_label = Label(root, text="Time entered is invalid",
                                    bg=looks['bg'], fg=looks['fg'],
                                    highlightbackground=looks['highlightbackground'])  ###
                error_label.pack()
        else:
            time_label = Label(root, text='Entered time is invalid',
                               bg=looks['bg'], fg=looks['fg'], highlightbackground=looks['highlightbackground'])
            time_label.pack()
    else:
        error_label = Label(root, text="Same station",
                            bg=looks['bg'], fg=looks['fg'], highlightbackground=looks['highlightbackground'])  ###
        error_label.pack()


def main():
    """ Check if User is Accessing the Application within train running periods"""
    if in_time(time(5, 00), time(0)):  # 5AM -> MIDNIGHT
        ''' Call upon GUI'''
        ''' Get input and insert into Dijkstra's Algorithm'''
        gr.path = gr.shortest2(gr.graph, source, destination, int(depart_hour.get()))
        if checking_time(str(depart_hour.get()), str(depart_min.get())) is False:
            root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='Photos/lol.gif'))
            messagebox.showerror("Incorrect Time", "Entered time is not valid")
        else:
            display_gui(checking_time(str(depart_hour.get()), str(depart_min.get())))
            # gr.display(checking_time(str(depart_hour.get()), str(depart_min.get())))
            ''' Display within the GUI'''
    else:
        root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='Photos/lol.gif'))
        messagebox.showerror("Application not available", "No trians are ruinning at this hour. The train should run "
                                                          "between the hours of 5:00am to Midnight")


""" input for starting station"""

src_input = Entry(root, bg=looks['bg'], fg=looks['fg'], highlightbackground=looks['highlightbackground'])
src_input.insert(0, "From:")
src_input.place(relx=0.5, rely=0.125, anchor=CENTER)

""" input for destination station"""
des_input = Entry(root, bg=looks['bg'], fg=looks['fg'], highlightbackground=looks['highlightbackground'])
des_input.insert(0, "To:")
des_input.place(relx=0.5, rely=0.2, anchor=CENTER)

time_label = Label(root, text='Enter time of departure', bg=looks['bg'], fg=looks['fg'],
                   highlightbackground=looks['highlightbackground'])
time_label.place(relx=0.5, rely=0.25, anchor=CENTER)
collon = Label(root, text=":", bg=looks['bg'], fg=looks['fg'], highlightbackground=looks['highlightbackground'])
collon.place(relx=0.5, rely=0.3, anchor=CENTER)

depart_hour = Entry(root, width=2, bg=looks['bg'], fg=looks['fg'], highlightbackground=looks['highlightbackground'])
depart_hour.insert(0, str(cur_time)[:2])
depart_hour.place(relx=0.48, rely=0.3, anchor=CENTER)

depart_min = Entry(root, width=2, bg=looks['bg'], fg=looks['fg'], highlightbackground=looks['highlightbackground'])
depart_min.insert(0, str(cur_time)[3:5])
depart_min.place(relx=0.52, rely=0.3, anchor=CENTER)


def checking_time(a, b):
    if (0 <= int(a) < 24) & (0 <= int(b) < 60):
        return '{}:{}'.format(a, b)
    else:
        return False


""" button to confirm station entries"""
confirm_btn = Button(root, text="Confirm", command=confirm,
                     bg=looks['bg'], fg='black', highlightbackground=looks['highlightbackground'])
confirm_btn.place(relx=0.5, rely=0.375, anchor=CENTER)

""" resets entry boxes, but not the station confirmations (can't seem to get that to work)"""


def reset():
    src_input.delete(0, END)
    des_input.delete(0, END)
    src_input.insert(0, "From:")
    des_input.insert(0, "To: ")
    confirm_label.pack_forget()
    confirm_label1.pack_forget()
    error_label.pack_forget()


""" confirm_label.delete(0, END)"""

reset_btn = Button(root, text="Reset", command=reset,
                   bg=looks['bg'], fg='black', highlightbackground=looks['highlightbackground'])
reset_btn.place(relx=0.5, rely=0.425, anchor=CENTER)

""" Button that will open up TFL Map"""


def map_page():
    global map_img
    map_tab = Toplevel()
    map_tab.title("TFL Map")
    map_img = ImageTk.PhotoImage(Image.open("london_underground_map.png"))
    map_label = Label(map_tab, image=map_img)
    map_label.pack()


map_btn = Button(root, text="Map", command=lambda: [webbrowser.open("http://content.tfl.gov.uk/standard-tube-map.pdf")],
                 bg=looks['bg'], fg='black', highlightbackground=looks['highlightbackground'])
map_btn.place(relx=0.5, rely=0.475, anchor=CENTER)

""" Exit button:"""
exit_btn = Button(root, text="Exit", command=root.quit,
                  bg=looks['bg'], fg='black', highlightbackground=looks['highlightbackground'])
exit_btn.place(relx=0.5, rely=0.525, anchor=CENTER)


def display_gui(time):
    gr.final = []
    global display
    display = Tk()
    display.title('Route')
    if len(gr.path) < 20:
        height = 30
    else:
        height = len(gr.path) * 2
    text = Text(display, height=height, width=60)
    text.pack()

    Button(display, text='Main page', command=lambda: [text.delete(1.0, END), display.destroy()]).pack()
    cur_time = time
    gr.path_finder()
    temp = gr.final[1]

    text.tag_configure('Main_station', font=('Arial', 18, 'bold'))
    text.tag_configure('bold', font=('Arial', 14, 'bold'))
    text.tag_configure('stations', font=('Arial', 14,))

    colours = {'Bakerloo': '#B36305', 'Central': '#E32017', 'Circle': '#FFD300', 'District': '#00782A',
               'Hammersmith_&_City': '#F3A9BB', 'Jubilee': '#A0A5A9', 'Metropolitan': '#9B0056', 'Northern': '#000000',
               'Piccadilly': '#003688', 'Victoria': '#0098D4', 'Waterloo_&_City': '#95CDBA'}

    '''      
            if changes is None:
                changes = lines
            else:
                changes = changes + ', ' + lines
        # Label(display, text='{}{}{}{}'.format(' '*5,changes,' '*5, gr.cum_time(cur_time, i[2]))).pack(anchor=W)
        text.insert(END, '{}{}{}{}\n'.format(' ' * 2, changes, ' ' * 2, gr.cum_time(cur_time, i[2])), 'lines')
    '''

    for i in gr.final:
        if i[1] == temp:
            if i == gr.final[-1]:
                text.insert(END, i[0] + '\n', 'Main_station')
                text.insert(END, 'Final time:{}'.format(gr.cum_time(cur_time, i[2])), 'Main_station')

            else:
                text.insert(END, ' ' * 5, 'stations')

                for j in i[1]:
                    text.tag_configure(j, font=('Arial', 15, 'bold'), foreground=colours[j])
                    text.insert(END,'|', j)

                text.insert(END, '-{}'.format(i[0]) + '\n', 'stations')

        else:

            text.insert(END, i[0] + '\n', 'Main_station')
            for lines in i[1]:
                temp1 = lines
                if lines == 'Hammersmith & City':
                    temp1 = 'Hammersmith_&_City'
                if lines == 'Waterloo & City':
                    temp1 = 'Waterloo_&_City'

                text.tag_configure(temp1, font=('Arial', 15, 'bold'), foreground=colours[temp1])
                if temp1 == i[1][-1]:
                    text.insert(END, ' ' + temp1, '{}'.format(temp1))
                    text.insert(END, ' ' + gr.cum_time(cur_time, i[2]) + '\n', 'bold')
                elif temp == i[1][0]:
                    text.insert(END, ' ' * 7 + temp1 + ',', '{}'.format(temp1))
                else:
                    text.insert(END, temp1 + ',', '{}'.format(temp1))
        temp = i[1]


mainloop()
