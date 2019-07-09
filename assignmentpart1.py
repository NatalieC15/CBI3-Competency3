#Applying ICT in a clinical environment assignment part 1
#By Rebecca Sadler and Natalie Card
#Load in the file 'CT.jpg' and display it
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc

plt.rcParams['figure.figsize'] = (16.0, 12.0)

image = misc.imread("CT.jpg",flatten=True)
#plt.imshow(image) 
#plt.show() #this opens the CT image as a separate window

print(image) #this prints the array details of the picture
print(image.shape)#this shows the shape of the image
print(image.dtype)#this shows the image type

#Plot a histogram of the image
fig = plt.figure()

ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax.imshow(image, interpolation="none", cmap="Greys_r")
ax2.hist(image.flatten(), bins=255, facecolor="Red",edgecolor="Black")

plt.show() #This shows the histogram of the image
plt.close()

#write a function to display the CT image with different window levels

def windowfunction(window, level):
    plt.imshow(image, cmap="Greys_r", vmin=(level - (0.5*window)), vmax=(level + (0.5*window)))
    plt.show()
	
#windowfunction(5,2.5)#shows variations in the black background
#windowfunction(8,10)#shows detail of the table and bed
#windowfunction(4,28) #white of the table, person and cloth, background is all black
windowfunction(20,40) #lung
#windowfunction(14,107) #skin
#windowfunction(12,120)#shows soft tissue contrast and bone structure in white

plt.close