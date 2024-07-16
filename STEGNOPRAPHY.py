#bg = border and fg = foreground(used to customize the appearance of the text with in the widgets)
# Imports all classes and functions from the tkinter module. The * means everything will be imported.
#used for creating GUI
from tkinter import * 

#provides dialog windows for file-related operations.
from tkinter import filedialog 

#Imports the Image and ImageTk classes from the Python Imaging Library (PIL), which is used for working with images.
from PIL import Image, ImageTk 

#Imports the os module, which provides a way to interact with the operating system, used here for getting the current working directory.
import os 

# Imports the least significant bit (LSB) method from the stegano library for hiding and revealing information in images.
from stegano import lsb 

#Imports the messagebox module from tkinter for displaying message boxes.
from tkinter import messagebox

#Defines a function resize_image that takes an image and resizes it to the specified width and height using the Lanczos resampling algorithm.
def resize_image(image, width, height):
    return image.resize((width, height), Image.LANCZOS)


# Defines a function showimage that opens a file dialog for selecting an image file.
# It sets the filename global variable to the selected file's path.
# If a file is selected, it opens the image, resizes it, converts it to a Tkinter PhotoImage, and displays it in a label (lbl).
# If no file is selected, it shows an error message.
# Exception handling is included to catch any errors during this process.
def showimage():
    global filename
    try:
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title='Select Image File',
            filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"), ("All files", "*.*"))
        )
        if filename:
            img = Image.open(filename)
            img = resize_image(img, 250, 250)
            img = ImageTk.PhotoImage(img)
            lbl.configure(image=img)
            lbl.image = img
        else:
            messagebox.showerror("Error", "Please select an image.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Defines a function Hide that hides a message obtained from a Text widget into the selected image using the LSB method.
# Sets the secret global variable to the steganographic object.
# Displays a success message and clears the text widget.
# Shows an error if no image is selected.
# Exception handling is included.
def Hide():
    global secret
    global filename
    message = text1.get(1.0, END)
    try:
        if filename:
            secret = lsb.hide(filename, message)
            messagebox.showinfo("Success", "Message hidden successfully.")
            text1.delete(1.0, END)
        else:
            messagebox.showerror("Error", "Please select an image first.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


#Defines a function Show that reveals a hidden message from the selected image and displays it in a Text widget.
# Shows an error if no image is selected.
# Exception handling is included.
def Show():
    global filename
    try:
        if filename:
            clear_message = lsb.reveal(filename)
            text1.delete(1.0, END)
            text1.insert(END, clear_message)
        else:
            messagebox.showerror("Error", "Please select an image first.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


#Defines a function save that saves the image with the hidden message to a file named "encrypted.png".
# Shows an error if there is no image to save.
# Exception handling is included.
def save():
    try:
        if 'secret' in globals():
            secret.save("encrypted.png")
            messagebox.showinfo("Success", "Image saved successfully.")
        else:
            messagebox.showerror("Error", "No image to save.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


#This block creates the main window with specific characteristics( title, geometry, and background color.)
root = Tk()
root.title("Steganography - Hide a Secret Text Message in an Image")
root.geometry("700x500+150+180")
root.resizable(False, False)
root.configure(bg="#2f4155")


#Global variables to store the selected filename and the steganographic object.
filename = ""
secret = None

#Sets the window icon and loads a logo for the GUI.
image_icon = PhotoImage(file="logo.jpg")
root.iconphoto(False, image_icon)
logo = PhotoImage(file="logo.png")

#Several frames and labels are created to organize and display different elements in the GUI.

#Creates and places labels with a logo and a title in the Tkinter window.
Label(root, image=logo, bg="#2d4155").place(x=10, y=0)
Label(root, text="CYBER SCIENCE", bg="#2d4155", 
fg="white", font="arial 25 bold").place(x=100, y=20)

#Creates a frame (f) and a label (lbl) within it, where the image will be displayed.
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)
lbl = Label(f, bg="black")
lbl.place(x=10, y=10)  # Adjusted the placement of the label

#Creates a frame (frame2), a Text widget (text1) within it for displaying text, and a vertical scrollbar for the Text widget.
frame2 = Frame(root, bd=3, bg="white", width=340, height=280, relief=GROOVE)
frame2.place(x=350, y=80)
text1 = Text(frame2, font="Robote 20", bg="white", fg="black", relief=GROOVE)
text1.place(x=0, y=0, width=320, height=295)
scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=295)  # Adjusted the height
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

#Creates a frame (frame3) with a black groove border (relief=GROOVE), a background color of #2f4155, a width of 330 pixels, and a height of 100 pixels. It is positioned at coordinates (10, 370) within the main Tkinter window.
frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

#Buttons of frame3
# The first button ("Open Image") is associated with the showimage function when clicked. It is positioned at (20, 30).
Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showimage).place(x=20, y=30)

# The second button ("Save Image") is similar to the first button but is associated with the save function. It is positioned at (180, 30).
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)

# The label displays the text "Picture, Image, Photo File" with a background color of #2f4115 and text color of yellow. It is positioned at (20, 5).
Label(frame3, text="Picture, Image, Photo File", bg="#2d4155", fg="yellow").place(x=20, y=5)

# Creates a label to display your name at the bottom center of the main frame.
Label(root, text="Mohd Faziel", bg="#2f4155", fg="white", font=("arial 5 bold")).place(relx=0.5, rely=1, anchor='s')


# Creates a frame (frame4) with similar characteristics to frame3. It is positioned at coordinates (360, 370) within the main Tkinter window.
frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

#Buttons of frame4
# The first button ("Hide Data") is associated with the Hide function when clicked. It is positioned at (20, 30).
Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=Hide).place(x=20, y=30)

#The second button ("Show Data") is similar to the first button but is associated with the Show function. It is positioned at (180, 30).
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", command=Show).place(x=180, y=30)

#The label displays the text "Picture, Image, Photo File" with a background color of #2f4115 and text color of yellow. It is positioned at (20, 5).
Label(frame4, text="Picture, Image, Photo File", bg="#2d4155", fg="yellow").place(x=20, y=5)


#This starts the Tkinter event loop, allowing the GUI to interact with the user.
root.mainloop()
