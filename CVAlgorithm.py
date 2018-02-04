import cv2
import numpy
import sys
from Queue import Queue
from PIL import Image



maze_image = cv2.imread('testfive.jpg')

maze_image_black_and_white = cv2.cvtColor( maze_image, cv2.COLOR_BGR2GRAY )

unneeded_object, maze_image_thresholded = cv2.threshold( maze_image_black_and_white, 127, 255, cv2.THRESH_BINARY)

maze_image_height, maze_image_width =  maze_image.shape[ : 2 ]

start = (21, 495)

end = (508,517)

def iswhite(value):
    if value == 255:
        return True

def getadjacent(n):
    x,y = n

    if x >= maze_image_width -1 or x <= 0 or y >= maze_image_height-1 or y <=0:
        return []

    return [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]

def BFS(start, end, pixels):
    queue = Queue()
    queue.put([start]) # Wrapping the start tuple in a list

    while not queue.empty():

        path = queue.get()
        pixel = path[-1]

        if pixel == end:
            return path

        if getadjacent(pixel) == None:
            continue

        for adjacent in getadjacent(pixel):
            x,y = adjacent

            if iswhite( pixels[ x,y ] ):
                print(x,y)
                pixels[x,y] = 127 # see note
                new_path = list(path)
                new_path.append(adjacent)
                queue.put(new_path)

    print "Queue has been exhausted. No answer was found."



kernel_height = maze_image_height // 100

kernel_width = maze_image_width // 100

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ( kernel_width,kernel_height ) )

maze_image_with_closed_pixels = cv2.morphologyEx( maze_image_thresholded, cv2.MORPH_CLOSE, kernel )

unneeded_object, maze_image_with_closed_pixels = cv2.threshold( maze_image_with_closed_pixels, 127, 255, cv2.THRESH_BINARY )

final_maze_image = Image.fromarray(  maze_image_with_closed_pixels )  ##########

final_maze_image.save( "temporary_results.jpg" )  ##############



base_img = Image.open( 'temporary_results.jpg' ) # Image.open('temporary_results.jpg')

base_pixels = base_img.load()

path = BFS(start, end, base_pixels)

path_img = Image.open('temporary_results.jpg')
path_pixels = path_img.load()

for position in path:

    x,y = position

    path_pixels[x,y] = 127

path_img.save("final_resultsAA.jpg")
