import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path

import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

top=tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image !')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

def select_image():
    image_path=easygui.fileopenbox()
    cartooning_image(image_path)


def cartooning_image(image_path):
    # read the image
    selected_image_from_device = cv2.imread(image_path)
    selected_image_from_device = cv2.cvtColor(selected_image_from_device, cv2.COLOR_BGR2RGB)
    #print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if selected_image_from_device is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    resized_image_1 = cv2.resize(selected_image_from_device, (960, 960))
    #plt.imshow(resized_image_1, cmap='gray')


    #converting an image to grayscale
    gray_scale_image= cv2.cvtColor(selected_image_from_device, cv2.COLOR_BGR2GRAY)
    resized_image_2 = cv2.resize(gray_scale_image, (960, 960))
    #plt.imshow(resized_image_2, cmap='gray')


    #applying median blur to smoothen an image
    blur_image = cv2.medianBlur(gray_scale_image, 5)
    resized_image_3 = cv2.resize(blur_image, (960, 960))
    #plt.imshow(resized_image_3, cmap='gray')

    #retrieving the edges for cartoon effect
    #by using thresholding technique
    detecting_edges_in_body = cv2.adaptiveThreshold(blur_image, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    resized_image_4 = cv2.resize(detecting_edges_in_body, (960, 960))
    #plt.imshow(resized_image_4, cmap='gray')

    #applying bilateral filter to remove noise 
    #and keep edge sharp as required
    colored_blur_image = cv2.bilateralFilter(selected_image_from_device, 9, 300, 300)
    resized_image_5 = cv2.resize(colored_blur_image, (960, 960))
    #plt.imshow(resized_image_5, cmap='gray')


    #masking edged image with our "BEAUTIFY" image
    cartooned_image = cv2.bitwise_and(colored_blur_image, colored_blur_image, mask=detecting_edges_in_body)

    resized_image_6 = cv2.resize(cartooned_image, (960, 960))
    #plt.imshow(resized_image_6, cmap='gray')

    # Plotting the whole transition
    collecting_images=[resized_image_1, resized_image_2, resized_image_3, resized_image_4, resized_image_5, resized_image_6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(collecting_images[i], cmap='gray')

    save_image=Button(top,text="Save cartoon image",command=lambda: save_cartooned_image(resized_image_6, image_path),padx=30,pady=5)
    save_image.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save_image.pack(side=TOP,pady=50)
    
    plt.show()
    
    #end.
    
    
def save_cartooned_image(resized_image_6, image_path):
    #saving an image using imwrite()
    name_for_file_after_saving="cartoonified_Image"
    path1 = os.path.dirname(image_path)
    extension=os.path.splitext(image_path)[1]
    path = os.path.join(path1, name_for_file_after_saving+extension)
    cv2.imwrite(path, cv2.cvtColor(resized_image_6, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + name_for_file_after_saving +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

select_image=Button(top,text="Cartoonify an Image",command=select_image,padx=10,pady=5)
select_image.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
select_image.pack(side=TOP,pady=50)

top.mainloop()



