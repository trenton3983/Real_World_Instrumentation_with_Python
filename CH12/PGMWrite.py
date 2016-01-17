#! /usr/bin/python
#-------------------------------------------------------------------------------
# PGMWrite.py
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import struct

def PGMWrite(imgsrc, imgname, filename, width, height, bitdepth=8):
    """ Generates an 8bpp or 16bpp PGM image from aribitary data.

        Parameters:

        imgsrc:     source of image data (a list of integer values)
        imgname:    image name string written into the image file header
        filename:   output file name for image data
        width:      width of image
        height:     height of image
    """

    # verify source data type (must be a list)
    if type(imgsrc) != list:
        print "Input data must be a list of integer values"
        return

    # verify pixel bit depth
    sizemult = 0
    if bitdepth == 8:
        sizemult  = 1
        img_depth = 255
    elif bitdepth >= 9:
        sizemult  = 2
        img_depth = 65535
    else:
        print "Invalid pixel depth"
        return

    # generate image parameters
    img_height = height
    img_width  = width
    img_size   = img_height * img_width
    data_size  = img_size * sizemult

    # initalize the image output array
    pixels = []

    # generate the image array from input data
    i = 0   # input index
    # load data into the image array
    for y in range(0, img_height):
        for x in range(0, img_width):
            # fetch next input value from source if mod result is zero
            inval = imgsrc[i]

            if (bitdepth == 8) and (inval > 255):
                pixval = 255
            elif inval > 65535:
                pixval = 65535
            else:
                pixval = inval

            i += 1
            pixels.append(pixval)

    if bitdepth == 8:
        pix_data = "".join(map(chr,pixels))
    else:
        pix_data = pixels

    # load the header data variables and get string lengths
    img_type_str    = "P5\n"
    img_name_str    = "#%s\n" % imgname     # a comment in image header
    img_width_str   = "%d\n"  % img_height
    img_height_str  = "%d\n"  % img_width
    img_depth_str   = "%d\n"  % img_depth

    img_name_len    = len(img_name_str)
    img_width_len   = len(img_width_str)
    img_height_len  = len(img_height_str)
    img_depth_len   = len(img_depth_str)

    # create the image header structure
    hdrvals  = (img_type_str, img_name_str, img_width_str, img_height_str, img_depth_str)

    hdrobj = struct.Struct('3s %ds %ds %ds %ds'% (img_name_len,
                                                  img_width_len,
                                                  img_height_len,
                                                  img_depth_len))
    # create the pixel data
    if sizemult == 1:
        pixobj = struct.Struct('%dc'% (img_size))
    else:
        pixobj = struct.Struct('%dH'% (img_size))

    # pack the data into the structures
    img_hdr_data = hdrobj.pack(*hdrvals)
    img_pix_data = pixobj.pack(*pix_data)
    img_data = img_hdr_data + img_pix_data

    # now write it all out to the file
    fimg = open(filename,"wb")
    fimg.write(img_data)
    fimg.close()


if __name__ == "__main__":
    # generate 8bpp image
    datavals = []
    for i in range(0, 65536):
        datavals.append(i/256)

    PGMWrite(datavals, "incshade8", "incshade8.pgm", 256, 256, bitdepth=8)

    # generate 16bpp image
    datavals = []
    for i in range(0, 65536):
        datavals.append(i/256)

    PGMWrite(datavals, "incshade16", "incshade16.pgm", 256, 256, bitdepth=16)
