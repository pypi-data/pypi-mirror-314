import pytest
import os
from travo.console_scripts import Travo


@pytest.mark.parametrize("embed_option", [False, True])
def test_quickstart(embed_option, tmp_path):
    # Initialise the course directory
    course_dir = os.path.join(tmp_path, "MyCourse")
    Travo.quickstart(course_dir=course_dir, embed=embed_option)
    if embed_option:
        clab_dir = os.path.join(course_dir, "Instructors")
    else:
        clab_dir = course_dir
    assert os.path.isdir(course_dir + "/Instructors")
    assert os.path.isdir(clab_dir + "/ComputerLab")
