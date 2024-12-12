"""
Helper methods to download and open IIIF images, and manage polygons.
"""

import functools
import os
import re
import tempfile
from collections import namedtuple
from collections.abc import Generator, Iterator
from io import BytesIO
from math import ceil
from pathlib import Path
from typing import TYPE_CHECKING

import humanize
import requests
from PIL import Image
from shapely.affinity import rotate, scale, translate
from shapely.geometry import LinearRing
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from arkindex_worker import logger
from arkindex_worker.utils import pluralize
from teklia_toolbox.requests import should_verify_cert

# Avoid circular imports error when type checking
if TYPE_CHECKING:
    from arkindex_worker.cache import CachedElement
    from arkindex_worker.models import Element

# See http://docs.python-requests.org/en/master/user/advanced/#timeouts
DOWNLOAD_TIMEOUT = (30, 60)

BoundingBox = namedtuple("BoundingBox", ["x", "y", "width", "height"])

# To parse IIIF Urls
IIIF_URL = re.compile(r"\w+:\/{2}.+\/.+\/.+\/.+\/(?P<size>.+)\/!?\d+\/\w+\.\w+")
# Full size of the region
IIIF_FULL = "full"
# Maximum size available
IIIF_MAX = "max"
# Ratio to resize image
IMAGE_RATIO = [1, 0.9, 0.85, 0.80, 0.75, 0.70, 0.60, 0.50, 0.40, 0.30]


def update_pillow_image_size_limit(func):
    """
    Update Pillow Image size limit
    """

    @functools.wraps(func)
    def wrapper(
        *args,
        max_image_pixels: str | int | None = os.getenv("ARKINDEX_MAX_IMAGE_PIXELS"),
        **kwargs,
    ):
        """
        Wrapper to update Pillow Image size limit and restore it at the end of the function.

        :param *args: Positional arguments passed to the function.
        :param max_image_pixels: Pillow Image size limit to use.
        :param **kwargs: Keyword arguments passed to the function.
        """
        MAX_IMAGE_PIXELS = Image.MAX_IMAGE_PIXELS

        # Override Pillow Image size limit
        if max_image_pixels is not None:
            max_image_pixels = int(max_image_pixels)
            # Override Pillow limit for detecting decompression bombs, disabled if set to 0
            if max_image_pixels == 0:
                logger.warning(
                    "Pillow Image size limit is completely disabled, make sure you trust the image source."
                )
                Image.MAX_IMAGE_PIXELS = None
            else:
                Image.MAX_IMAGE_PIXELS = max_image_pixels

        try:
            results = func(*args, **kwargs)
        except:
            # Restore initial Pillow Image size limit
            Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS
            raise

        # Restore initial Pillow Image size limit
        Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS
        return results

    return wrapper


@update_pillow_image_size_limit
def open_image(
    path: str,
    mode: str | None = "RGB",
    rotation_angle: int | None = 0,
    mirrored: bool | None = False,
) -> Image:
    """
    Open an image from a path or a URL.

    Warns:
    Prefer [arkindex_worker.models.Element.open_image][] whenever possible.

    :param path: Path or URL to open the image from.
       This parameter will be interpreted as a URL when it has a `http` or `https` scheme
       and no file exist with this path locally.
    :param mode: Pillow mode for the image. See [the Pillow documentation](https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes).
    :param rotation_angle: Rotation angle to apply to the image, in degrees.
       If it is not a multiple of 90°, then the rotation can cause empty pixels of
       the mode's default color to be added for padding.
    :param mirrored: Whether or not to mirror the image horizontally.
    :returns: A Pillow image.
    """
    if (
        path.startswith("http://")
        or path.startswith("https://")
        or not Path(path).exists()
    ):
        image = download_image(path)
    else:
        try:
            image = Image.open(path)
        except (OSError, ValueError):
            image = download_image(path)

    if image.mode != mode:
        image = image.convert(mode)

    if mirrored:
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    if rotation_angle:
        image = image.rotate(-rotation_angle, expand=True)

    return image


def download_image(url: str) -> Image:
    """
    Download an image and open it with Pillow.

    :param url: URL of the image.
    :returns: A Pillow image.
    """
    assert url.startswith("http"), "Image URL must be HTTP(S)"

    # Download the image
    # Cannot use stream=True as urllib's responses do not support the seek(int) method,
    # which is explicitly required by Image.open on file-like objects
    try:
        resp = _retried_request(url)
    except requests.exceptions.HTTPError as e:
        if 400 <= e.response.status_code < 500 and (
            # Check if we are trying to download an image
            (parsed_url := IIIF_URL.match(url))
            # Check if we requested the full size of the image
            and parsed_url.group("size") == IIIF_FULL
        ):
            # Limit the size to maximum allowed
            resp = _retried_request(
                url[: parsed_url.start("size")]
                + IIIF_MAX
                + url[parsed_url.end("size") :]
            )
        else:
            raise e

    # Preprocess the image and prepare it for classification
    image = Image.open(BytesIO(resp.content))
    logger.info(
        f"Downloaded image {url} - size={image.size[0]}x{image.size[1]} in {resp.elapsed}"
    )

    return image


def upload_image(image: Image, url: str) -> requests.Response:
    """
    Upload a Pillow image to a URL.

    :param image: Pillow image to upload.
    :param url: Destination URL.
    :returns: The upload response.
    """
    assert url.startswith("http"), "Destination URL for the image must be HTTP(S)"

    # Retrieve a binarized version of the image
    image_bytes = BytesIO()
    image.save(image_bytes, format="jpeg")
    image_bytes.seek(0)

    # Upload the image
    resp = _retried_request(url, method=requests.put, data=image_bytes)
    logger.info(f"Uploaded image to {url} in {resp.elapsed}")

    return resp


def resized_images(
    *args,
    element: "Element",
    max_pixels: int | None = None,
    max_bytes: int | None = None,
    **kwargs,
) -> Iterator[Generator[tempfile.NamedTemporaryFile, None, None]]:
    """
    Build resized images according to the pixel and byte limits.

    :param *args: Positional arguments passed to [arkindex_worker.models.Element.open_image_tempfile][].
    :param element: Element whose image needs to be resized.
    :param max_pixels: Maximum pixel size of the resized images.
    :param max_bytes: Maximum byte size of the resized images.
    :param **kwargs: Keyword arguments passed to [arkindex_worker.models.Element.open_image_tempfile][].
    :returns: An iterator of the temporary file of the resized image.
    """
    _, _, element_width, element_height = polygon_bounding_box(element.polygon)

    logger.info(f"This element's image sizes are ({element_width} x {element_height}).")
    if max_pixels and max(element_width, element_height) > max_pixels:
        logger.warning(
            f"Maximum image input size supported is ({max_pixels} x {max_pixels})."
        )
        logger.warning("The image will be resized.")

    element_pixel, param = (
        (element_width, "max_width")
        if element_width > element_height
        else (element_height, "max_height")
    )

    for resized_pixel in sorted(
        set(
            min(round(ratio * element_pixel), max_pixels or element_pixel)
            for ratio in IMAGE_RATIO
        ),
        reverse=True,
    ):
        with element.open_image_tempfile(
            *args, **{**kwargs, param: resized_pixel}
        ) as image:
            pillow_image = Image.open(image)
            if (
                pillow_image.width != element_width
                or pillow_image.height != element_height
            ):
                logger.warning(
                    f"The image was resized to ({pillow_image.width} x {pillow_image.height})."
                )

            # The image is still too large
            image_size = Path(image.name).stat().st_size
            if max_bytes and image_size > max_bytes:
                logger.warning(f"The image size is {humanize.naturalsize(image_size)}.")
                logger.warning(
                    f"Maximum image input size supported is {humanize.naturalsize(max_bytes)}."
                )
                logger.warning("The image will be resized.")
                continue

            yield image


def polygon_bounding_box(polygon: list[list[int | float]]) -> BoundingBox:
    """
    Compute the rectangle bounding box of a polygon.

    :param polygon: Polygon to get the bounding box of.
    :returns: Bounding box of this polygon.
    """
    x_coords, y_coords = zip(*polygon, strict=True)
    x, y = min(x_coords), min(y_coords)
    width, height = max(x_coords) - x, max(y_coords) - y
    return BoundingBox(x, y, width, height)


def _retry_log(retry_state, *args, **kwargs):
    logger.warning(
        f"Request to {retry_state.args[0]} failed ({repr(retry_state.outcome.exception())}), "
        f'retrying in {retry_state.idle_for} {pluralize("second", retry_state.idle_for)}'
    )


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2),
    retry=retry_if_exception_type(requests.RequestException),
    before_sleep=_retry_log,
    reraise=True,
)
def _retried_request(url, *args, method=requests.get, **kwargs):
    resp = method(
        url, *args, timeout=DOWNLOAD_TIMEOUT, verify=should_verify_cert(url), **kwargs
    )
    resp.raise_for_status()
    return resp


def download_tiles(url: str) -> Image:
    """
    Reconstruct a full IIIF image on servers that cannot serve the full-sized image, using tiles.

    :param url: URL of the image.
    :returns: A Pillow image.
    """
    if not url.endswith("/"):
        url += "/"
    logger.debug("Downloading image information")
    info = _retried_request(url + "info.json").json()

    image_width, image_height = info.get("width"), info.get("height")
    assert image_width and image_height, "Missing image dimensions in info.json"
    assert info.get(
        "tiles"
    ), "Image cannot be retrieved at full size and tiles are not supported"

    # Take the biggest available tile size
    tile = sorted(info["tiles"], key=lambda tile: tile.get("width", 0), reverse=True)[0]
    tile_width = tile["width"]
    # Tile height is optional and defaults to the width
    tile_height = tile.get("height", tile_width)

    full_image = Image.new("RGB", (image_width, image_height))

    for tile_x in range(ceil(image_width / tile_width)):
        for tile_y in range(ceil(image_height / tile_height)):
            region_x = tile_x * tile_width
            region_y = tile_y * tile_height

            # Prevent trying to crop outside the bounds of an image
            region_width = min(tile_width, image_width - region_x)
            region_height = min(tile_height, image_height - region_y)

            logger.debug(f"Downloading tile {tile_x},{tile_y}")
            resp = _retried_request(
                f"{url}{region_x},{region_y},{region_width},{region_height}/full/0/default.jpg"
            )

            tile_img = Image.open(BytesIO(resp.content))

            # Some bad IIIF image server implementations may sometimes return tiles with a few pixels of difference
            # with the expected sizes, causing Pillow to raise ValueError('images do not match').
            actual_width, actual_height = tile_img.size
            if actual_width < region_width or actual_height < region_height:
                # Fail when tiles are too small
                raise ValueError(
                    f"Expected size {region_width}×{region_height} for tile {tile_x},{tile_y}, "
                    f"but got {actual_width}×{actual_height}"
                )

            if actual_width > region_width or actual_height > region_height:
                # Warn and crop when tiles are too large
                logger.warning(
                    f"Cropping tile {tile_x},{tile_y} from {actual_width}×{actual_height} "
                    f"to {region_width}×{region_height}"
                )
                tile_img = tile_img.crop((0, 0, region_width, region_height))

            full_image.paste(
                tile_img,
                box=(
                    region_x,
                    region_y,
                    region_x + region_width,
                    region_y + region_height,
                ),
            )

    return full_image


def trim_polygon(
    polygon: list[list[int]], image_width: int, image_height: int
) -> list[list[int]]:
    """
    Trim a polygon to an image's boundaries, with non-negative coordinates.

    :param polygon: A polygon to trim.
    :param image_width: Width of the image.
    :param image_height: Height of the image.
    :returns: A polygon trimmed to the image's bounds.
       Some points may appear as missing, as the trimming can deduplicate points.
       The first and last point are always equal, to reproduce the behavior
       of the Arkindex backend.
    :raises AssertionError: When argument types are invalid or when the trimmed polygon
       is entirely outside of the image's bounds.
    """

    assert isinstance(
        polygon, list | tuple
    ), "Input polygon must be a valid list or tuple of points."
    assert all(
        isinstance(point, list | tuple) for point in polygon
    ), "Polygon points must be tuples or lists."
    assert all(
        len(point) == 2 for point in polygon
    ), "Polygon points must be tuples or lists of 2 elements."
    assert all(
        isinstance(point[0], int) and isinstance(point[1], int) for point in polygon
    ), "Polygon point coordinates must be integers."
    assert any(
        point[0] <= image_width and point[1] <= image_height for point in polygon
    ), "This polygon is entirely outside the image's bounds."

    trimmed_polygon = [
        [
            min(image_width, max(0, x)),
            min(image_height, max(0, y)),
        ]
        for x, y in polygon
    ]

    updated_polygon = []
    for point in trimmed_polygon:
        if point not in updated_polygon:
            updated_polygon.append(point)

    # Add back the matching last point, if it was present in the original polygon
    if polygon[-1] == polygon[0]:
        updated_polygon.append(updated_polygon[0])

    return updated_polygon


def revert_orientation(
    element: "Element | CachedElement",
    polygon: list[list[int | float]],
    reverse: bool = False,
) -> list[list[int]]:
    """
    Update the coordinates of the polygon of a child element based on the orientation of
    its parent.

    This method should be called before sending any polygon to Arkindex, to undo the possible
    orientation applied by [arkindex_worker.models.Element.open_image][].

    In some cases, we want to apply the parent's orientation on the child's polygon instead. This is done
    by enabling `reverse=True`.

    :param element: Parent element.
    :param polygon: Polygon corresponding to the child element.
    :param reverse: Whether we should revert or apply the parent's orientation.
    :return: A polygon with updated coordinates.
    """
    from arkindex_worker.cache import CachedElement
    from arkindex_worker.models import Element

    assert element and isinstance(
        element, Element | CachedElement
    ), "element shouldn't be null and should be an Element or CachedElement"
    assert polygon and isinstance(
        polygon, list
    ), "polygon shouldn't be null and should be a list"
    assert isinstance(reverse, bool), "Reverse should be a bool"
    # Rotating with Pillow can cause it to move the image around, as the image cannot have negative coordinates
    # and must be a rectangle.  This means the origin point of any coordinates from an image is invalid, and the
    # center of the bounding box of the rotated image is different from the center of the element's bounding box.
    # To properly undo the mirroring and rotation implicitly applied by open_image, we first need to find the center
    # of the rotated bounding box.
    if isinstance(element, Element):
        assert (
            element.zone and element.zone.polygon
        ), "element should have a zone and a polygon"
        parent_ring = LinearRing(element.zone.polygon)
    elif isinstance(element, CachedElement):
        assert element.polygon, "cached element should have a polygon"
        parent_ring = LinearRing(element.polygon)

    rotated_ring = rotate(parent_ring, element.rotation_angle, origin="center")

    # This rotated ring might have negative coordinates, so we get the vector that Pillow applies to offset the
    # image to non-negative coordinates using the rotated bounding box.
    offset_x, offset_y, _, _ = rotated_ring.bounds

    # This uses the same calculation as what Shapely does for rotate/scale(origin='center').
    # We will use this below to rotate around the center of the parent bounding box and not of each child polygon.
    # https://github.com/Toblerity/Shapely/blob/462de3aa7a8bbd80408762a2d5aaf84b04476e4d/shapely/affinity.py#L98-L101
    minx, miny, maxx, maxy = parent_ring.bounds
    origin = ((maxx + minx) / 2.0, (maxy + miny) / 2.0)

    ring = LinearRing(polygon)

    if reverse:
        # Apply the parent's orientation on the child's polygon
        # Apply mirroring
        if element.mirrored:
            ring = scale(ring, xfact=-1, origin=origin)
        # Apply rotation
        if element.rotation_angle:
            ring = rotate(ring, element.rotation_angle, origin=origin)
        # At last translate coordinates offset
        ring = translate(ring, xoff=-offset_x, yoff=-offset_y)
    else:
        # First undo the negative coordinates offset, since this is the last step of the original transformation
        ring = translate(ring, xoff=offset_x, yoff=offset_y)
        # Revert any rotation
        if element.rotation_angle:
            ring = rotate(ring, -element.rotation_angle, origin=origin)
        # Revert any mirroring
        if element.mirrored:
            ring = scale(ring, xfact=-1, origin=origin)

    return [[int(x), int(y)] for x, y in ring.coords]
