import os
import io
import json
from PIL import Image
from datetime import datetime
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage

from .utils import change_video_quality, text_details_view, moving_images_overlay, crop_video, change_aspect_ratio, remove_audio, concatenate_video


BASE_URL = "http://192.168.18.233:9999"
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


# class VideoProcessingView(APIView):
#     def post(self, request, format=None):
#         video = request.FILES.get('video')
#         resolution = request.data.get('resolution')
#         text_details = request.data.get('text_details')
#         image_details = request.data.get('image_details')
#         clip_details = request.data.get('clip_details')
#         clip_details = json.loads(clip_details)
#         print(f"Clip Details: {clip_details}")

#         audio = request.data.get('audio')

#         aspect_ratio = request.data.get('aspect_ratio')

#         video_width = int(request.data.get('video_width'))
#         video_height = int(request.data.get('video_height'))

#         start_time = request.data.get('start_time')
#         end_time = request.data.get('end_time')

#         # print(f"--------------- Video Width: {video_width} - Video Height: {video_height} ---------------")
#         # print(f"--------------- Video Start Time: {start_time} - Video End Time: {end_time} ---------------")

#         if not video:
#             return Response({"error": "Video must be provided."}, status=status.HTTP_400_BAD_REQUEST)

#         text_details = json.loads(text_details) if text_details else []
#         image_details = json.loads(image_details) if image_details else []

#         print(f"Aspect Ratio: {aspect_ratio}")

#         image_names = extract_image_names(image_details)
#         images_to_save = retrieve_images_by_name(image_names, request.FILES)

#         os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

#         image_paths = []
#         for name, file in images_to_save.items():
#             file_path = os.path.join(IMAGE_SAVE_DIR, name)
#             save_image(file, file_path)
#             image_paths.append(file_path)

#         current_time = int(datetime.timestamp(datetime.now()))
#         video_name, video_extension = os.path.splitext(video.name)

#         input_file_name = f"{video_name}_{current_time}{video_extension}"
#         input_path = os.path.join(settings.MEDIA_ROOT, 'input', 'videos', input_file_name)

#         converted_file_name = f"{video_name}_converted_{current_time}{video_extension}"
#         converted_path = os.path.join(settings.MEDIA_ROOT, 'output', converted_file_name)

#         os.makedirs(os.path.dirname(input_path), exist_ok=True)
#         os.makedirs(os.path.dirname(converted_path), exist_ok=True)

#         with default_storage.open(input_path, 'wb+') as destination:
#             for chunk in video.chunks():
#                 destination.write(chunk)

#         # Apply image overlay if images are provided
#         if start_time and end_time:
#             cropped_video_path = crop_video(input_path, start_time, end_time)
#         else:
#             cropped_video_path = input_path

#         if image_paths:
#             watermarked_video = moving_images_overlay(BASE_DIR, cropped_video_path, image_details, image_paths, video_width, video_height)
#             print(f"********** Watermarked Video saved at: {watermarked_video} **********")
#         else:
#             watermarked_video = input_path

#         if text_details:
#             final_video = text_details_view(BASE_DIR, watermarked_video, text_details, video_width, video_height)
#             print(f"********** Text Overlayed Video saved at: {final_video} **********")
#         else:
#             final_video = watermarked_video

#         if clip_details:
#             output_path = f"{BASE_DIR}/media"
#             final_video = concatenate_video(final_video, clip_details, output_path)

#         if final_video is None:
#             return Response({"error": "Error processing the video."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         final_video_abs_path = final_video.split('\\')[-1]
#         processed_video_url = f"{BASE_URL}/media/moving_overlay/{final_video_abs_path}"

#         if audio:
#             muted_video = remove_audio(final_video, converted_path)
#             nuted_video_name = muted_video.split('\\')[-1]
#             processed_video_url = f"{BASE_URL}/media/output/{nuted_video_name}"

#         # Apply resolution change if resolution is provided
#         # if resolution:
#         #     try:
#         #         cropped_video_path = crop_video(final_video, start_time, end_time)
#         #         resolution = RESOLUTIONS.get(resolution)
#         #         if not resolution:
#         #             return Response({"error": "Unsupported resolution."}, status=status.HTTP_400_BAD_REQUEST)

#         #         quality_changed_video = change_video_quality(cropped_video_path, converted_path, resolution)
#         #         changed_video_name = quality_changed_video.split('\\')[-1]
#         #         processed_video_url = f"{BASE_URL}/media/output/{changed_video_name}"

#         #     except Exception as e:
#         #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         if resolution:
#             try:
#                 resolution_str = RESOLUTIONS.get(resolution)
#                 if not resolution_str:
#                     return Response({"error": "Unsupported resolution."}, status=status.HTTP_400_BAD_REQUEST)

#                 quality_changed_video = change_video_quality(final_video, converted_path, resolution_str)
#                 final_video_abs_path = os.path.basename(quality_changed_video)
#                 processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             final_video_abs_path = os.path.basename(final_video)
#             processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"

#         if aspect_ratio:
#             try:
#                 aspected_video = change_aspect_ratio(final_video, converted_path, aspect_ratio)
#                 final_video_abs_path = aspected_video.split('\\')[-1]
#                 processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # elif bitrate:
#         #     try:
#         #         bit_rate_changed_video = change_bitrate(final_video, converted_path, bitrate)
#         #         final_video_abs_path = bit_rate_changed_video.split('\\')[-1]
#         #         processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"
#         #     except Exception as e:
#         #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response({"processed_video": processed_video_url}, status=status.HTTP_200_OK)



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

        # if start_time and end_time:
        #     cropped_video_path = crop_video(input_path, start_time, end_time)
        # else:
        #     cropped_video_path = input_path

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

        if audio:
            muted_video = remove_audio(final_video, converted_path)
            muted_video_name = os.path.basename(muted_video)
            processed_video_url = f"{BASE_URL}/media/output/{muted_video_name}"

        # Apply resolution change if resolution is provided
        # if resolution:
        #     try:
        #         cropped_video_path = crop_video(final_video, start_time, end_time)
        #         resolution = RESOLUTIONS.get(resolution)
        #         if not resolution:
        #             return Response({"error": "Unsupported resolution."}, status=status.HTTP_400_BAD_REQUEST)

        #         quality_changed_video = change_video_quality(cropped_video_path, converted_path, resolution)
        #         changed_video_name = os.path.basename(quality_changed_video)
        #         processed_video_url = f"{BASE_URL}/media/output/{changed_video_name}"

        #     except Exception as e:
        #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # if resolution:
        #     try:
        #         resolution_str = RESOLUTIONS.get(resolution)
        #         if not resolution_str:
        #             return Response({"error": "Unsupported resolution."}, status=status.HTTP_400_BAD_REQUEST)

        #         quality_changed_video = change_video_quality(final_video, converted_path, resolution_str)
        #         final_video_abs_path = os.path.basename(quality_changed_video)
        #         processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"
        #     except Exception as e:
        #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # else:
        #     final_video_abs_path = os.path.basename(final_video)
        #     processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"

        if aspect_ratio:
            try:
                aspected_video = change_aspect_ratio(final_video, converted_path, aspect_ratio)
                final_video_abs_path = os.path.basename(aspected_video)
                processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # elif bitrate:
        #     try:
        #         bit_rate_changed_video = change_bitrate(final_video, converted_path, bitrate)
        #         final_video_abs_path = os.path.basename(bit_rate_changed_video)
        #         processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"
        #     except Exception as e:
        #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        final_video_abs_path = os.path.basename(final_video)
        processed_video_url = f"{BASE_URL}/media/output/{final_video_abs_path}"

        return Response({"processed_video": processed_video_url}, status=status.HTTP_200_OK)
