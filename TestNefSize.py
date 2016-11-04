from PIL import Image as PIL_Image
from wand.image import Image as wand_Image
import imageio
from PIL.ExifTags import TAGS
import exifread
from collections import namedtuple


def get_exif(fname):
    # http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/
    ret = {}
    i = PIL_Image.open(fname)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


def get_imagesize_PIL(fname):
    with PIL_Image.open(fname) as im:
        return im.size


def get_imagesize_PIL2(fname):
    ret = get_exif(fname)


def get_imagesize_PIL3(fname):
    with PIL_Image.open(fname) as im:
        return im.info


def get_imagesize_imageioraw(fname):
    return imageio.imread(fname, "raw").shape[:-1]


def get_imagesize_imageio(fname):
    return imageio.imread(fname).shape[:-1]


def get_imagesize_exifread(fname):  # http://stackoverflow.com/a/18027454/1562285
    ex = exifread.process_file(open(fname, 'rb'), strict=True)
    return ex['Image XResolution'], ex['Image YResolution']


def get_imagesize_exifread2(fname):
    ex = exifread.process_file(open(fname, 'rb'), strict=True)
    return ex['Image ImageLength'], ex['Image ImageWidth']


def get_imagesize_exifread3(fname):
    ex = exifread.process_file(open(fname, 'rb'), strict=True)
    return ex['MakerNote CropHiSpeed']


def get_imagesize_exifread4(fname):
    ex = exifread.process_file(open(fname, 'rb'), strict=True)
    return ex['EXIF ExifImageLength'], ex['EXIF ExifImageWidth']


def get_imagesize_wand(fname):
    with wand_Image(filename=fname) as img:
        return img.size


def get_imagesize_wand2(fname):
    with wand_Image(filename=fname) as img:
        return img.page


# def get_imagesize_wand3(fname):
#     with wand_Image(filename=fname) as img:
#         return img.info


def create_eval(fmethod, fname):
    try:
        eval_str = "get_imagesize_%s('%s')" % (fmethod, fname)
        # print(eval_str)
        return eval(eval_str)
    except BaseException as e:
        return str(e)


if __name__ == '__main__':

    file_nt = namedtuple("image_file", "filename tag")
    filetypes = list()
    filetypes.append(file_nt("20120917_131155 DSC_0159.JPG", "jpeg"))
    filetypes.append(file_nt("20120917_131155 DSC_0159.NEF", "nef"))
    # filetypes.append(file_nt("20120917_131155 DSC_0159.xmp", "xmp"))

    methods = [
        "PIL",
        "PIL2",
        "PIL3",
        "imageioraw",
        "imageio",
        "exifread",
        "exifread2",
        "exifread3",
        "exifread4",
        "wand",
        "wand2",
        "wand3",
    ]

    for method in methods:
        for filetype in filetypes:
            print("%s %s: %s" % (filetype.tag, method, repr(create_eval(method, filetype.filename))))
