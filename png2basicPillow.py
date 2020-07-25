from PIL import Image, ImageDraw
import array as arr


def get_buckets_255(n):
    """Take a value normalize it to one of 4 values to be used for a 16 bit colors

    Args:
        n is the input value

    """
    bucket = 0
    if (n < 44):
        bucket = 0
    if (n > 43 and n < 128):
        bucket = 85
    if (n > 127 and n < 213):
        bucket = 170
    if (n > 212):
        bucket = 255
    #print("empty bucket", bucket)
    return bucket

def get_EGA16_Basic(red,green,blue):
    """Convert an INT RDB value into a Hackaday Basic command

    Args:
        red: an int value for red limited for a 16 color pallet
        green: an int value for green limited for a 16 color pallet
        blue: an int value for blue limited for a 16 color pallet


    """
    str_output = " color 0,0"        #making this default off
    if (red is 255 and green is 255 and blue is 255):
        str_output = " color 15,0"  #Bright White
    elif ( red is 255 and green is 255 ):
        str_output = " color 14,0"  #Bright Yellow
    elif ( red is 255 and blue is 255 ):
        str_output = " color 13,0"  #Bright Magenta
    elif ( red is 255 ):
        str_output = " color 12,0"  #Bright Red
    elif ( green is 255 and blue is 255 ):
        str_output = " color 11,0"  #Bright Cyan
    elif ( green is 255 ):
        str_output = " color 10,0"  #Bright Green
    elif ( blue is 255 ):
        str_output = " color 9,0"  #Bright Blue
    elif ( red is 85 and green is 85 and blue is 85 ):
        str_output = " color 8,0"  #Dark Gray
    elif ( red is 170 and green is 170 and blue is 170):
        str_output = " color 7,0"  #Light Gray
    elif ( red is 170 and green is 85 ):
        str_output = " color 6,0"  #Brown
    elif ( red is 170 and blue is 170 ):
        str_output = " color 5,0"  #Magenta
    elif ( red is 170 ):
        str_output = " color 4,0"  #Red
    elif ( green is 170 and blue is 170 ):
        str_output = " color 3,0"  #Cyan
    elif ( green is 170 ):
        str_output = " color 2,0"  #Green
    elif ( blue is 170 ):
        str_output = " color 1,0"  #Blue
        
    return str_output

original_png = 'hard_test.png'
shrunk_png = 'hard_test_shrunk.png'
basic_text = 'basic_06.txt'

output_image_x = 64
output_image_y = 64

im = Image.open(original_png)
rgb_im = im.convert('RGB')
im_shrink = Image.new('RGB',(output_image_x,output_image_y))
rgb_imDraw = ImageDraw.Draw(im_shrink)
rgb_im_shrink = im_shrink.convert('RGB')


orig_x_end,orig_y_end = im.size
print(orig_x_end)
print(orig_y_end)
#The Shrunk Image is 40x20px
box_x_end = int(orig_x_end/output_image_x)
box_y_end = int(orig_y_end/output_image_y)
box_x_start = 0
box_y_start = 0
#Start at 0,0 read all the pixels. Average them.
#Move over by box_x_end until box_x_start >= orig_x_end
x_shrunk = 0
y_shrunk = 0

box_x_step_size = (box_x_end - box_x_start)
box_y_step_size = (box_y_end - box_y_start)

x = 0
y = 0

x_new = 0
y_new = 0

r_temp = 0
g_temp = 0
b_temp = 0
output_text = ''
count = 0
place_holder = ''
text_file = open(basic_text, "w")

print("Start!")
while( (y_new is not (output_image_y)) and (x_new is not output_image_x)):
    arr_r = arr.array('i')
    arr_g = arr.array('i')
    arr_b = arr.array('i')

    red_average = 0
    green_average = 0
    blue_average = 0
    
    for y in range(box_y_start, box_y_end):
        for x in range(box_x_start, box_x_end):
            r, g, b = rgb_im.getpixel((x, y))
            arr_r.append(r)
            arr_g.append(g)
            arr_b.append(b)

    for a in range(0, len(arr_r)):
        red_average = red_average + arr_r[a]
    red_average = int(red_average/(len(arr_r)))
    for a in range(0, len(arr_g)):
        green_average = green_average + arr_g[a]
    green_average = int(green_average /(len(arr_g)))
    for a in range(0, len(arr_b)):
        blue_average = blue_average + arr_b[a]
    blue_average = int(blue_average /(len(arr_b)))
    rgb_imDraw.point((x_new,y_new),(red_average,green_average,blue_average))

    im_shrink.save(shrunk_png,"PNG")
    r_temp = get_buckets_255(red_average)
    g_temp = get_buckets_255(green_average)
    b_temp = get_buckets_255(blue_average)
    
    output_text = get_EGA16_Basic(r_temp,g_temp,b_temp)
    count = count + 10
    output_text = str(count) + output_text +"\n"
    text_file.write(output_text)
    count = count + 10
    output_text = str(count) + " setxy " + str(x_new) + "," + str(y_new) + "\n"
    text_file.write(output_text)
    count = count + 10
    output_text = str(count) + " chr 254 \n"
    text_file.write(output_text)
    
    x_new = x_new + 1

    if (x_new is output_image_x):
        x_new = 0
        y_new = y_new + 1

    box_x_start = box_x_start + box_x_step_size
    box_x_end = box_x_end + box_x_step_size
    if (box_x_end > orig_x_end):
        box_x_start = 0
        box_x_end = box_x_step_size
        box_y_start = box_y_start + box_y_step_size
        box_y_end = box_y_end + box_y_step_size
    
print("done!")
im.close()
im_shrink.close()




im_shrink = Image.open(shrunk_png)
rgb_im_shrink = im_shrink.convert('RGB')

text_file.close()
'''
Ok so what I need to do is look at the image size. Look at a field size
proportional to size of the image.

Stow the pixel information into an array. Take the average of that array.
Write the associated condensed point on the shrunk image.

On the shrunk image is done, make a txt containing the basic commands needed
to draw the screen.

Color Maps

Black 0,0,0 (basic 0)
Blue 0,0,170 (basic 1)
Green 0,170,0 (basic 2)
Cyan 0,170,170 (basic 3)
Red 170,0,0 (basic 4)
Magenta 170,0,170 (basic 5)
Brown 170,85,0 (basic 6)
White/light gray 170,170,170 (basic 7)

Dark gray 85,85,85 (basic 8)
Bright Blue 85,85,255 (basic 9)
Bright Green 85,255,85 (basic 10)
Bright Cyan 85,255,255 (basic 11)
Bright Red 255,85,85 (basic 12)
Bright Magenta 255,85,255 (basic 13)
Bright Yellow 255,255,85 (basic 14)
Bright White 255,255,255 (basic 15)

There are only 4 valid values. Set up buckets for the data.
0    85    170    255
if 0 to 43 then 0
if 43 to 128 then 85
if 129 to 212 then 170
if 213 to 255 then 255

from there use the fixed color values to figure it out.

If any value is 255, then modify the other values


'''

