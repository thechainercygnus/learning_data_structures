# hash_distribution.py

from collections import Counter


def distribute(items, num_containers, hash_function=hash):
    return Counter([hash_function(item) % num_containers for item in items])


def plot(histogram):
    for key in sorted(histogram):
        count = histogram[key]
        padding = (max(histogram.values()) - count) * " "
        print(f"{key:3} {'■' * count}{padding} ({count})")


def hashcheck(integer: int) -> int | None:
    """finds the max int for hash == self"""
    for i in range(integer):
        if i != hash(i):
            return i
    return None


def hash_function(key):
    return sum(
        index * ord(character)
        for index, character in enumerate(repr(key).lstrip("'"), start=1)
    )
