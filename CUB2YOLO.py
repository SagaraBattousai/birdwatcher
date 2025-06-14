import sys
import os

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




if __name__ == "__main__":
    classmap = getClassMap(DS_ROOT + "/classes.txt")
    print(classmap)
    for dirpath, dirnames, filenames in os.walk(DS_ROOT + "/images"):
        break
        print(dirpath)
    sys.exit(0)
