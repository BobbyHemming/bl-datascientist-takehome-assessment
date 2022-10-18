"""
At BehaviourLab, it's very important that all employees use secure passwords. A password is considered secure only if it meets the following four conditions:

It must have between 7 and 25 characters
It must contain at least one lowercase letter, at least one uppercase letter, and at least one digit
It must not contain any individual character more than three times in succession (e.g. "..bbb.." is weak, "..aa...a." is strong)
It must not include any of the common passwords in the provided common-passwords.txt. You may convert the common-passwords.txt into any format of your choice if necessary.
Given a string called password, return the number of steps required to make the password secure. If the password is already secure, return 0.

One step can be any of the following three actions:

Insert one character to the password,
Delete one character from the password, or
Replace one character of the password with another character.

EXPECTATIONS
Please don't spend more than 40-60 mins on this task.
Please use Python to complete this task.
We're most interested to see problem solving and your approach.
Keep it simple, keep it DRY, but don't over complicate or over engineer.
Please comment the code and write tests where appropriate.
Include any assumptions you have made.

"""
import math
from itertools import groupby


common_passwords = open("data/common-passwords.txt", "r").read().split('\n')


def password_security(password):
    """
    -> It must have between 7 and 25 characters
    -> It must contain at least one lowercase letter, at least one uppercase letter, and at least one digit
    -> It must not contain any individual character more than three times in succession
        -> e.g. "..bbb.." is weak, "..aa...a." is strong
    -> It must not include any of the common passwords in the provided common-passwords.txt.
    :param str password: Given a string called password
    :returns int: the number of steps required to make the password secure.
    """

    steps = 0   # If the password is already secure, return 0.

    if not any(x.isupper() for x in password):
        steps += 1

    if not any(x.islower() for x in password):
        steps += 1

    if not any(x.isdigit() for x in password):
        steps += 1

    # Examine repeated consecutive chars
    result = [(label, sum(1 for _ in group)) for label, group in groupby(password)]

    consecutive_changes, _steps = 0, steps
    for char, count in result:
        if count >= 3:
            extra_values_required = math.floor(count / 3)
            # if we already need extra characters, we can use those to break up the consecutive chars
            if _steps - consecutive_changes < extra_values_required:
                consecutive_changes += extra_values_required
                _steps += 1
            else:
                _steps -= 1   # if we do use a previous change, we have fewer steps to use

    steps += consecutive_changes

    for common_password in common_passwords:  # we can't use common_password changes to disrupt repeated consec values
        if common_password in password:
            steps += 1  # we need value change to disrupt password

    # Examine Password length
    password_length = len(password) + steps
    if 7 > password_length:
        steps += 7 - password_length
    if password_length > 25:
        steps += password_length - 25

    return steps  # number of steps required to make the password secure


def test_password_security_function(func):
    tests_passed = 0
    test_cases = [("z", 6), ("aA1", 4), ("1377C0d3", 0), ('AB7aaabbbccc', 3), ('aaabbb', 2)]
    for password, no_required_steps in test_cases:
        result = func(password)
        if no_required_steps == result:
            tests_passed += 1
            print(f"Passed test case password = {password}, no steps required = {no_required_steps}, ans = {result}")
        else:
            print(f"Failed test case password = {password}, no steps required = {no_required_steps} ans = {result} ")
    print(f'\n{tests_passed}/{len(test_cases)} tests passed.')
    pass


if __name__ == '__main__':
    test_password_security_function(password_security)

