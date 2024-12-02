# Problem: https://adventofcode.com/2024/day/2#part2

NEUTRAL_STATE    = 0 # we have not determined if the list is increasing or decreasing
INCREASING_STATE = 1 # the list is increasing
DECREASING_STATE = 2 # the list is decreasing

def is_safe_between_levels(level: int, prev_level: int, report_state: int) -> bool:
    """
    Check if the level is safe to add to the report by comparing it to the previous level.
    If the level is the same as the previous level, then the report is not safe.
    If the level is increasing when we previously found it to be decreasing, then the report is not safe.
    If the level is decreasing when we previously found it to be increasing, then the report is not safe.
    If the previous level differs more or less than 1,2 or 3, then the report is not safe.
    Otherwise, the report is safe.

    NOTE: assumes that the level is not negative and the report_state is not NEUTRAL_STATE

    :param level:
    :param prev_level:
    :param report_state:
    :return:
    """
    if level == prev_level:
        return False

    if level > prev_level:
        if report_state == DECREASING_STATE:
            return False

    if level < prev_level:
        if report_state == INCREASING_STATE:
            return False

    if abs(level - prev_level) > 3 or abs(level - prev_level) == 0:
        return False

    return True

def is_report_safe(report: list) -> bool:
    """
    Check if the report is safe by comparing each level to the previous level.

    :param report:
    :return: True if the report is safe, False otherwise
    """
    prev_level = int(report[0])  # assuming there is at least one level in the report
    report_state = NEUTRAL_STATE
    for level_index in range(1, len(report)):
        level = int(report[level_index])

        # This is the first time we are comparing two levels, so we can set the state to increasing or decreasing
        if report_state == NEUTRAL_STATE:
            if level > prev_level:
                report_state = INCREASING_STATE
            elif level < prev_level:
                report_state = DECREASING_STATE

        # check if the level is increasing, decreasing, or the same
        if not is_safe_between_levels(level, prev_level, report_state):
            return False

        prev_level = level

    return True

def puzzle1():
    total_safe_reports = 0
    with open('../data/input2.txt') as f:
        for line in f:
            report = line.split()
            if is_report_safe(report):
                total_safe_reports += 1

    print(f"Puzzle 1 Answer: {total_safe_reports}")

def puzzle2():
    """
    Check if the report is safe by removing one level and checking if the report is safe.
    If the report is safe after removing one level, then the report is safe.
    Otherwise, the report is not safe.

    :return:
    """
    total_safe_reports = 0

    with open('../data/input2.txt') as f:
        for line in f:
            report = line.split()
            for i in range(len(report)):
                part = report[:i] + report[i + 1:]
                if is_report_safe(part):
                    total_safe_reports += 1
                    break

    print(f"Puzzle 2 Answer: {total_safe_reports}")

def main():
    puzzle1()
    puzzle2()

if __name__ == '__main__':
    main()