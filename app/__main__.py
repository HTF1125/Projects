"""ROBERT"""
import os
import sys

# add current package to the path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(__file__), "../..")))

from app.web import app

app.run()
