"""ROBERT"""

import os
from typing import List
from PIL import Image


def all_filenames() -> List[str]:
    directory = os.path.dirname(__file__)
    # Get all filenames in the directory
    filenames = os.listdir(directory)
    return [
        os.path.join(directory, filename)
        for filename in filenames
        if not filename.startswith("__")
    ]


def get_profile():
    return Image.open(os.path.join(os.path.dirname(__file__), "assets", "profile.jpeg"))

def get_resume():
    file =os.path.join(os.path.dirname(__file__), "assets", "CV.pdf")
    with open(file, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        return PDFbyte