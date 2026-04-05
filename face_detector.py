import numpy as np
from PIL import Image
from typing import List, Tuple, Optional
import cv2


class ImageEnhancer:
    @staticmethod
    def upscale_image(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
        img = np.array(image.convert('RGB'))
        upscaled = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)
        return Image.fromarray(upscaled)

    @staticmethod
    def apply_unsharp_mask(image: Image.Image, radius: float = 1.5, amount: float = 0.8) -> Image.Image:
        img = np.array(image.convert('RGB'))
        blurred = cv2.GaussianBlur(img, (0, 0), radius)
        sharpened = float(1 + amount) * img - float(amount) * blurred
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        return Image.fromarray(sharpened)


class FaceDetector:
    def __init__(self):
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        self.haar_detector = cv2.CascadeClassifier(cascade_path)

    def detect_faces(self, image: Image.Image, min_confidence: float = 0.3) -> List[dict]:
        try:
            img_array = np.array(image.convert('RGB'))
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            results = self.haar_detector.detectMultiScale(gray, 1.1, 3)
            
            faces = []
            for result in results:
                x, y, w, h = result
                faces.append({
                    'box': (int(x), int(y), int(w), int(h)),
                    'confidence': 0.9,
                    'keypoints': {}
                })
            return faces
        except Exception as e:
            print(f"Face detection error: {e}")
            return []


class FaceCropper:
    def __init__(self):
        self.enhancer = ImageEnhancer()

    def crop_around_face(self, image: Image.Image, face: dict, target_width: int, target_height: int, padding_percent: float = 0.2, enhance: bool = True) -> Image.Image:
        img_width, img_height = image.size
        x, y, w, h = face['box']
        
        center_x = x + w // 2
        center_y = y + h // 2
        face_size = max(w, h)
        crop_size = int(face_size * (1 + padding_percent))
        
        half_crop = crop_size // 2
        crop_left = max(0, center_x - half_crop)
        crop_top = max(0, center_y - half_crop)
        crop_right = min(img_width, crop_left + crop_size)
        crop_bottom = min(img_height, crop_top + crop_size)
        
        cropped = image.crop((crop_left, crop_top, crop_right, crop_bottom))
        
        if enhance:
            cropped = self.enhancer.upscale_image(cropped, target_width, target_height)
            cropped = self.enhancer.apply_unsharp_mask(cropped)
        else:
            cropped = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        return cropped

    def crop_combined(self, image: Image.Image, faces: List[dict], target_width: int, target_height: int, padding_percent: float = 0.2, enhance: bool = True) -> Optional[Image.Image]:
        if not faces:
            return None
        
        min_x = min(f['box'][0] for f in faces)
        min_y = min(f['box'][1] for f in faces)
        max_x = max(f['box'][0] + f['box'][2] for f in faces)
        max_y = max(f['box'][1] + f['box'][3] for f in faces)
        
        center_x = (min_x + max_x) // 2
        center_y = (min_y + max_y) // 2
        face_size = max(max_x - min_x, max_y - min_y)
        crop_size = int(face_size * (1 + padding_percent))
        
        img_width, img_height = image.size
        half_crop = crop_size // 2
        crop_left = max(0, center_x - half_crop)
        crop_top = max(0, center_y - half_crop)
        crop_right = min(img_width, crop_left + crop_size)
        crop_bottom = min(img_height, crop_top + crop_size)
        
        cropped = image.crop((crop_left, crop_top, crop_right, crop_bottom))
        
        if enhance:
            cropped = self.enhancer.upscale_image(cropped, target_width, target_height)
            cropped = self.enhancer.apply_unsharp_mask(cropped)
        else:
            cropped = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        return cropped