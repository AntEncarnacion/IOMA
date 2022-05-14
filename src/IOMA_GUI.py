from calendar import leapdays
from struct import pack
import tkinter as tk
from tkinter import *
import client

client = client.Client()

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

#Button so the peers can download entire conversation
downloadButton = Button(right_frame, text="Download Conversation")
downloadButton.pack()

#Label that says "Message: "
messageLabel = Label(right_frame, text="Message: ")
messageLabel.pack()

#Textbox so that a peer can write a message
messageTextBox = Text(right_frame,height=5, width=40)
messageTextBox.pack()

#Button that says "SEND"
sendButton = Button(right_frame, text="SEND", command=lambda: submit) #to add a function to the button just add ", command=yourfunction" inside parenthesis
sendButton.pack()

def submit():  # Callback function for SUBMIT Button
    text = messageTextBox.get("1.0", END)  # For line 1, col 0 to end.
    client.send_message(text)
    messageTextBox.delete("1.0", END)  # For line 1, col 0 to end.

window.protocol("WM_DELETE_WINDOW", client.client_leave)


#Size of the window and title of the window
window.geometry("600x600+10+10")
window.title('Inter-Office Messaging Application')
window.mainloop()