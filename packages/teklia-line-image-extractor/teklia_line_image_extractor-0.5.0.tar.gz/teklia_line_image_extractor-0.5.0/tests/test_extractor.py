# -*- coding: utf-8 -*-
import pytest

from line_image_extractor.extractor import extract, read_img
from line_image_extractor.image_utils import WHITE, Extraction, polygon_to_bbox, resize

TEST_POLYGONS = [
    [[100, 100], [300, 100], [300, 200], [100, 200]],
    [[400, 100], [600, 100], [600, 200], [400, 200]],
    [[700, 100], [1100, 100], [1100, 200], [700, 200]],
    [[100, 100], [900, 100], [900, 400], [100, 400]],
    [[100, 3500], [2500, 3500], [2500, 3800], [100, 3800]],
]
TEST_POLYGONS_MOMENTS = [
    {"m00": 20000.0, "m10": 4000000.0, "m01": 3000000.0},
    {"m00": 20000.0, "m10": 10000000.0, "m01": 3000000.0},
    {"m00": 40000.0, "m10": 36000000.0, "m01": 6000000.0},
    {"m00": 240000.0, "m10": 120000000.0, "m01": 60000000.0},
    {"m00": 720000.0, "m10": 936000000.0, "m01": 2628000000.0},
]
RESIZED_TEST_POLYGONS = [
    [[89, 50], [310, 50], [310, 250], [89, 250]],
    [[390, 50], [610, 50], [610, 250], [390, 250]],
    [[680, 50], [1120, 50], [1120, 250], [680, 250]],
    [[59, 0], [940, 0], [940, 550], [59, 550]],
    [[0, 3350], [2620, 3350], [2620, 3834], [0, 3834]],
]


def is_close(a, b, allowed_diff=0.01):
    return abs(a - b) <= allowed_diff


@pytest.mark.parametrize(
    "mode, grayscale, expected_white_ratio",
    (
        (Extraction.boundingRect, False, 0),
        (Extraction.polygon, False, 0.56),
        (Extraction.boundingRect, True, 0),
        (Extraction.polygon, True, 0.56),
    ),
)
def test_extract__no_extra(
    mode, grayscale, expected_white_ratio, fake_page_img_path, fake_line_polygon
):
    page_img = read_img(fake_page_img_path, grayscale)
    bbox = polygon_to_bbox(fake_line_polygon)
    extracted_img = extract(
        page_img, fake_line_polygon, bbox, mode, grayscale=grayscale
    )

    (H, W) = extracted_img.shape[:2]
    assert H == bbox.height
    assert W == bbox.width

    if grayscale:
        completely_white_count = (extracted_img == WHITE).sum()
    else:
        completely_white_count = (extracted_img == WHITE).all(axis=2).sum()
    # after extracting the polygon image there will be white background
    white_ratio = completely_white_count / (H * W)
    assert is_close(white_ratio, expected_white_ratio)


@pytest.mark.parametrize(
    "mode, grayscale, expected_white_ratio",
    (
        (Extraction.min_area_rect, False, 0.50),
        (Extraction.min_area_rect, True, 0.50),
    ),
)
def test_extract_min_area_rect(
    mode, grayscale, expected_white_ratio, fake_page_img_path, fake_line_polygon
):
    page_img = read_img(fake_page_img_path, grayscale)
    bbox = polygon_to_bbox(fake_line_polygon)
    extracted_img = extract(
        page_img, fake_line_polygon, bbox, mode, grayscale=grayscale
    )

    (H, W) = extracted_img.shape[:2]
    # true for this particular test, might not be for others
    assert H == bbox.height
    assert W != bbox.width
    assert W == 2051

    if grayscale:
        completely_white_count = (extracted_img == WHITE).sum()
    else:
        completely_white_count = (extracted_img == WHITE).all(axis=2).sum()
    # after extracting the polygon image there will be white background
    white_ratio = completely_white_count / (H * W)
    assert is_close(white_ratio, expected_white_ratio)


@pytest.mark.parametrize(
    "mode, grayscale, expected_white_ratio",
    (
        (Extraction.deskew_polygon, False, 0.13),
        (Extraction.deskew_min_area_rect, False, 0.02),
        (Extraction.deskew_polygon, True, 0.13),
        (Extraction.deskew_min_area_rect, True, 0.02),
    ),
)
def test_extract_deskew(
    mode, grayscale, expected_white_ratio, fake_page_img_path, fake_line_polygon
):
    page_img = read_img(fake_page_img_path, grayscale)
    bbox = polygon_to_bbox(fake_line_polygon)
    extracted_img = extract(
        page_img,
        fake_line_polygon,
        bbox,
        mode,
        max_deskew_angle=45,
        grayscale=grayscale,
    )

    (H, W) = extracted_img.shape[:2]
    # height gets smaller after deskewing
    assert H < bbox.height
    # width gets bigger after deskewing
    assert W > bbox.width

    if grayscale:
        completely_white_count = (extracted_img == WHITE).sum()
    else:
        completely_white_count = (extracted_img == WHITE).all(axis=2).sum()
    # after extracting the polygon image there will be white background
    white_ratio = completely_white_count / (H * W)
    assert is_close(white_ratio, expected_white_ratio)


@pytest.mark.parametrize(
    "mode, grayscale, skew_angle, expected_white_ratio",
    (
        (Extraction.skew_polygon, False, 5, 0.55),
        (Extraction.skew_polygon, False, 2, 0.22),
        (Extraction.skew_min_area_rect, False, 5, 0.54),
        (Extraction.skew_min_area_rect, False, 2, 0.12),
        (Extraction.skew_polygon, True, 5, 0.55),
        (Extraction.skew_polygon, True, 2, 0.22),
        (Extraction.skew_min_area_rect, True, 5, 0.54),
        (Extraction.skew_min_area_rect, True, 2, 0.12),
    ),
)
def test_extract_skew(
    mode,
    grayscale,
    skew_angle,
    expected_white_ratio,
    fake_page_img_path,
    fake_line_polygon,
):
    page_img = read_img(fake_page_img_path, grayscale)
    bbox = polygon_to_bbox(fake_line_polygon)
    extracted_img = extract(
        page_img,
        fake_line_polygon,
        bbox,
        mode,
        skew_angle=skew_angle,
        grayscale=grayscale,
    )

    (H, W) = extracted_img.shape[:2]
    # height changes after skewing
    assert H != bbox.height
    # width changes after skewing
    assert W != bbox.width

    if grayscale:
        completely_white_count = (extracted_img == WHITE).sum()
    else:
        completely_white_count = (extracted_img == WHITE).all(axis=2).sum()
    # after extracting the polygon image there will be white background
    white_ratio = completely_white_count / (H * W)
    assert is_close(white_ratio, expected_white_ratio)


@pytest.mark.parametrize(
    "input_poly, expected",
    (list(zip(TEST_POLYGONS, RESIZED_TEST_POLYGONS))),
)
def test_resize(input_poly, expected):
    resized_poly = resize(
        polygon=input_poly,
        max_width=2921,
        max_height=3834,
        scale_x=1.1,
        scale_y_top=2,
        scale_y_bottom=2,
    )
    assert resized_poly.tolist() == expected
