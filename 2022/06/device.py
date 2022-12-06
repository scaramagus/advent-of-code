"""Solution for adventofcode.com/2022/day/06
"""
def get_marker_position(stream: str, group_size: int) -> int:
    """Returns the number of characters processed until a marker has been found in stream.
    A marker is defined as the first group of distinct characters of size group_size found.

    >>> get_marker_position('bvwbjplbgvbhsrlpgdmjqwftvncz', 4)
    5
    >>> get_marker_position('nppdvjthqldpwncqszvftbrmjlhg', 4)
    6
    >>> get_marker_position('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4)
    10
    >>> get_marker_position('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4)
    11
    >>> get_marker_position('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14)
    19
    >>> get_marker_position('bvwbjplbgvbhsrlpgdmjqwftvncz', 14)
    23
    >>> get_marker_position('nppdvjthqldpwncqszvftbrmjlhg', 14)
    23
    >>> get_marker_position('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14)
    29
    >>> get_marker_position('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14)
    26
    """
    for start in range(len(stream)):
        end = start + group_size
        letter_group = stream[start:end]

        if len(set(letter_group)) == len(letter_group):
            return end


if __name__ == "__main__":
    with open("input.txt") as f:
        stream = f.read().strip()

    position = get_marker_position(stream, 4)
    print(f"Marker found after {position} characters")

    position = get_marker_position(stream, 14)
    print(f"Start of message found after {position} characters")
