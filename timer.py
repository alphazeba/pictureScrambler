# timer
import time

class timer:
    def __init__( self ):
        self.running = False
        self.startTime = 0
        self.stopTime = 0

    def start( self ):
        self.running = True
        self.startTime = self.getNow()

    def getNow( self ):
        return time.time()

    def getTimeSeconds( self ):
        if( self.running ):
            return self.getNow() - self.startTime
        return 0

    def getTimeResultString( self, thingBeingTimed ):
        return "Time to " + thingBeingTimed + ": " + str( self.getTimeSeconds() ) + " seconds"

