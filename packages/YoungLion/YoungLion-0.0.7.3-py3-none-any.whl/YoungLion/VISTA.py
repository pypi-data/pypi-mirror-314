"""
VISTA (Visual Information System and Technological Analysis)

VISTA is a comprehensive Python library designed for advanced visual data handling, manipulation, and analysis. It facilitates seamless interaction with image and video content, making it accessible for a wide range of applications from data visualization to machine learning preprocessing. The library is structured to include a modular framework for various data processing needs, with specialized classes and methods tailored for visual information processing.

Key Features of VISTA:
    - **Image Operations**: Enables reading, writing, resizing, and optimizing of images, with support for multiple formats, including raster and vector images. Offers utilities for advanced editing and metadata extraction.
    - **Video Processing**: Supports loading, modifying, and analyzing video files, offering functionality to extract frames, manipulate playback, and capture metadata.
    - **Data Visualization**: Provides tools for creating various types of visualizations, such as tables, charts, and graphs. These features are ideal for analytical and presentation purposes.
    - **Graphical Display of Information**: Includes methods to convert complex datasets into understandable visual formats, enabling quick insights and in-depth analysis.
    - **Error Handling and Customizable Settings**: Ensures robust error handling for file and format inconsistencies, allowing developers to adjust settings flexibly to fit specific requirements.

"""

# Imports

import os
import requests
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image as pilImage
from PIL import ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
from moviepy.video.VideoClip import ImageClip
from moviepy import *
from moviepy.video.VideoClip import VideoClip
import ffmpeg
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from tqdm import tqdm

class ImageTool:
    """
    A utility class that provides various image processing functionalities, such as loading,
    saving, resizing, and manipulating images. Primarily used as a helper to manage
    common image processing tasks.
    """

    def __init__(self) -> None:
        pass

    def load(self, path: str):
        """
        Loads an image from the specified path. If the image does not exist, creates a
        default 16x16 black image.

        :param path: The file path of the image.
        :return: A PIL Image object.
        """
        if os.path.exists(path):
            return pilImage.open(path)
        else:
            # Creates a 16x16 black placeholder image if file is not found
            return pilImage.new("RGBA", (16, 16), (0, 0, 0, 255))

    def save(self, image, path: str, format: str = 'PNG', optimize: bool = True, quality: int = 85):
        """
        Saves an image to the specified path with given format and optimization options.

        :param image: The PIL Image object to save.
        :param path: Path where the image will be saved.
        :param format: Image format (e.g., PNG, JPEG).
        :param optimize: Whether to optimize the image size.
        :param quality: Quality setting for saving (applicable to lossy formats).
        """
        image.save(path, format=format, quality=quality, optimize=optimize)

    def load_url(self, url: str, mode: str = 'RGBA'):
        """
        Loads an image from a URL and converts it to the specified mode.

        :param url: URL of the image to load.
        :param mode: Color mode (default is RGBA).
        :return: A PIL Image object.
        """
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return pilImage.open(response.raw).convert(mode)
        else:
            raise ValueError("Incorrect URL or unable to load image from the specified URL.")

    def resize(self, image, size: tuple):
        """
        Resizes the image to the specified dimensions.

        :param image: The PIL Image object to resize.
        :param size: New size as a tuple (width, height).
        :return: The resized PIL Image object.
        """
        return image.resize(size)

    def convert_to_grayscale(self, image):
        """
        Converts the image to grayscale.

        :param image: The PIL Image object.
        :return: A grayscale PIL Image object.
        """
        return image.convert("L")

    def read_text_from_image(self, image):
        """
        Extracts text from the image using OCR (Optical Character Recognition).

        :param image: The PIL Image object containing text.
        :return: Extracted text as a string.
        """
        return pytesseract.image_to_string(image)

    def draw_text_on_image(self, image, text: str, position: tuple = (10, 10), font_size: int = 15, color: str = "white"):
        """
        Draws specified text on the image at the given position.

        :param image: The PIL Image object.
        :param text: Text to be drawn on the image.
        :param position: Position (x, y) on the image where text should appear.
        :param font_size: Size of the text font.
        :param color: Color of the text.
        :return: The PIL Image object with the text drawn.
        """
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        draw.text(position, text, fill=color, font=font)
        return image

    def convert_to_binary(self, image, threshold: int = 128):
        """
        Converts the image to binary (black and white) using a specified threshold.

        :param image: The PIL Image object.
        :param threshold: Threshold level (0-255) for conversion.
        :return: A binary PIL Image object.
        """
        return image.convert("L").point(lambda x: 255 if x > threshold else 0, mode="1")

class Image:
    """
    A class to encapsulate image processing operations. Each instance represents
    a single image loaded and processed through the ImageTool helper.
    """

    def __init__(self, image=None):
        """
        Initializes the Image class, which wraps around a PIL Image object.

        :param image: Optionally, a PIL Image object can be loaded at initialization.
        """
        self.image = image

    def load(self, path: str):
        """
        Loads an image from the specified path using the ImageTool.

        :param path: Path of the image to load.
        :return: The Image instance (self) for method chaining.
        """
        self.image = ImageTool().load(path)
        return self

    def load_from_url(self, url: str, mode: str = 'RGBA'):
        """
        Loads an image from a URL.

        :param url: URL of the image.
        :param mode: Color mode (default is RGBA).
        :return: The Image instance (self) for method chaining.
        """
        self.image = ImageTool().load_url(url, mode)
        return self

    def save(self, path: str, format: str = 'PNG', optimize: bool = True, quality: int = 85):
        """
        Saves the loaded image to the specified path.

        :param path: Path to save the image.
        :param format: Format in which to save the image.
        :param optimize: Whether to optimize the saved image.
        :param quality: Quality setting for lossy formats.
        """
        ImageTool().save(self.image, path, format, optimize, quality)

    def show(self):
        """
        Displays the image using the default image viewer.
        """
        self.image.show()

    def resize(self, size: tuple):
        """
        Resizes the image to the specified size.

        :param size: New size as (width, height).
        :return: The Image instance (self) for method chaining.
        """
        self.image = ImageTool().resize(self.image, size)
        return self

    def convert_to_grayscale(self):
        """
        Converts the image to grayscale.

        :return: The Image instance (self) for method chaining.
        """
        self.image = ImageTool().convert_to_grayscale(self.image)
        return self

    def read_text(self):
        """
        Extracts text from the image using OCR.

        :return: Extracted text as a string.
        """
        return ImageTool().read_text_from_image(self.image)

    def draw_text(self, text: str, position: tuple = (10, 10), font_size: int = 15, color: str = "white"):
        """
        Draws text onto the image.

        :param text: Text to draw.
        :param position: Position (x, y) for text.
        :param font_size: Font size of the text.
        :param color: Color of the text.
        :return: The Image instance (self) for method chaining.
        """
        self.image = ImageTool().draw_text_on_image(self.image, text, position, font_size, color)
        return self

    def convert_to_binary(self, threshold: int = 128):
        """
        Converts the image to binary format.

        :param threshold: Threshold level for conversion.
        :return: The Image instance (self) for method chaining.
        """
        self.image = ImageTool().convert_to_binary(self.image, threshold)
        return self


class VideoTool:
    """
    VideoTool class provides functionalities for:
    - Creating a video from images.
    - Adding audio to video files.
    - Visualizing audio waveforms and converting them into video.
    - Combining images and audio in different formats.
    """

    def image_to_video(self, image_path: str, duration: int, output_path: str, fps: int = 24):
        """
        Converts a single image into a video with a specified duration.
        
        :param image_path: Path to the image file that will be converted to video.
        :param duration: Duration of the video in seconds.
        :param output_path: Path where the resulting video will be saved.
        :param fps: Frames per second for the video (default is 24).
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file '{image_path}' not found.")

        try:
            # Create the video clip using the image path
            clip = ImageClip(image_path).with_duration(duration)
            clip.write_videofile(output_path, codec="libx264", fps=fps)
        except Exception as e:
            raise RuntimeError(f"An error occurred while creating the video: {str(e)}")
    def audio_to_waveform_video(self, audio_path: str, output_path: str, sample_rate: int = 44100, fps: int = 24, height: int = 4, width: int = 8, sensitivity: float = 1.0):
        """
        Converts an audio file into a video with a waveform in dark theme.
        
        :param audio_path: Path to the audio file.
        :param output_path: Path where the resulting video will be saved.
        :param sample_rate: Sampling rate for the audio waveform.
        :param fps: Frames per second for the resulting video.
        :param height: Maximum height of the waveform.
        :param width: Width of the video.
        :param sensitivity: Sensitivity for waveform amplitude scaling.
        """
        # Load audio file
        y, sr = librosa.load(audio_path, sr=sample_rate)
        duration = librosa.get_duration(y=y, sr=sr)
        samples_per_frame = int(len(y) / (duration * fps))

        # Prepare frames folder
        if not os.path.exists("frames"):
            os.makedirs("frames")

        # Configure matplotlib for faster plotting
        plt.switch_backend('Agg')
        plt.style.use("dark_background")

        frames = []
        total_frames = int(duration * fps)

        print("Creating waveform frames...")

        # Progress bar setup
        with tqdm(total=total_frames, desc="Processing frames", unit="frame") as pbar:
            for i in range(total_frames):
                start_sample = i * samples_per_frame
                end_sample = start_sample + samples_per_frame
                frame_samples = y[start_sample:end_sample]

                # Scale amplitude by sensitivity
                frame_samples = frame_samples * sensitivity
                frame_samples = np.clip(frame_samples, -1, 1)  # Ensure values are in -1 to 1 range

                # Set color based on amplitude
                amplitude = np.max(np.abs(frame_samples))
                if amplitude > 0.7:
                    color = 'red'
                elif amplitude > 0.3:
                    color = 'yellow'
                else:
                    color = 'green'

                # Plot waveform for each frame
                plt.figure(figsize=(width, height), dpi=100)
                plt.plot(np.linspace(0, 1, len(frame_samples)), frame_samples, color=color)
                plt.ylim(-1, 1)
                plt.axis('off')

                # Save frame and add to frames list
                frame_filename = f"frames/frame_{i}.jpg"
                plt.savefig(frame_filename, bbox_inches='tight', pad_inches=0)
                frames.append(frame_filename)
                plt.close()

                # Update progress bar
                pbar.update(1)

        # Create video clip from frames and attach audio
        print("Combining frames into video...")
        clip = ImageSequenceClip(frames, fps=fps)
        audio_clip = AudioFileClip(audio_path)
        clip = clip.with_audio(audio_clip)  # Güncellendi
        clip.write_videofile(output_path, codec="libx264", fps=fps)

        # Clean up frames
        for frame_filename in frames:
            os.remove(frame_filename)

        print("Waveform video creation completed.")


    def create_video_from_images(self, images: list, duration: int, output_path: str, fps: int = 24):
        """
        Create a video from a list of image files.
        
        :param images: List of image file paths.
        :param duration: Duration each image should be displayed (in seconds).
        :param output_path: Path where the video will be saved.
        :param fps: Frames per second for the video.
        """
        if not all(os.path.exists(image) for image in images):
            raise FileNotFoundError("One or more image files in the list do not exist.")

        clips = []
        for image_path in images:
            try:
                clip = ImageClip(image_path).with_duration(duration)
                clips.append(clip)
            except Exception as e:
                print(f"Error processing image '{image_path}': {str(e)}")
                continue

        if not clips:
            raise RuntimeError("No valid images could be processed for video creation.")

        video = concatenate_videoclips(clips, method="compose")
        video.write_videofile(output_path, codec='libx264', fps=fps)

    def load_video(self, video_path: str) -> VideoFileClip:
        """
        Loads a video file for further processing.

        :param video_path: Path to the video file to be loaded.
        :return: A VideoFileClip object representing the loaded video.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file '{video_path}' not found.")

        try:
            video = VideoFileClip(video_path)
            print(f"Loaded video: {video_path}")
            return video
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the video: {str(e)}")

    def save_video(self, clip: VideoFileClip, output_path: str, codec: str = "libx264", fps: int = 24):
        """
        Saves a video clip to the specified path.

        :param clip: A VideoFileClip object to be saved.
        :param output_path: Path where the video will be saved.
        :param codec: Codec to use for encoding the video (default is 'libx264').
        :param fps: Frames per second for the output video (default is 24).
        """
        if not isinstance(clip, VideoFileClip):
            raise ValueError("Provided clip is not a valid VideoFileClip object.")

        try:
            clip.write_videofile(output_path, codec=codec, fps=fps)
            print(f"Video saved to: {output_path}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while saving the video: {str(e)}")


    def change_video_format(self, input_path: str, output_path: str, target_format: str = "mp4", codec: str = "libx264", fps: int = 24):
        """
        Converts a video file to a specified format.

        :param input_path: Path to the input video file.
        :param output_path: Path to the output video file (should include the target format extension).
        :param target_format: Desired video format (default is 'mp4').
        :param codec: Codec to use for encoding the video (default is 'libx264').
        :param fps: Frames per second for the output video (default is 24).
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input video file '{input_path}' not found.")

        if not output_path.endswith(f".{target_format}"):
            raise ValueError(f"Output path must have the extension '.{target_format}'.")

        try:
            clip = VideoFileClip(input_path)
            clip.write_videofile(output_path, codec=codec, fps=fps)
            print(f"Video format changed to {target_format} and saved to: {output_path}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while changing video format: {str(e)}")

    def extract_audio_from_video(self, video_path: str, output_audio_path: str):
        """
        Extracts the audio track from a video file and saves it as a separate file.

        :param video_path: Path to the video file.
        :param output_audio_path: Path where the extracted audio will be saved.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file '{video_path}' not found.")

        try:
            video = VideoFileClip(video_path)
            audio = video.audio
            if audio:
                audio.write_audiofile(output_audio_path)
                print(f"Audio extracted and saved to: {output_audio_path}")
            else:
                raise ValueError("The video does not contain an audio track.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while extracting audio: {str(e)}")

    def add_audio_to_video(self, video_path: str, audio_path: str, output_path: str):
        """
        Adds an audio track to a video file.

        :param video_path: Path to the video file.
        :param audio_path: Path to the audio file.
        :param output_path: Path where the resulting video will be saved.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file '{video_path}' not found.")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file '{audio_path}' not found.")

        try:
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            video_with_audio = video.with_audio(audio)
            video_with_audio.write_videofile(output_path, codec="libx264", fps=video.fps)
            print(f"Audio added to video and saved to: {output_path}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while adding audio to video: {str(e)}")


    def resize_video(self, video_path: str, output_path: str, width: int = None, height: int = None):
        """
        Resizes a video to specified dimensions while maintaining the aspect ratio if only one dimension is provided.

        :param video_path: Path to the input video file.
        :param output_path: Path where the resized video will be saved.
        :param width: Desired width of the output video (optional).
        :param height: Desired height of the output video (optional).
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file '{video_path}' not found.")

        if width is None and height is None:
            raise ValueError("At least one of 'width' or 'height' must be specified.")

        try:
            video = VideoFileClip(video_path)
            # Maintain aspect ratio if only one dimension is provided
            if width is None:
                aspect_ratio = video.size[0] / video.size[1]
                width = int(height * aspect_ratio)
            elif height is None:
                aspect_ratio = video.size[1] / video.size[0]
                height = int(width * aspect_ratio)

            resized_video = video.resized((width, height))
            resized_video.write_videofile(output_path, codec="libx264", fps=video.fps)
            print(f"Video resized to {width}x{height} and saved to: {output_path}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while resizing the video: {str(e)}")

    def add_text_to_video(self,video_path: str, text: str, output_path: str, position: tuple = ('center', 'center'), font: str = "arial", font_size: int = 50, color: str = "white"):
        """
        Adds text overlay to a video.

        :param video_path: Path to the input video file.
        :param text: The text to be added to the video.
        :param output_path: Path where the final video (with text) will be saved.
        :param position: Tuple (x, y) for text location.
        :param font: Name of the font (system-installed).
        :param font_size: Font size of the text.
        :param color: Color of the text.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        video = VideoFileClip(video_path)

        try:
            # Create a text clip
            text_clip = (
                TextClip(
                    text=text,
                    font_size=font_size,
                    font=font,
                    color=color
                )
            )
            text_clip=text_clip.with_position(position).with_duration(video.duration)
        except Exception as e:
            raise ValueError(f"Error creating TextClip: {e}")

        # Combine the video and text
        final_video = CompositeVideoClip([video, text_clip])

        # Write the output video
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")


    def trim_video(self, video_path: str, start_time: float, end_time: float, output_path: str):
        """
        Trims a video between the given start and end times, including audio.

        :param video_path: Path to the input video file.
        :param start_time: Start time (in seconds) for the trimmed video.
        :param end_time: End time (in seconds) for the trimmed video.
        :param output_path: Path where the trimmed video will be saved.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        try:
            # Load the video file
            video = VideoFileClip(video_path)

            # Check if the video has audio
            if video.audio is None:
                print(f"Warning: Video '{video_path}' has no audio track.")
            
            # Extract the specified segment of the video
            trimmed_video = video.subclip(start_time, end_time)
            
            # Write the trimmed video to the output path
            trimmed_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        except Exception as e:
            print(f"An error occurred while trimming the video: {e}")

    def concatenate_videos(self, video_paths: list, output_path: str):
        """
        Concatenates multiple videos into a single video, including audio.

        :param video_paths: List of paths to the video files to be concatenated.
        :param output_path: Path where the concatenated video will be saved.
        """
        try:
            # Load each video as a VideoFileClip object
            clips = [VideoFileClip(video) for video in video_paths]
            
            # Ensure all clips include audio
            for clip in clips:
                if clip.audio is None:
                    print(f"Warning: Video '{clip.filename}' has no audio track.")
            
            # Concatenate the video clips
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Write the concatenated video to the output path
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        except Exception as e:
            print(f"Error during concatenation: {e}")

    def merge_videos(self, video_paths: list, output_path: str):
        """
        Merges multiple video files into a single video by concatenating them, including audio.

        :param video_paths: List of paths to the input video files.
        :param output_path: Path where the merged video file will be saved.
        """
        if not all(os.path.exists(path) for path in video_paths):
            raise FileNotFoundError("One or more video files not found.")

        try:
            # Load each video as a VideoFileClip object
            clips = [VideoFileClip(path) for path in video_paths]
            
            # Ensure all clips include audio
            for clip in clips:
                if clip.audio is None:
                    print(f"Warning: Video '{clip.filename}' has no audio track.")
            
            # Concatenate the video clips
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Write the concatenated video to the output path
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        except Exception as e:
            print(f"An error occurred while merging videos: {e}")


class AudioTool:
    """
    A utility class for performing various operations on audio files.
    Includes functions for trimming, duration adjustment, waveform generation, and more.

    Usage:
        tool = AudioTool()
        tool.trim_audio("input.wav", "output.wav", target_duration=10.0)
    """
    
    def __init__(self) -> None:
        pass

    def trim_audio(self, audio_path: str, output_path: str, target_duration: float, sample_rate: int = 44100):
        """
        Trims the audio file to a specified duration by cutting from the end if needed.

        :param audio_path: Path to the input audio file.
        :param output_path: Path where the trimmed audio file will be saved.
        :param target_duration: Target duration for the output audio file in seconds.
        :param sample_rate: Sampling rate for loading and saving the audio.
        """
        # Load the audio file
        y, sr = librosa.load(audio_path, sr=sample_rate)
        original_duration = librosa.get_duration(y=y, sr=sr)
        
        # Calculate the number of samples for the target duration
        target_samples = int(target_duration * sr)
        
        # Trim if the audio is longer than the target duration
        if original_duration > target_duration:
            y = y[:target_samples]  # Cut from the end
        
        # Save the trimmed audio file
        sf.write(output_path, y, sr)
        print(f"Audio trimmed to {target_duration} seconds and saved at {output_path}")
    def trim_audio_section(self, audio_path: str, output_path: str, start_time: float, end_time: float, sample_rate: int = 44100):
        """
        Trims a specific section of an audio file.

        :param audio_path: Path to the input audio file.
        :param output_path: Path where the trimmed audio file will be saved.
        :param start_time: Start time in seconds.
        :param end_time: End time in seconds.
        :param sample_rate: Sampling rate for loading and saving the audio.
        """
        y, sr = librosa.load(audio_path, sr=sample_rate)
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        trimmed_audio = y[start_sample:end_sample]
        sf.write(output_path, trimmed_audio, sr)
        print(f"Audio section from {start_time}s to {end_time}s saved at {output_path}")

    
    def change_speed(self, audio_path: str, output_path: str, speed_factor: float, sample_rate: int = 44100):
        """
        Changes the speed of an audio file.

        :param audio_path: Path to the input audio file.
        :param output_path: Path where the modified audio will be saved.
        :param speed_factor: Factor by which to speed up (>1.0) or slow down (<1.0) the audio.
        :param sample_rate: Sampling rate for loading and saving the audio.
        """
        y, sr = librosa.load(audio_path, sr=sample_rate)

        y_fast = librosa.effects.time_stretch(y, speed_factor)  
        sf.write(output_path, y_fast, sr)

        print(f"Audio speed changed by a factor of {speed_factor} and saved at {output_path}")
    def change_pitch(self, audio_path: str, output_path: str, n_steps: int, sample_rate: int = 44100):
        """
        Changes the pitch of an audio file.

        :param audio_path: Path to the input audio file.
        :param output_path: Path where the modified audio file will be saved.
        :param n_steps: Number of semitones to shift (e.g., +2 for two semitones up, -3 for three semitones down).
        :param sample_rate: Sampling rate for loading and saving the audio.
        """
        y, sr = librosa.load(audio_path, sr=sample_rate)
        y_pitch = librosa.effects.pitch_shift(y, sr, n_steps)
        sf.write(output_path, y_pitch, sr)
        print(f"Pitch shifted by {n_steps} semitones and saved at {output_path}")

    
    def adjust_volume(self, audio_path: str, output_path: str, volume_factor: float, sample_rate: int = 44100):
        """
        Adjusts the volume of an audio file.

        :param audio_path: Path to the input audio file.
        :param output_path: Path where the volume-adjusted audio will be saved.
        :param volume_factor: Factor to adjust volume (>1.0 for increase, <1.0 for decrease).
        :param sample_rate: Sampling rate for loading and saving the audio.
        """
        y, sr = librosa.load(audio_path, sr=sample_rate)
        y_adjusted = y * volume_factor
        y_adjusted = np.clip(y_adjusted, -1.0, 1.0)  # Prevent clipping
        sf.write(output_path, y_adjusted, sr)
        print(f"Volume adjusted by a factor of {volume_factor} and saved at {output_path}")
    
    def merge_audios(self, audio_paths: list, output_path: str, sample_rate: int = 44100):
        """
        Merges multiple audio files into a single file.

        :param audio_paths: List of paths to the input audio files.
        :param output_path: Path where the merged audio file will be saved.
        :param sample_rate: Sampling rate for loading and saving the audio.
        """
        merged_audio = np.array([])
        for path in audio_paths:
            y, sr = librosa.load(path, sr=sample_rate)
            merged_audio = np.concatenate((merged_audio, y))
        
        sf.write(output_path, merged_audio, sample_rate)
        print(f"Audio files merged and saved at {output_path}")
    
    def generate_sine_wave(self, frequency: float, duration: float, output_path: str, sample_rate: int = 44100):
        """
        Generates a sine wave sound file.

        :param frequency: Frequency of the sine wave in Hertz.
        :param duration: Duration of the sine wave in seconds.
        :param output_path: Path where the generated sine wave will be saved.
        :param sample_rate: Sampling rate for the sine wave.
        """
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # Amplitude scaled to 0.5
        sf.write(output_path, sine_wave, sample_rate)
        print(f"Sine wave of {frequency}Hz generated and saved at {output_path}")
    def generate_tone(self, frequency: float, duration: float, sample_rate: int = 44100):
        """
        Generates a sine wave tone at a given frequency and duration.

        :param frequency: Frequency of the tone in Hz (e.g., 440 for A4).
        :param duration: Duration of the tone in seconds.
        :param sample_rate: Sampling rate for the audio.
        :return: Numpy array representing the audio waveform.
        """
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        tone = 0.5 * np.sin(2 * np.pi * frequency * t)  # Amplitude scaled to 0.5 to avoid clipping
        return tone
    
    def extract_segment(self, audio_path: str, output_path: str, start_time: float, end_time: float, sample_rate: int = 44100):
        """
        Extracts a specific segment from an audio file.

        :param audio_path: Path to the input audio file.
        :param output_path: Path where the extracted segment will be saved.
        :param start_time: Start time of the segment in seconds.
        :param end_time: End time of the segment in seconds.
        :param sample_rate: Sampling rate for loading and saving the audio.
        """
        y, sr = librosa.load(audio_path, sr=sample_rate)
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        segment = y[start_sample:end_sample]
        sf.write(output_path, segment, sr)
        print(f"Segment from {start_time}s to {end_time}s extracted and saved at {output_path}")
    def merge_audios(self, audio_paths: list, output_path: str, sample_rate: int = 44100):
        """
        Merges multiple audio files into a single file by concatenating them.

        :param audio_paths: List of paths to the input audio files.
        :param output_path: Path where the merged audio file will be saved.
        :param sample_rate: Sampling rate for loading and saving the audio.
        """
        merged_audio = np.array([])
        try:
            for path in audio_paths:
                y, sr = librosa.load(path, sr=sample_rate)
                merged_audio = np.concatenate((merged_audio, y))
            sf.write(output_path, merged_audio, sample_rate)
            print(f"Audio files merged and saved at {output_path}")
        except Exception as e:
            print(f"An error occurred while merging audios: {e}")
    def remix_audios(self, audio_path1: str, audio_path2: str, output_path: str, sample_rate: int = 44100, volume1: float = 1.0, volume2: float = 1.0):
        """
        Creates a remix by combining two audio files.

        :param audio_path1: Path to the first audio file.
        :param audio_path2: Path to the second audio file.
        :param output_path: Path where the remix audio file will be saved.
        :param sample_rate: Sampling rate for loading and saving the audio.
        :param volume1: Volume adjustment for the first audio (default 1.0).
        :param volume2: Volume adjustment for the second audio (default 1.0).
        """
        # Load both audio files
        y1, sr1 = librosa.load(audio_path1, sr=sample_rate)
        y2, sr2 = librosa.load(audio_path2, sr=sample_rate)

        # Ensure both audio files are of the same length
        min_length = min(len(y1), len(y2))
        y1 = y1[:min_length] * volume1
        y2 = y2[:min_length] * volume2

        # Mix the audios
        remix = y1 + y2

        # Normalize the output to prevent clipping
        remix = remix / np.max(np.abs(remix))

        # Save the remix
        sf.write(output_path, remix, sample_rate)
        print(f"Remix created and saved at {output_path}")
    def reverse_audio(self, audio_path: str, output_path: str, sample_rate: int = 44100):
        """
        Reverses the audio file.

        :param audio_path: Path to the input audio file.
        :param output_path: Path where the reversed audio will be saved.
        :param sample_rate: Sampling rate for loading and saving the audio.
        """
        y, sr = librosa.load(audio_path, sr=sample_rate)
        y_reversed = y[::-1]
        sf.write(output_path, y_reversed, sr)
        print(f"Audio reversed and saved at {output_path}")
    def apply_rhythm(self, tones: list, durations: list, sample_rate: int = 44100):
        """
        Combines tones into a rhythm by applying durations and silences.

        :param tones: List of tones (numpy arrays).
        :param durations: List of durations for each tone in seconds.
        :param sample_rate: Sampling rate for the audio.
        :return: Combined waveform as a numpy array.
        """
        rhythm = []
        for tone, duration in zip(tones, durations):
            rhythm.append(tone)
            silence = np.zeros(int(sample_rate * 0.1))  # Add 0.1 seconds of silence between tones
            rhythm.append(silence)
        return np.concatenate(rhythm)
    def combine_tones(self, tones: list):
        """
        Combines multiple tones into a single waveform (e.g., for chords).

        :param tones: List of tones (numpy arrays) to combine.
        :return: Combined waveform as a numpy array.
        """
        combined = sum(tones) / len(tones)  # Average the waveforms to avoid clipping
        return combined / np.max(np.abs(combined))  # Normalize
    def save_composition(self, waveform: np.ndarray, output_path: str, sample_rate: int = 44100):
        """
        Saves a waveform as an audio file.

        :param waveform: The audio waveform as a numpy array.
        :param output_path: Path where the audio file will be saved.
        :param sample_rate: Sampling rate for the audio.
        """
        sf.write(output_path, waveform, sample_rate)
        print(f"Composition saved at {output_path}")

class AnalysisTableTool:
    def __init__(self) -> None:
        """
        Initializes the AnalysisTableTool class.
        """
        pass

    def curve_edge(self, x0, y0, x1, y1, rad):
        """
        Generates a curved edge between two points for a more visually appealing graph.
        """
        t = np.linspace(0, 1, 100)
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = (x1 - x0), (y1 - y0)
        xc, yc = xm - rad * dy, ym + rad * dx
        xt = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * xc + t ** 2 * x1
        yt = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * yc + t ** 2 * y1
        return xt, yt

    def plot_graph(self, 
                   nodes: dict, 
                   edges: list, 
                   title: str="VISTA", 
                   rad: int = 0, 
                   backgroundcolor="black",
                   save_path: str = None,
                   show: bool = True,
                   save_html: bool = False):
        """
        Creates and displays a graph visualization based on user-defined nodes and edges.

        :param nodes: A dictionary where keys are node names, and values are dictionaries with
                      attributes like color and position. Example:
                      {
                          "Node1": {"color": "red", "pos": (0, 1)},
                          "Node2": {"color": "blue", "pos": (1, 0)}
                      }
        :param edges: A list of tuples representing connections between nodes.
                      Each tuple contains (start_node, end_node, color). Example:
                      [
                          ("Node1", "Node2", "black"),
                          ("Node2", "Node3", "blue")
                      ]
        :param title: Title of the graph visualization.
        :param rad: Curvature radius for edges.
        :param backgroundcolor: Background color (string or RGB tuple).
        :param save_path: Path to save the graph (as an image or HTML file).
        :param show: Boolean to control whether the graph is displayed.
        :param save_html: Boolean to control whether the graph is saved as an HTML file.
        """
        # Handle background color input
        if isinstance(backgroundcolor, tuple):
            backgroundcolor = f"rgb({backgroundcolor[0]}, {backgroundcolor[1]}, {backgroundcolor[2]})"

        # Extract node attributes
        node_x = []
        node_y = []
        node_labels = []
        node_colors = []

        for node, attr in nodes.items():
            node_x.append(attr['pos'][0])
            node_y.append(attr['pos'][1])
            node_labels.append(node)
            node_colors.append(attr['color'])

        # Create figure
        fig = go.Figure()

        # Plot edges
        for i, edge in enumerate(edges):
            x0, y0 = nodes[edge[0]]['pos']
            x1, y1 = nodes[edge[1]]['pos']
            xt, yt = self.curve_edge(x0, y0, x1, y1, rad * ((-1) ** i))
            fig.add_trace(go.Scatter(
                x=xt, y=yt,
                mode='lines',
                line=dict(width=2, color=edge[2]),
                hoverinfo='none'
            ))

        # Plot nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(size=40, color=node_colors, line=dict(width=2)),
            text=node_labels,
            textposition='top center',
            hoverinfo='text'
        ))

        # Customize layout
        fig.update_layout(
            title=title,
            title_font_size=20,
            showlegend=False,
            plot_bgcolor=backgroundcolor,
            paper_bgcolor=backgroundcolor,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )

        # Hide axes
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)

        # Save graph if save_path is specified
        if save_path:
            file_name, file_extension = os.path.splitext(save_path)
            if save_html or file_extension.lower() == '.html':
                pio.write_html(fig, file=f"{file_name}.html")
            else:
                # Save as an image (requires `kaleido` or `orca`)
                fig.write_image(save_path)

        # Show graph if `show` is True
        if show:
            pio.show(fig)
    def generate_bar_chart(self, data: dict, x_axis_label: str, y_axis_label: str, bar_colors: list = None, save_path: str = None, show: bool = True,title: str="VISTA", ):
        """
        Generates a bar chart.

        :param data: Dictionary with keys as categories (x-axis) and values as numerical data (y-axis).
        :param title: Title of the chart.
        :param x_axis_label: Label for the x-axis.
        :param y_axis_label: Label for the y-axis.
        :param bar_colors: Optional list of colors for each bar.
        :param save_path: Path to save the chart as an image (if provided).
        :param show: Whether to display the chart (default is True).
        """
        fig = go.Figure()
        categories = list(data.keys())
        values = list(data.values())

        fig.add_trace(go.Bar(x=categories, y=values, marker_color=bar_colors, name="Values"))

        fig.update_layout(
            title=title,
            xaxis_title=x_axis_label,
            yaxis_title=y_axis_label,
            template="plotly_dark"
        )

        if save_path:
            fig.write_image(save_path)
        if show:
            fig.show()

    def generate_line_chart(self, x_data: list, y_data: list, title: str, x_axis_label: str, y_axis_label: str, line_color: str = "blue", save_path: str = None, show: bool = True):
        """
        Creates a line chart.

        :param x_data: List of values for the x-axis.
        :param y_data: List of values for the y-axis.
        :param title: Title of the chart.
        :param x_axis_label: Label for the x-axis.
        :param y_axis_label: Label for the y-axis.
        :param line_color: Color of the line (default is blue).
        :param save_path: Path to save the chart as an image (if provided).
        :param show: Whether to display the chart (default is True).
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', line=dict(color=line_color), name="Line"))

        fig.update_layout(
            title=title,
            xaxis_title=x_axis_label,
            yaxis_title=y_axis_label,
            template="plotly_dark"
        )

        if save_path:
            fig.write_image(save_path)
        if show:
            fig.show()

    def generate_pie_chart(self, data: dict, title: str, save_path: str = None, show: bool = True):
        """
        Generates a pie chart.

        :param data: Dictionary with keys as categories and values as proportions.
        :param title: Title of the pie chart.
        :param save_path: Path to save the chart as an image (if provided).
        :param show: Whether to display the chart (default is True).
        """
        fig = go.Figure()
        labels = list(data.keys())
        values = list(data.values())

        fig.add_trace(go.Pie(labels=labels, values=values, hole=0.3))

        fig.update_layout(
            title=title,
            template="plotly_dark"
        )

        if save_path:
            fig.write_image(save_path)
        if show:
            fig.show()

    def generate_scatter_plot(self, x_data: list, y_data: list, title: str, x_axis_label: str, y_axis_label: str, marker_color: str = "red", save_path: str = None, show: bool = True):
        """
        Creates a scatter plot.

        :param x_data: List of x-axis values.
        :param y_data: List of y-axis values.
        :param title: Title of the scatter plot.
        :param x_axis_label: Label for the x-axis.
        :param y_axis_label: Label for the y-axis.
        :param marker_color: Color of the markers (default is red).
        :param save_path: Path to save the plot as an image (if provided).
        :param show: Whether to display the chart (default is True).
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers', marker=dict(color=marker_color, size=10), name="Points"))

        fig.update_layout(
            title=title,
            xaxis_title=x_axis_label,
            yaxis_title=y_axis_label,
            template="plotly_dark"
        )

        if save_path:
            fig.write_image(save_path)
        if show:
            fig.show()
    def generate_histogram(self, 
                       data: list, 
                       x_axis_label: str, 
                       y_axis_label: str, 
                       num_bins: int = 10, 
                       title: str='VISTA',
                       bar_color: str = "blue", 
                       save_path: str = None, 
                       show: bool = True,
                       figsize:tuple=(10,6)):
        """
        Generates and optionally saves a histogram plot.

        :param data: List of numerical data to create the histogram.
        :param title: Title of the histogram.
        :param x_axis_label: Label for the x-axis (default: "Values").
        :param y_axis_label: Label for the y-axis (default: "Frequency").
        :param num_bins: Number of bins in the histogram (default: 10).
        :param bar_color: Color of the bars (default: "blue").
        :param save_path: File path to save the generated plot.
        :param show: Whether to display the plot in a window (default: True).
        :param figsize: Tuple of figure size (width, height) in inches (default: (10,6))
        """
        
        # Create the histogram
        plt.figure(figsize=figsize)
        plt.hist(data, bins=num_bins, color=bar_color, edgecolor="black")
        
        # Set titles and labels
        plt.title(title, fontsize=16)
        plt.xlabel(x_axis_label, fontsize=14)
        plt.ylabel(y_axis_label, fontsize=14)
        
        # Save the plot
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        
        # Show the plot if requested
        if show:
            plt.show()
        
        # Clear the figure to prevent overlaps in successive calls
        plt.clf()
    def generate_scatter_plot(self, 
                          x_data: list, 
                          y_data: list, 
                          title: str, 
                          x_axis_label: str = "X-axis", 
                          y_axis_label: str = "Y-axis", 
                          point_color: str = "blue", 
                          point_size: int = 10, 
                          save_path: str = None, 
                          show: bool = True,
                          figsize:tuple=(10,6)):
        """
        Generates and optionally saves a scatter plot.

        :param x_data: List of values for the X-axis.
        :param y_data: List of values for the Y-axis.
        :param title: Title of the scatter plot.
        :param x_axis_label: Label for the X-axis (default: "X-axis").
        :param y_axis_label: Label for the Y-axis (default: "Y-axis").
        :param point_color: Color of the scatter points (default: "blue").
        :param point_size: Size of the scatter points (default: 10).
        :param save_path: File path to save the generated plot.
        :param show: Whether to display the plot in a window (default: True).
        :param figsize: Tuple of figure size (width, height) in inches (default: (10,6))
        """

        # Create the scatter plot
        plt.figure(figsize=figsize)
        plt.scatter(x_data, y_data, color=point_color, s=point_size)

        # Set titles and labels
        plt.title(title, fontsize=16)
        plt.xlabel(x_axis_label, fontsize=14)
        plt.ylabel(y_axis_label, fontsize=14)

        # Save the plot
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        # Show the plot if requested
        if show:
            plt.show()

        # Clear the figure to prevent overlaps in successive calls
        plt.clf()
    def generate_box_plot(self, 
                      data: list, 
                      labels: list, 
                      title: str, 
                      y_axis_label: str = "Values", 
                      box_color: str = "blue", 
                      save_path: str = None, 
                      show: bool = True,
                      figsize:tuple=(10,6)):
        """
        Generates and optionally saves a box plot.

        :param data: List of numerical datasets for the box plot.
        :param labels: List of labels for each dataset.
        :param title: Title of the box plot.
        :param y_axis_label: Label for the Y-axis (default: "Values").
        :param box_color: Color of the box outlines (default: "blue").
        :param save_path: File path to save the generated plot.
        :param show: Whether to display the plot in a window (default: True).
        :param figsize: Tuple of figure size (width, height) in inches (default: (10,6))
        """

        # Create the box plot
        plt.figure(figsize=figsize)
        box = plt.boxplot(data, patch_artist=True, labels=labels)

        # Set box colors
        for patch in box['boxes']:
            patch.set(facecolor="lightblue", edgecolor=box_color)

        # Set titles and labels
        plt.title(title, fontsize=16)
        plt.ylabel(y_axis_label, fontsize=14)

        # Save the plot
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        # Show the plot if requested
        if show:
            plt.show()

        # Clear the figure to prevent overlaps in successive calls
        plt.clf()
    def generate_pie_chart(self, 
                       labels: list, 
                       values: list, 
                       title: str, 
                       colors: list = None, 
                       save_path: str = None, 
                       show: bool = True,
                       figsize:tuple=(8,8)):
        """
        Generates and optionally saves a pie chart.

        :param labels: List of categories for the pie chart.
        :param values: Corresponding values for each category.
        :param title: Title of the pie chart.
        :param colors: List of colors for the slices (default: None, uses default colors).
        :param save_path: File path to save the generated plot.
        :param show: Whether to display the plot in a window (default: True).
        :param figsize: Tuple of figure size (width, height) in inches (default: (8,8)
        """
        # Create the pie chart
        plt.figure(figsize=figsize)
        plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)

        # Set title
        plt.title(title, fontsize=16)

        # Save the chart
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        # Show the chart if requested
        if show:
            plt.show()

        # Clear the figure to prevent overlaps in successive calls
        plt.clf()


