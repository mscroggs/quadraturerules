import os


def join(*folders):
    if len(folders) == 1:
        return folders[0]

    return join(os.path.join(*folders[:2]), *folders[2:])


def test_numbering():
    folder = join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
        "rules",
    )
    qr_files = []
    folders = []
    for file in os.listdir(folder):
        if file.endswith(".qr"):
            assert os.path.isfile(os.path.join(folder, file))
            qr_files.append(file[:-3])
        else:
            assert os.path.isdir(os.path.join(folder, file))
            folders.append(file)

    assert set(qr_files) == set(folders)
    for i in range(1, len(qr_files) + 1):
        assert "Q" + f"000000{i}"[-6:] in qr_files