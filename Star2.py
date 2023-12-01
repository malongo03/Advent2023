def unscamble_calibration(file):
    f = open(file)
    text = f.read()
    text = text.split()

    digit_pairs = []
    dict = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

    for line in text:
        first_digit = -1
        last_digit = -1
        last_chas = ""

        for cha in line:

            if cha.isdigit():
                last_digit = int(cha)
                if first_digit == -1:
                    first_digit = int(cha)
                last_chas = ""

            else:
                last_chas += cha
                length = min([len(last_chas), 5])

                for i in range(1, length + 1):
                    check = dict.get(last_chas[-i:], None)
                    if check is not None:
                        last_digit = check
                        if first_digit == -1:
                            first_digit = check

        digit_pairs.append(first_digit * 10 + last_digit)

    return sum(digit_pairs)

print(unscamble_calibration("star1.txt"))