from osgeo import gdal
import numpy as np
import sys
import math

def dos(input, output):
    image = gdal.Open(input)
    if image is None:
        print ('Unable to open the source file')
        sys.exit()
    [cols, rows] = np.array(image.GetRasterBand(1).ReadAsArray()).shape
    trans = image.GetGeoTransform()
    proj = image.GetProjection()
    outfile = output
    outdriver = gdal.GetDriverByName("GTiff")
    outdata = outdriver.Create(str(outfile), rows, cols, image.RasterCount, gdal.GDT_Float32)
    for band in range(image.RasterCount):
        band += 1
        stats = image.GetRasterBand(band).GetStatistics(True, True)
        minimum = stats[0]
        bandarray = np.array(image.GetRasterBand(band).ReadAsArray())
        outdata.GetRasterBand(band).WriteArray(bandarray - minimum)
        outdata.SetGeoTransform(trans)
        outdata.SetProjection(proj)

def sac(input, output, angle):
    image = gdal.Open(input)
    if image is None:
        print ('Unble to open the source file')
        sys.exit()
    [cols, rows] = np.array(image.GetRasterBand(1).ReadAsArray()).shape
    trans = image.GetGeoTransform()
    proj = image.GetProjection()
    outfile = output
    outdriver = gdal.GetDriverByName('GTiff')
    outdata = outdriver.Create(str(outfile), rows, cols, 4, gdal.GDT_Float32)
    for band in range(image.RasterCount):
        band += 1
        bandarray = np.array(image.GetRasterBand(band).ReadAsArray())
        bandarray1 = bandarray / math.sin(angle)
        outdata.GetRasterBand(band).WriteArray(bandarray1)
        outdata.SetGeoTransform(trans)
        outdata.SetProjection(proj)

def avg_filter(input, output):
    image = gdal.Open(input)
    if image is None:
        print ('Unable to open the source file')
        sys.exit()
    [cols, rows] = np.array(image.GetRasterBand(1).ReadAsArray()).shape
    trans = image.GetGeoTransform()
    proj = image.GetProjection()
    outfile = output
    outdriver = gdal.GetDriverByName("GTiff")
    outdata = outdriver.Create(str(outfile), rows, cols, image.RasterCount, gdal.GDT_Float32)
    for band in range(image.RasterCount):
        band += 1
        baseArray = np.array(image.GetRasterBand(band).ReadAsArray())
        frows = np.asarray([[0] * rows])
        rarray = np.vstack([frows, baseArray, frows])
        fcols = np.asarray([[0]] * (cols + 2))
        filterArray = np.hstack([fcols, rarray, fcols])
        bandArray = filterArray
        filter = [0] * 9
        for i in range(1, len(filterArray) - 1):
            for j in range(1, len(filterArray[0]) - 1):
                filter[0] = filterArray[i - 1][j - 1]
                filter[1] = filterArray[i - 1][j]
                filter[2] = filterArray[i - 1][j + 1]
                filter[3] = filterArray[i][j - 1]
                filter[4] = filterArray[i][j]
                filter[5] = filterArray[i][j + 1]
                filter[6] = filterArray[i + 1][j - 1]
                filter[7] = filterArray[i + 1][j]
                filter[8] = filterArray[i + 1][j + 1]
                bandArray[i][j] = np.mean(filter)
        rmrowarray = np.delete(bandArray, (0, len(bandArray) - 1), axis=0)
        rmColArray = np.delete(rmrowarray, (0, len(rmrowarray[0]) - 1), axis=1)
        outdata.GetRasterBand(band).WriteArray(rmColArray)
        outdata.SetGeoTransform(trans)

def weighted_avg_filter(input, output):
    image = gdal.Open(input)
    if image is None:
        print ('Unable to open the source file')
        sys.exit()
    [cols, rows] = np.array(image.GetRasterBand(1).ReadAsArray()).shape
    trans = image.GetGeoTransform()
    proj = image.GetProjection()
    outfile = output
    outdriver = gdal.GetDriverByName("GTiff")
    outdata = outdriver.Create(str(outfile), rows, cols, image.RasterCount, gdal.GDT_Float32)
    for band in range(image.RasterCount):
        band += 1
        baseArray = np.array(image.GetRasterBand(band).ReadAsArray())
        frows = np.asarray([[0] * rows])
        rarray = np.vstack([frows, baseArray, frows])
        fcols = np.asarray([[0]] * (cols + 2))
        filterArray = np.hstack([fcols, rarray, fcols])
        bandArray = filterArray
        filter = [0] * 9
        for i in range(1, len(filterArray) - 1):
            for j in range(1, len(filterArray[0]) - 1):
                filter[0] = filterArray[i - 1][j - 1]
                filter[1] = (filterArray[i - 1][j])*2
                filter[2] = filterArray[i - 1][j + 1]
                filter[3] = (filterArray[i][j - 1])*2
                filter[4] = (filterArray[i][j])*4
                filter[5] = (filterArray[i][j + 1])*2
                filter[6] = filterArray[i + 1][j - 1]
                filter[7] = (filterArray[i + 1][j])*2
                filter[8] = filterArray[i + 1][j + 1]
                bandArray[i][j] = sum(filter)/16
        rmrowarray = np.delete(bandArray, (0, len(bandArray) - 1), axis=0)
        rmColArray = np.delete(rmrowarray, (0, len(rmrowarray[0]) - 1), axis=1)
        outdata.GetRasterBand(band).WriteArray(rmColArray)
        outdata.SetGeoTransform(trans)
        outdata.SetProjection(proj)

def x_gradient_filter(input, output):
    image = gdal.Open(input)
    if image is None:
        print ('Unable to open the source file')
        sys.exit()
    [cols, rows] = np.array(image.GetRasterBand(1).ReadAsArray()).shape
    trans = image.GetGeoTransform()
    proj = image.GetProjection()
    outfile = output
    outdriver = gdal.GetDriverByName("GTiff")
    outdata = outdriver.Create(str(outfile), rows, cols, image.RasterCount, gdal.GDT_Float32)
    for band in range(image.RasterCount):
        band += 1
        baseArray = np.array(image.GetRasterBand(band).ReadAsArray())
        frows = np.asarray([[0] * rows])
        rarray = np.vstack([frows, baseArray, frows])
        fcols = np.asarray([[0]] * (cols + 2))
        filterArray = np.hstack([fcols, rarray, fcols])
        bandArray = filterArray
        filter = [0] * 9
        for i in range(1, len(filterArray) - 1):
            for j in range(1, len(filterArray[0]) - 1):
                filter[0] = (filterArray[i - 1][j - 1])*(-1)
                filter[1] = (filterArray[i - 1][j])*0
                filter[2] = filterArray[i - 1][j + 1]
                filter[3] = (filterArray[i][j - 1])*(-1)
                filter[4] = (filterArray[i][j])*0
                filter[5] = filterArray[i][j + 1]
                filter[6] = (filterArray[i + 1][j - 1])*(-1)
                filter[7] = (filterArray[i + 1][j])*0
                filter[8] = filterArray[i + 1][j + 1]
                bandArray[i][j] = sum(filter)
        rmrowarray = np.delete(bandArray, (0, len(bandArray) - 1), axis=0)
        rmColArray = np.delete(rmrowarray, (0, len(rmrowarray[0]) - 1), axis=1)
        outdata.GetRasterBand(band).WriteArray(rmColArray)
        outdata.SetGeoTransform(trans)
        outdata.SetProjection(proj)