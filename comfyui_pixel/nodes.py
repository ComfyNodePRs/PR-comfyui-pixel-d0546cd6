from comfy_annotations import ComfyFunc, ImageTensor, NumberInput, Choice
from comfyui_pixel.scale_utils import oe_downscale, downscale
from comfyui_pixel.quantization_utils import palette_reduction, palette_swap
from comfyui_pixel.tensor_utils import tensor2pil, pil2tensor


@ComfyFunc(
    category="Pixel Image Processing",
    display_name="Pixel Image Downscale By",
    is_output_node=True,
    debug=True,
)
def scale_by(
    image: ImageTensor,
    downscale_factor: int = NumberInput(0, 0, 4096, 64, "number"),
    scale_method: str = Choice(["k-centroid", "nearest-neighbors"]),
    outline_expansion: bool = False,
) -> ImageTensor:
    """Rescale an image by dividing it's current size by the downscale factor."""

    image = tensor2pil(image)
    new_image: ImageTensor
    match outline_expansion:
        case True:
            new_image = oe_downscale(image, downscale_factor, scale_method)
        case False:
            new_image = downscale(image, downscale_factor, scale_method)

    return pil2tensor(new_image)


@ComfyFunc(
    category="Pixel Image Processing",
    display_name="Pixel Image Reduce Palette",
    is_output_node=True,
    debug=True,
)
def palette_reduce_node(
    image: ImageTensor,
    palette_size: int = NumberInput(0, 0, 256, 1, "number"),
    method: str = Choice(
        [
            "Quantize.MEDIANCUT",
            "Quantize.MAXCOVERAGE",
            "Quantize.FASTOCTREE",
            "Elbow Method",
        ]
    ),
) -> ImageTensor:
    """Reduce the palette of an image to the specified size."""

    image = tensor2pil(image)
    new_image = palette_reduction(image, palette_size, method)
    return pil2tensor(new_image)


@ComfyFunc(
    category="Pixel Image Processing",
    display_name="Pixel Image Palette Swap",
    validate_inputs=lambda image, palette_image: image and palette_image is not None,
    is_output_node=True,
    debug=True,
)
def palette_swap_node(
    image: ImageTensor,
    palette_image: ImageTensor,
    method: str = Choice(
        [
            "Quantize.MEDIANCUT",
            "Quantize.MAXCOVERAGE",
            "Quantize.FASTOCTREE",
            "KMeans Elbow Method",
        ]
    ),
) -> ImageTensor:
    """Reduce and optionally swap the palette of an image to the specified size."""

    image = tensor2pil(image)
    new_image = palette_swap(image, tensor2pil(palette_image))
    return pil2tensor(new_image)
