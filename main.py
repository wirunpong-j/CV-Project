from Tkinter import *
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import cv2
import imutils
import imageScanner
import tkMessageBox
import numpy

# grab a reference to the image panels
panelA = None
panelB = None
result = None


def select_image():

    global panelA
    global panelB
    global result
 
    # open a file chooser dialog and allow the user to select an input
    # image
    path = tkFileDialog.askopenfilename()

    # ensure a file path was selected
    if len(path) > 0:
        # load the image from disk, convert it to grayscale, and detect
        # edges in it
        image = cv2.imread(path)
        image = imutils.resize(image, height = 700)
        # edged = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # edged = cv2.Canny(gray, 50, 100)
        result = imageScanner.scanImage(path, 2)

        result_Resize = imutils.resize(result, height = 700)
 
        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
        # convert the images to PIL format...
        arr_image = Image.fromarray(image)
        arr_result = Image.fromarray(result_Resize)
 
        # ...and then to ImageTk format
        arr_image = ImageTk.PhotoImage(arr_image)
        arr_result = ImageTk.PhotoImage(arr_result)
        # if the panels are None, initialize them
        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=arr_image)
            panelA.image = arr_image
            panelA.pack(side="left", padx=10, pady=10)
 
            # while the second panel will store the edge map
            panelB = Label(image=arr_result)
            panelB.image = arr_result
            panelB.pack(side="right", padx=10, pady=10)
 
        # otherwise, update the image panels
        else:
            # update the pannels
            updatePanels(panelA, panelB, arr_image, arr_result)


def flipImage():
    global result

    if (panelA == None or panelB == None):
        tkMessageBox.showinfo("ERROR", "Please select image.")
    else:
        result = cv2.flip(result, 0)
        result = cv2.flip(result, 1)
        result_Resize = imutils.resize(result, height = 700)
        arr_result = Image.fromarray(result_Resize)
        arr_result = ImageTk.PhotoImage(arr_result)
        updatePanels(panelA, panelB, None, arr_result)
    

def updatePanels(panelA, panelB, arr_image, arr_result):
    if arr_image != None:
        panelA.configure(image=arr_image)
        panelA.image = arr_image
    panelB.configure(image=arr_result)
    panelB.image = arr_result


def saveImage():
    try:
        if (panelA == None or panelB == None):
            tkMessageBox.showinfo("ERROR", "Please select image.")
        else:
            filename = tkFileDialog.asksaveasfilename(initialdir = "/", title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
            if (filename):
                cv2.imwrite(filename, result)

    except:
        tkMessageBox.showinfo("ERROR", "Invalid file name.")

    

# initialize the window toolkit along with the two image panels
root = Tk()
panelA = None
panelB = None

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

saveBtn = Button(root, text="Save Image", command=saveImage)
saveBtn.pack(side="bottom", fill="both", expand="yes", padx="5", pady="5")

flipBtn = Button(root, text="Flip Image", command=flipImage)
flipBtn.pack(side="bottom", fill="both", expand="yes", padx="5", pady="5")

# kick off the GUI
root.mainloop()


