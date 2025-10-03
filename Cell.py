from typing import Self, Iterable
class Cell:
    
   
    def __init__(self, row:int, col:int):
        self.row, self.col = row, col
        self.links = {}
        
        self.north:"Cell" = None
        self.south:"Cell" = None
        self.east:"Cell" = None
        self.west:"Cell" = None
        
    def link(self, cell:"Cell", bidi:bool=True) -> None:
        self.links[cell] = True
        if bidi:
            cell.link(self, False)
    
    def unlink(self, cell:"Cell", bidi:bool = True) -> None:
        self.links.pop(cell)
        if bidi:
            cell.unlink(self, False)
    
    def getLinks(self) -> Iterable["Cell"]:
        return self.links.keys()
    
    def isLinked(self, cell:"Cell") -> bool:
        return self.links.get(cell, False)
    
    def neighbours(self) -> list["Cell"]:
        return [i for i in [self.north, self.south, self.east, self.west] if i is not None]
        