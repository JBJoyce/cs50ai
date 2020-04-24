import itertools
import random

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """
    

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        
        self.local_mines = set()
        self.local_safe = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        if len(self.cells) == self.count:
            for cell in self.cells:
                self.local_mines.add(cell)
        
            return self.local_mines
        else:
             return None 				

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
        
        if self.count == 0:
            for cell in self.cells:
                self.local_safe.add(cell)
            return self.local_safe
        else:
             return None    				

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        if cell in self.cells:
            self.cells.remove(cell)
            
class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        

        self.moves_made.add(cell)
       
        self.mark_safe(cell)
        self.knowledge.append(Sentence(cell, count))
        
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)
                mine_cells = sentence.known_mines()
                safe_cells = sentence.known_safes()
                if mine_cells is not None:
                    for	mine_cell in mine_cells:
                        mark_mine(mine_cell)
                if safe_cells is not None:
                    for safe_cell in safe_cells:
                        mark_safe(safe_cells)        								
       

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        raise NotImplementedError
