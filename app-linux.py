#!/usr/bin/env python3

import gi
import os
import yt_dlp
import threading

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class VideoDownloaderApp:
    def __init__(self, glade_file):
        # Load the Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.builder.connect_signals(self)

        # Get the main window
        self.main_window = self.builder.get_object('main_window')
        self.main_window.connect('destroy', Gtk.main_quit)

        # Get UI elements
        self.download_button = self.builder.get_object('download_button')
        self.download_button.connect("clicked", self.on_download_button_clicked)
        self.url_entry = self.builder.get_object('url_entry')
        self.format_selector = self.builder.get_object('format_selector')
        self.save_path_entry = self.builder.get_object('save_path_entry')
        self.save_path_chooser = self.builder.get_object('save_path_chooser')
        self.download_button = self.builder.get_object('download_button')
        self.download_progress = self.builder.get_object('download_progress')
        self.log_view = self.builder.get_object('log_view')

        # Set default save path
        default_save_path = os.path.expanduser('~/Downloads')
        self.save_path_entry.set_text(default_save_path)

        # Initialize log buffer
        self.log_buffer = self.log_view.get_buffer()

    def on_save_path_chooser_file_set(self, widget):
        """Update save path when file chooser is used"""
        selected_folder = self.save_path_chooser.get_filename()
        if selected_folder:
            self.save_path_entry.set_text(selected_folder)

    def log_message(self, message):
        """Add message to log view"""
        GLib.idle_add(self._append_to_log, message)

    def _append_to_log(self, message):
        """Thread-safe method to append to log buffer"""
        end_iter = self.log_buffer.get_end_iter()
        self.log_buffer.insert(end_iter, message + '\n')
        # Scroll to the end of the log
        self.log_view.scroll_to_iter(
            self.log_buffer.get_end_iter(), 
            0.0, False, 0.0, 0.0
        )

    def update_progress(self, fraction, text=''):
        """Update download progress bar"""
        GLib.idle_add(self._set_progress, fraction, text)

    def _set_progress(self, fraction, text):
        """Thread-safe method to update progress bar"""
        self.download_progress.set_fraction(fraction)
        if text:
            self.download_progress.set_text(text)

    def on_download_button_clicked(self, widget):
        """Handle video download process"""
        # Reset progress
        self.update_progress(0, 'Starting download...')
        
        # Get URL and validate
        url = self.url_entry.get_text().strip()
        if not url:
            self.log_message('Error: Please enter a valid URL')
            return

        # Get selected format
        format_index = self.format_selector.get_active()
        format_map = {
            0: 'mp3',     # Audio only
            1: '144p',    # Video 144p
            2: '240p',    # Video 240p
            3: '360p',    # Video 360p
            4: '480p',    # Video 480p
            5: '720p',    # Video HD 720p
            6: '1080p',   # Video FHD 1080p
            7: '1440p',   # Video 2K 1440p
            8: '2160p',   # Video 4K 2160p
            9: '4320p'    # Video 8K 4320p
        }
        selected_format = format_map.get(format_index, '720p')

        # Get save path
        save_path = self.save_path_entry.get_text()
        os.makedirs(save_path, exist_ok=True)

        # Start download in a separate thread
        threading.Thread(
            target=self.download_video, 
            args=(url, save_path, selected_format), 
            daemon=True
        ).start()

    def download_video(self, url, save_path, selected_format):
        """Download video using yt-dlp"""
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'format': f'bestvideo[height<={selected_format.rstrip("p")}]+bestaudio[ext=m4a]/best[height<={selected_format.rstrip("p")}]',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',  # Ép định dạng đầu ra là mp4
                'progress_hooks': [self.yt_dlp_progress],
                'noplaylist': True
            }

            # Specific handling for audio only
            if selected_format == 'mp3':
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]

            # Download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_title = info_dict.get('title', 'Unknown Title')
                
            self.log_message(f'Successfully downloaded: {video_title}')
            self.update_progress(1.0, 'Download Complete!')

        except Exception as e:
            self.log_message(f'Error downloading video: {str(e)}')
            self.update_progress(0.0, 'Download Failed')

    def yt_dlp_progress(self, d):
        """Progress callback for yt-dlp"""
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total > 0:
                progress = downloaded / total
                status = f"Downloading: {progress*100:.1f}%"
                self.update_progress(progress, status)
        elif d['status'] == 'finished':
            self.update_progress(1.0, 'Processing...')

    def run(self):
        """Start the application"""
        self.main_window.show_all()
        Gtk.main()

def main():
    app = VideoDownloaderApp('ui.glade')
    app.run()

if __name__ == '__main__':
    main()

