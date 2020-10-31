from tkinter import * 
from PIL import ImageTk, Image

root = Tk()
root.title('Route Planner App')
root.geometry('800x500')
root.iconbitmap('train.png') # remember to credit the author 'freepick', 
#from website: https://www.flaticon.com/authors/freepik

# 'From' Entry box
def Confirm():
	with open ('stations.txt', 'r') as file:
			if user_input.get() and user_input1.get() in file.read():
				confirm_label = Label(root, text="Starting Station: " + user_input.get()).pack()
				confirm_label1 = Label(root, text="Destination Station: " + user_input1.get()).pack()
			
			else:
				error_label = Label(root, text="both stations not found").pack() 
				

user_input = Entry(root)
user_input.insert(0, "From:")
user_input.pack()
user_input1 = Entry(root)
user_input1.insert(0, "To:")
user_input1.pack()

confirm_btn = Button(root, text="Confirm", command=Confirm)
confirm_btn.pack()

def reset(): 
	user_input.delete(0, END)
	user_input1.delete(0, END)
	user_input.insert(0, "From:")
	user_input1.insert(0, "To: ")
	confirm_label.delete(0, END)
	

reset_btn = Button(root, text="Reset", command=reset)
reset_btn.pack()

# INCLUDE A REFRESH BUTTON


# Button that will open up TFL Map
def map_page(): 
	global map_img
	map_tab = Toplevel()
	map_tab.title("TFL Map")
	map_img = ImageTk.PhotoImage(Image.open("london_underground_map.png"))
	map_label = Label(map_tab, image=map_img)
	map_label.pack()
	exit_btn1 = Button(map_tab, text="Exit map", command=map_tab.quit)
	exit_btn1.pack()

map_btn = Button(root, text="Map", command=map_page)
map_btn.pack()


# Exit button: 
exit_btn = Button(root, text="Exit", command=root.quit)
exit_btn.pack()


mainloop()

