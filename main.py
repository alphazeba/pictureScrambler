#main.py
import sys
import pictureScrambler

def getCommandLineArgument( n , errorIfNotAvailable ):
    if( len( sys.argv ) <= n ):
        exit( errorIfNotAvailable )
    return sys.argv[n]

def getArgument( n ):
    return getCommandLineArgument( 2 + n, "You must provide more arguments" )

def getCommand():
    return getCommandLineArgument( 1, "You must enter a command" )



def swapHandler():
    filea = getArgument( 0 )
    fileb = getArgument( 1 )
    pictureScrambler.swapImageColor( filea, fileb )

def sortHandler():
    file = getArgument( 0 )
    pictureScrambler.convertImage( file )

def helpHandler():
    f = open( "readme.md", "r" )
    print( f.read() ) 




handlers = [
    ( ["swap"], swapHandler ),
    ( ["sort"], sortHandler ),
    ( ["help", "h", "-h" ], helpHandler )
]

inputCommand = getCommand()
commandWasHandled = False
for handler in handlers:
    keys, fn = handler
    if( inputCommand in keys ):
        fn()
        commandWasHandled = True
        break
if( not commandWasHandled ):
    pictureScrambler.log( inputCommand + " was not recognized as a command" )
