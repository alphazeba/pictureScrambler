# opens a picture and reads in all of the pixels

# sorts the pixels and then makes a new photo with them.

import math
from PIL import Image
import os
import requests
from lonePixel import lonePixel
from timer import timer

def log( message ):
    header = "pcs > "
    print( header + message )

def isUrl( path ):
    return path.startswith("http")

def openImage( filename ):
    thingToOpen = filename
    if( isUrl( filename ) ):
        thingToOpen = requests.get( filename, stream=True ).raw
    return Image.open( thingToOpen )

def saveImage( image, filename ):
    image.save( filename )

def defaultSortingFunction( pix ):
    r,b,g = pix
    return r + b * 255 + g * 255 * 255

def sortImage( image, sortingFunction = defaultSortingFunction ):
    # break the image into an array
    w,h = image.size
    pixels = []
    for i in range( w * h ):
        location = defaultMappingFunction( image.size, i )
        color = image.getpixel( location )
        pixels.append( lonePixel( color, location ) )
    pixels = sorted( pixels, key= lambda x: sortingFunction( x.getColor() ) )
    return pixels

def defaultMappingFunction( size, i ):
    # returns an x,y coord
    w, h = size
    y = i // w
    x = i % w
    return ( x, y )

def buildImage( pixels, size, mappingFunction = defaultMappingFunction ):
    w,h = size
    assert w * h <= len( pixels )
    image = Image.new( mode="RGB", size=size )
    # build an image
    for i in range( w * h ):
        location = mappingFunction( size, i )
        image.putpixel( location, pixels[i].getColor() )
    return image

def rebuildImage( pixels, size ):
    image = Image.new( mode="RGB", size=size )
    for pixel in pixels:
        location = pixel.getLocation()
        color = pixel.getColor()
        image.putpixel( location, color )
    return image

def buildAutoLocalFile( filename, textToAdd ):
    filename = os.path.basename( filename )
    root, ext = os.path.splitext( filename )
    # force png because it seems to save better.
    return root + textToAdd + ".png"

def convertImage( filename, newFileName=None ):
    if( newFileName == None ):
        newFileName = buildAutoLocalFile( filename, "scrambleVersion" )
    image = openImage( filename )
    pixels = sortImage( image )
    w = math.floor( math.sqrt( len( pixels ) ) )
    newImage = buildImage( pixels, (w, w) )
    saveImage( newImage, newFileName )
    log( "completed converting the image, saved it at " + newFileName )

def getRelativeIndexInOtherArray( a, b, i ):
    pos = i / len( a )
    return math.floor( pos * len( b ) )

def swapImageColor( filenameA, filenameB ):
    files = [ filenameA, filenameB ]
    sortedPixels = []
    originalSize = []
    totalT = timer()
    totalT.start()
    t = timer()

    log( "start sorting pixels" )
    t.start()
    for filename in files: 
        image = openImage( filename )
        originalSize.append( image.size )
        pixels = sortImage( image )
        sortedPixels.append( pixels )
    log( t.getTimeResultString( "sort pixels" ) )

    log( "start swapping pixels" )
    t.start()
    swappedPixels = []
    for i in range( 2 ):
        thisIndex = i
        otherIndex = (i+1)%2
        swapped = []
        for j in range( len( sortedPixels[thisIndex] ) ):
            thisPixel = sortedPixels[thisIndex][j]
            otherPixel = sortedPixels[otherIndex][getRelativeIndexInOtherArray( sortedPixels[thisIndex], sortedPixels[otherIndex], j )]
            swapped.append( lonePixel( otherPixel.getColor(), thisPixel.getLocation() ) )
        swappedPixels.append( swapped )
    log( t.getTimeResultString( "swap pixels" ) )
    
    log( "start rebuilding the images" )
    t.start()
    for i in range( len( files ) ):
        image = rebuildImage( swappedPixels[i], originalSize[i] )
        filename = buildAutoLocalFile( files[i], "swapped" )
        saveImage( image, filename )
        log( "completed image " + filename )
    log( t.getTimeResultString( "rebuild the images" ) )

    log( "fully completed swap in " + str( totalT.getTimeSeconds() ) )