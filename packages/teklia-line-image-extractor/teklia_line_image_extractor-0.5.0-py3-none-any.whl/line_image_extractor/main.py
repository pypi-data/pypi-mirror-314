# -*- coding: utf-8 -*-
import argparse
from pathlib import Path

from line_image_extractor.extractor import extract_from_img_file
from line_image_extractor.image_utils import Extraction


def create_cli_parser():

    parser = argparse.ArgumentParser(
        description="Script to extract line polygon images with different methods",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-i", "--in_file", type=Path, required=True, help="Input image")

    parser.add_argument(
        "-o", "--out_file", type=Path, required=True, help="Output image"
    )

    parser.add_argument(
        "-p",
        "--polygon_file",
        type=Path,
        required=True,
        help="Input file containing a polygon (2D list of ints)",
    )

    parser.add_argument(
        "-e",
        "--extraction_mode",
        type=lambda x: Extraction[x],
        default=Extraction.boundingRect,
        help=f"Mode for extracting the line images: {[e.name for e in Extraction]}",
    )

    parser.add_argument(
        "--max_deskew_angle",
        type=int,
        default=45,
        help="Maximum angle by which deskewing is allowed to rotate the line image. "
        "If the angle determined by deskew tool is bigger than max "
        "then that line won't be deskewed/rotated.",
    )

    parser.add_argument(
        "--skew_angle",
        type=int,
        default=0,
        help="Angle by which the line image will be rotated. Useful for data augmentation"
        " - creating skewed text lines for a more robust model."
        " Only used with skew_* extraction modes.",
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--grayscale",
        action="store_true",
        dest="grayscale",
        help="Convert images to grayscale (By default grayscale)",
    )
    group.add_argument(
        "--color", action="store_false", dest="grayscale", help="Use color images"
    )
    group.set_defaults(grayscale=True)

    parser.add_argument(
        "--scale_x",
        type=float,
        default=None,
        help="Ratio of how much to scale the polygon horizontally (1.0 means no rescaling)",
    )
    parser.add_argument(
        "--scale_y_top",
        type=float,
        default=None,
        help="Ratio of how much to scale the polygon vertically on the top (1.0 means no rescaling)",
    )

    parser.add_argument(
        "--scale_y_bottom",
        type=float,
        default=None,
        help="Ratio of how much to scale the polygon vertically on the bottom (1.0 means no rescaling)",
    )

    return parser


def main():
    parser = create_cli_parser()
    args = parser.parse_args()

    extract_from_img_file(**vars(args))


if __name__ == "__main__":
    main()
