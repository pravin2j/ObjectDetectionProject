# importing libraries and modules
import os
import sys
from imageai.Detection import *
#from imageai.Detection import ObjectDetection
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import tkinter.messagebox as messagebox

#resource path function to locate resources
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#loading the model 
recognizer = ObjectDetection()
path_model = resource_path(r"Object_Detection\Models\yolov3.pt")
recognizer.setModelTypeAsYOLOv3()
recognizer.setModelPath(path_model)
recognizer.loadModel()


# main window
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.title("Object Detection Project")
root.config(bg="#1e1e1e")
root.iconbitmap(resource_path(r"Object_Detection\icon.ico"))

# project title frame
frame = Frame(root, background="white")
frame.place(relx=.5, rely=0.05, anchor="center")
label0 = Label(frame, text="OBJECT DETECTION", font=("Arial", 20, "bold"),
               background="#519aba", foreground="white", padx=10000, pady=10)
label0.pack()

# frame to browse device to select image
frame1 = Frame(root, bg="#1e1e1e", height=20, width=100)
frame1.place(relx=0.5, rely=0.15, anchor="center")

label1 = Label(frame1, text="Select Image:", font=("Arial", 12, "bold"),
               foreground="white", background="#519aba")
entry1 = Entry(frame1, background="gray", bd=3, foreground="White", width=40)
button1 = Button(frame1, text="Browse", command=lambda: select_file(),
                 cursor="hand2")
label1.grid(row=0, column=0)
entry1.grid(row=0, column=1)
button1.grid(row=0, column=2)

# function that browses and selects image
file = None
label_input_image = Label()


def select_file():
    try:
        file_formats = [("JPG Files", "*.jpg")]
        global file
        file = askopenfile(
            title="Choose Image file",
            mode='r',
            filetypes=file_formats)
        # print("File selected: ",str(file.name))
        entry1.delete(0, 'end')
        entry1.insert(END, str(file.name))
        file.close()
        file1 = Image.open(file.name)
        width1, height1 = file1.size
        if (10000 > width1 > 500):
            file1 = file1.resize((int(width1 / 5), int(height1 / 5)))
        file2 = ImageTk.PhotoImage(file1)
        file1.close()
        global label_input_image
        label_input_image = Label(frame2, image=file2)
        label_input_image.image = file2
        label_input_image.place(relx=0.5, rely=.5, anchor="center")
    except:
        messagebox.showerror("Error","Could not load/find image, Please try again with a .jpg image!")


# function to display output image
output_image = resource_path(r"Object_Detection\Output\newimage.jpg")
button_output_image = Label()


def output_display():
    o_file = Image.open(output_image)
    width1, height1 = o_file.size
    # resized = None
    if (10000 > width1 > 500):
        o_file = o_file.resize((int(width1 / 6), int(height1 / 6)))
    file_2 = ImageTk.PhotoImage(o_file)
    global button_output_image
    button_output_image = Button(frame4, image=file_2,
                                 command=lambda:open_output(),
                                 cursor="hand2")
    button_output_image.image = file_2
    button_output_image.place(relx=0.5, rely=.5, anchor="center")


# function to detect objects in the image
def start_detection():
    try:
        #recognizer = ObjectDetection()

        path_input = (entry1.get())
        path_output = output_image
        recognition = recognizer.detectObjectsFromImage(
            input_image=path_input,
            output_image_path=path_output
        )
        if (recognition == []):
            messagebox.showwarning("Warning","Could not Detect objects in the image!")
        else:
            text.insert(END, "Object  :")
            text.insert(END, " Percentage-Probability")
            text.insert(END, "\n")
            for eachItem in recognition:
                confirm_str = ""
                if eachItem["percentage_probability"] >=50.0:
                    confirm_str = "(Object Confirmed)"
                else:
                    confirm_str = "(Object Not Confirmed)"

            #print(eachItem["name"], " : ", eachItem["percentage_probability"])
                text.insert(END, str(eachItem["name"]))
                text.insert(END, " : ")
                text.insert(END, str(eachItem["percentage_probability"]))
                text.insert(END, " : ")
                text.insert(END, confirm_str)
                text.insert(END, "\n")
            output_display()
            messagebox.showinfo("Information", "Detection Sucessfull")
        

    except Exception as e:
        error_message()


# error displaying function

def error_message():

    messagebox.showerror('Application Error',
                         "Error: Something went wrong.\nThere is some error Try Again!")


# function to clear log

def clear_log():
    text.delete("1.0", "end")
    label_input_image.destroy()
    button_output_image.destroy()

# function to view full output image


def open_output():
    image=Image.open(resource_path(r"Object_Detection/Output/newimage.jpg"))
    image.show()
    image.close()


# input image display frame
frame2 = Frame(root, bg="gray", width=400, height=400)
frame2.place(relx=0.2, rely=0.5, anchor="center")

label2 = Label(frame2, text="No file selected", bg="gray", fg='White',
               font=("Arial", 14, "bold"))
label2.place(relx=0.5, rely=0.5, anchor="center")

# frame to display output data detected by imageAI
frame3 = Frame(root, bg="#1e1e1e", width=400, height=400)
frame3.place(relx=.5, rely=.5, anchor="center")

label3 = Label(frame3, text="Detected Objects:", font=("Arial", 14, "bold"),
               fg="white", bg="#1e1e1e")
label3.place(relx=.01, rely=.01)
text = Text(frame3, width=50, height=18,
            background="#2f4b6b",foreground="white",bd=3,
            font=("Arial",11,"bold"))
text.place(relx=0.5, rely=.5, anchor="center")

# frame to display output image
frame4 = Frame(root, bg="gray", width=400, height=400)
frame4.place(relx=.8, rely=.5, anchor="center")

label4 = Label(
    frame4,
    text="Output image will\nbe displayed Here",
    bg="gray",
    fg='White',
    font=("Arial",14,"bold"))
label4.place(relx=0.5, rely=0.5, anchor="center")

# frame to store "start" button and "view output" button
frame5 = Frame(root, width=100, height=50)
frame5.place(relx=.5, rely=.8, anchor="center")

button3 = Button(
    text="Clear log",
    bd=3,
    font=("Arial",10,"bold"),
    fg="white",
    bg="red",
    command=lambda: clear_log(),
    cursor="hand2")
button3.place(x=810, y=180)

button4 = Button(
    text="View output",
    bd=3,
    font=("Arial",10,"bold"),
    fg="white",
    bg="blue",
    command=lambda: open_output(),
    cursor="hand2")
button4.place(x=638, y=650)

start_btn = Button(
    frame5,
    text="Start",
    background="#519aba",
    fg="White",
    font=("Arial",20,"bold"),
    padx=20,
    pady=5,
    command=lambda: start_detection(),
    cursor="hand2")
start_btn.pack()

#tkinter mainloop
root.mainloop()