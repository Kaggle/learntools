import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def load_my_image(fname = '/kaggle/input/dog-breed-identification/train/0246f44bb123ce3f91c939861eb97fb7.jpg'):
    '''returns array containing greyscale values for supplied file (at thumbnail size)'''
    image_color = Image.open(fname).resize((90, 125), Image.ANTIALIAS)
    image_grayscale = image_color.convert('L')
    image_array = np.asarray(image_grayscale)
    return(image_array)

def apply_conv_locally(conv, image_section):
    '''Returns output of applying conv to image_section. Both inputs are numpy arrays.
    image_section is assumed to be same size/shape as conv.
    '''
    out = (conv * image_section).sum()
    return out

def print_hints(conv):
    '''Simple tests on conv array. Prints advice to output. Unique to this exercise'''
    try:
        conv_array = np.array(conv)
    except:
        print("The supplied convolution could not be converted to an array."
              "Is it a nested list containing only numbers? Each sublist "
              " should contain only numbers and have same length")
    assert(conv_array.ndim == 2), "Convolution was " + str(conv_array.ndim) + " dimensions. Should be 2."
    if (conv_array >= 0).all():
        print("All items in the convolutional array were either 0 or positive. This is MIGHT work "
             "but it tends to find bright spots rather than edges/lines. There is a better solution.")
    elif (conv_array <= 0).all():
        print("All items in the convolutional array were either 0 or negative. This is MIGHT work "
             "but it tends to find dark spots rather than edges/lines. There is a better solution.")
    elif (conv_array == 0).all():
        print("All items in the convolutional array were 0.  Try non-zero numbers to capture patterns in the image")
    elif (conv_array[0,0] == conv_array[1,0]) and (conv_array[0,1] == conv_array[1,1]):
        # we've already filtered cases where first column and second column have same sign
        print("Congrats.  That did it.")

def scale_for_display(image):
    '''Scales numpy array containing image data to be integers in range [0, 256]'''
    out = image - image.min()
    out = (out / out.max() * 256)
    return out.astype(int)


def apply_conv_to_image(conv, image):
    '''Applies conv (supplied as list of lists) to image (supplied as numpy array). Returns output array'''
    assert(type(image) == np.ndarray)
    print("----------------------------")
    print("Filter: ")
    print(np.array(conv))
    print_hints(conv)
    image_height, image_width = image.shape
    conv_array = np.array(conv)
    conv_height, conv_width = conv_array.shape
    filtered_image_height = image.shape[0] - conv_height + 1
    filtered_image_width = image.shape[1] - conv_width + 1
    filtered_image = np.zeros((filtered_image_height, filtered_image_width))
    for i in range(filtered_image_height):
        for j in range(filtered_image_width):
            filtered_image[i, j] = apply_conv_locally(conv_array, image[i:i+conv_height, j:j+conv_width])
    return(filtered_image)

def show(image, scale_before_display=True):
    '''Displays numpy array as image.  Scale_before_display ensures values are integers in [0, 256]'''
    if scale_before_display:
        to_display = scale_for_display(image)
    else:
        to_display = image
    plt.imshow(to_display, cmap='gray')
    plt.axis('off')
    plt.show()
