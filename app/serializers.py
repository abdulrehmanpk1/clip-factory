from rest_framework import serializers


class VideoProcessingSerializer(serializers.Serializer):
    video = serializers.FileField()
    text = serializers.CharField()
    text_color = serializers.CharField()
    font_family = serializers.CharField()
    text_x_percent = serializers.FloatField()
    text_y_percent = serializers.FloatField()
    image = serializers.FileField()
    image_w = serializers.IntegerField()
    image_h = serializers.IntegerField()
    image_x_percent = serializers.FloatField()
    image_y_percent = serializers.FloatField()
    # output_video = serializers.CharField()


class VideoQualitySerializer(serializers.Serializer):
    video = serializers.FileField()
    resolution = serializers.CharField(default='1920:1080')
    video_bitrate = serializers.CharField(default='5000k')
    audio_bitrate = serializers.CharField(default='256k')
    codec = serializers.CharField(default='libx264')
    crf = serializers.CharField(default='18')
    preset = serializers.CharField(default='slow')
