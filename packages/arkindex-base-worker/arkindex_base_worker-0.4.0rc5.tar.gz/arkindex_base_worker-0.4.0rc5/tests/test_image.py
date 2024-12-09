import logging
import math
import uuid
from io import BytesIO
from operator import attrgetter
from pathlib import Path

import pytest
from PIL import Image, ImageChops, ImageOps
from requests import HTTPError

from arkindex_worker.cache import CachedElement, create_tables, init_cache_db
from arkindex_worker.image import (
    IIIF_FULL,
    IIIF_MAX,
    BoundingBox,
    download_image,
    download_tiles,
    open_image,
    polygon_bounding_box,
    resized_images,
    revert_orientation,
    trim_polygon,
    update_pillow_image_size_limit,
    upload_image,
)
from arkindex_worker.models import Element
from tests import FIXTURES_DIR

TILE = FIXTURES_DIR / "test_image.jpg"
FULL_IMAGE = FIXTURES_DIR / "tiled_image.jpg"
ROTATED_IMAGE = FIXTURES_DIR / "rotated_image.jpg"
MIRRORED_IMAGE = FIXTURES_DIR / "mirrored_image.jpg"
ROTATED_MIRRORED_IMAGE = FIXTURES_DIR / "rotated_mirrored_image.jpg"
TEST_IMAGE = {"width": 800, "height": 300}


@pytest.fixture()
def mock_page():
    class Page(Element):
        def open_image(
            self,
            *args,
            max_width: int | None = None,
            max_height: int | None = None,
            use_full_image: bool | None = False,
            **kwargs,
        ) -> Image.Image:
            # Image from Socface (https://socface.site.ined.fr/) project (AD026)
            image = Image.open(FIXTURES_DIR / "AD026_6M_00505_0001_0373.jpg")
            image.thumbnail(size=(max_width or image.width, max_height or image.height))

            return image

    return Page(
        id="page_id",
        name="1",
        zone={
            "polygon": [[0, 0], [1000, 0], [1000, 3000], [0, 3000], [0, 0]],
            "image": {"width": 1000, "height": 3000},
        },
        rotation_angle=0,
        mirrored=False,
    )


def _root_mean_square(img_a, img_b):
    """
    Get the root-mean-square difference between two images for fuzzy matching
    See https://effbot.org/zone/pil-comparing-images.htm
    """
    h = ImageChops.difference(img_a, img_b).histogram()
    return math.sqrt(
        sum((value * ((idx % 256) ** 2) for idx, value in enumerate(h)))
        / float(img_a.size[0] * img_a.size[1])
    )


@pytest.mark.parametrize(
    ("max_image_pixels", "expected_image_pixels"),
    [
        # Pillow Image size limit not updated
        (None, Image.MAX_IMAGE_PIXELS),
        # Pillow Image size limit set to None
        ("0", None),
        (0, None),
        # Update Pillow Image size limit
        ("1", 1),
        (1, 1),
    ],
)
def test_update_pillow_image_size_limit(max_image_pixels, expected_image_pixels):
    MAX_IMAGE_PIXELS = Image.MAX_IMAGE_PIXELS

    @update_pillow_image_size_limit
    def function() -> int | None:
        return Image.MAX_IMAGE_PIXELS

    assert function(max_image_pixels=max_image_pixels) == expected_image_pixels
    assert Image.MAX_IMAGE_PIXELS == MAX_IMAGE_PIXELS


def test_download_tiles(responses):
    expected = Image.open(FULL_IMAGE).convert("RGB")
    tile_bytes = TILE.read_bytes()

    responses.add(
        responses.GET,
        "http://nowhere/info.json",
        json={"width": 543, "height": 720, "tiles": [{"width": 181, "height": 240}]},
    )

    for x in (0, 181, 362):
        for y in (0, 240, 480):
            responses.add(
                responses.GET,
                f"http://nowhere/{x},{y},181,240/full/0/default.jpg",
                body=tile_bytes,
            )

    actual = download_tiles("http://nowhere")

    assert _root_mean_square(expected, actual) <= 5.0


def test_download_tiles_crop(responses):
    """
    Ensure download_tiles does not care about tiles that are slightly bigger than expected
    (occasional issue with the Harvard IDS image server where 1024×1024 tiles sometimes are returned as 1024x1025)
    """
    expected = Image.open(FULL_IMAGE).convert("RGB")
    tile_bytes = BytesIO()
    # Add one extra pixel to each tile to return slightly bigger tiles
    ImageOps.pad(Image.open(TILE), (181, 241)).save(tile_bytes, format="jpeg")

    tile_bytes = tile_bytes.getvalue()

    responses.add(
        responses.GET,
        "http://nowhere/info.json",
        json={"width": 543, "height": 720, "tiles": [{"width": 181, "height": 240}]},
    )

    for x in (0, 181, 362):
        for y in (0, 240, 480):
            responses.add(
                responses.GET,
                f"http://nowhere/{x},{y},181,240/full/0/default.jpg",
                body=tile_bytes,
            )

    actual = download_tiles("http://nowhere")

    assert _root_mean_square(expected, actual) <= 5.0


def test_download_tiles_small(responses):
    small_tile = BytesIO()
    Image.new("RGB", (1, 1)).save(small_tile, format="jpeg")
    small_tile.seek(0)

    responses.add(
        responses.GET,
        "http://nowhere/info.json",
        json={"width": 543, "height": 720, "tiles": [{"width": 181, "height": 240}]},
    )

    responses.add(
        responses.GET,
        "http://nowhere/0,0,181,240/full/0/default.jpg",
        body=small_tile.read(),
    )

    with pytest.raises(
        ValueError, match="Expected size 181×240 for tile 0,0, but got 1×1"
    ):
        download_tiles("http://nowhere")


@pytest.mark.parametrize(
    ("path", "is_local"),
    [
        ("http://somewhere/test.jpg", False),
        ("https://somewhere/test.jpg", False),
        ("path/to/something", True),
        ("/absolute/path/to/something", True),
    ],
)
def test_open_image(path, is_local, monkeypatch):
    """Check if the path triggers a local load or a remote one"""

    monkeypatch.setattr(Path, "exists", lambda x: True)
    monkeypatch.setattr(Image, "open", lambda x: Image.new("RGB", (1, 10)))
    monkeypatch.setattr(
        "arkindex_worker.image.download_image", lambda x: Image.new("RGB", (10, 1))
    )
    image = open_image(path)

    if is_local:
        assert image.size == (1, 10)
    else:
        assert image.size == (10, 1)


@pytest.mark.parametrize(
    ("rotation_angle", "mirrored", "expected_path"),
    [
        (0, False, TILE),
        (45, False, ROTATED_IMAGE),
        (0, True, MIRRORED_IMAGE),
        (45, True, ROTATED_MIRRORED_IMAGE),
    ],
)
def test_open_image_rotate_mirror(rotation_angle, mirrored, expected_path):
    expected = Image.open(expected_path).convert("RGB")
    actual = open_image(str(TILE), rotation_angle=rotation_angle, mirrored=mirrored)
    actual.save(f"/tmp/{rotation_angle}_{mirrored}.jpg")
    assert _root_mean_square(expected, actual) <= 15.0


@pytest.mark.parametrize(
    ("polygon", "error"),
    [
        # Polygon input isn't a list or tuple
        (
            {
                "polygon": [
                    [99, 200],
                    [25, 224],
                    [0, 0],
                    [0, 300],
                    [102, 300],
                    [260, 300],
                    [288, 295],
                    [296, 260],
                    [352, 259],
                    [106, 210],
                    [197, 206],
                    [99, 208],
                ]
            },
            "Input polygon must be a valid list or tuple of points.",
        ),
        # Point coordinates are not integers
        (
            [
                [9.9, 200],
                [25, 224],
                [0, 0],
                [0, 300],
                [102, 300],
                [260, 300],
                [288, 295],
                [296, 260],
                [352, 259],
                [106, 210],
                [197, 206],
                [99, 20.8],
            ],
            "Polygon point coordinates must be integers.",
        ),
        # Point coordinates are not lists or tuples
        (
            [
                [12, 56],
                [29, 60],
                [35, 61],
                "[42, 59]",
                [58, 57],
                [65, 61],
                [72, 57],
                [12, 56],
            ],
            "Polygon points must be tuples or lists.",
        ),
        # Point coordinates are not lists or tuples of length 2
        (
            [
                [12, 56],
                [29, 60, 3],
                [35, 61],
                [42, 59],
                [58, 57],
                [65, 61],
                [72, 57],
                [12, 56],
            ],
            "Polygon points must be tuples or lists of 2 elements.",
        ),
        # None of the polygon's points are inside the image
        (
            [
                [999, 200],
                [1097, 224],
                [1020, 251],
                [1232, 350],
                [1312, 364],
                [1325, 310],
                [1318, 295],
                [1296, 260],
                [1352, 259],
                [1006, 210],
                [997, 206],
                [999, 200],
            ],
            "This polygon is entirely outside the image's bounds.",
        ),
    ],
)
def test_trim_polygon_errors(polygon, error):
    with pytest.raises(AssertionError, match=error):
        trim_polygon(polygon, TEST_IMAGE["width"], TEST_IMAGE["height"])


def test_trim_polygon_negative_coordinates():
    """
    Negative coordinates are ignored and replaced by 0 with no error being thrown
    """
    polygon = [
        [99, 200],
        [25, 224],
        [-8, -52],
        [-12, 350],
        [102, 364],
        [260, 310],
        [288, 295],
        [296, 260],
        [352, 259],
        [106, 210],
        [197, 206],
        [99, 200],
    ]
    expected_polygon = [
        [99, 200],
        [25, 224],
        [0, 0],
        [0, 300],
        [102, 300],
        [260, 300],
        [288, 295],
        [296, 260],
        [352, 259],
        [106, 210],
        [197, 206],
        [99, 200],
    ]
    assert (
        trim_polygon(polygon, TEST_IMAGE["width"], TEST_IMAGE["height"])
        == expected_polygon
    )


def test_trim_polygon_partially_outside_image():
    polygon = [
        [99, 200],
        [197, 224],
        [120, 251],
        [232, 350],
        [312, 364],
        [325, 310],
        [318, 295],
        [296, 260],
        [352, 259],
        [106, 210],
        [197, 206],
        [99, 200],
    ]
    expected_polygon = [
        [99, 200],
        [197, 224],
        [120, 251],
        [232, 300],
        [312, 300],
        [325, 300],
        [318, 295],
        [296, 260],
        [352, 259],
        [106, 210],
        [197, 206],
        [99, 200],
    ]
    assert (
        trim_polygon(polygon, TEST_IMAGE["width"], TEST_IMAGE["height"])
        == expected_polygon
    )


def test_trim_polygon():
    polygon = (
        (12, 56),
        (29, 60),
        (35, 61),
        (42, 59),
        (58, 57),
        (65, 61),
        (72, 57),
        (12, 56),
    )
    expected_polygon = [
        [12, 56],
        [29, 60],
        [35, 61],
        [42, 59],
        [58, 57],
        [65, 61],
        [72, 57],
        [12, 56],
    ]
    assert (
        trim_polygon(polygon, TEST_IMAGE["width"], TEST_IMAGE["height"])
        == expected_polygon
    )


@pytest.mark.parametrize(
    ("angle", "mirrored", "updated_bounds", "reverse"),
    [
        (
            0,
            False,
            {"x": 295, "y": 11, "width": 111, "height": 47},  # upper right
            True,
        ),
        (
            90,
            False,
            {"x": 510, "y": 295, "width": 47, "height": 111},  # lower right
            True,
        ),
        (
            180,
            False,
            {"x": 9, "y": 510, "width": 111, "height": 47},  # lower left
            True,
        ),
        (
            270,
            False,
            {"x": 11, "y": 9, "width": 47, "height": 111},  # upper left
            True,
        ),
        (
            0,
            True,
            {"x": 9, "y": 11, "width": 111, "height": 47},  # upper left
            True,
        ),
        (
            90,
            True,
            {"x": 510, "y": 9, "width": 47, "height": 111},  # upper right
            True,
        ),
        (
            180,
            True,
            {"x": 295, "y": 510, "width": 111, "height": 47},  # lower right
            True,
        ),
        (
            270,
            True,
            {"x": 11, "y": 295, "width": 47, "height": 111},  # lower left
            True,
        ),
        (
            0,
            False,
            {"x": 295, "y": 11, "width": 111, "height": 47},  # upper right
            False,
        ),
        (
            90,
            False,
            {"x": 11, "y": 162, "width": 47, "height": 111},  # upper left
            False,
        ),
        (
            180,
            False,
            {"x": 9, "y": 510, "width": 111, "height": 47},  # lower left
            False,
        ),
        (
            270,
            False,
            {"x": 357, "y": 295, "width": 47, "height": 111},  # lower right
            False,
        ),
        (
            0,
            True,
            {"x": 9, "y": 11, "width": 111, "height": 47},  # upper left
            False,
        ),
        (
            90,
            True,
            {"x": 357, "y": 162, "width": 47, "height": 111},  # lower left
            False,
        ),
        (
            180,
            True,
            {"x": 295, "y": 510, "width": 111, "height": 47},  # lower right
            False,
        ),
        (
            270,
            True,
            {"x": 11, "y": 295, "width": 47, "height": 111},  # upper right
            False,
        ),
    ],
)
def test_revert_orientation(angle, mirrored, updated_bounds, reverse, tmp_path):
    """Test cases, for both Elements and CachedElements:
    - no rotation or orientation
    - rotation with 3 different angles (90, 180, 270)
    - rotation + mirror with 4 angles (0, 90, 180, 270)
    """
    child_polygon = [[295, 11], [295, 58], [406, 58], [406, 11], [295, 11]]

    # Setup cache db to test with CachedElements
    db_path = f"{tmp_path}/db.sqlite"
    init_cache_db(db_path)
    create_tables()

    image_polygon = [
        [0, 0],
        [0, 568],
        [415, 568],
        [415, 0],
        [0, 0],
    ]
    element = Element(
        {
            "mirrored": mirrored,
            "rotation_angle": angle,
            "zone": {"polygon": image_polygon},
        }
    )
    cached_element = CachedElement.create(
        id=uuid.uuid4(),
        type="paragraph",
        polygon=image_polygon,
        mirrored=mirrored,
        rotation_angle=angle,
    )

    assert polygon_bounding_box(
        revert_orientation(element, child_polygon, reverse=reverse)
    ) == BoundingBox(**updated_bounds)

    assert polygon_bounding_box(
        revert_orientation(cached_element, child_polygon, reverse=reverse)
    ) == BoundingBox(**updated_bounds)


def test_download_image_retry_with_max(responses):
    base_url = "https://blabla.com/iiif/2/image_path.jpg/231,699,2789,3659/{size}/0/default.jpg"

    full_url = base_url.format(size=IIIF_FULL)
    max_url = base_url.format(size=IIIF_MAX)

    # Full size gives an error
    responses.add(
        responses.GET,
        full_url,
        status=400,
    )
    # Max size works
    responses.add(
        responses.GET,
        max_url,
        status=200,
        body=TILE.read_bytes(),
    )

    image = download_image(full_url)
    assert image

    # We try 3 times with the first URL
    # Then the first try with the new URL is successful
    assert len(responses.calls) == 4
    assert list(map(attrgetter("request.url"), responses.calls)) == [full_url] * 3 + [
        max_url
    ]


def test_upload_image_retries(responses):
    dest_url = "https://blabla.com/iiif/2/image_path.jpg/full/full/0/default.jpg"
    responses.add(
        responses.PUT,
        dest_url,
        status=400,
    )

    image = Image.open(FULL_IMAGE).convert("RGB")
    with pytest.raises(
        HTTPError, match=f"400 Client Error: Bad Request for url: {dest_url}"
    ):
        upload_image(image, dest_url)

    # We try 3 times
    assert len(responses.calls) == 3
    assert list(map(attrgetter("request.url"), responses.calls)) == [dest_url] * 3


def test_upload_image(responses):
    dest_url = "https://blabla.com/iiif/2/image_path.jpg/full/full/0/default.jpg"
    responses.add(
        responses.PUT,
        dest_url,
        status=200,
    )

    image = Image.open(FULL_IMAGE).convert("RGB")
    resp = upload_image(image, dest_url)
    assert resp

    assert len(responses.calls) == 1
    assert list(map(attrgetter("request.url"), responses.calls)) == [dest_url]


@pytest.mark.parametrize(
    ("max_pixels", "max_bytes", "expected_sizes", "expected_logs"),
    [
        # No limits
        (
            None,
            None,
            [
                (1992, 3000),
                (1793, 2700),
                (1694, 2550),
                (1594, 2400),
                (1494, 2250),
                (1395, 2100),
                (1195, 1800),
                (996, 1500),
                (797, 1200),
                (598, 900),
            ],
            [
                (logging.WARNING, "The image was resized to (1992 x 3000)."),
                (logging.WARNING, "The image was resized to (1793 x 2700)."),
                (logging.WARNING, "The image was resized to (1694 x 2550)."),
                (logging.WARNING, "The image was resized to (1594 x 2400)."),
                (logging.WARNING, "The image was resized to (1494 x 2250)."),
                (logging.WARNING, "The image was resized to (1395 x 2100)."),
                (logging.WARNING, "The image was resized to (1195 x 1800)."),
                (logging.WARNING, "The image was resized to (996 x 1500)."),
                (logging.WARNING, "The image was resized to (797 x 1200)."),
                (logging.WARNING, "The image was resized to (598 x 900)."),
            ],
        ),
        # Image already under the limits
        (
            10000,
            4000000,  # 4MB
            [
                (1992, 3000),
                (1793, 2700),
                (1694, 2550),
                (1594, 2400),
                (1494, 2250),
                (1395, 2100),
                (1195, 1800),
                (996, 1500),
                (797, 1200),
                (598, 900),
            ],
            [
                (logging.WARNING, "The image was resized to (1992 x 3000)."),
                (logging.WARNING, "The image was resized to (1793 x 2700)."),
                (logging.WARNING, "The image was resized to (1694 x 2550)."),
                (logging.WARNING, "The image was resized to (1594 x 2400)."),
                (logging.WARNING, "The image was resized to (1494 x 2250)."),
                (logging.WARNING, "The image was resized to (1395 x 2100)."),
                (logging.WARNING, "The image was resized to (1195 x 1800)."),
                (logging.WARNING, "The image was resized to (996 x 1500)."),
                (logging.WARNING, "The image was resized to (797 x 1200)."),
                (logging.WARNING, "The image was resized to (598 x 900)."),
            ],
        ),
        # Image above the limits
        (
            None,
            100000,  # 100kB
            [(598, 900)],
            [
                (logging.WARNING, "The image was resized to (1992 x 3000)."),
                (logging.WARNING, "The image size is 773.4 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (1793 x 2700)."),
                (logging.WARNING, "The image size is 616.0 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (1694 x 2550)."),
                (logging.WARNING, "The image size is 546.4 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (1594 x 2400)."),
                (logging.WARNING, "The image size is 479.4 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (1494 x 2250)."),
                (logging.WARNING, "The image size is 416.1 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (1395 x 2100)."),
                (logging.WARNING, "The image size is 360.5 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (1195 x 1800)."),
                (logging.WARNING, "The image size is 258.6 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (996 x 1500)."),
                (logging.WARNING, "The image size is 179.0 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (797 x 1200)."),
                (logging.WARNING, "The image size is 115.7 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (598 x 900)."),
            ],
        ),
        # Image above the limits
        (
            2000,
            None,
            [(1328, 2000), (1195, 1800), (996, 1500), (797, 1200), (598, 900)],
            [
                (
                    logging.WARNING,
                    "Maximum image input size supported is (2000 x 2000).",
                ),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (1328 x 2000)."),
                (logging.WARNING, "The image was resized to (1195 x 1800)."),
                (logging.WARNING, "The image was resized to (996 x 1500)."),
                (logging.WARNING, "The image was resized to (797 x 1200)."),
                (logging.WARNING, "The image was resized to (598 x 900)."),
            ],
        ),
        # Image above the limits
        (
            2000,
            100000,  # 100kB
            [(598, 900)],
            [
                (
                    logging.WARNING,
                    "Maximum image input size supported is (2000 x 2000).",
                ),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (1328 x 2000)."),
                (logging.WARNING, "The image size is 325.5 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (1195 x 1800)."),
                (logging.WARNING, "The image size is 258.6 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (996 x 1500)."),
                (logging.WARNING, "The image size is 179.0 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (797 x 1200)."),
                (logging.WARNING, "The image size is 115.7 kB."),
                (logging.WARNING, "Maximum image input size supported is 100.0 kB."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (598 x 900)."),
            ],
        ),
        # Image always above the limits
        (
            50,
            50,  # 50B
            [],
            [
                (logging.WARNING, "Maximum image input size supported is (50 x 50)."),
                (logging.WARNING, "The image will be resized."),
                (logging.WARNING, "The image was resized to (33 x 50)."),
                (logging.WARNING, "The image size is 1.0 kB."),
                (logging.WARNING, "Maximum image input size supported is 50 Bytes."),
                (logging.WARNING, "The image will be resized."),
            ],
        ),
    ],
)
def test_resized_images(
    max_pixels, max_bytes, expected_sizes, expected_logs, mock_page, caplog
):
    caplog.set_level(logging.WARNING)

    assert [
        Image.open(image).size
        for image in resized_images(
            element=mock_page, max_pixels=max_pixels, max_bytes=max_bytes
        )
    ] == expected_sizes
    assert [
        (record.levelno, record.message) for record in caplog.records
    ] == expected_logs
