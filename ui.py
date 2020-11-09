from datetime import datetime, time
from tkinter import *
from PIL import ImageTk, Image
import Graph_A_Dijk as gr

class PageOne:
    def __init__(self, master):
        self.master = master
        self.frame = Tk.Frame(self.master)
        self.button1 = Tk.Button(self.frame, text='Main Page', width=25, command=self.new_window)
        self.button1.pack()
        self.frame.pack()
        self.cur_time = datetime.utcnow().time()
        # func to confirm entered stations
        self.source = None
        self.estination = None
        self.confirm_label = Label(self.frame)
        self.confirm_label1 = Label(self.frame)
        self.error_label = Label(self.frame)
        """ input for starting station"""

        self.src_input = Entry(self.frame)
        self.src_input.insert(0, "From:")
        self.src_input.place(relx=0.5, rely=0.125, anchor=CENTER)

        """ input for destination station"""
        self.des_input = Entry(self.frame)
        self.des_input.insert(0, "To:")
        self.des_input.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.HOURS = [x for x in range(23)]
        self.MINUTES = [x for x in range(60)]

        self.time_label = Label(self.frame, text='Enter time of departure')
        self.time_label.place(relx=0.5, rely=0.25, anchor=CENTER)
        self.collon = Label(self.frame, text=":")
        self.collon.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.depart_hour = Entry(self.frame, width=2)
        self.depart_hour.insert(0, str(self.cur_time)[:2])
        self.depart_hour.place(relx=0.48, rely=0.3, anchor=CENTER)

        self.depart_min = Entry(self.frame, width=2)
        self.depart_min.insert(0, str(self.cur_time)[3:5])
        self.depart_min.place(relx=0.52, rely=0.3, anchor=CENTER)

        """ button to confirm station entries"""
        self.confirm_btn = Button(self.frame, text="Confirm", command=self.confirm)
        self.confirm_btn.place(relx=0.5, rely=0.375, anchor=CENTER)

        """ confirm_label.delete(0, END)"""

        self.reset_btn = Button(self.frame, text="Reset", command=self.reset)
        self.reset_btn.place(relx=0.5, rely=0.425, anchor=CENTER)

        self.map_btn = Button(self.frame, text="Map", command= self.map_page)
        self.map_btn.place(relx=0.5, rely=0.475, anchor=CENTER)

        """ Exit button:"""
        self.exit_btn = Button(self.frame, text="Exit", command=self.frame.quit)
        self.exit_btn.place(relx=0.5, rely=0.525, anchor=CENTER)
        """ root.iconbitmap('train.png') # remember to credit the author 'freepick',
         from website: https://www.flaticon.com/authors/freepik """

    def new_window(self):
        self.newWindow = Tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)


    def words(self, string):
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


    def in_time(self, startTime, endTime):
        """Current Universal Time"""
        if startTime < endTime:
            ''' The Current Time falls within the '''
            return startTime <= self.cur_time <= endTime
        else:
            ''' The 'or' takes into account if the period spans overnight'''
            return self.cur_time >= startTime or self.cur_time <= endTime


    def confirm(self, words):
        global source
        global destination
        global confirm_label
        global confirm_label1
        global error_label
        confirm_label.destroy()
        confirm_label1.destroy()
        error_label.destroy()

        self.source = words(self.src_input.get().lower().strip())
        self.destination = words(self.des_input.get().lower().strip())
        if source in gr.graph.nodes():
            if destination in gr.graph.nodes():
                confirm_label = Label(self.frame, text="Starting Station: " + words(self.source))
                confirm_label.pack()
                confirm_label1 = Label(self.frame, text="Destination Station: " + words(self.destination))
                confirm_label1.pack()
                main()
            else:
                error_label = Label(self.frame, text="Destination not found")
                error_label.pack()
        else:
            error_label = Label(self.frame, text="Starting station not found")  ###
            error_label.pack()  ###


    def main(self, in_time, checking_time):
        """ Check if User is Accessing the Application within train running periods"""
        if in_time(time(5, 00), time(0)):  # 5AM -> MIDNIGHT
            ''' Call upon GUI'''
            ''' Get input and insert into Dijkstra's Algorithm'''
            gr.path = gr.shortest2(gr.graph, source, destination)
            gr.display(checking_time(str(self.depart_hour.get()), str(self.depart_min.get())))
            ''' Display within the GUI'''

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

    def checking_time(self, a, b):
        if (0 <= int(a) < 24) & (0 <= int(b) < 60):
            return '{}:{}'.format(a, b)
        else:
            Label(self.frame, text='Time not entered correctly')

    """ resets entry boxes, but not the station confirmations (can't seem to get that to work)"""
    def reset(self):
        self.src_input.delete(0, END)
        self.des_input.delete(0, END)
        self.src_input.insert(0, "From:")
        self.des_input.insert(0, "To: ")
        confirm_label.pack_forget()  ###
        confirm_label1.pack_forget()  ###
        error_label.pack_forget()  ###

    def map_page(self):
        global map_img
        map_tab = Toplevel()
        map_tab.title("TFL Map")
        map_img = ImageTk.PhotoImage(Image.open("london_underground_map.png"))
        map_label = Label(map_tab, image=map_img)
        map_label.pack()





class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = Tk.Frame(self.master)
        self.quitButton = Tk.Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


def main():
    root = Tk()
    root.geometry('800x500')

    app = PageOne(root)
    root.mainloop()


if __name__ == '__main__':
    main()

mainloop()