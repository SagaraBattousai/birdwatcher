import sys
import os

from PIL import Image

DS_ROOT: str = "CUB_200_2011_YOLO"


# Usually want to convert the otherway around (like for translating a prediction)
# However as this is for converting the dataset we want it this way around
def getClassMap(mapfile: str) -> dict[str, int]:
    classmap = {}
    with open(mapfile, "rt") as mf:
        line = mf.readline()
        while line != "":
            # Could try catch to enforce format of mapfile but for now....
            class_index, class_name = line.split(" ", maxsplit=1)
            # classname strips the three digit code and . and the \n from the end
            # class_index is -1 to convert to zero indexed
            classmap[class_name[4:-1]] = int(class_index) - 1
            line = mf.readline()
    return classmap


# ANSWER = ((121, 'Parakeet_Auklet_0032_795986.jpg'), (120, 'Pomarine_Jaeger_0007_795764.jpg'))
def getMinImageDimensions(
    images_root_dir: str,
) -> tuple[tuple[int, str], tuple[int, str]]:
    minWidth = (65535, "")
    minHeight = (65535, "")

    for dirpath, dirnames, filenames in os.walk(images_root_dir):
        #As is the case of the root dir and theoretically any empty dirs
        if len(filenames) == 0:
            continue
        for imagefile in filenames:
            with Image.open(f"{dirpath}/{imagefile}") as image:
                if image.width < minWidth[0]:
                    # minWidth[0] = image.width
                    # minWidth[1] = imagefile
                    minWidth = (image.width, imagefile)
                if image.height < minHeight[0]:
                    minHeight = (image.height, imagefile)

    return (minWidth, minHeight)


if __name__ == "__main__":
    classmap = getClassMap(DS_ROOT + "/classes.txt")
    print(classmap)

    minDims = getMinImageDimensions(DS_ROOT + "/images")
    print(minDims)
    sys.exit(0)
