import os
import json
import time
import subprocess

from PIL import Image
from datetime import datetime
from django.conf import settings


RESOLUTION_SETTINGS = {
    '720x480': {
        'video_bitrate': '1000k',
        'audio_bitrate': '128k',
        'codec': 'libx264',
        'crf': '23',
        'preset': 'medium'
    },
    '1280x720': {
        'video_bitrate': '2500k',
        'audio_bitrate': '192k',
        'codec': 'libx264',
        'crf': '21',
        'preset': 'slow'
    },
    '1920x1080': {
        'video_bitrate': '5000k',
        'audio_bitrate': '256k',
        'codec': 'libx264',
        'crf': '19',
        'preset': 'slow'
    },
    '2560x1440': {
        'video_bitrate': '8000k',
        'audio_bitrate': '320k',
        'codec': 'libx264',
        'crf': '18',
        'preset': 'slow'
    },
    '3840x2160': {
        'video_bitrate': '12000k',
        'audio_bitrate': '320k',
        'codec': 'libx264',
        'crf': '17',
        'preset': 'slow'
    },
    '7680x4320': {
        'video_bitrate': '20000k',
        'audio_bitrate': '320k',
        'codec': 'libx264',
        'crf': '16',
        'preset': 'slow'
    }
}


def calculate_pixel_position(total_size, percent):
    try:
        percent = float(percent)
    except ValueError:
        raise ValueError(f"Invalid percentage value: {percent}")
    return float(total_size * percent / 100)


def moving_images_overlay(BASE_DIR, video, image_details, image_paths, video_width, video_height):
    current_time = datetime.now().strftime('%H%M%S')
    output_dir = os.path.join(BASE_DIR, 'media', 'moving_overlay')
    os.makedirs(output_dir, exist_ok=True)

    temp_file = video

    for index, details in enumerate(image_details):
        if index >= len(image_paths):
            print(f"No image available for index {index}. Skipping...")
            continue

        local_image = image_paths[index]
        image_x_percent = float(details['image_x'])
        image_y_percent = float(details['image_y'])
        image_w_percent = float(details['image_w'])
        image_h_percent = float(details['image_h'])
        start_time = details.get('start_time', 0)
        end_time = details.get('end_time', 'end')

        # image_x = calculate_pixel_position(video_width, image_x_percent)
        # image_y = calculate_pixel_position(video_height, image_y_percent)
        # image_w = calculate_pixel_position(video_width, image_w_percent)
        # image_h = calculate_pixel_position(video_height, image_h_percent)

        image_x = int(video_width * image_x_percent / 100)
        image_y = int(video_height * image_y_percent / 100)
        image_w = int(video_width * image_w_percent / 100)
        image_h = int(video_height * image_h_percent / 100)

        output_file = os.path.join(output_dir, f"video_watermarked_{current_time}_{index}.mp4")

        if os.path.exists(output_file):
            os.remove(output_file)
        
        opacity = details.get('opacity', 1.0)

        if opacity is not None:
            print(f"Opacity: {opacity}")
            opacity = max(0.0, min(1.0, opacity))

            watermark_command = (
                f'ffmpeg -i "{temp_file}" -i "{local_image}" -filter_complex '
                f'"[1:v]scale={image_w}:{image_h},format=rgba,colorchannelmixer=aa={opacity}[watermark];'
                f'[0:v][watermark]overlay={image_x}:{image_y}:enable=\'between(t,{start_time},{end_time})\'" '
                f'-c:v libx264 -c:a copy "{output_file}"'
            )
        else:
            watermark_command = (
                f'ffmpeg -i "{temp_file}" -i "{local_image}" -filter_complex '
                f'"[1:v]scale={image_w}:{image_h}[watermark];'
                f'[0:v][watermark]overlay={image_x}:{image_y}:enable=\'between(t,{start_time},{end_time})\'" '
                f'-c:v libx264 -c:a copy "{output_file}"'
            )

        try:
            subprocess.run(watermark_command, capture_output=True, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running ffmpeg command: {e}")
            return None

        temp_file = output_file

    return temp_file


def text_details_view(BASE_DIR, input_file, text_details, video_width, video_height):
    video_file = os.path.basename(input_file)
    file_name, file_extension = os.path.splitext(video_file)
    current_time = datetime.now().strftime('%H%M%S')

    output_dir = os.path.join(BASE_DIR, 'media', 'moving_overlay')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    temp_file = input_file

    for index, detail in enumerate(text_details):
        text = detail['text']
        text_color = detail['text_color']
        text_size = float(video_height * (float(detail['text_size']) / 100))
        text_x = calculate_pixel_position(video_width, float(detail['text_x']))
        text_y = calculate_pixel_position(video_height, float(detail['text_y']))
        start_time = detail['start_time']
        end_time = detail['end_time']

        BASE_DIR = str(BASE_DIR).replace('\\', '/')

        font_family_map = {
            "Arial": f"{BASE_DIR}/fonts/arial.ttf",
            "Times New Roman": f"{BASE_DIR}/fonts/times-new-roman.ttf",
            # "Helvetica": f"{BASE_DIR}/fonts/helvetica.ttf",
            # "Roboto": f"{BASE_DIR}/fonts/roboto.ttf",
            # "Sans Serif": f"{BASE_DIR}/fonts/sans-serif.otf",
            "Verdana": f"{BASE_DIR}/fonts/verdana.ttf",
            "Brush Script MT": f"{BASE_DIR}/fonts/brush-script.ttf",
            "Tahoma": f"{BASE_DIR}/fonts/tahoma.ttf",
            "Trebuchet MS": f"{BASE_DIR}/fonts/trebuc.ttf",
            "Courier New": f"{BASE_DIR}/fonts/cour.ttf",
            "Georgia": f"{BASE_DIR}/fonts/georgia.ttf",
            "Garamond": f"{BASE_DIR}/fonts/garamond.ttf",

        }
        font_family = font_family_map.get(detail['font_family'], font_family_map["Arial"])

        output_file = os.path.join(output_dir, f"{file_name}_{current_time}_{index}{file_extension}")

        # print("\n\n****************************************************************")
        # print(f"Font Family: {font_family}")
        # print("****************************************************************\n\n")

        text_command = (
            f'ffmpeg -i "{temp_file}" -vf "drawtext=text=\'{text}\':fontfile={font_family}:'
            f'fontcolor={text_color}:fontsize={text_size}:x={text_x}:y={text_y}:'
            f'enable=\'between(t,{start_time},{end_time})\'" '
            f'-codec:a copy "{output_file}"'
        )

        try:
            subprocess.run(text_command, capture_output=True, shell=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running ffmpeg command: {e.stderr}")
            return None

        temp_file = output_file

    return temp_file


def crop_video(input_path, start_time, end_time):
    input_path = input_path.replace('\\', '/')
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_cropped{ext}"

    print(f"----------------------: {start_time} and {end_time} :----------------------")

    command = [
        'ffmpeg',
        '-i', input_path,
        '-ss', str(start_time),
        '-to', str(end_time),
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-b:v', '1000k',
        '-b:a', '128k',
        output_path
    ]

    try:
        subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise

    return output_path


def change_video_quality(input_file, output_file, resolution):
    settings = RESOLUTION_SETTINGS.get(resolution)
    
    if settings is None:
        raise ValueError(f"Unsupported resolution: {resolution}")

    scale_filter = f"scale={resolution}"
    
    command = [
        'ffmpeg',
        '-y',
        '-i', input_file,
        '-vf', scale_filter,
        '-c:v', settings['codec'],
        '-preset', settings['preset'],
        '-crf', settings['crf'],
        '-b:v', settings['video_bitrate'],
        '-c:a', 'aac',
        '-b:a', settings['audio_bitrate'],
        '-r', '30',
        output_file
    ]

    try:
        subprocess.run(command, capture_output=True, shell=True, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        raise Exception(f"An error occurred: {e}")


def change_aspect_ratio(input_video_path, output_video_path, aspect_ratio):
    width, height = map(float, aspect_ratio.split(':'))
    scale_filter = f'scale=iw:2*trunc(iw*{height/width}/2)'  # Ensure height is divisible by 2
    
    command = [
        'ffmpeg',
        '-i', input_video_path,
        '-vf', scale_filter,
        '-c:a', 'copy',
        output_video_path
    ]

    try:
        subprocess.run(command, capture_output=True, check=True, text=True)
        print(f"---------------------: {command} :---------------------")
    except subprocess.CalledProcessError as e:
        print(f"Error changing aspect ratio: {e}")
        print(f"ffmpeg output: {e.stderr}")
        return None

    return output_video_path


def concatenate_video(input_video_file, clip_details, output_dir):
    input_file_name = input_video_file.replace('\\', '/').split('/')[-1]

    if not clip_details:
        raise ValueError("clip_details must contain at least one item.")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    segment_files = []
    
    for i, clip in enumerate(clip_details):
        start = clip['start_time']
        end = clip['end_time']

        segment_file = os.path.join(output_dir, f"segment_{i+1}.mp4")
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", input_video_file, "-ss", start, "-to", end, 
            "-c", "copy", segment_file
        ]
        try:
            subprocess.run(ffmpeg_cmd, capture_output=True, check=True)
            segment_files.append(segment_file)
            print(f"Created segment: {segment_file}")
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg command failed: {e}")
            return None

    list_file = os.path.join(output_dir, "segments_list.txt")
    try:
        with open(list_file, "w") as f:
            for segment_file in segment_files:
                f.write(f"file '{segment_file}'\n")
        print(f"Generated list file: {list_file}")
    except IOError as e:
        print(f"Failed to write list file: {e}")
        return None
    
    output_file = os.path.join(output_dir, f"final_{input_file_name}")
    ffmpeg_concat_cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file, 
        "-c", "copy", output_file
    ]
    try:
        subprocess.run(ffmpeg_concat_cmd, check=True)
        print(f"Created final output: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg concat command failed: {e}")
        return None
    
    time.sleep(1)

    for file_to_remove in segment_files + [list_file]:
        try:
            os.remove(file_to_remove)
            print(f"Deleted file: {file_to_remove}\n")
        except PermissionError:
            print(f"PermissionError: Unable to delete {file_to_remove}. It may still be in use.")
        except Exception as e:
            print(f"Error deleting {file_to_remove}: {e}")

    return output_file


def get_aspect_ratio(video_path):
    command = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,display_aspect_ratio',
        '-of', 'json',
        video_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    video_info = json.loads(result.stdout)
    width = video_info['streams'][0]['width']
    height = video_info['streams'][0]['height']
    aspect_ratio = video_info['streams'][0].get('display_aspect_ratio', f'{width}:{height}')
    return aspect_ratio


# video_path = 'C:/zulkifal/NIMAR-Extras/api/media/output/jutt_juliet_song_converted_1725518810.mp4'
# aspect_ratio = get_aspect_ratio(video_path)
# print(f'Aspect ratio: {aspect_ratio}')





"""

def change_video_bitrate(input_path, output_path, target_bitrate):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-b:v', f'{target_bitrate}k',
        '-vf', f'scale=iw:ih',
        '-c:a', 'copy',
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Bitrate changed successfully. Output saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")

input_video = "C:/zulkifal/NIMAR-Extras/api/media/input_video.mp4"
output_video = "C:/zulkifal/NIMAR-Extras/api/media/output.mp4"
target_bitrate = 1000

change_video_bitrate(input_video, output_video, target_bitrate)


def get_video_properties(video_path):
    command = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration,bit_rate',
        '-show_entries', 'stream=codec_name,width,height,avg_frame_rate',
        '-of', 'json',
        video_path
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)

        format_info = video_info.get('format', {})
        duration = format_info.get('duration', 'Unknown')
        bit_rate = format_info.get('bit_rate', 'Unknown')

        stream_info = video_info.get('streams', [{}])[0]
        codec_name = stream_info.get('codec_name', 'Unknown')
        width = stream_info.get('width', 'Unknown')
        height = stream_info.get('height', 'Unknown')
        avg_frame_rate = stream_info.get('avg_frame_rate', 'Unknown')

        if avg_frame_rate != 'Unknown':
            num, denom = map(float, avg_frame_rate.split('/'))
            frame_rate = num / denom if denom != 0 else 'Unknown'
        else:
            frame_rate = 'Unknown'

        return {
            'codec_name': codec_name,
            'resolution': f'{width}x{height}',
            'duration': f'{float(duration):.2f} seconds' if duration != 'Unknown' else 'Unknown',
            'bit_rate': f'{int(bit_rate) / 1000} kbps' if bit_rate != 'Unknown' else 'Unknown',
            'frame_rate': f'{frame_rate:.2f} fps' if frame_rate != 'Unknown' else 'Unknown',
        }

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while retrieving video properties: {e.stderr}")
        return None


properties = get_video_properties(output_video)
if properties:
    print("Video Properties:")
    for key, value in properties.items():
        print(f"{key}: {value}")
"""





def remove_audio(input_file, output_file):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-an',
        '-vcodec', 'copy',
        output_file
    ]
    subprocess.run(command, capture_output=True, check=True)

    return output_file
