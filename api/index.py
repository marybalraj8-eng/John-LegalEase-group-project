import sys
import os

# Project root-ஐ python import path-ல் சேர்க்கிறது
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from legalEaseAPI.main import app

# Vercel இந்த app object-ஐ தானாகவே Handler-ஆக எடுத்துக்கொள்ளும்