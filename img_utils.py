import cv2
import numpy as np
import os
import glob
import shutil

def resize_keep_aspect(im, desired_size):
    ## opencv has copyMakeBorder() method which is handy for making borders
    old_size = im.shape[:2]  # old_size is in (height, width) format
    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])

    # new_size should be in (width, height) format
    im = cv2.resize(im, (new_size[1], new_size[0]))

    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    color = [0, 0, 0]
    return cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)


def create_zero_mask(file, dim=512, suffix='_label'):
    im = np.full((dim, dim), 0)
    base, tail = os.path.split(file)
    name = os.path.splitext(tail)[0] + suffix + '.png'
    file_path = os.path.join(base, name)
    cv2.imwrite(file_path, im)


def convert_images(path, src='jpg', dst='png'):
    glob_path = os.path.join(path, '*.' + src)
    for j in glob.glob(glob_path):
        print('converted file: ', j)
        img = cv2.imread(j)
        base, tail = os.path.split(j)
        name = os.path.splitext(tail)[0]
        file_path = os.path.join(base, name)  # path without extension
        cv2.imwrite(file_path + '.' + dst, img)
        os.remove(j)

# defined myself
def move_pics(source, dest):
    for f in glob.glob(source):
        print(f)
        shutil.move(f, dest)


# defined myself
def copy_pics(source, dest):
    for f in glob.glob(source):
        print(f)
        shutil.copy(f, dest)


# defined myself
def rename_pics(source, suffix='_label.png'):
    for img in glob.glob(source):
        base, tail = os.path.split(img)
        name = os.path.splitext(tail)[0]
        os.rename(img, os.path.join(base, name + suffix))


def remove_images(path, ext='jpg'):
    glob_path = os.path.join(path, '*.' + ext)
    for j in glob.glob(glob_path):
        print('deleted file: ', j)
        os.remove(j)


def transform_mask(image, class_mapping=[(1, 0), (2, 0)]):
    # transform labels with right rgb colors
    for old, new in class_mapping:
        image[image[:, :, 0] == old] = [new, new, new]

    return image

def match_label(img_names, mask_names):
    img_names.sort()
    mask_names.sort()
    return [name for name in img_names if any(n in name for n in mask_names)]

if __name__ == '__main__':

    # paths
    file_base = 'C:\\Users\\kramersi\\polybox\\4.Semester\\Master_Thesis\\03_ImageSegmentation\\structure_vidFloodExt\\'
    src_img = os.path.join(file_base, 'frames', 'floodX_cam5', '*')
    src_mask = os.path.join(file_base, 'video_masks', 'floodX_cam1', 'masks', '*')
    dst = os.path.join(file_base, 'video_masks', 'floodX_cam5', 'images')

    # # match label with images
    # img_names = glob.glob(src_img)
    # mask_names = glob.glob(src_mask)
    # msk = [os.path.split(m)[1].split('_')[5] for m in mask_names]
    # match = match_label(img_names, msk)
    # for m in match:
    #     copy_pics(m, dst)

    # changes pictures in directory, outcomment steps, which are not necessary
    for file in glob.glob(src_mask):

        base, tail = os.path.split(file)
        name = os.path.splitext(tail)[0]
        file_path = os.path.join(base, name)  # path without extension
        ext = 'png'

        im = cv2.imread(file)
        im = transform_mask(im, class_mapping=[(1, 0), (2, 1)])
        im = resize_keep_aspect(im, 512)
        os.remove(file)
        cv2.imwrite(file_path + '.' + ext, im)  # renamin or changing extension
