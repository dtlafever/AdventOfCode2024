# Problem: https://adventofcode.com/2024/day/3#part2

import re

# (?<=mul\()  => lookbehind positive for "mul(", but does not capture it
# ([0-9]{1,3},[0-9]{1,3}) => captures 1-3 digits, followed by a comma, followed by 1-3 digits
# (?=\)) => lookahead positive for ")", but does not capture it
# EX. mul(1,564)
MULT_RE_EXPRESSION = r"(?<=mul\()([0-9]{1,3},[0-9]{1,3})(?=\))"

# EX. do()
DO_RE_EXPRESSION = r"(do\(\))"
DO_STR = "do()"
# EX. don't()
DONT_RE_EXPRESSION = r"(don't\(\))"
DONT_STR = "don't()"

DO_AND_DONT_RE_EXPRESSION = r"(do\(\)|don't\(\))"

def puzzle1():
    total_sum_of_products = 0

    with open('../data/input3.txt') as f:
        for line in f:
            # find all matches for the MULT_RE_EXPRESSION
            # EX. mul(1,564)
            matches = re.findall(MULT_RE_EXPRESSION, line)

            for match in matches:
                num1, num2 = match.split(',')
                product = int(num1) * int(num2)
                total_sum_of_products += product

                # print(matches)

    print(total_sum_of_products)

def puzzle2():
    lines = [] # for combining file lines to one string
    with open('../data/input3.txt') as f:
        for line in f:
            lines.append(line)

    is_currently_enabled = True
    combined_lines = ''.join(lines)
    enabled_index_start = 0
    enabled_index_end = -1
    enabled_indices = []
    # loop through all instances of "do()" and "don't()" and track
    # the indices of the enabled sections
    for match in re.finditer(DO_AND_DONT_RE_EXPRESSION, combined_lines):

        if match.group() == DO_STR:
            if not is_currently_enabled:
                # start tracking the enabled index
                is_currently_enabled = True
                _, enabled_index_start = match.span()

                enabled_index_end = -1
        elif match.group() == DONT_STR:
            if is_currently_enabled:
                # stop tracking the enabled index
                is_currently_enabled = False
                enabled_index_end, _ = match.span()
                enabled_indices.append((enabled_index_start, enabled_index_end))

                enabled_index_start = -1

    # Special Case if there is no "don't()" at the end of the file
    if is_currently_enabled:
        enabled_indices.append((enabled_index_start, -1))

    # calculate the sum of the products for the enabled indices
    total_sum_of_products = 0
    for start, end in enabled_indices:
        enabled_line = combined_lines[start:end]
        # find all matches for the MULT_RE_EXPRESSION
        # EX. mul(1,564)
        matches = re.findall(MULT_RE_EXPRESSION, enabled_line)

        for match in matches:
            num1, num2 = match.split(',')
            product = int(num1) * int(num2)
            total_sum_of_products += product


    print(total_sum_of_products)

def main():
    puzzle1()
    puzzle2()

if __name__ == '__main__':
    main()