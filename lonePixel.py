# lonePixel
class lonePixel:
    def __init__( self, color, location ):
        self.setColor( color )
        self.location = location
    
    def setColor( self, color ):
        self.color = color[:3]
    
    def getColor( self ):
        return self.color
    
    def getLocation( self ):
        return self.location

    def swapColor( self, other ):
        temp = self.getColor()
        self.color = other.getColor()
        other.color = temp