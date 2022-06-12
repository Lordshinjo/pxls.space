import sys
from typing import NamedTuple
from urllib.parse import quote, urlencode

import numpy as np
import PIL.Image
import requests


class Color(NamedTuple):
    r: int
    g: int
    b: int
    name: str

    @property
    def rgba(self):
        return self.r, self.g, self.b, 255


COLORS = [
    Color(0, 0, 0, "Black"),
    Color(34, 34, 34, "Dark Grey"),
    Color(85, 85, 85, "Deep Grey"),
    Color(136, 136, 136, "Medium Grey"),
    Color(205, 205, 205, "Light Grey"),
    Color(255, 255, 255, "White"),
    Color(255, 213, 188, "Beige"),
    Color(255, 183, 131, "Peach"),
    Color(182, 109, 61, "Brown"),
    Color(119, 67, 31, "Chocolate"),
    Color(252, 117, 16, "Rust"),
    Color(252, 168, 14, "Orange"),
    Color(253, 232, 23, "Yellow"),
    Color(255, 244, 145, "Pastel Yellow"),
    Color(190, 255, 64, "Lime"),
    Color(112, 221, 19, "Green"),
    Color(49, 161, 23, "Dark Green"),
    Color(11, 95, 53, "Forest"),
    Color(39, 126, 108, "Dark Teal"),
    Color(50, 182, 159, "Light Teal"),
    Color(136, 255, 243, "Aqua"),
    Color(36, 181, 254, "Azure"),
    Color(18, 92, 199, "Blue"),
    Color(38, 41, 96, "Navy"),
    Color(139, 47, 168, "Purple"),
    Color(210, 76, 233, "Mauve"),
    Color(255, 89, 239, "Magenta"),
    Color(255, 169, 217, "Pink"),
    Color(255, 100, 116, "Watermelon"),
    Color(240, 37, 35, "Red"),
    Color(177, 18, 6, "Rose"),
    Color(116, 12, 0, "Maroon"),
]


def generate(template_branch: str) -> None:
    with requests.get(
        f"https://github.com/iratekalypso/pxls.space/raw/{template_branch}/VGV_numbers.png",
        stream=True,
    ) as resp:
        image = PIL.Image.open(resp.raw)
        pixels = np.array(image.convert("RGBA"))

    transparent_pixel = np.array([0, 0, 0, 0])
    for i, color in enumerate(COLORS):
        filtered_pixels = pixels.copy()
        color_rgba = np.array(color.rgba)
        filtered_pixels[~(filtered_pixels == color_rgba).all(axis=-1)] = transparent_pixel
        filtered_image = PIL.Image.fromarray(filtered_pixels, mode="RGBA")
        filtered_image.save(file_name(i))
        print("Generated", i)

    with open("README.md", "w") as f:
        print("Here are the template urls:", file=f)
        for i, color in enumerate(COLORS):
            params = {
                "x": "879",
                "y": "487",
                "scale": "2",
                "template": f"https://github.com/Lordshinjo/pxls.space/raw/main/{file_name(i)}",
                "ox": "629",
                "oy": "312",
                "tw": "500",
                "title": f"VGV (only {color.name} - {i})",
                "convert": "unconverted",
            }
            full_url = f"https://pxls.space/#{urlencode(params, quote_via=quote)}"
            print(
                f"- [{i:02d} - {color.name}]({full_url})",
                file=f,
            )


def file_name(index: int) -> str:
    return f"VGV_color_{index:02d}.png"


if __name__ == "__main__":
    template_branch = "main"
    if len(sys.argv) > 1:
        template_branch = sys.argv[1]
    generate(template_branch)
