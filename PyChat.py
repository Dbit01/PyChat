import random
#Graphics Library
from Tkinter import *
from tkColorChooser import askcolor
from tkFileDialog import *
from ScrolledText import ScrolledText
import tkMessageBox
#import PIL.Image
import PyChatBuddies
#variable to take on main library
root = Tk()

#title of frame
#root.title("PyChat")
#root.rowconfigure(0, weight = 1)
#root.columnconfigure(0, weight = 1)
#TODO if no thumbnail is created, the program will err out


class Application(Frame):
    #create global variables
    #chatColors = ['billColor', 'jeffColor', 'mattColor']
    buddies = {'Bill the Conqueror': 'PyChatBuddies.bill_the_conqueror', 'Matt the Unstable': 'PyChatBuddies.matt_the_unstable', 'Jeff the Grand': 'PyChatBuddies.jeff_the_grand'}


    randNum = 0
    userName = ""
    userColor = ""
    """
    function to initialize frame
    """
    def __init__(self, master):
        #initialize frame
        Frame.__init__(self,master)
        self.grid(row =0, column = 0)
        #screen to ask user for input
        self.login_screen()

    """
    function to generate random integers
    """
    def generateRand(self, size):
        #seed the randomness
        random.seed()
        #declaration allows us to modify global variable
        global randNum
        #random number between 0 and size of list -1 (to account for zero indexing
        randNum = random.randint(0, size - 1)
        return randNum
    """
    function for user input
    """
    def userInput(self, userName):
         #get text from input field
        lastResponse = self.inputField.get()
        userIndex = self.chatbox.index("insert")
        self.chatbox.insert('insert', userName + ": " + lastResponse + "\n")
        self.chatbox.tag_add("userColor", userIndex + "", "insert")
    """
    Function to remove friend
    """
    def removeFriend(self, username, friendToRemoveIndex):
        buddies = self.buddies
        friendToRemove = buddies[friendToRemoveIndex]
        buddies.remove(friendToRemove)

        print "here is self.buddies"
        for e in self.buddies:
            print e
        print "here is buddies"
        for e in buddies:
            print e
        self.friendsList.delete(friendToRemoveIndex)
    """
    Function for the AI to think of a response
    """
    def chatThink(self, event):
        #Make a copy of the username global variable
        userName = self.userName
        self.userInput(userName)
        #You do need to use the insert method after the delete method, as shown below
        self.inputField.delete(0, END)
        self.inputField.insert(0, "")
        self.inputField.configure(state='disabled')
        random
        #choose random buddy
        buddy = self.friendsList.get(ACTIVE)
        print buddy
        buddies = self.buddies
        #choose chat color
        #chatColorTag = buddies.get(buddy)
        chatList = buddies.get(buddy).get_greetings()
        chat = chatList[random.randrange(0, 3)]
        chatColorTag = buddies.get(buddy).get_chat_color()
        #choose random chat
        #find the index to start the text coloring
        index = self.chatbox.index('insert')
        self.chatRespond(buddy, chat, chatColorTag, index)
        self.inputField.configure(state='normal')

    """
    function to generate Bill's Messages
    """
    def chatRespond(self, buddy, chat, chatColorTag, index):
        self.chatbox.insert('insert', buddy + ": " + chat)
        userColor = self.userColor
        self.chatbox.tag_configure(userColor, foreground = chatColorTag)
        self.chatbox.tag_add(userColor, index + "", "insert")
        #scroll to end
        self.chatbox.see('end')
    """
    function to validate username input
    """
    def inputValidate(self, event):
        #TODO validate input
        self.userName = self.inputField.get()
        #make a copy to a local variable
        userName = self.userName
        #self.userProfilePicture = 'profile_pics/' + userName + '_thumbnail.png'
        #TODO do this for friends list
        tkMessageBox.showinfo('UserName', 'Your name is ' + userName)
         #create chat
        self.chat_screen()
        #create friends list
        #self.friends_screen()
        """
    function to upload a profile picture
    """
    def uploadProfilePicture(self):
        fileName = askopenfilename(filetypes = [('PNG FILES', '*.png')])
        #the following is a script to resize an image while maintaining the aspect ratio
        #http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
        basewidth = 50
        img = PIL.Image.open(fileName)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        img.save('profile_pics/' + self.userName + '_thumbnail.png')
        self.userProfilePicture = 'profile_pics/' + self.userName + '_thumbnail.png'
        self.userProfileScreen()
    """
    function to create initial widgets
    """
    def login_screen(self):
        """
        Using a loop is infesible because the value of i will always be used and generate the phrases of the last buddies in the array
        best fix for right now is to use a finite number of buddies
        TODO make a class for these different screens
        """
        root.title("Enter a username")
        self.enterLabel = Label(self, text = "Please enter a username")
        self.enterLabel.grid(row = 2, column = 2, columnspan = 2)
        #username input field
        self.inputField = Entry(self)
        self.inputField.grid(row =3, column = 3)
        self.inputField.bind('<Return>', self.inputValidate)

    """
    function to create initial widgets
    """
    def chat_screen(self):
        """
        Using a loop is infesible because the value of i will always be used and generate the phrases of the last buddies in the array
        best fix for right now is to use a finite number of buddies
        TODO make a class for these different screens
        """
        #destroy old frame and add new one
        self.destroy()
        Frame.__init__(self)
        self.grid(row = 0, column = 0)
        root.title("PyChat")
        #making copies of global variables
        userName = self.userName
        userColor = self.userColor
        #TODO move friendslist to a file
        buddies = self.buddies
        if hasattr(self, 'userProfilePicture'):
            self.profilePictureThumbnail = PhotoImage(file = self.userProfilePicture)
            self.profilePictureThumbnailLabel = Label(self, image = self.profilePictureThumbnail)
            self.profilePictureThumbnailLabel.grid(row = 10, column = 2)
        else:
            self.profilePictureThumbnailLabel = Label(self, text = "You have no Profile Picture Yet")
            self.profilePictureThumbnailLabel.grid(row = 10, column = 2)
        #username label
        self.userNameLabel = Label(self, text = userName)
        self.userNameLabel.grid(row = 9, column = 2)
        #profile button
        self.profileButton = Button(self, text = "Profile", command = self.userProfileScreen)
        self.profileButton.grid(row = 9, column = 0)
        #chatbox
        self.chatbox = ScrolledText(self, wrap = 'word', width = 50, height = 20, bg = 'beige')
        self.chatbox.grid(row = 0, column = 0, rowspan =8, columnspan =7)
        #input field
        self.inputField = Entry(self)
        self.inputField.grid(row =9, column = 6)
        self.inputField.bind('<Return>', self.chatThink)
        #friends list
        self.friendsList = Listbox(self, selectmode=BROWSE)
        self.friendsList.grid(row = 0, column = 8, rowspan = 8, columnspan = 8)
        #populate friendslist
        for buddy in buddies.keys():
            self.friendsList.insert(END, buddy)
        #add friend
        #self.addFriendButton = Button(self, text = "Add friend", command = self.addFriendScreen)
        #self.addFriendButton.grid(row = 9, column = 8)
        #remove friend
        self.removeFriendButton = Button(self, text = "Remove friend", command =lambda self=self: self.removeFriend(userName, 1))
        self.removeFriendButton.grid(row = 9, column = 9)
    """
    function to create profile widgets
    """
    def userProfileScreen(self):
        #destroy old frame and add new one
        self.destroy()
        Frame.__init__(self)
        self.grid(row = 0, column = 0)
        root.title(self.userName + "'s Profile")
        username = self.userName
        userColor = self.userColor
        self.uploadProfilePictureButton = Button(self, text = "Upload New Picture", command = self.uploadProfilePicture)
        self.uploadProfilePictureButton.grid()
        if hasattr(self, 'userProfilePicture'):
            self.profilePictureImage = PhotoImage(file = self.userProfilePicture)
            self.profilePictureLabel = Label(self, image = self.profilePictureImage)
            self.profilePictureLabel.grid()
        else:
            self.profilePictureLabel = Label(self, text = "Please Upload a new Image")
            self.profilePictureLabel.grid()
        self.uploadProfilePictureButton = Button(self, text = "Back", command = self.chat_screen)
        self.uploadProfilePictureButton.grid()
        #username
        #self.userNameLabel = Label(self, text = "username: " + userName)
        #TODO create change button

#frame size
root.geometry("")

#making the application the root
app = Application(root)
#starting the main loop
root.mainloop()

import tkMessageBox
