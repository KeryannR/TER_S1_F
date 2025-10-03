from Cell import Cell
import numpy as np
from typing import Iterator

class Grid():
    def __init__(self, rows:int, columns:int, seed:int=None):
        self.rows, self.columns = rows, columns
        self.rng = np.random.RandomState(seed)
        
        self.grid = self.prepareGrid()
        self.configureCells()
    
    def __str__(self) -> str:
        output = "+" + "---+" * self.columns + "\n"
        for row in self.eachRow():
            top = "|"
            bottom = "+"
            
            for cell in row:
                cell = Cell(-1,-1) if cell is None else cell
                body = "   "
                east_boundary = " " if cell.isLinked(cell.east) else "|"
                
                top += body + east_boundary
                
                south_boundary = "   " if cell.isLinked(cell.south) else "---"
                corner = "+"
                bottom += south_boundary + corner
            
            output += top + "\n"
            output += bottom + "\n"
        
        return output
                
    
    def prepareGrid(self) -> list[list["Cell"]]:
        grid = []
        for row in range(self.rows):
            grid.append([Cell(row, column) for column in range(self.columns)])
        
        return grid
    
    def configureCells(self) -> None:
        for rowIndex, row in enumerate(self.grid):
            for colIndex, cell in enumerate(row):
                cell.north = self.grid[rowIndex-1][colIndex] if rowIndex != 0 else None
                cell.south = self.grid[rowIndex+1][colIndex] if rowIndex != len(self.grid)-1 else None
                cell.west = self.grid[rowIndex][colIndex-1] if colIndex != 0 else None
                cell.east = self.grid[rowIndex][colIndex+1] if colIndex != len(row)-1 else None
    
    def randomCell(self) -> Cell:
        row = self.rng.randint(self.rows)
        col = self.rng.randint(self.columns)
        return self.grid[row][col]

    def getSize(self) -> int:
        return self.rows * self.columns
    
    def eachRow(self) -> Iterator[list[Cell]]:
        for row in self.grid:
            yield row
        
    def eachCell(self) -> Iterator[Cell]:
        for row in self.eachRow():
            for cell in row:
                if cell is not None:
                    yield cell
                 
    def deadends(self) -> list[Cell]:
        deadendsList = []
        
        for cell in self.eachCell():
            if len(cell.links) == 1:
                deadendsList.append(cell)
        
        return deadendsList
    
    def braid(self, p:float = 1) -> None:
        deadendsList = self.deadends()
        self.rng.shuffle(deadendsList)
        
        for cell in deadendsList:
            if len(cell.links) != 1 or self.rng.rand() > p:
                continue
            
            neighbours = [n for n in cell.neighbours() if not cell.isLinked(n)]
            best = [n for n in neighbours if len(n.links) == 1]
            
            if not best:
                best = neighbours
            
            if best:
                neighbours = self.rng.choice(best)
                cell.link(neighbours)
                   
if __name__ == "__main__":
    g = Grid(2,2)