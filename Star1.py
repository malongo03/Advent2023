def unscamble_calibration(file):
    f = open(file)
    text = f.read()
    text = text.split()

    digit_pairs = []

    for line in text:
        first_digit = -1
        last_digit = -1
        for cha in line:
            if cha.isdigit():
                last_digit = int(cha)
                if first_digit == -1:
                    first_digit = int(cha)
        digit_pairs.append(first_digit * 10 + last_digit)

    return sum(digit_pairs)

print(unscamble_calibration("star1.txt"))