# Line image extractor

This is a tool and a library to be used for extracting line images. Built by [Teklia](https://teklia.com) and freely available as open-source under the MIT licence.

It supports different extraction methods:
* boundingRect - bounding rectangle of the line polygon
* polygon - exact polygon
* min_area_rect - minimum area rectangle containing the polygon
* deskew_polygon - deskew the polygon
* deskew_min_area_rect - deskew the minimum area rectangle
* skew_polygon - skew the polygon (rotate by some angle)
* skew_min_area_rect - skew the minimum area rectangle (rotate by some angle)

Install the library using stable version from Pypi:

```bash
pip install teklia-line-image-extractor
```

Install the library in development mode:

```bash
pip install -e .
```

Test extraction:

```bash
line-image-extractor -i tests/data/page_img.jpg -o out.jpg -p tests/data/line_polygon.json -e deskew_min_area_rect --color
```

How to use it?:

```python
from pathlib import Path
import numpy as np
from line_image_extractor.extractor import extract, read_img, save_img
from line_image_extractor.image_utils import polygon_to_bbox
from line_image_extractor.image_utils import Extraction

page_img = read_img(Path("tests/data/page_img.jpg"))
polygon = np.asarray([[241, 1169], [2287, 1251], [2252, 1190], [244, 1091], [241, 1169]])
bbox = polygon_to_bbox(polygon)
extracted_img = extract(
    page_img, polygon, bbox, Extraction.polygon
)
save_img("line_output.jpg", extracted_img)
```
