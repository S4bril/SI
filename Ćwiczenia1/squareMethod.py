def load_words(filepath):
    dict = {}
    with open(filepath, 'r', encoding="utf8") as file:
        words = [line.strip() for line in file]
        for word in words:
            length = len(word)
            if length not in dict:
                dict[length] = {word}
            else:
                dict[length].add(word)
    return dict

words_base = load_words("words_for_ai1.txt")

def square_of_lengths(words_list):
    return sum(len(word)**2 for word in words_list)

def refactor_text(text):
    state = {}
    state[""] = []
    def helper(text):
        if text in state:
            copy = state[text][:]
            return copy
        else:
            result = []
            best_length = 0
            for i in range(1, min(30, len(text) + 1)):
                if text[:i] in words_base[i]:
                    rest = helper(text[i:])
                    length = square_of_lengths(rest)
                    if i**2 + length > best_length:
                        result = rest
                        result.insert(0, text[:i])
                        best_length = i**2 + length
            state[text] = result[:]
            return result
    return helper(text)

def write_result_to_file(result_list, filepath):
    with open(filepath, 'w', encoding="utf8") as file:
        file.write(result_list)

if __name__ == '__main__':
    with open('in.txt', 'r', encoding="utf8") as file:
        tests = file.readlines()
        result = [' '.join(refactor_text(test.strip())) for test in tests]
        write_result_to_file('\n'.join(result), 'out_squares.txt')