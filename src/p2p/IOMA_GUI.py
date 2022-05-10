from calendar import leapdays
from struct import pack
import tkinter as tk
from tkinter import *

#main window
window = tk.Tk()

#Frames are for the organization of the view
left_frame = Frame(window)
left_frame.pack(side=LEFT)

right_frame = Frame(window)
right_frame.pack(side=RIGHT)

bottom_frame = Frame(window)
bottom_frame.pack(side=BOTTOM)

#Label for peers
peersLabel = Label(left_frame, text="Peers")
peersLabel.pack()

#Label that says "Messages List"
messagesLabel = Label(right_frame, text="Messages List")
messagesLabel.pack()

#List on where the peers are supposed to appear
peerList = Listbox(left_frame,height=35, width=40)
peerList.pack()

#List where the messages are suppose to appear
messageList = Listbox(right_frame,height=25, width=50)
messageList.pack()

#Label that says "Message: "
messageLabel = Label(right_frame, text="Message: ")
messageLabel.pack()

#Textbox so that a peer can write a message
messageTextBox = Text(right_frame,height=5, width=40)
messageTextBox.pack()

#Button that says "SEND"
sendButton = Button(right_frame, text="SEND") #to add a function to the button just add ", command=yourfunction" inside parenthesis
sendButton.pack()


#Size of the window and title of the window
window.geometry("600x600+10+10")
window.title('Inter-Office Messaging Application')
window.mainloop()