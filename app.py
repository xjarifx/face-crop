import streamlit as st
from PIL import Image
import io
import zipfile
import os
from typing import List, Tuple
from face_detector import FaceDetector, FaceCropper


st.set_page_config(
    page_title="Face Crop",
    page_icon="✂️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


COLORS = {
    'bg': '#0D0D0D',
    'surface': '#1A1A1A',
    'primary': '#FF6B35',
    'secondary': '#2ECC71',
    'text': '#FFFFFF',
    'text_secondary': '#A0A0A0',
    'border': '#333333'
}


st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');
    
    * {{
        font-family: 'Outfit', sans-serif !important;
    }}
    
    .stApp {{
        background: {COLORS['bg']};
    }}
    
    h1, h2, h3 {{
        color: {COLORS['text']} !important;
        font-weight: 700 !important;
    }}
    
    .stMarkdown, .stText {{
        color: {COLORS['text']} !important;
    }}
    
    .section-card {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
    }}
    
    .drop-zone {{
        border: 2px dashed {COLORS['border']};
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        transition: border-color 0.3s, background 0.3s;
        cursor: pointer;
    }}
    
    .drop-zone:hover {{
        border-color: {COLORS['primary']};
        background: rgba(255, 107, 53, 0.05);
    }}
    
    .stButton > button {{
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }}
    
    .stButton > button:first-child {{
        background: {COLORS['primary']};
        color: white;
        border: none;
    }}
    
    .stButton > button:first-child:hover {{
        background: #ff8555;
        transform: translateY(-1px);
    }}
    
    .preview-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
    }}
    
    .preview-item {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 12px;
    }}
    
    .preview-item img {{
        border-radius: 8px;
        width: 100%;
    }}
    
    .stAlert {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
    }}
    
    div[data-testid="stFileUploader"] {{
        background: {COLORS['surface']};
        border-radius: 12px;
        padding: 16px;
    }}
    
    div[data-testid="stFileUploader"] label {{
        display: block;
        margin-bottom: 8px;
    }}
    
    div[data-testid="stFileUploader"] button {{
        margin-top: 8px;
    }}
    
    .stNumberInput > div > div {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
    }}
    
    .stSlider > div > div {{
        color: {COLORS['primary']};
    }}
    
    .download-all {{
        background: {COLORS['secondary']};
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }}
    
    .download-all:hover {{
        background: #27ae60;
        transform: translateY(-1px);
    }}
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if 'processed_images' not in st.session_state:
        st.session_state.processed_images = []
    if 'original_names' not in st.session_state:
        st.session_state.original_names = []
    if 'face_info' not in st.session_state:
        st.session_state.face_info = []


def create_zip_download(all_images: List[Tuple[Image.Image, str]]) -> io.BytesIO:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for img, name in all_images:
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            zf.writestr(name, img_bytes.getvalue())
    buffer.seek(0)
    return buffer


def main():
    init_session_state()
    
    st.markdown("<h1 style='text-align: center;'>✂️ Face Crop</h1>", unsafe_allow_html=True)
    st.markdown(f"""
        <p style='text-align: center; color: {COLORS['text_secondary']};'>
            Upload images to detect and crop around faces with custom dimensions
        </p>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    
    st.markdown("### 📁 Import Images", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Drop images here or click to browse",
        type=['jpg', 'jpeg', 'png', 'webp'],
        accept_multiple_files=True,
        help="Supported formats: JPG, PNG, WebP"
    )
    
    st.markdown("### 📂 Or Drop a Folder", unsafe_allow_html=True)
    
    folder_input = st.text_input(
        "Enter folder path containing images",
        placeholder="/path/to/folder",
        key="folder_input_input"
    )
    
    if folder_input and os.path.isdir(folder_input):
        supported_ext = ['.jpg', '.jpeg', '.png', '.webp']
        folder_files = []
        for root, dirs, files in os.walk(folder_input):
            for f in files:
                if os.path.splitext(f.lower())[1] in supported_ext:
                    folder_files.append(os.path.join(root, f))
        if folder_files:
            st.markdown(f"✅ Found **{len(folder_files)}** images in folder")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        target_width = st.number_input("Output Width (px)", min_value=50, max_value=2000, value=500, step=10)
    with col2:
        target_height = st.number_input("Output Height (px)", min_value=50, max_value=2000, value=500, step=10)
    
    scale_factor = st.slider("Scale Factor", 0.5, 3.0, 1.0, 0.1)
    
    if scale_factor != 1.0:
        target_width = int(target_width * scale_factor)
        target_height = int(target_height * scale_factor)
    
    padding_options = {"None": 0.0, "Small (10%)": 0.1, "Medium (20%)": 0.2, "Large (30%)": 0.3}
    padding_choice = st.selectbox("Face Padding", list(padding_options.keys()), index=2)
    padding_percent = padding_options[padding_choice]
    
    st.markdown("### 🖼️ Image Enhancement")
    
    col_enh1, col_enh2 = st.columns(2)
    with col_enh1:
        enhance_quality = st.toggle("Enhance Image Quality", value=False, help="Apply sharpening and detail enhancement")
    with col_enh2:
        st.empty()
    
    min_confidence = st.slider("Detection Confidence", 0.3, 0.9, 0.5, 0.05)
    
    crop_all_faces = st.checkbox("Crop each face separately", value=False, help="If multiple faces detected, create separate crop for each")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        process_btn = st.button("🔍 Detect & Crop", use_container_width=True)
    with col_btn2:
        clear_btn = st.button("🗑️ Clear All", use_container_width=True)
    
    if clear_btn:
        st.session_state.processed_images = []
        st.session_state.original_names = []
        st.session_state.face_info = []
        st.rerun()
    
    supported_ext = ['.jpg', '.jpeg', '.png', '.webp']
    
    if process_btn and (uploaded_files or (folder_input and os.path.isdir(folder_input))):
        detector = FaceDetector()
        cropper = FaceCropper()
        
        all_results = []
        
        images_to_process = []
        
        if uploaded_files:
            for f in uploaded_files:
                images_to_process.append(('upload', f.name, f))
        
        if folder_input and os.path.isdir(folder_input):
            folder_files = [f for f in os.listdir(folder_input) 
                          if os.path.splitext(f.lower())[1] in supported_ext]
            for f in folder_files:
                images_to_process.append(('folder', f, os.path.join(folder_input, f)))
        
        with st.spinner("Processing images..."):
            progress_bar = st.progress(0)
            
            for idx, (source_type, name, path_or_file) in enumerate(images_to_process):
                if source_type == 'upload':
                    image = Image.open(path_or_file)
                else:
                    image = Image.open(path_or_file)
                original_name = os.path.splitext(name)[0]
                
                faces = detector.detect_faces(image, min_confidence)
                
                if not faces:
                    st.warning(f"⚠️ No face detected in {name}")
                    continue
                
                if crop_all_faces:
                    for face_idx, face in enumerate(faces):
                        cropped = cropper.crop_around_face(
                            image, face, target_width, target_height, padding_percent,
                            enhance=enhance_quality
                        )
                        save_name = f"{original_name}_face{face_idx + 1}.png"
                        all_results.append((cropped, save_name, {'face': face, 'source': name}))
                else:
                    combined = cropper.crop_combined(
                        image, faces, target_width, target_height, padding_percent,
                        enhance=enhance_quality
                    )
                    if combined:
                        save_name = f"{original_name}_crop.png"
                        all_results.append((combined, save_name, {'face': faces[0], 'source': name}))
                
                progress_bar.progress((idx + 1) / len(images_to_process))
        
        st.session_state.processed_images = [r[0] for r in all_results]
        st.session_state.original_names = [r[1] for r in all_results]
        st.session_state.face_info = [r[2] for r in all_results]
        
        progress_bar.empty()
        
        if all_results:
            st.success(f"✅ Successfully processed {len(all_results)} image(s)")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.processed_images:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("### 📸 Results")
        
        all_images_list = list(zip(
            st.session_state.processed_images,
            st.session_state.original_names
        ))
        
        if len(all_images_list) > 1:
            zip_buffer = create_zip_download(all_images_list)
            st.download_button(
                label="📦 Download All as ZIP",
                data=zip_buffer,
                file_name="face_crops.zip",
                mime="application/zip",
                use_container_width=True
            )
        
        st.markdown("<div class='preview-grid'>", unsafe_allow_html=True)
        
        for idx, (img, name) in enumerate(all_images_list):
            with st.container():
                st.image(img, use_container_width=True)
                info = st.session_state.face_info[idx]
                face = info['face']
                conf = face.get('confidence', 0)
                st.caption(f"{name} • {img.size[0]}×{img.height} • conf: {conf:.2f}")
                
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                buf.seek(0)
                
                st.download_button(
                    label="💾 Download",
                    data=buf.getvalue(),
                    file_name=name,
                    mime="image/png",
                    key=f"dl_{idx}"
                )
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"""
        <p style='text-align: center; color: {COLORS['text_secondary']}; font-size: 14px;'>
            Face Crop System • Powered by MTCNN
        </p>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()