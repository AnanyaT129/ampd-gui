# Justin Bahr
# Capstone

def parse_text(file_name):
    col_1 = []
    col_2 = []
    with open(file_name, 'r') as file:
        next(file)
        for line in file:
            parts = line.strip().split()
            col_1.append(float(parts[0]))
            col_2.append(float(parts[1]))
    return col_1, col_2

# parse_text('')

def main():
    print('LTSpice Data Filename: ')
    filename = input()
    x,y = parse_text(filename)
    print(x)
    print(y)

main()