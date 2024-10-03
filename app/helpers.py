import os
import io

from PIL import Image


def extract_image_names(image_details):
    return [item['name'] for item in image_details]


def save_image(file, file_path):
    try:
        with file.open('rb') as f:
            image_stream = io.BytesIO(f.read())
            image = Image.open(image_stream)

            file_extension = os.path.splitext(file_path)[1].lower()
            if not file_extension:
                file_extension = '.png'
                file_path += file_extension

            image.save(file_path, format=file_extension.lstrip('.').upper())
    except Exception as e:
        raise ValueError(f"Error saving image: {e}")


def retrieve_images_by_name(image_names, request_files):
    image_map = {}
    for name in image_names:
        file = request_files.get(name)
        if file:
            if not name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                name += '.png'
            image_map[name] = file
    return image_map
