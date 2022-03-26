import numpy as np
from PIL import Image

from config import PATH


def main():
    image_path = f"{PATH}/../../assets/units"
    names = ["swordsman.png", "bowman.png", "cavalry.png", "cannon.png", "pikeman.png"]
    range_of_color = *zip(tuple(range(200, 256)), tuple(range(200, 256)), tuple(range(200, 256))),
    for name in names:
        im = Image.open(f"{image_path}/{name}")
        im = im.convert(mode="RGBA")
        img_arr = np.asarray(im)
        for y in range(50):
            for x in range(50):
                if tuple(img_arr[y, x, 0:3]) in range_of_color:
                    img_arr[y, x, 0:3] = (85, 30, 15)
        img = Image.fromarray(img_arr, "RGBA")
        img.save(f"{name}.png")


if __name__ == '__main__':
    main()
