import os
import json

from PIL import Image
from datetime import datetime
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage

from .helpers import (
    extract_image_names,
    save_image,
    retrieve_images_by_name
)
from .utils import (
    change_video_quality,
    text_details_view,
    moving_images_overlay,
    crop_video,
    change_aspect_ratio,
    remove_audio,
    concatenate_video
)


BASE_URL = "https://nimarrenderingapi.forbmax.ai"
BASE_DIR = settings.BASE_DIR 
IMAGE_SAVE_DIR = os.path.join(BASE_DIR, 'media', 'input', 'images')

RESOLUTIONS = {
    'SD': '720x480',
    'HD': '1280x720',
    'FHD': '1920x1080',
    'QHD': '2560x1440',
    'UHD': '3840x2160',
    '8K': '7680x4320'
}

SOCIAL_MEDIA_PLATFORMS = [
    {
        "platform": "YouTube",
        "format": "MP4"
    },
    {
        "platform": "Facebook",
        "format": "MOV"
    },
    {
        "platform": "Instagram",
        "format": "MP4"
    }
]


class VideoProcessingView(APIView):
    def post(self, request, format=None):
        video = request.FILES.get('video')
        resolution = request.data.get('resolution')
        is_enhanced = request.data.get('is_enhanced')

        audio = request.data.get('audio')
        aspect_ratio = request.data.get('aspect_ratio')
        video_width = int(request.data.get('video_width'))
        video_height = int(request.data.get('video_height'))

        text_details = request.data.get('text_details')
        image_details = request.data.get('image_details')
        clip_details = request.data.get('clip_details')
        clip_details = json.loads(clip_details) if clip_details else []

        social_media_support = request.data.get('social_media_support')

        text_details = json.loads(text_details) if text_details else []
        image_details = json.loads(image_details) if image_details else []

        if not video:
            return Response({"error": "Video must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            image_names = extract_image_names(image_details)
            images_to_save = retrieve_images_by_name(image_names, request.FILES)

            os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

            image_paths = []
            for name, file in images_to_save.items():
                file_path = os.path.join(IMAGE_SAVE_DIR, name)
                save_image(file, file_path)
                image_paths.append(file_path)

            current_time = int(datetime.timestamp(datetime.now()))
            video_name, video_extension = os.path.splitext(video.name)

            input_file_name = f"{video_name}_{current_time}{video_extension}"
            input_path = os.path.join(settings.MEDIA_ROOT, 'input', 'videos', input_file_name)

            converted_file_name = f"{video_name}_converted_{current_time}{video_extension}"
            converted_path = os.path.join(settings.MEDIA_ROOT, 'output', converted_file_name)

            os.makedirs(os.path.dirname(input_path), exist_ok=True)
            os.makedirs(os.path.dirname(converted_path), exist_ok=True)

            with default_storage.open(input_path, 'wb+') as destination:
                for chunk in video.chunks():
                    destination.write(chunk)

            if image_paths:
                watermarked_video = moving_images_overlay(BASE_DIR, input_path, image_details, image_paths, video_width, video_height)
                print(f"**** Watermarked Video saved at: {watermarked_video} ****")
            else:
                watermarked_video = input_path

            if text_details:
                final_video = text_details_view(BASE_DIR, watermarked_video, text_details, video_width, video_height)
                print(f"**** Text Overlayed Video saved at: {final_video} ****")
            else:
                final_video = watermarked_video

            if clip_details:
                output_path = f"{BASE_DIR}/media/output"
                output_path = output_path.replace('\\', '/')
                final_video = concatenate_video(final_video, clip_details, output_path)

            if final_video is None:
                return Response({"error": "Error processing the video."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                if audio == "false":
                    print(f"Audio: {audio}")
                    print("--------------------------------")
                    muted_video = remove_audio(final_video, converted_path)
                    muted_video_name = os.path.basename(muted_video)
                    processed_video_url = f"{BASE_URL}/media/output/{muted_video_name}"
                else:
                    processed_video_url = f"{BASE_URL}/media/output/{os.path.basename(final_video)}"

                if aspect_ratio:
                    try:
                        aspected_video = change_aspect_ratio(final_video, converted_path, aspect_ratio)
                        final_video_abs_path = os.path.basename(aspected_video)
                        processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"
                    except Exception as e:
                        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    final_video_abs_path = os.path.basename(final_video)
                    processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"

            return Response({"processed_video": processed_video_url}, status=status.HTTP_200_OK)
