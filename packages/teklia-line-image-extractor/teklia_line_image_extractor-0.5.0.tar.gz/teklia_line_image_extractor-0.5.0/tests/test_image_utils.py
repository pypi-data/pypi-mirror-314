# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pytest

from line_image_extractor.image_utils import determine_rotate_angle


@pytest.mark.parametrize(
    "angle, expected_rotate_angle",
    (
        (-1, -1),
        (0, 0),
        (10, 10),
        (44.9, 45),
        (45.1, -45),
        (45, 0),
        (46, -44),
        (50, -40),
        (89, -1),
        (90, 0),
        (91, 1),
        (134, 44),
        (135, 0),
        (136, -44),
        (179, -1),
        (180, 0),
        (-180, 0),
        (-179, 1),
        (-91, -1),
        (-90, 0),
        (-46, 44),
        (-45, 0),
        (-44, -44),
    ),
)
def test_determine_rotate_angle(angle, expected_rotate_angle):
    top_left = [300, 300]
    shape = [400, 100]
    # create polygon with expected angle
    box = cv2.boxPoints((top_left, shape, angle))
    box = np.intp(box)
    _, _, calc_angle = cv2.minAreaRect(box)
    rotate_angle = determine_rotate_angle(box)

    assert (
        round(rotate_angle) == expected_rotate_angle
    ), f"C, A, R: {calc_angle} === {angle} === {rotate_angle}"
