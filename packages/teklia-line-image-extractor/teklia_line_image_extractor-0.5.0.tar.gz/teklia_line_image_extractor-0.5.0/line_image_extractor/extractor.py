# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import Union

import cv2
import numpy as np

from line_image_extractor.image_utils import (
    DESKEW,
    SKEW,
    WHITE,
    BoundingBox,
    Extraction,
    deskew_image,
    extract_bbox_image,
    extract_min_area_rect_image,
    extract_polygon_image,
    logger,
    polygon_to_bbox,
    resize,
    rotate_and_trim,
)


def extract(
    img: np.ndarray,
    polygon: np.ndarray,
    bbox: BoundingBox,
    extraction_mode: Extraction,
    max_deskew_angle: int = None,
    skew_angle: int = None,
    grayscale: bool = False,
) -> np.ndarray:
    """
    This is the main function to be used for extracting line images in tools/workers.

    It extracts either a bounding box image, a polygon or a minimum area rectangle.

    Also polygon and minimum area rectangles can be deskewed or skewed.

    :param img: Input page image (read with cv2(
    :param polygon: the polygon of the line to be extracted
    :param bbox: the bounding box of the line to be extracted
    :param extraction_mode: which mode of extraction to be used
    :param max_deskew_angle: limit deskew angle - avoid deskewing lines with a bigger abs(angle)
    :param skew_angle: skew the image in degrees (- for clockwise, + for counter clockwise)
    :param grayscale: convert the image to grayscale
    :return: the extracted image
    """
    if grayscale:
        background = WHITE
    else:
        background = (WHITE, WHITE, WHITE)

    if extraction_mode == Extraction.boundingRect:
        return extract_bbox_image(img, bbox=bbox)
    elif extraction_mode == Extraction.polygon:
        return extract_polygon_image(img, polygon=polygon, bbox=bbox)
    elif extraction_mode == Extraction.min_area_rect:
        return extract_min_area_rect_image(img, polygon=polygon)
    elif extraction_mode.extra == DESKEW:
        assert (
            max_deskew_angle is not None and max_deskew_angle > 0
        ), "max_deskew_angle can't be None and must be greater than 0"

        if extraction_mode == Extraction.deskew_polygon:
            extracted_img = extract_polygon_image(img, polygon=polygon, bbox=bbox)
        elif extraction_mode == Extraction.deskew_min_area_rect:
            extracted_img = extract_min_area_rect_image(img, polygon=polygon)
        else:
            raise ValueError(f"Unsupported deskew extraction mode: {extraction_mode}")

        return deskew_image(extracted_img, polygon, max_deskew_angle, background)

    elif extraction_mode.extra == SKEW:
        assert (
            skew_angle is not None and skew_angle != 0
        ), "skew_angle can't be None and must not equal 0"

        if extraction_mode == Extraction.skew_polygon:
            extracted_img = extract_polygon_image(img, polygon=polygon, bbox=bbox)

        elif extraction_mode == Extraction.skew_min_area_rect:
            extracted_img = extract_min_area_rect_image(img, polygon=polygon)
        else:
            raise ValueError(f"Unsupported skew extraction mode: {extraction_mode}")

        return rotate_and_trim(extracted_img, skew_angle, background)

    else:
        raise ValueError(f"Unsupported extraction mode: {extraction_mode}")


def extract_from_img_file(
    in_file: Path,
    out_file: Path,
    polygon_file: Path,
    extraction_mode: Extraction = Extraction.boundingRect,
    max_deskew_angle: int = None,
    skew_angle: int = None,
    grayscale: bool = False,
    scale_x: float = None,
    scale_y_top: float = None,
    scale_y_bottom: float = None,
    # **kwargs,
) -> bool:
    img = read_img(in_file, grayscale)
    poly_json = json.loads(polygon_file.read_text())
    polygon = np.asarray(poly_json)
    if scale_x or scale_y_top or scale_y_bottom:
        max_height = img.shape[0]
        max_width = img.shape[1]
        scale_x = scale_x or 1.0
        scale_y_top = scale_y_top or 1.0
        scale_y_bottom = scale_y_bottom or 1.0
        polygon = resize(
            polygon, max_width, max_height, scale_x, scale_y_top, scale_y_bottom
        )
        polygon = np.asarray(polygon)
    rect = polygon_to_bbox(polygon)
    extracted_img = extract(
        img, polygon, rect, extraction_mode, max_deskew_angle, skew_angle, grayscale
    )
    return save_img(out_file, extracted_img)


def read_img(path: Union[Path, str], grayscale=False) -> np.ndarray:
    if grayscale:
        _cv2_flag = cv2.IMREAD_GRAYSCALE
    else:
        _cv2_flag = cv2.IMREAD_COLOR
    img = np.asarray(cv2.imread(str(path), _cv2_flag))
    return img


def save_img(path: Union[Path, str], img: np.ndarray) -> bool:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(path), img)
    if not success:
        logger.info(f"Saving image to {path} failed")
    return success
