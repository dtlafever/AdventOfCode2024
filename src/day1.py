# Problem: https://adventofcode.com/2024/day/1#part2

from collections import defaultdict

def puzzle1():
    left_list  = []
    right_list = []

    with open('../data/input1.txt') as f:
        for line in f:
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))

    # NOTE: it would be faster to sort as we are adding elements to the list instead of after
    left_list.sort()
    right_list.sort()

    distance_sum = 0
    # NOTE: this will not work if each list is not the same length
    for i in range(len(left_list)):
        distance_sum += abs(left_list[i] - right_list[i])

    print(f"Puzzle 1 Answer: {distance_sum}")

def puzzle2():
    left_list  = []
    right_dict = defaultdict(int)  # Creates dict with default value of 0
    with open('../data/input1.txt') as f:
        for line in f:
            left, right = line.split()
            left_list.append(int(left))
            right_dict[int(right)] += 1

    distance_sum = 0
    for num in left_list:
        if num in right_dict:
            distance_sum += num * right_dict[num]
        # if num not in right_dict, then we don't need to do anything since it will be 0

    print(f"Puzzle 2 Answer: {distance_sum}")

def main():
    puzzle1()
    puzzle2()

if __name__ == '__main__':
    main()