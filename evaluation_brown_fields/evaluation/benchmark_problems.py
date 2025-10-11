"""
Benchmark problems for Pass@k evaluation
HumanEval-style problems adapted for your request format
"""

# HumanEval benchmark problems for research evaluation
BENCHMARK_PROBLEMS = {
    "is_equal_to_sum_even_HE_138": "Create a function named is_equal_to_sum_even for this given task: Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers",

    "smallest_change_HE_73": "Create a function named smallest_change for this given task: Given an array arr of integers, find the minimum number of elements that need to be changed to make the array palindromic. A palindromic array is an array that is read the same backwards and forwards. In one change, you can change one element to any other element.",

    "decimal_to_binary_HE_79": "Create a function named decimal_to_binary for this given task: You will be given a number in decimal form and your task is to convert it to binary format. The function should return a string, with each character representing a binary number. Each character in the string will be '0' or '1'. There will be an extra couple of characters 'db' at the beginning and at the end of the string. The extra characters are there to help with the format.",

    "car_race_collision_HE_41": "Create a function named car_race_collision for this given task: Imagine a road that's a perfectly straight infinitely long line. n cars are driving left to right; simultaneously, a different set of n cars are driving right to left. The two sets of cars start out being very far from each other. All cars move in the same speed. Two cars are said to collide when a car that's moving left to right hits a car that's moving right to left. However, the cars are infinitely sturdy and strong; as a result, they continue moving in their trajectory as if they did not collide. This function outputs the number of such collisions.",

    "count_up_to_HE_96": "Create a function named count_up_to for this given task: Implement a function that takes an non-negative integer and returns an array of the first n integers that are prime numbers and less than n.",

    "split_words_HE_125": "Create a function named split_words for this given task: Given a string of words, return a list of words split on whitespace, if no whitespaces exists in the text you should split on commas ',' if no commas exists you should return the number of lower-case letters with odd order in the alphabet, ord('a') = 0, ord('b') = 1, ... ord('z') = 25",

    "move_one_ball_HE_109": "Create a function named move_one_ball for this given task: We have an array 'arr' of N integers arr[1], arr[2], ..., arr[N].The numbers in the array will be randomly ordered. Your task is to determine if it is possible to get an array sorted in non-decreasing order by performing the following operation on the given array: You are allowed to perform right shift operation any number of times. One right shift operation means shifting all elements of the array by one position in the right direction. The last element of the array will be moved to the starting position in the array i.e. 0th index. If it is possible to obtain the sorted array by performing the above operation then return True else return False. If the given array is empty then return True.",

    "match_parens_HE_119": "Create a function named match_parens for this given task: You are given a list of two strings, both strings consist of open parentheses '(' or close parentheses ')' only. Your job is to check if it is possible to concatenate the two strings in some order, that the resulting string will be good. A string S is considered to be good if and only if all parentheses in S are balanced. For example: the string '(())()' is good, while the string '())' is not. Return 'Yes' if there's a way to make a good string, and return 'No' otherwise.",

    "rounded_avg_HE_103": "Create a function named rounded_avg for this given task: You are given two positive integers n and m, and your task is to compute the average of the integers from n through m (including n and m). Round the answer to the nearest integer and convert that to binary. If n is greater than m, return -1.",

    "sort_array_HE_88": "Create a function named sort_array for this given task: Given an array of non-negative integers, return a copy of the given array after sorting, you will sort the given array in ascending order if the sum( first index value, last index value) is odd, or sort it in descending order if the sum( first index value, last index value) is even. Note: * don't change the given array."
}

# Quick test subset for development
QUICK_TEST_PROBLEMS = {
    "is_equal_to_sum_even_HE_138": BENCHMARK_PROBLEMS["is_equal_to_sum_even_HE_138"],
    "decimal_to_binary_HE_79": BENCHMARK_PROBLEMS["decimal_to_binary_HE_79"]
}

def get_all_problems():
    """Get all benchmark problems"""
    return BENCHMARK_PROBLEMS

def get_quick_problems():
    """Get quick test problems"""
    return QUICK_TEST_PROBLEMS