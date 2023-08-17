from PIL import Image
from itertools import product


def valid_input(
    image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]
) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    return (
        image_size[0] % tile_size[0] == 0
        and image_size[1] % tile_size[1] == 0
        and len(set(ordering)) == len(ordering)
        and len(ordering)
        == (image_size[0] * image_size[1]) // (tile_size[0] * tile_size[1])
    )


def create_coordinates(image_size: tuple[int, int], tile_size: tuple[int, int]):
    return list(
        product(
            range(0, image_size[1], tile_size[0]), range(0, image_size[0], tile_size[1])
        )
    )


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

    im = Image.open(image_path)

    mode = None
    try:
        im.getchannel("A")
        mode = "RGBA"
    except ValueError:
        mode = "RGB"

    im_out = Image.new(mode, im.size, (0, 0, 0, 0))

    if not valid_input(im.size, tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")

    crop_coordinates = create_coordinates(im.size, tile_size)
    tiles = []

    for x, y in crop_coordinates:
        tiles.append(im.crop((y, x, y + tile_size[0], x + tile_size[1])))

    for i in range(len(ordering)):
        tile = tiles[ordering[i]]
        x, y = crop_coordinates[i]
        pos = (y, x, y + tile_size[0], x + tile_size[1])
        im_out.paste(tile, pos)

    im_out.save(out_path, "PNG")
