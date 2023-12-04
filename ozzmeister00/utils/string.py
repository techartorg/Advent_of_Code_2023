import re
import string


SYMBOLS = string.punctuation.replace('.', '')


def findall(subString, inString):
    """
    Return a list of indexes of all the start of the instances of
     the input subString in the input string

    :param str subString: the substring for which to search
    :param str inString: the string in which to search

    :return list[int]: the indexes of all the instances of the input substring in the input string
    """
    return [i.start() for i in re.finditer(subString, inString)]


def findall_end(subString, inString):
    """
    Return a list of indexes of the end of all of the instances 
    of the input subString in the input string

    :param str subString: the substring for which to search
    :param str inString: the string in which to search

    :return list[int]: the indexes of the ends of all the instances of the input substring in the input string
    """
    return [i.end() for i in re.finditer(subString, inString)]

def findall_range(subString, inString):
    """
    Return a list of tuples describing the start and end of all of the instances 
    of the input subString in the input string

    :param str subString: the substring for which to search
    :param str inString: the string in which to search

    :return list[(int, int)]: the indexes of the starts and ends of all the instances of the input substring in the input string
    """
    return list(zip(findall(subString, inString), findall_end(subString, inString)))

