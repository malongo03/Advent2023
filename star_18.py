def difference_in_sequence(sequence):
    diff_seq = []
    last_val = sequence[0]
    for val in sequence[1:]:
        diff_seq.append(val - last_val)
        last_val = val

    if set(diff_seq) == set([0]):
        return last_val

    next_diff = difference_in_sequence(diff_seq)
    return last_val + next_diff

def parse_data(file):
    lst_of_lst = []
    f = open(file, encoding = "utf-8")
    text = f.read()
    text = text.split("\n")

    for line in text:
        num_lst = line.split()
        num_lst = [int(num) for num in num_lst]
        num_lst = num_lst[::-1]
        lst_of_lst.append(num_lst)

    return lst_of_lst

def extrapolate_list(file):
    lst_of_seq = parse_data(file)

    answer = 0
    for seq in lst_of_seq:
        answer += difference_in_sequence(seq)
    
    return answer

print(extrapolate_list("day_9.txt"))