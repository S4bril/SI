def check(file_path):
    with open("out.txt", 'r', encoding="utf8") as correct_output:
        with open(file_path, 'r', encoding="utf8") as output:
            correct_lines = correct_output.readlines()
            lines_to_check = output.readlines()
            n = len(correct_lines)
            good = 0
            for line_correct, line_to_check in zip(correct_lines, lines_to_check):
                good += int(line_correct == line_to_check)
            return round((good / n) * 100.0, 2)

if __name__ == '__main__':
    print("Random: {}%, Squares: {}%".format(check("out_random.txt"), check("out_squares.txt")))

    blotkarz_total = 376992
    figurant_total = 4368
    blotkarz = [20, 288, 1728, 484, 5100, 16128, 36288, 193536]
    figurant = [0, 48, 288, 0, 0, 768, 1728, 1536]

    blotkarz_probability = [0.0] * 8
    figurant_probability = [0.0] * 8

    for i in range(8):
        blotkarz_probability[i] = blotkarz[i] / blotkarz_total
        figurant_probability[i] = figurant[i] / figurant_total
    res = 0.0
    for i in range(7):
        for j in range(i + 1, 8):
            res += blotkarz_probability[i] * figurant_probability[j]
    print(f'Blotkarz probability of winning: {res * 100}%')