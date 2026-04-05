# Face Crop System - Specification

## 1. Project Overview

**Project Name:** Face Crop  
**Type:** Web Application (Streamlit)  
**Core Functionality:** Detect human faces in images and crop them with user-defined dimensions, supporting upscale/downscale and batch processing.  
**Target Users:** Anyone needing face-centric image crops (portraits, profile photos, ID images, etc.)

---

## 2. UI/UX Specification

### Layout Structure

- **Single Page Application** with vertical flow
- **Header:** App title and brief description
- **Input Section:** File upload area (multiple images supported)
- **Settings Section:** Crop dimensions and scaling options
- **Output Section:** Preview and download cropped images

### Responsive Design

- Mobile-friendly (Stack layout)
- Minimum width: 320px
- Max content width: 900px centered

### Visual Design

**Color Palette:**
- Background: `#0D0D0D` (near black)
- Surface: `#1A1A1A` (dark gray)
- Primary: `#FF6B35` (vibrant orange)
- Secondary: `#2ECC71` (emerald green)
- Text Primary: `#FFFFFF`
- Text Secondary: `#A0A0A0`
- Border: `#333333`

**Typography:**
- Font Family: `"Outfit", sans-serif`
- Heading (H1): 32px, weight 700
- Heading (H2): 24px, weight 600
- Body: 16px, weight 400
- Small: 14px, weight 400

**Spacing:**
- Section gap: 32px
- Element gap: 16px
- Padding: 24px

**Visual Effects:**
- Cards: subtle border `1px solid #333`, border-radius 12px
- Buttons: border-radius 8px, smooth hover transitions
- File drop zone: dashed border, hover highlight

### Components

1. **File Uploader**
   - Drag & drop zone + click to browse
   - Accept: jpg, jpeg, png, webp
   - Multiple files allowed
   - Show thumbnail preview after upload

2. **Dimension Controls**
   - Width input (px): number input, default 400
   - Height input (px): number input, default 500
   - Scale factor slider: 0.5x to 3x, default 1x

3. **Processing Options**
   - Face padding dropdown: None, Small (10%), Medium (20%), Large (30%)
   - Detection confidence threshold: slider 0.3-0.9, default 0.5

4. **Action Buttons**
   - "Detect & Crop" - primary button
   - "Clear All" - secondary button

5. **Output Gallery**
   - Grid of cropped images (2 columns)
   - Each shows: thumbnail, dimensions, face count
   - "Download All as ZIP" button
   - Individual download buttons

---

## 3. Functionality Specification

### Core Features

1. **Multi-Image Upload**
   - Accept 1-20 images per session
   - Show upload progress
   - Validate image format

2. **Face Detection**
   - Use MTCNN (PyTorch) for accurate face detection
   - Use Haar Cascade as fallback
   - Detect all faces in each image
   - Return bounding boxes with confidence scores

3. **Smart Cropping**
   - Crop around detected face(s)
   - Apply padding percentage around face
   - Maintain face center position
   - Support multiple faces (crop each separately or combined)

4. **Dimension Control**
   - User-defined output width/height
   - Scale factor for proportional resize
   - Option to fit within bounds (maintain aspect ratio)

5. **Batch Download**
   - Download individual cropped images
   - Download all as ZIP archive
   - Preserve original filenames with suffix

### User Interactions

1. User uploads one or more images
2. User sets desired crop dimensions (width x height)
3. User adjusts scale factor if needed
4. User clicks "Detect & Crop"
5. System processes all images, shows previews
6. User reviews and downloads desired results

### Edge Cases

- No face detected: Show warning, offer full image crop option
- Multiple faces: Crop each face as separate image
- Very small images: Warn about upscale quality loss
- Corrupted files: Skip with error message

---

## 4. Acceptance Criteria

1. ✅ Can upload multiple images (jpg, png, webp)
2. ✅ Face detection runs automatically on upload
3. ✅ Crop dimensions can be customized (width/height)
4. ✅ Scale factor adjusts output size proportionally
5. ✅ Preview shows cropped result before download
6. ✅ Single image download works
7. ✅ Batch ZIP download works
8. ✅ Handles no-face images gracefully
9. ✅ Handles multiple faces in one image
10. ✅ UI looks polished with dark theme

---

## 5. Technical Stack

- **Framework:** Streamlit
- **Face Detection:** mtcnn (MTCNN)
- **Image Processing:** Pillow (PIL)
- **ZIP Creation:** Python zipfile
- **Deployment:** Local Streamlit server