from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from Filtering import *
from BandFilter import *
from notch import *
import cv2

root = Tk()
def browseFile():
    browseFile.filename = askopenfilename()
    image = Image.open(browseFile.filename)
    image = image.resize((200, 200), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image1 = Label(root, image=photo)
    image1.image = photo
    image1.place(x=250, y=150)



def convert():
    img = cv2.imread(browseFile.filename, 0)
    filtertype=tkVarPass.get()
    if(tkVarFilter.get()=='Normal Filter'):
        if (tkVarPass.get()=='Butterworth Low Pass')or (tkVarPass.get()=='Butterworth High Pass'):
            order = int(change_dropdown.orderEntry.get())
            filterimage,mask = filtering_order(img, int( cutOffEntry.get()),filtertype,order)
        else:
            filterimage, mask = filtering(img, int(cutOffEntry.get()), filtertype)
    elif (tkVarFilter.get() == 'Band Filter'):
        if (tkVarPass.get() == 'Butterworth Low Pass') or (tkVarPass.get() == 'Butterworth High Pass'):
            order = int(change_dropdown.orderEntry.get())
            filterimage, mask = filtering_band_filter_order(img, int(cutOffEntry.get()), int(change_dropdown.WidthEntry.get()),order,filtertype)
        else:
            filterimage, mask = filtering_band_filter(img, int(cutOffEntry.get()), int(change_dropdown.WidthEntry.get()),filtertype)
    else:
        filterimage, mask = filtering(img, int(cutOffEntry.get()), filtertype='Ideal Low Pass')

    imagejpg = Image.fromarray(filterimage)
    imagejpg.save("output.jpg")
    image = Image.open("output.jpg")
    image = image.resize((200, 200), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image2 = Label(root, image=photo)
    image2.image = photo
    image2.place(x=730, y=150)


    imagejpg = Image.fromarray(mask)
    imagejpg.save("outputimage.jpg")
    image = Image.open("outputimage.jpg")
    image = image.resize((200, 200), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image2 = Label(root, image=photo)
    image2.image = photo
    image2.place(x=950, y=150)

    #cutOffEntry.pack()
def notch():
    img = cv2.imread(browseFile.filename, 0)
    filterimage,mask=notch_filter(img)
    imagejpg = Image.fromarray(filterimage)
    imagejpg.save("output.jpg")
    image = Image.open("output.jpg")
    image = image.resize((200, 200), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image2 = Label(root, image=photo)
    image2.image = photo
    image2.place(x=730, y=150)

    imagejpg = Image.fromarray(mask)
    imagejpg.save("outputimage.jpg")
    image = Image.open("outputimage.jpg")
    image = image.resize((200, 200), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image2 = Label(root, image=photo)
    image2.image = photo
    image2.place(x=950, y=150)


def saveImage():
    print('saving image')


#window size
root.geometry('1200x700')

# #placement of image
photo = PhotoImage(file="200x200.png")
image1= Label(root,image=photo)
image1.place(x=250,y=150)

#placement of the changed image
image2= Label(root,image=photo)
image2.place(x=730,y=150)

#title details
title = Label(root, text="FREQUENCY FILTERING", bg="white", fg="black")
#placing the title top center
title.place(x=540, y=0)

browseImage =Button(root,text="Browse Image", bg="white",fg="black",command=browseFile)
browseImage.place(x=300,y=400)


#saveImage = Button(root,text="Save Image", bg="white", fg="black",command=saveImage)
#saveImage.place(x=800,y=400)

convertImage = Button(root,text="Click here\nto Convert", bg="white", fg="black",command=convert)
convertImage.place(x=565,y=200)



#############################Filter type#############################################
#label for filter type
filterType= Label(root,text="Filter Type",bg='white', fg="black")
filterType.place(x=330,y=505)
# Create a Tkinter variable Filter
tkVarFilter = StringVar(root)

# Dictionary for filter
filters = {
    'Normal Filter',
    'Band Filter',
    }
tkVarFilter.set('None') #sets to default

#Drop down gui for filter
popupMenuFilter = OptionMenu(root,tkVarFilter,*filters)
popupMenuFilter.place(x=300,y=525)

#cutoff lable
cutOff = Label(root, text="Cutoff", fg="black")
cutOff.place(x=565, y=500)

#cutoff user input
cutOffEntry = Entry(root,width=10)
cutOffEntry.place(x=615,y=500)
cutOffEntry.insert(0,'50')
#function for what each type of drop down will do
def change_dropdown(self,*args):
    if tkVarFilter.get() == 'Normal Filter':
        Width = Label(root, text="                                       ")
        Width.place(x=565, y=550)

    if tkVarFilter.get() == 'Band Filter':
        Width = Label(root, text="Width", fg="black")
        Width.place(x=565, y=550)
        change_dropdown.WidthEntry = Entry(root, width=10)
        change_dropdown.WidthEntry.place(x=615, y=550)
        change_dropdown.WidthEntry.insert(0, '10')


convertImage = Button(root, text="Band Notch", bg="white", fg="black", command=notch)
convertImage.place(x=565, y=250)
# link function to change filter dropdown
tkVarFilter.trace('w', change_dropdown)
##################################Pass Type####################################################
#print(tkVarFilter.get())
# Create a Tkinter variable pass
tkVarPass = StringVar(root)
# Dictionary for the passes
passes = {
    'Ideal Low Pass',
    'Ideal High Pass',
    'Butterworth Low Pass',
    'Butterworth High Pass',
    'Gaussain Low Pass',
    'Gaussian High Pass'}
tkVarPass.set('None                  ') #sets to default

#Drop down gui for passes
popupMenuPass = OptionMenu(root,tkVarPass,*passes)
popupMenuPass.place(x=300,y=550)

#function for what each type of drop down will do
def change_dropdown(*args):
    if tkVarPass.get() == 'Butterworth Low Pass':
        print("in")
        lowInput= None
        order = Label(root,text="Order ",fg="black")
        order.place(x=565,y=525)
        #places an input box for the user
        change_dropdown.orderEntry = Entry(root,width=10)
        change_dropdown.orderEntry.place(x=615, y=525)
        change_dropdown.orderEntry.insert(0, '2')
        #print(orderEntry.get())
    if tkVarPass.get() == 'Butterworth High Pass':
        order = Label(root,text="Order ", fg="black")
        order.place(x=565,y=525)
        # places an input box for the user
        change_dropdown.orderEntry = Entry(root,width=10)
        change_dropdown.orderEntry.place(x=615, y=525)
        change_dropdown.orderEntry.insert(0,'2')
    #from here on these passes will display over the Order label and user entry to block
    if tkVarPass.get() == 'Gaussain Low Pass':
        order = Label(root,text="                                        ")
        order.place(x=565,y=525)
    if tkVarPass.get() == 'Gaussian High Pass':
        order = Label(root,text="                                        ")
        order.place(x=565,y=525)
    if tkVarPass.get() == 'Ideal High Pass':
        order = Label(root, text="                                       ")
        order.place(x=565, y=525)
    if tkVarPass.get() == 'Ideal Low Pass':
        order = Label(root, text="                                       ")
        order.place(x=565, y=525)
# link function to change pass dropdown
tkVarPass.trace('w', change_dropdown)
##############################################################################

root.mainloop()