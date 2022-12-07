import directories


def test_from_command_list():
    root_dir = directories.Node.from_file("test_input.txt")

    assert root_dir["a"]["e"]["i"].total_size == 584
    assert root_dir["a"]["f"].total_size == 29116
    assert root_dir["a"]["g"].total_size == 2557
    assert root_dir["a"]["h.lst"].total_size == 62596
    assert root_dir["b.txt"].total_size == 14848514
    assert root_dir["c.dat"].total_size == 8504156
    assert root_dir["d"]["j"].total_size == 4060174
    assert root_dir["d"]["d.log"].total_size == 8033020
    assert root_dir["d"]["d.ext"].total_size == 5626152
    assert root_dir["d"]["k"].total_size == 7214296


def test_calculate_sum_of_sizes():
    root_dir = directories.Node.from_file("test_input.txt")
    total_size = directories.calculate_total_size_of_dirs_to_delete(root_dir, 100000)
    assert total_size == 95437

def test_find_smallest_dir_to_delete():
    root_dir = directories.Node.from_file("test_input.txt")
    smallest_dir = directories.find_smallest_dir_to_delete(root_dir, 70000000, 30000000)
    assert smallest_dir.name == "d"
    assert smallest_dir.total_size == 24933642
