from ai import AI

if __name__ == "__main__":
    ai = AI()
    data = ""
    with open("./data/sudoku1.json") as f:
        data = f.read()
    ai.solve(data)