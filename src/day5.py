from re import match
from collections import defaultdict

RULES_RE_EXP = r"[0-9]+\|[0-9]+"
UPDATE_RE_EXP = r"([0-9]+,)+[0-9]+" # not the best REGEX, but it works for validation
BEFORE = "before"
AFTER = "after"

DEBUG = False
INPUT_FILE = '../data/input5.txt'

def parse_rule(rule: str, rules: dict[str, dict[str, set[str]]]) -> None:
    """
    Parse the rule and add it to the rules dictionary. We are adding the rule to the dictionary in the following way:
    - key:   number
    - value: {"before": [list of numbers], "after": [list of numbers]}

    We make sure to add the before rule for each number on the left, and the after rule for each number on the right

    :param rule: the rule string to parse consisting of two numbers separated by a pipe
    :param rules: the dictionary to add the rule to
    :return: None, since we are updating the rules dictionary in place
    """
    priority_num, secondary_num = rule.split('|')
    rules[priority_num][BEFORE].add(secondary_num)
    rules[secondary_num][AFTER].add(priority_num)

def is_valid_update(update: list[str], rules: dict[str, dict[str, set[str]]]) -> bool:
    """
    Check if the update is valid based on the rules. The update is valid if the numbers in the update list are in the correct order based on the rules.
    :param update: the list of numbers to check
    :param rules: the dictionary of rules to check against
    :return: True if the update is valid, False otherwise
    """
    for index in range(len(update)):
        num = update[index]
        if num not in rules:
            # Special Case: if the number is not in the rules, then it is no printer rule so it is valid
            return True

        nums_before_this = set(update[0:index])
        nums_after_this = set(update[index+1:])
        # check if any of the numbers before this number are in the "before" set, meaning that they should come after this number
        if len(nums_before_this.intersection(rules[num][BEFORE])) > 0:
            return False
        # check if any of the numbers before this number are in the "after" set, meaning that they should come before this number
        if len(nums_after_this.intersection(rules[num][AFTER])) > 0:
            return False
    return True

def puzzle1():
    # key:   number
    # value: {"before": [list of numbers], "after": [list of numbers]}
    # TODO: probably make this rule a class since it is getting a bit complex
    rules = defaultdict(lambda: {BEFORE: set(), AFTER: set()})
    total_valid_updates = 0
    total_valid_middle_sums = 0
    finished_with_printer_rules = False
    with open(INPUT_FILE) as f:
        for line in f:
            if not finished_with_printer_rules:
                # continue parsing rules
                if match(RULES_RE_EXP, line):
                    parse_rule(line.strip(), rules)
                    continue
                else:
                    finished_with_printer_rules = True
                    if DEBUG:
                        for key in rules:
                            print(f"Key: {key}\nBefore: {rules[key][BEFORE]}\nAfter: {rules[key][AFTER]}")
                        print("========================================")

            # check updates
            if match(UPDATE_RE_EXP, line):
                update = line.strip().split(",")
                if is_valid_update(update, rules):
                    # get the middle number in the list and add it to the total
                    total_valid_middle_sums += int(update[len(update) // 2])
                    total_valid_updates += 1

        print(f"Total Valid Updates: {total_valid_updates}")
        print(f"Total Valid Middle Sums: {total_valid_middle_sums}")

def get_max_index_from_list_of_numbers(update: list[str], set_of_nums: set[str]) -> int:
    """
    Get the maximum index of the number in the update list
    :param update: the list to search
    :param set_of_nums: the set of numbers to search in the update list
    :return: the maximum index of the number in the list
    """
    max_index = -1
    try:
        num_indices = [update.index(num) for num in set_of_nums]
        max_index = max(num_indices)
    except ValueError:
        # not found in the list, so we just do nothing and return -1
        pass
    return max_index

def get_min_index_from_list_of_numbers(update: list[str], set_of_nums: set[str]) -> int:
    """
    Get the minimum index of the number in the update list
    :param update: the list to search
    :param set_of_nums: the set of numbers to search in the update list
    :return: the minimum index of the number in the list
    """
    min_index = 0
    try:
        num_indices = [update.index(num) for num in set_of_nums]
        max_index = min(num_indices)
    except ValueError:
        # not found in the list, so we just do nothing and return default value
        pass
    return max_index

def fix_update_order(update: list[str], rules: dict[str, dict[str, set[str]]]) -> list[str]:
    """
    Fix the update order based on the rules. We will make sure that the numbers are in the correct order based on the rules.
    :param update: the list of numbers to fix
    :param rules: the dictionary of rules to check against
    :return: the fixed list of numbers
    """
    # NOTE: I HATE THIS WHILE LOOP. I was so close (<1% over the guess) of getting the correct answer without the while loop,
    # but alas I could not figure it out. I know it has got to be some edge case I am not considering that is causing the issue.
    while not is_valid_update(update, rules):
        for index in range(len(update)):
            num = update[index]
            if num not in rules:
                # Special Case: if the number is not in the rules, then it is no printer rule so it is valid
                continue

            nums_before_this = set(update[0:index])
            nums_after_this = set(update[index+1:])
            # check if any of the numbers before this number are in the "before" set, meaning that they should come after this number
            bad_before_nums = nums_before_this.intersection(rules[num][BEFORE])
            if len(bad_before_nums) > 0:
                if DEBUG:
                    print(f"\t{num} should go before {bad_before_nums}")
                # NOTE: we are not adding plus 1 to the index since we are removing the number from the list
                new_index = get_min_index_from_list_of_numbers(update, bad_before_nums)
                update.insert(new_index, update.pop(index))
                # print(update)
            # check if any of the numbers before this number are in the "after" set, meaning that they should come before this number
            bad_after_nums = nums_after_this.intersection(rules[num][AFTER])
            if len(bad_after_nums) > 0:
                if DEBUG:
                    print(f"\t{num} should go after {bad_after_nums}")
                # NOTE: we are not adding plus 1 to the index since we are removing the number from the list
                new_index = get_max_index_from_list_of_numbers(update, bad_after_nums)
                update.insert(new_index, update.pop(index))
    return update

def puzzle2():
    # key:   number
    # value: {"before": [list of numbers], "after": [list of numbers]}
    # TODO: probably make this rule a class since it is getting a bit complex
    rules = defaultdict(lambda: {BEFORE: set(), AFTER: set()})
    total_fixed_updates = 0
    total_fixed_middle_sums = 0
    finished_with_printer_rules = False
    with open(INPUT_FILE) as f:
        for line in f:
            if not finished_with_printer_rules:
                # continue parsing rules
                if match(RULES_RE_EXP, line):
                    parse_rule(line.strip(), rules)
                    continue
                else:
                    finished_with_printer_rules = True
                    if DEBUG:
                        for key in rules:
                            print(f"Key: {key}\nBefore: {rules[key][BEFORE]}\nAfter: {rules[key][AFTER]}")
                        print("========================================")

            # check updates
            if match(UPDATE_RE_EXP, line):
                update = line.strip().split(",")
                if not is_valid_update(update, rules):
                    # fix the update order
                    if DEBUG:
                        print(f"Original Update: {update}")
                    # TODO: put fix inside of validate function for more efficiency since we are looping through the list twice
                    fixed_update = fix_update_order(update, rules)
                    if DEBUG:
                        print(f"Fixed Update: {fixed_update}")
                    total_fixed_middle_sums += int(update[len(fixed_update) // 2])
                    total_fixed_updates += 1

        print(f"Total Fixed Updates: {total_fixed_updates}")
        print(f"Total Fixed Middle Sums: {total_fixed_middle_sums}")

def main():
    puzzle1()
    puzzle2()

if __name__ == "__main__":
    main()