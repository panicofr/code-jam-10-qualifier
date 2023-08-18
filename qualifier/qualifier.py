from PIL import Image


def valid_input(
    image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]
) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    image_width, image_height = image_size
    tile_width, tile_height = tile_size

    return all(
        [
            image_width % tile_width == 0,
            image_height % tile_height == 0,
            (image_width / tile_width) * (image_height / tile_height) == len(ordering),
            len(ordering) == len(set(ordering)),
        ]
    )


def extract_tile(
    im: Image.Image, tile_size: tuple[int, int], tile_index: int, tiles_by_row: int
) -> Image.Image:
    row_index = int(tile_index / tiles_by_row)
    col_index = tile_index % tiles_by_row
    left = col_index * tile_size[0]
    top = row_index * tile_size[1]
    right = left + tile_size[0]
    bottom = top + tile_size[1]
    return im.crop((left, top, right, bottom))


def recompose_image(
    src_image: Image.Image, tiles: list[Image.Image], tiles_by_row: int
) -> Image.Image:
    image = Image.new(src_image.mode, src_image.size)
    for tile_index, tile in enumerate(tiles):
        row_index = int(tile_index / tiles_by_row)
        col_index = tile_index % tiles_by_row
        tile_width, tile_height = tile.size
        image.paste(tile, (col_index * tile_width, row_index * tile_height))
    return image


def rearrange_tiles(
    image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str
) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """

    tile_width = tile_size[0]

    with Image.open(image_path) as image:
        image_size = image.size
        image_width, image_height = image_size

        if not valid_input(image_size, tile_size, ordering):
            raise ValueError(
                "The tile size or ordering are not valid for the given image"
            )

        x_tiles_count = int(image_width / tile_width)

        tiles = [
            extract_tile(image, tile_size, tile_index, x_tiles_count)
            for tile_index in ordering
        ]
        output_image = recompose_image(image, tiles, x_tiles_count)
        output_image.save(out_path)
