Alphabet = ['A', 'B', 'C', 'Č', 'D', 'E', 'F','G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'Š', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ž', ' ', ',', '.', '!', '?', '-', '_', '+', '*', '"', '#', '$', '&']

def Diff_Table(Alphabet):
    diff_dict = {}
    for i in range(len(Alphabet)):
        letter = Alphabet[i]
        diff_dict[letter] = i
    return  diff_dict