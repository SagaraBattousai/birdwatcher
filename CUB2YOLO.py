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

    for dirpath, _, filenames in os.walk(images_root_dir):
        # As is the case of the root dir and theoretically any empty dirs
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


# ANSWER = (467.88683406854426, 386.02994570749917)
def getAvgImageDimensions(images_root_dir: str) -> tuple[float, float]:
    total_width = 0
    total_height = 0
    image_count = 0

    for dirpath, _, filenames in os.walk(images_root_dir):
        # As is the case of the root dir and theoretically any empty dirs
        if len(filenames) == 0:
            continue
        for imagefile in filenames:
            with Image.open(f"{dirpath}/{imagefile}") as image:
                total_width += image.width
                total_height += image.height
                image_count += 1

    return (total_width / image_count, total_height / image_count)


# under 128 = (1, 1, 0)
# under 256 = (152, 241, 102) # Thats 291 total images
#
# under 224 = (72, 125, 49) # 148 total *** This is the one!
# under 448 = (2571, 9001, 675) # 10897 total
#
def get_num_images_under_size(
    images_root_dir: str, min_width: int = 256, min_height: int = 256
) -> tuple[int, int, int]:
    under_width_count = 0
    under_height_count = 0
    under_both_count = 0

    for dirpath, _, filenames in os.walk(images_root_dir):
        # As is the case of the root dir and theoretically any empty dirs
        if len(filenames) == 0:
            continue
        for imagefile in filenames:
            with Image.open(f"{dirpath}/{imagefile}") as image:
                if image.width < min_width:
                    under_width_count += 1
                    if image.height < min_height:
                        under_height_count += 1
                        under_both_count += 1
                        # could write continue but elif does that :)
                elif image.height < min_height:
                    under_height_count += 1

    return (under_width_count, under_height_count, under_both_count)


if __name__ == "__main__":
    classmap = getClassMap(DS_ROOT + "/classes.txt")
    print(classmap)

    # minDims = getMinImageDimensions(DS_ROOT + "/images")
    # print(minDims)

    # avgDims = getAvgImageDimensions(DS_ROOT + "/images")
    # print(avgDims)


    under_448 = get_num_images_under_size(DS_ROOT + "/images", 448, 448)
    print(under_448)



    sys.exit(0)
