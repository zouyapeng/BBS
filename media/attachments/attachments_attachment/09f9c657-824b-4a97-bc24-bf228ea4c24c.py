"""
Given an old and new markdown snippet, detect if any new person
references have been added.
"""

import difflib
import re


# Detect references to person with hashcode, eg @JohnSmith-a1b2c
PERSON_REGEX = re.compile(r"@\w+-([\w^_]+)", re.UNICODE)

def diff_snippets(text1, text2, ignore_moved=False):
    """
    Perform a comparison of two markdown strings. Return the segments that
        are different.
    :param text1: The first markdown string
    :param text2: The second markdown string
    :param ignore_moved: Should this skip lines that have moved in the file?
        They would show up as diffs, even though
    :param junk_func: A function used to determine what lines to accept.
        Eg, can only examine lines where a person is mentioned.
    :return: list: The lines that are marked as changes (ONLY present in
        one file or the other)
    """
    differ = difflib.ndiff(text1.splitlines(), text2.splitlines())

    old_only = []
    new_only = []

    # Find lines corresponding to actual differences
    for diff in differ:
        d_text = diff[2:]

        if diff.startswith("- "):
            old_only.append(d_text)
        elif diff.startswith("+ "):
            new_only.append(d_text)
    return old_only, new_only


def new_mentions(line_strings):
    """
    Given a diff between two files, identify new lines that mention a person.

    From markdown person mentions (eg @JohnSmith-a1b2c), extract hashcodes
    :param line_strings: list: A list of strings representing each line in file
    :return: A list of hashcode person-ids
    """
    # TODO: Initial version would send emails if the line was changed at all-
    # eg if punctuation was added after a person. That is undesirable.
    new_person_hashes = []
    for line in line_strings:
        new_person_hashes.extend(re.findall(PERSON_REGEX, line))

    return new_person_hashes


# TODO: Should user feedback mechanism exist to update markdown when a person has been deleted?