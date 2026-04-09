# Face Crop ✂️

> Quick start:
> ```bash
> python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && streamlit run app.py
> ```

A web application for detecting and cropping human faces from images with customizable dimensions and quality enhancement.

## Features

- **Multi-Image Upload** - Upload multiple images at once (JPG, PNG, WebP)
- **Face Detection** - Automatic face detection using Haar Cascade classifier
- **Custom Dimensions** - Set custom output width and height
- **Scale Factor** - Proportionally scale output images (0.5x to 3x)
- **Face Padding** - Add padding around detected faces (None, Small, Medium, Large)
- **Image Enhancement** - Optional sharpening and detail enhancement to reduce blurriness
- **Batch Processing** - Process multiple images in one go
- **Download Options** - Download individual crops or all as ZIP archive

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Run the application:
   ```bash
   streamlit run app.py
   ```
3. Open your browser to `http://localhost:8501`

## How It Works

1. **Upload Images** - Drag and drop or browse for images
2. **Configure Settings**:
   - Set output width and height in pixels
   - Adjust scale factor if needed
   - Choose face padding amount
   - Enable image enhancement for sharper results
3. **Detect & Crop** - Click the button to process images
4. **Download** - Preview results and download individually or as ZIP

## Project Structure

```
face-crop/
├── app.py              # Main Streamlit application
├── face_detector.py    # Face detection and cropping module
├── requirements.txt    # Python dependencies
├── SPEC.md            # Specification document
├── README.md          # This file
└── venv/              # Virtual environment (not in git)
```

## Dependencies

- streamlit >= 1.28.0
- Pillow >= 10.0.0
- numpy >= 1.24.0
- opencv-python-headless >= 4.8.0
- werkzeug >= 3.0.0

## Image Enhancement

The application includes image enhancement features to combat blurriness when upscaling:

- **LANCZOS4 Interpolation** - High-quality upscaling algorithm
- **Unsharp Mask** - Edge enhancement for sharper details
- Applied automatically when "Enhance Image Quality" is enabled

## Notes

- Face detection works best with clear, well-lit photos showing frontal faces
- The Haar Cascade detector may not detect faces in cartoons, drawings, or heavily filtered images
- For best results, use photos with good lighting and visible facial features
- Image enhancement improves quality but may increase processing time

## License

MIT