"""
driver.py

Includes main functions to run the boggle word finder using DFS on an input board (storing a dictionary of valid words as a Trie).

@author: Sanjana Marce

"""
import tkinter as tkinter
import vocab
import trie
import argparse
import time

iteration = 0
"""
get_neighbors: returns a list of tuples corresponding to the (r, c) coordinates 
of those cells within the input board around the cell at (row, col). Takes
into account if the input cell is at an edge and does not return cells that
would lie outside the board

@param: 2D list - board: input board
@param: int - row: row coordinate of the cell whose neighbors we get 
@param: int - col: col coordinate of the cell whose neighbors we get
@return: list of tuples
"""
def get_neighbors(board, row, col):
    neighbors = []
    diff = [-1, 0, 1]
    M, N = len(board), len(board[0])
    for i in diff:
        if (row + i) < 0 or (row + i) >= M:
            continue
        for j in diff:
            if (col + j) < 0 or (col + j) >= N:
                continue
            if  (i == j == 0) :
                continue
            neighbors.append((row+i,col+j))
    return neighbors

"""
recursive_solve: helper function for solve that recursively searches
the board using DFS while leveraging the Trie data structure to prevent 
searching deeper in directions where no valid words lie. 

@param: 2D list - board: input board
@param: Trie - vocab_trie: Trie of the active vocabulary
@param: 2D list - visited: 2D list equal in dimensions to the input board
that maintains cells that have already been visited in this branch
@param: int - row: row coordinate of the cell we are exploring from
@param: int - col: col coordinate of the cell we are exploring from
@param: str - word: word that has been produced so far from this branch of the search
@return: list
"""
def recursive_solve(board, vocab_trie, visited, row, col, word, board3D, root, showWord):
    global iteration
    iteration += 1
    min_word_len = 3
    output_words = []

    visited[row][col] = True
    board3D[row][col].config(bg= "gray51")
    root.update()
    # time.sleep(0.1)
    word = word + board[row][col]
    prefix = vocab_trie.is_valid(word)
    if len(word) >= min_word_len and prefix == 0:
        showWord.config(text= word)
        output_words.append(word)
        root.update()
        time.sleep(1)
        showWord.config(text= "")
        root.update()
    # if prefix >= 0:
    if len(word) <= 5:
        neighbors = get_neighbors(board, row, col)
        for neighbor in neighbors:
            new_row = neighbor[0]
            new_col = neighbor[1]
            if not visited[new_row][new_col]:
                output_words = output_words + recursive_solve(board, vocab_trie, visited, new_row, new_col, word, board3D, root, showWord)

    # backtrack
    word = word[:-1]
    visited[row][col] = False
    board3D[row][col].config(bg= "white")
    root.update()
    return output_words


def recursive_heuristic_solve(board, vocab_trie, visited, row, col, word, board3D, root, showWord):
    global iteration
    iteration += 1
    min_word_len = 3
    output_words = []

    visited[row][col] = True
    board3D[row][col].config(bg= "gray51")
    root.update()
    # time.sleep(0.1)
    word = word + board[row][col]
    prefix = vocab_trie.is_valid(word)
    if len(word) >= min_word_len and prefix == 0:
        showWord.config(text= word)
        output_words.append(word)
        root.update()
        time.sleep(1)
        showWord.config(text= "")
        root.update()
    # if prefix >= 0:
    if len(word) <= 5:
        neighbors = get_neighbors(board, row, col)

        sorted_neighbors = sorted(neighbors, key=lambda cord: vocab_trie.get_prob(word + board[cord[0]][cord[1]]), reverse=True);

        for neighbor in sorted_neighbors:

            new_row = neighbor[0]
            new_col = neighbor[1]

            if (vocab_trie.get_prob(word + board[new_row][new_col])) <= 0:
                continue

            if not visited[new_row][new_col]:
                output_words = output_words + recursive_heuristic_solve(board, vocab_trie, visited, new_row, new_col, word, board3D, root, showWord)

    # backtrack
    word = word[:-1]
    visited[row][col] = False
    board3D[row][col].config(bg= "white")
    root.update()
    return output_words


"""
solve: function to run the boggle word finder using DFS on an input board 
(storing a dictionary of valid words as a Trie). Returns list of 
all the output_words found in the board.

@param: 2D list - board: input board
@param: Trie - vocab_trie: Trie of the active vocabulary
@return: list
"""
def solve(board, vocab_trie, board3D, root, showWord, showListWord):
    global iteration
    M, N = len(board), len(board[0])
    visited = [[False for i in range(N)] for j in range(M)]

    output_words = []
    for row in range(M):
        for col in range(N):
            output_words = output_words + recursive_solve(board, vocab_trie, visited, row, col, "", board3D, root, showWord)
            # output_words = output_words + recursive_heuristic_solve(board, vocab_trie, visited, row, col, "", board3D, root, showWord)
    print(output_words)
    listWord = ""
    wordCount = 0
    for i in output_words:
        listWord = listWord + i
        if wordCount < 5:
            listWord = listWord + " "
            wordCount += 1
        else:
            listWord = listWord + "\n"
            wordCount = 0
    showListWord.config(text=listWord)

    print("Iteration usage ", iteration)
    iteration = 0
    return output_words

"""
construct_vocab_trie: given an input board and a dictionary txt file loads in
the dictionary, reduces the dictionary to only include those words with characters
that appear in the board, and populates and returns a Trie with that reduced dictionary

@param: 2D list - board: input board
@param: str - vocab_file: path to dictionary txt file
@return: Trie
"""
def construct_vocab_trie(board, vocab_file):
    # flatten 2 dimensional board into single list of characters and remove duplicates to create 
    # an alphabet of all the characters seen on the board
    alphabet = list(set([ch for row in board for ch in row]))
    
    full_vocab = vocab.load_dictionary(vocab_file)
    active_vocab = vocab.reduce_vocab(full_vocab, alphabet)

    # store vocab as trie for optimized checking if word is in the dictionary
    vocab_trie = trie.Trie(alphabet)
    vocab_trie.construct(active_vocab)
    return vocab_trie

"""
get_args: uses the argparse package to take in optional command line arguments specifying an input
Boggle board and a txt file containing a dictionary of valid words.

--board: board represented as a string with spaces between each row
         default board: "rael mofs teok nati"
--vocab: txt file of vocabulary with each valid word on a new line
         default vocab: "dictionary.txt"; Source: http://www.gwicks.net/dictionaries.htm (194,000 English words)

"""
def get_args():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument("-b", "--board", default = "rael mofs teok nati", type=str, help='board represented as a string with spaces between each row')
    my_parser.add_argument("-v", "--vocab", default = "AI_word_search\dictionary\AI_BRILL_NEW.txt", type=str, help='txt file of vocabulary with each valid word on a new line')
    args = my_parser.parse_args()
    return args

if __name__ == '__main__':

    root = tkinter.Tk()
    root.geometry("320x600")

    board3D=[]
    frame1 = tkinter.Frame(root)
    frame1.grid(row=0,column=0)
    for x in range(4):
        boardRow=[]
        for y in range(4):
            label = tkinter.Label(frame1, text="-", relief=tkinter.RIDGE, borderwidth=1.5, font=("Arial",18), width=5, height=2)
            label.grid(row=x,column=y)
            boardRow.append(label)
        board3D.append(boardRow)
    # board3D[0][0].config(bg= "gray51")
    # board3D[0][0].config(text= "a")
    
    args = get_args()

    # Convert board string into 2D array
    board_str = args.board
    board = [list(row) for row in board_str.split()]
    print("board",board)
    for x in range(4):
        for y in range(4):
            board3D[x][y].config(text= board[x][y])
    
    vocab_file = args.vocab
    
    vocab_trie = construct_vocab_trie(board, vocab_file)
    frame2 = tkinter.Frame(root)
    frame2.grid(row=1,column=0, pady=10)
    WordLabel = tkinter.Label(frame2, text="Word :",font=("Arial",18), height=2)
    WordLabel.grid(row=0, column=1, padx=20)
    showWord = tkinter.Label(frame2, text="", relief=tkinter.RIDGE, borderwidth=1.5, font=("Arial",18), height=2)
    showWord.grid(row=0, column=2, padx=20)
    showListWord = tkinter.Label(root, text="",font=("Arial",18),)
    showListWord.grid(row=3, column=0)
    searchButton = tkinter.Button(root, text="Search", command= lambda: solve(board, vocab_trie, board3D, root, showWord, showListWord))
    searchButton.grid(row=2,column=0, pady=20)
    root.mainloop()

    # output_words = solve(board, vocab_trie, board3D)

    ## If we would like to ignore cases where the same word can be formed in multiple ways,
    ## uncomment the following:
    # output_words = list(set(output_words))
    
    # print(output_words)

