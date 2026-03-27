from __future__ import annotations

from PIL import Image, ImageOps


def preprocess_image(image: Image.Image) -> Image.Image:
    """Apply light preprocessing that preserves the invoice layout."""
    grayscale = ImageOps.grayscale(image)
    return ImageOps.autocontrast(grayscale)
