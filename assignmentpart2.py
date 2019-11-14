# Applying ICT in a clinical environment assignment part 2

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import misc
# from scipy.ndimage import interpolation
# from scipy.ndimage import rotate

# Task 1: Load image of lung1 and lung2 and plot figure with multiple subplots
# plt.rcParams['figure.figsize'] = (16.0, 12.0)

# lungs1 = misc.imread("lungs.jpg",flatten=True)
# lungs2 = misc.imread("lungs2.jpg",flatten=True)

# Task 2: Displaying both images on to the same axes using transparency and colour maps
# keep lungs1 fixed and lungs2 as being able to move
# fig = plt.figure()
# ax = fig.add_subplot(111)

# ax.imshow(lungs1,alpha=1, cmap="Greens_r") #looks purple
# floating = ax.imshow(lungs2, alpha=0.5, cmap="Purples_r") #looks green
# plt.show()

# Task 3: Function to shift the floating image
# def shiftImages(shift):
#    global lungs2
#    #global floating
#    lungs2 = interpolation.shift(lungs2, shift, mode="nearest")
#    floating.set_data(lungs2)
#    fig.canvas.draw()

# xiii
# shiftImages([-25,-50]) #moves the image up 25 pixels and left 50 pixels
# plt.show()
# plt.close()

import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from scipy.ndimage import interpolation
from scipy.ndimage import rotate

# Task 1: Load image of lung1, lung2 and lung 3 and overlay them

plt.rcParams['figure.figsize'] = (16.0, 12.0)

lungs1 = misc.imread("lungs.jpg", flatten=True)
lungs2 = misc.imread("lungs2.jpg", flatten=True)
lungs3 = misc.imread("lungs3.jpg", flatten=True)

# Task 2: Displaying both images on to the same axes using transparency and colour maps
# keep lungs1 fixed and lungs2 as being able to move
fig = plt.figure()
ax = fig.add_subplot(111)

ax.imshow(lungs1,alpha=1, cmap="Greens_r") #looks purple
# floating = ax.imshow(lungs2, alpha=0.5, cmap="Purples_r") #looks green
floating = ax.imshow(lungs3, alpha=0.5, cmap="Blues_r") #looks green
# plt.show()


# Task 3: Apply appropriate shifts and rotations to make the images overlap
# Function to shift the floating image
# Function to rotate the rotating image

def shiftImages(shift):
    global lungs3
    lungs3 = interpolation.shift(lungs3, shift, mode="nearest")
    floating.set_data(lungs3)
    fig.canvas.draw()


def rotateImages(rotates):
    global lungs3
    lungs3 = rotate(lungs3, rotates, reshape=False)
    floating.set_data(lungs3)
    fig.canvas.draw()

# replaced rotating with floating on lungs 3 - see if works
# shiftImages([-25,-50])  # moves the image up 25 pixels and left 50 pixels
# rotateImages(-5)  # rotates the image
# plt.show()
# plt.close()

# Task 4: Map left and right shifts to left and right keys
# Task 5: Map up and down shifts to up and down keys
# Task 6: Map rotations
# manual movement of the image using special keys from the keyboard
# the keys are up, down, left and right for shifting. alt+left and alt+right are for rotating


def eventHandler(event):
    whichKey = event.key
    if whichKey == "up":
        shiftImages((-1, 0))
    elif whichKey == "down":
        shiftImages((1, 0))
    elif whichKey == "left":
        shiftImages((0, -1))
    elif whichKey == "right":
        shiftImages((0, 1))
    elif whichKey == "alt+left":
        rotateImages(1)
    elif whichKey == "alt+right":
        rotateImages(-1)


# Task 7: Use the code to align the images
fig.canvas.draw()
fig.canvas.mpl_connect('key_press_event', eventHandler)
plt.show()
