from PIL import Image as PIL_Image
from wand.image import Image as wand_Image
import imageio
from PIL.ExifTags import TAGS
import exifread
from collections import namedtuple
from rawkit.raw import Raw as rawkit_Raw


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
    exif = get_exif(fname)
    return exif['ExifImageHeight'], exif['ExifImageWidth']


def get_imagesize_PIL3(fname):
    with PIL_Image.open(fname) as im:
        return im.info


def get_imagesize_imageioraw(fname):
    return imageio.imread(fname, "raw").shape[:-1]


def get_imagesize_imageio(fname):
    return imageio.imread(fname).shape[:-1]


def get_imagesize_exifread(fname):  # http://stackoverflow.com/a/18027454/1562285
    exif = exifread.process_file(open(fname, 'rb'), strict=True)
    return exif['Image XResolution'], exif['Image YResolution']


def get_imagesize_exifread2(fname):
    exif = exifread.process_file(open(fname, 'rb'), strict=True)
    return exif['Image ImageLength'], exif['Image ImageWidth']


def get_imagesize_exifread3(fname):
    exif = exifread.process_file(open(fname, 'rb'), strict=True)
    return exif['MakerNote CropHiSpeed']


def get_imagesize_exifread4(fname):
    exif = exifread.process_file(open(fname, 'rb'), strict=True)
    return exif['EXIF ExifImageLength'], exif['EXIF ExifImageWidth']


def get_imagesize_wand(fname):
    with wand_Image(filename=fname) as img:
        return img.size


def get_imagesize_wand2(fname):
    with wand_Image(filename=fname) as img:
        return img.page

def get_imagesize_libraw(fname):
    with rawkit_Raw(filename=fname) as raw:
        print(raw.Metadata.height, raw.Metadata.width)


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
    # @TODO: add method to check into xmp?

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
        "libraw",
    ]

    for method in methods:
        for filetype in filetypes:
            print("%s %s: %s" % (filetype.tag, method, repr(create_eval(method, filetype.filename))))
            # @TODO: add timers to check the fastest method
