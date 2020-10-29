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


            
            


root.mainloop()
