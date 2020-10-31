from datetime import datetime, time
from tkinter import * 
from PIL import ImageTk, Image
import Graph_A_Dijk as gr

root = Tk()
root.title('Route Planner App')
root.geometry('800x500')
#root.iconbitmap('train.png') # remember to credit the author 'freepick', 
#from website: https://www.flaticon.com/authors/freepik

# func to confirm entered stations
source = None
destination = None
def words(string):
	if " " in string:
		newText = ''
		wap = string.split(' ')
		for val in wap:
			# Remove space from starting and ending
			val = val.strip()

			# Capitalize each list item and merge with '.'
			newText += val.capitalize() + ' '

			# Remove the last dot

		return newText.strip()
	else:
		return string.capitalize()


def in_time(startTime, endTime):
	'''Current Universal Time'''
	cur_time = datetime.utcnow().time()
	if startTime < endTime:
		''' The Current Time falls within the '''
		return cur_time >= startTime and cur_time <= endTime
	else:
		''' The 'or' takes into account if the period spans overnight'''
		return cur_time >= startTime or cur_time <= endTime


def main():
	''' Check if User is Accessing the Application within train running periods'''
	if in_time(time(5, 00), time(0)):  # 5AM -> MIDNIGHT
		''' Call upon GUI'''
		''' Get input and insert into Dijkstra's Algorithm'''
		gr.dijkstra(gr.graph, source)
		gr.shortest(source, destination)
		''' Display within the GUI'''


def Confirm():
<<<<<<< HEAD
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

			# input for starting station
src_input = Entry(root)
src_input.insert(0, "Morden")
=======
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
>>>>>>> 5b3a4aa2d8cf7e68379e09e64eb0cf1d08be1c19
src_input.pack()


# input for destination station
des_input = Entry(root)
des_input.insert(0, "edgware")
des_input.pack()

# button to confirm station entries
confirm_btn = Button(root, text="Confirm", command=Confirm)
confirm_btn.pack()

# resets entry boxes, but not the station confirmations (can't seem to get that to work)
def reset(): 
	src_input.delete(0, END)
<<<<<<< HEAD
	des_input.delete(0, END)
	src_input.insert(0, "From:")
	des_input.insert(0, "To: ")
=======
	user_input1.delete(0, END)
	src_input.insert(0, "From:")
	user_input1.insert(0, "To: ")
>>>>>>> 5b3a4aa2d8cf7e68379e09e64eb0cf1d08be1c19
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


