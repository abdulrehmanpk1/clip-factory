from django.db import models


class VideoFile(models.Model):
    video = models.FileField(upload_to='videos/')
    image = models.FileField(upload_to='images/')
    watermarked_video = models.FileField(upload_to='watermarked/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video {self.id} - {self.video_file.name}"

