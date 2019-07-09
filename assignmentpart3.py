#Applying ICT in a clinical environment assignment part 3
#By Rebecca Sadler and Natalie Card
from scipy.optimize import minimize, basinhopping, brute, differential_evolution
from scipy.ndimage import interpolation
import matplotlib.pyplot as plt
from scipy import misc
import numpy as np
import dicom

# Step 1: Load the four lung images from their DICOM files:
# The file names are IMG-0004-0000N.dcm where N is between 1 and 4
# Hint: the function you need is read_file in the dicom module
# Hint: you need to get the pixel array from the dicom object
# Hint: to make life easier, declare all the images global

global Image1
global Image2
global Image3
global Image4

Image1 = dicom.read_file("IMG-0004-00001.dcm").pixel_array
Image2 = dicom.read_file("IMG-0004-00002.dcm").pixel_array
Image3 = dicom.read_file("IMG-0004-00003.dcm").pixel_array
Image4 = dicom.read_file("IMG-0004-00004.dcm").pixel_array

# Now visualise one of the images to make sure it loaded okay
# Hint: this is just a quick check, should be doable in 2 lines!
#plt.imshow(patientImage4)#tested to check that all the images load correctly
#plt.show()

# Step 2: Modify your code from yesterday to enable automatic registration
# Hint: copy your shiftImages() function here, then tweak it to return a cost
# The shiftImages function
#fig = plt.figure()
#ax = fig.add_subplot(111)

#ax.imshow(Image1,alpha=1, cmap="Greens_r") #green in colour
#floating = ax.imshow(Image2, alpha=0.5, cmap="Purples_r") #purple colour
#floating = ax.imshow(Image3, alpha=0.5, cmap="Blues_r") #blue colour
#floating = ax.imshow(Image4, alpha=0.5, cmap="Oranges_r") #orange colour
#plt.show()

#Cost function
def costFunction(Image1, Image2):
    return np.mean((Image1 - Image2)**2)

#Shift function
def shiftImages(shift, image):
    global Image1
    global Image2
    global Image3
    global Image4
    Image_temp = interpolation.shift(image, shift, mode="nearest")
    #floating.set_data(Image_temp)
    #fig.canvas.draw()
    cost = costFunction(Image1, Image_temp)
    #ax.set_title("Cost = {}".format(cost))
    #plt.pause(0.001)
    return cost
#shiftImages([-25,-50])

def shiftImages2(shift, image):
    global Image1
    global Image2
    global Image3
    global Image4
    Image_temp = interpolation.shift(image, shift, mode="nearest")
    floating.set_data(Image_temp)
    fig.canvas.draw()
    cost = costFunction(Image1, Image_temp)
    ax.set_title("Cost = {}".format(cost))
    return Image_temp

#plt.show()

#Rotate function
#def rotateImages(rotates):
#    global Image2
#    Image2_temp = rotate(Image2, rotates, reshape=False)
#    floating.set_data(Image2_temp)
#    fig.canvas.draw()
#    cost = costFunction(Image1, Image2_temp)
#    ax.set_title()
#    return cost

# Step 3: Now we can implement an automatic optimiser. The brute force algorithm
# is a good one to start with.
# Hint: Identify which function you want to minimise
# Hint: the brute force optimiser takes parameter limits in a tuple of tuples
# documentation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brute.html

#Brute force optimisation
#res = brute(shiftImages, ((-100, 100),(-100, 100)), (Image2,))
#print(res)

# Step 4: The automatic registration will return a shift that it thinks best registers the images.
# Use your shift function to apply the registration, then visualise the result on a
# green/purple plot. Does it look okay?
# Hint: re-use some of the code from yesterday

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(Image1,alpha=1, cmap="Greens_r") #green in colour
floating = ax.imshow(Image2, alpha=0.5, cmap="Purples_r") #purple colour

def registerImages(Image1st, Image2nd):
    global res
    res = brute(shiftImages, ((-100, 100),(-100, 100)), (Image2nd,))
    print (res)
	
registerImages(Image1, Image2)
shiftImages2(res, Image2)

plt.show()
    
exit()
# Step 5: Below is some code to implement a clipbox you can use to select the region of
# image that contains the tumour for further analysis. You need to link up the event
# handlers with the right events so it will work

# Import the bit of matplotlib that can draw rectangles
import matplotlib.patches as patches

# Create a new figure
fig2 = plt.figure(2)
ax = fig2.add_subplot(111)# Stick a subplot into the figure
thePlot = ax.imshow(lungs_1, cmap="Greys_r") # Display the fixed image (your image name may be different)

# Start with a box drawn in the centre of the image
origin = (lungs_1.shape[0]/2, lungs_1.shape[1]/2)
rectParams = [origin[0], origin[1], 10, 10]
# Draw a rectangle in the image
# Question: why are x and y the other way round here?
rect = patches.Rectangle((rectParams[1], rectParams[0]),rectParams[2], rectParams[3], linewidth=2, edgecolor='r',facecolor='none')

ax.add_patch(rect)

global initPos
initPos = None

# Event handlers for the clipbox
def onPress(event):
    """
    This function is called when you press a mouse button inside the figure window
    """
    if event.inaxes == None:
        return# Ignore clicks outside the axes
    contains, attr = rect.contains(event)
    if not contains:
        return# Ignore clicks outside the rectangle

    global initPos # Grab the global variable to update it
    initPos = [rect.get_x(), rect.get_y(), event.xdata, event.ydata]

def onMove(event):
    """
    This function is called when you move the mouse inside the figure window
    """
    global initPos
    if initPos is None:
        return# If you haven't clicked recently, we ignore the event

    if event.inaxes == None:
        return# ignore movement outside the axes

    x = initPos[2]
    y = initPos[3]
    dx = event.xdata - initPos[2]
    dy = event.ydata - initPos[3]
                                    # This code does the actual move of the rectangle
    rect.set_x(initPos[0] + dx)
    rect.set_y(initPos[1] + dy)

    rect.figure.canvas.draw()

def onRelease(event):
    """
    This function is called whenever a mouse button is released inside the figure window
    """
    global initPos
    initPos = None # Reset the position ready for next click

def keyboardInterface(event):
    """
    This function handles the keyboard interface. It is used to change the size of the
    rectangle.
    """
    if event.key == "right":
        # Make the rectangle wider
        w0 = rect.get_width()
        rect.set_width(w0 + 1)
    elif event.key == "left":
        # Make the rectangle narrower
        w0 = rect.get_width()
        rect.set_width(w0 - 1)
    elif event.key == "up":
        # Make the rectangle shorter
        h0 = rect.get_height()
        rect.set_height(h0 - 1)
    elif event.key == "down":
        # Make the rectangle taller
        h0 = rect.get_height()
        rect.set_height(h0 + 1)
################################################################################
# The functions below here will need to be changed for use on Windows!
    elif event.key == "cmd+right":
        # Make the rectangle wider - faster
        w0 = rect.get_width()
        rect.set_width(w0 + 10)
    elif event.key == "cmd+left":
        # Make the rectangle narrower - faster
        w0 = rect.get_width()
        rect.set_width(w0 - 10)
    elif event.key == "cmd+up":
        # Make the rectangle shorter - faster
        h0 = rect.get_height()
        rect.set_height(h0 - 10)
    elif event.key == "cmd+down":
        # Make the rectangle taller - faster
        h0 = rect.get_height()
        rect.set_height(h0 + 10)

    rect.figure.canvas.draw()# update the plot window

# These need connecting to the right functions
cid1 = fig2.canvas.mpl_connect('button_press_event', )
cid2 = fig2.canvas.mpl_connect('motion_notify_event', )
cid3 = fig2.canvas.mpl_connect('button_release_event', )
cid4 = fig2.canvas.mpl_connect('key_press_event', )

plt.show()

indices = [int(rect.get_y()), int(rect.get_y() + rect.get_height()), int(rect.get_x()), int(rect.get_x() + rect.get_width())]
print(indices)
exit()
# Step 6: You should now have all four images registered in the same location, and a set of image indices
# that crop out just the region you're interested in. Use image processing tecniques to extract
# the volume of thr tumour in each image
# Hint: Start by extracting the volume in just the first image
# Hint: Any technique you think will work is fair game!


# Step 7: Now you have four measurements of tumour volume, plot a graph of tumour shrinkage over time
# from your data. Assume the images are taken 5 days apart, and label your axes accordingly.
# Save the plot as a .png image
