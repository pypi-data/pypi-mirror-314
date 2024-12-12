# -*- coding: utf-8 -*-
import logging
import math
import os
from enum import Enum
from typing import NamedTuple, Tuple, Union

import cv2
import numpy as np
from PIL import Image, ImageChops

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s/%(name)s: %(message)s"
)
logger = logging.getLogger(os.path.basename(__file__))

BoundingBox = NamedTuple(
    "BoundingBox", [("x", int), ("y", int), ("width", int), ("height", int)]
)

RIGHT_ANGLE = 90
WHITE = 255
DESKEW = "deskew"
SKEW = "skew"
NONE = "none"


class Extraction(Enum):
    boundingRect = (0, NONE)
    polygon = (1, NONE)
    # minimum containing rectangle with an angle (cv2.min_area_rect)
    min_area_rect = (2, NONE)
    deskew_polygon = (3, DESKEW)
    deskew_min_area_rect = (4, DESKEW)
    skew_polygon = (5, SKEW)
    skew_min_area_rect = (6, SKEW)

    def __init__(self, enum_id: int, extra: str):
        """
        Line image extraction modes
        :param enum_id: just a unique id
        :param extra: extra action to be done (deskew, skew) after extractin the line image
        """
        self.enum_id = enum_id
        self.extra = extra


def polygon_to_bbox(polygon: Union[list, np.ndarray]) -> BoundingBox:
    return BoundingBox._make(cv2.boundingRect(np.asarray(polygon).clip(0)))


def extract_bbox_image(img: np.ndarray, bbox: BoundingBox):
    (x, y, w, h) = bbox
    cropped = img[y : y + h, x : x + w].copy()
    return cropped


def extract_polygon_image(
    img: np.ndarray, polygon: np.ndarray, bbox: BoundingBox
) -> np.ndarray:
    """Extracts polygon from an image.
    Everything that is outside the polygon (background) is colored white"""
    pts = polygon.copy()
    cropped = extract_bbox_image(img, bbox)
    # start polygon coordinates from 0 after cropping
    pts = pts - pts.min(axis=0)
    # draw polygon mask for extraction
    mask = np.zeros(cropped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (WHITE, WHITE, WHITE), -1, cv2.LINE_AA)
    # extract polyon image (black background)
    poly_img = cv2.bitwise_and(cropped, cropped, mask=mask)
    # extract polygon background (white)
    bg = np.ones_like(cropped, np.uint8) * WHITE
    cv2.bitwise_not(bg, bg, mask=mask)
    # put polygon image and background together
    return bg + poly_img


def extract_min_area_rect_image(img: np.ndarray, polygon: np.ndarray) -> np.ndarray:
    min_area_rect = cv2.minAreaRect(polygon)
    # convert minimum area rect to polygon
    box = cv2.boxPoints(min_area_rect)
    box = np.intp(box)
    bbox = polygon_to_bbox(box)

    # get min area rect image
    box_img = extract_polygon_image(img, polygon=box, bbox=bbox)
    return box_img


# https://github.com/sbrunner/deskew
def rotate(
    image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(
        np.cos(angle_radian) * old_width
    )
    height = abs(np.sin(angle_radian) * old_width) + abs(
        np.cos(angle_radian) * old_height
    )

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(
        image, rot_mat, (int(round(height)), int(round(width))), borderValue=background
    )


# https://gist.githubusercontent.com/mattjmorrison/932345/raw/b45660bae541610f338bef715642b148c3c4d178/crop_and_resize.py
def trim(img: np.ndarray, border: Union[int, Tuple[int, int, int]] = WHITE):
    # TODO test if removing completely white rows (all pixels are 255) is faster
    image = Image.fromarray(img)
    background = Image.new(image.mode, image.size, border)
    diff = ImageChops.difference(image, background)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)


def rotate_and_trim(
    img: np.ndarray,
    rotate_angle: int,
    background: Union[int, Tuple[int, int, int]] = WHITE,
) -> np.ndarray:
    """
    Rotate image by given an angle and trim extra whitespace left after rotating
    """
    # rotate polygon image
    deskewed_img = rotate(img, rotate_angle, background)
    # trim extra whitespace left after rotating
    trimmed_img = trim(deskewed_img, background)
    trimmed_img = np.array(trimmed_img)

    return trimmed_img


def determine_rotate_angle(polygon: np.ndarray) -> float:
    """
    Use cv2.minAreaRect to get the angle of the minimal bounding rectangle
    and convert that angle to rotation angle.
    The polygon will be rotated by maximum of 45 degrees to either side.
    :param polygon:
    :return: rotation angle (-45, 45)
    """
    top_left, shape, angle = cv2.minAreaRect(polygon)

    if abs(angle) > RIGHT_ANGLE - 1:
        # correct rectangle (not rotated) gets angle = RIGHT_ANGLE from minAreaRect
        # since no way to know whether it should be rotated it will be ignored
        rotate_angle = 0
    elif angle > 45:
        rotate_angle = angle - RIGHT_ANGLE
    elif angle < -45:
        rotate_angle = angle + RIGHT_ANGLE
    elif abs(angle) == 45:
        # no way to know in which direction it should be rotated
        rotate_angle = 0
    else:
        rotate_angle = angle

    # logger.debug(f"ANGLE: {angle:.2f} => {rotate_angle:.2f}")

    return rotate_angle


def deskew_image(
    img: np.ndarray,
    polygon: np.ndarray,
    max_deskew_angle: int,
    background: Union[int, Tuple[int, int, int]] = WHITE,
) -> np.ndarray:
    """
    Deskew image based on the angle from cv2.min_area_rect from the polygon
    :param img: already extracted image (polygon or min_area_rect)
    :param polygon: polygon of the original text line element
    :param max_deskew_angle: can set a max deskew angle limit to avoid unnecessary rotation/deskewing
    :return: deskew/rotated and trimmed image
    """
    # get angle from min area rect
    rotate_angle = determine_rotate_angle(polygon)

    if abs(rotate_angle) > max_deskew_angle:
        logger.warning(
            f"Deskew angle ({rotate_angle}) over the limit ({max_deskew_angle}), won't rotate"
        )
        rotate_angle = 0

    if rotate_angle != 0:
        return rotate_and_trim(img, rotate_angle, background)
    else:
        return img


def resize(
    polygon: Union[list, np.ndarray],
    max_width: int,
    max_height: int,
    scale_x: float,
    scale_y_top: float,
    scale_y_bottom: float,
) -> np.ndarray:
    """
    resize a polygon, limit coordinates to max dimensions

    Copied from moka.polygon
    """

    pts = np.asarray(polygon)

    M = cv2.moments(pts)
    center_X = int(M["m10"] / M["m00"])
    center_Y = int(M["m01"] / M["m00"])

    center_diff_y = pts[:, 1] - center_Y
    top = np.where(center_diff_y < 0)
    bottom = np.where(center_diff_y >= 0)
    pts[top, 1] = center_diff_y[top] * scale_y_top + center_Y
    pts[bottom, 1] = center_diff_y[bottom] * scale_y_bottom + center_Y

    pts[:, 0] = np.clip((pts[:, 0] - center_X) * scale_x + center_X, 0, max_width)
    pts[:, 1] = np.clip(pts[:, 1], 0, max_height)

    return pts
