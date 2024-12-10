# HSL Six Color Image Processor

## Overview
`hslSixColor` is a Python package for image processing that applies HSL color adjustment and error diffusion dithering to images.

## Features
- Adjust image saturation using HSL color space
- Apply error diffusion dithering with a six-color palette
- Batch process images in a folder

## Installation
```bash
pip install hslSixColor
```

## Usage
```python
from hslSixColor import process_folder

# Process all images in a folder
process_folder('/path/to/input/folder', '/path/to/output/folder', saturation_factor=0.6)

# Or use the more flexible HSLSixColorProcessor class
from hslSixColor import HSLSixColorProcessor

processor = HSLSixColorProcessor()
processor.process_images('/path/to/input/folder', '/path/to/output/folder')
```

## Parameters
- `input_folder`: Path to the folder containing input images
- `output_folder`: Path to save processed images
- `saturation_factor`: Control the saturation adjustment (default: 0.8)

## Requirements
- Python 3.7+
- NumPy
- Pillow

## License
[Specify your license here]
