'''
import tkinter
from PIL import ImageTk, Image

root = tkinter.Tk()
root.geometry("800x500")
root.title("Router Planner App")
#root.iconbitmap()

#entry = tkinter.Entry(root)
#entry.pack()


def Confirm():
    with open("stations.txt", "r") as f: 
        if user_input.get() in f.read(): 
            alabel = tkinter.Label(root, text="You have confirmed " + user_input.get()).pack()
        else: 
            blabel = tkinter.Label(root, text="Not found").pack()

user_input = tkinter.Entry(root)
user_input.insert(0, "From")
user_input.pack()

button = tkinter.Button(root, text="Enter", command=Confirm)
button.pack()

user_input = tkinter.Entry(root)
user_input.insert(0, "To")
user_input.pack()

button = tkinter.Button(root, text="Enter", command=Confirm)
button.pack(pady=20)

# new window for Map view:
def map_page():
	map_tab = Toplevel()
	map_image = ImageTk.PhotoImage(Image.open("london_underground_map.png"))
	map_label = Label(map_tab, image=map_image).pack()

map_btn = tkinter.Button(root, text="Map", command=map_page)
map_btn.pack(pady=25)

root.mainloop()'''

from tkinter import * 
from PIL import ImageTk, Image

root = Tk()
root.title('Route Planner App')
root.geometry('800x500')
#root.iconbitmap('train.png') # remember to credit the author 'freepick', 
#from website: https://www.flaticon.com/authors/freepik

# func to confirm entered stations
def Confirm():
	with open ('stations.txt', 'r') as file:
			if src_input.get() and user_input1.get() in file.read():
				confirm_label = Label(root, text="Starting Station: " + src_input.get())
				confirm_label.pack()
				confirm_label1 = Label(root, text="Destination Station: " + user_input1.get())
				confirm_label1.pack()
			
			else:
				error_label = Label(root, text="both stations not found")
				error_label.pack() 
				
# input for starting station
src_input = Entry(root)
src_input.insert(0, "From:")
src_input.pack()


# input for destination station
user_input1 = Entry(root)
user_input1.insert(0, "To:")
user_input1.pack()

# button to confirm station entries
confirm_btn = Button(root, text="Confirm", command=Confirm)
confirm_btn.pack()

# resets entry boxes, but not the station confirmations (can't seem to get that to work)
def reset(): 
	src_input.delete(0, END)
	user_input1.delete(0, END)
	src_input.insert(0, "From:")
	user_input1.insert(0, "To: ")
	#confirm_label.delete(0, END)
	

reset_btn = Button(root, text="Reset", command=reset)
reset_btn.pack()


# Button that will open up TFL Map
def map_page(): 
	global map_img
	map_tab = Toplevel()
	map_tab.title("TFL Map")
	map_img = ImageTk.PhotoImage(Image.open("london_underground_map.png"))
	map_label = Label(map_tab, image=map_img)
	map_label.pack()

map_btn = Button(root, text="Map", command=map_page)
map_btn.pack()

# Exit button: 
exit_btn = Button(root, text="Exit", command=root.quit)
exit_btn.pack()


mainloop()


