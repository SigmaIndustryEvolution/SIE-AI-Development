import os
from PIL import Image, ImageOps

LINE_CLEAR = '\x1b[2K'
LINE_UP = '\033[1A'

def main():
    root = r'data'
    numberOfRotatedImages = 0
    for foldername, subfolders, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    image = Image.open(os.path.join(foldername, filename))
                    image = ImageOps.exif_transpose(image, True)
                    image.save(os.path.join(foldername, filename))
                    numberOfRotatedImages += 1
                    print(LINE_UP, end = LINE_CLEAR)
                    print("Rotating image")
                except:
                    print(LINE_UP, end = LINE_CLEAR)
                    print("No exif information, image is probably rotated")
                    
    print(f"{numberOfRotatedImages} number of images was rotated to portrait mode")


if __name__ == '__main__':
	# Calling main() function
    main()