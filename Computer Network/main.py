import peer
from tkinter import *
from tkinter import filedialog
from tkinter import font

def textEditor():
	def __init__(self,Name):
old_text = ""
def sync():
	global old_text
	new_text = my_text.get("1.0",END)
	peer.get_CRDT_commands(old_text,new_text)
	old_text = new_text


	root = Tk()
	root.title(f'{Name} - SecredText')
	root.geometry("1200x660")
	
	# Create Main Frame
	my_frame = Frame(root)
	my_frame.pack(pady = 5)
	
	#Create Scrollbar
	text_scroll = Scrollbar(my_frame)
	text_scroll.pack(side=RIGHT,fill=Y)
	
	# Create Text Box
	my_text = Text(my_frame,width = 97, height = 25, font = ("Helvetica",16), selectbackground="yellow",selectforeground="black",undo=True, yscrollcommand=text_scroll.set)
	my_text.pack()
	
	# Configure our Scrollbar
	text_scroll.config(command=my_text.yview)
	
	
	#Create Menu
	my_menu = Menu(root)
	root.config(menu = my_menu)
	
	# Add File Menu
	file_menu = Menu(my_menu, tearoff = False)
	my_menu.add_cascade(label = "File", menu=file_menu)
	file_menu.add_command(label = "New       ")
	file_menu.add_command(label = "Open")
	file_menu.add_command(label = "Save")
	file_menu.add_separator()
	file_menu.add_command(label = "Exit")
	
	# Add Connect Menu
	edit_menu = Menu(my_menu, tearoff = False)
	my_menu.add_cascade(label = "Connect", menu=edit_menu)
	edit_menu.add_command(label = "Join")
	edit_menu.add_command(label = "Add Editor")
	edit_menu.add_command(label = "Sync", command = sync)
	edit_menu.add_command(label = "Exit")
	
	
	#Add Status Bar to Bottom of App
	status_bar = Label(root, text="Connecting...		",anchor=E)
	status_bar.pack(fill=X,side=BOTTOM,ipady=5)
	root.mainloop()











