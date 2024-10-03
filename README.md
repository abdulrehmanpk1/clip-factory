# 🎬 Clip Factory Pro

**Clip Factory Pro** is a Django-based video editing tool that allows users to perform various video manipulation tasks, such as splitting videos, removing audio, changing resolutions, overlaying images and text, and adjusting the size of text and images on the video.

## ✨ Features

- 📌 **Video Splitting**: Easily split your videos into multiple parts.
- 🔇 **Audio Removal**: Remove audio tracks from your videos.
- 🖼️ **Resolution Adjustment**: Change video resolution as per your requirements.
- 🖼️ **Image Overlay**: Overlay images on top of your video.
- 📝 **Text Overlay**: Add text overlays with customizable sizes and positions.
- 📏 **Text and Image Resizing**: Dynamically resize text and images directly on the video.

## 🚀 Quick Start

Follow the steps below to set up and run the project locally:

### 1. Clone the repository
```bash
git clone https://github.com/NIMAR-DAM/clip-factory-pro-backend.git  
cd Clip-Factory-Pro
```

### 2. Create and Activate a Virtual Environment

Ensure you have Python installed, then create and activate a virtual environment:

```bash
# Create a virtual environment
python -m venv env

# Activate the virtual environment
# On Windows
.\env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

The project uses FFmpeg for video processing. Make sure you install it on your system:

- For Windows: [Download FFmpeg](https://ffmpeg.org/download.html#windows)
- For macOS/Linux: Install via package manager, e.g., for macOS:
  ```bash
  brew install ffmpeg
  ```

### 5. Apply Migrations

Make sure the database is set up correctly by running the migrations:

```bash
python manage.py migrate
```

### 6. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver 0.0.0.0:9999
```

Now, you should be able to access the app in your browser at `http://0.0.0.0:9999/`.

## ⚙️ Configuration

You can configure various settings, such as the database or the host, by modifying the `settings.py` file in the `app` directory.

### Database

By default, the project uses SQLite, but you can switch to PostgreSQL or another database by adjusting the `DATABASES` setting in `settings.py`.

## 📂 Directory Structure

Here’s an overview of the project structure:

```
ClipFactoryPro/
├── app/
├── ffmpegProject/
├── fonts/
├── media/
├── manage.py
├── db.sqlite3
├── requirements.txt
```

- **app/**: Contains the main Django application files.
- **ffmpegProject/**: Holds all FFmpeg-related scripts or configurations.
- **manage.py**: Django's command-line utility for administrative tasks.
- **fonts/**: Directory for font files used in text overlays.
- **media/**: Contains the uploaded videos and media assets.
- **requirements.txt**: Python dependencies for the project.
- **db.sqlite3**: SQLite database file for development.

## 🛠️ Other Settings

You can adjust other settings in the `settings.py` file as needed, such as:

- Database configuration
- Allowed hosts
- Static and media file settings

## 🤝 Contributing

If you would like to contribute to **Clip Factory Pro**, feel free to submit a pull request or open an issue.
# clip-factory
