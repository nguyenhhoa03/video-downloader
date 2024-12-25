# Video Downloader (Under Development)

**Video Downloader** is an application designed to help users easily download videos from websites supported by **yt-dlp** on **Linux** operating systems. The application is built using Python and employs the **GTK** library for its graphical user interface.

Currently, the app is under development and supports downloading videos via **yt-dlp**. The available source code includes **app.py** and **ui.glade**, with plans to add a browser extension in the future.

The app only supports **Linux** at the moment, but other operating systems will be supported in the future.

## Features

- **Download videos from yt-dlp-supported websites:** The app allows downloading videos from platforms like YouTube, Vimeo, and more.  
- **Select video quality:** Users can choose the quality of the video before downloading.  
- **Choose download location:** Users can specify the folder where downloaded videos will be saved.  
- **GTK-based UI:** Simple and user-friendly interface designed for Linux environments.  

## Installation

### 1. Install yt-dlp

Before running the application, you need to install **yt-dlp**, as it is not pre-installed on Linux:

```bash
pip install yt-dlp
```

### 2. GTK Requirements

GTK is typically pre-installed on most modern Linux distributions. If your system does not have GTK (a rare case), you can install it using the following commands based on your operating system:

- **Ubuntu/Debian:**
  ```bash
  sudo apt-get install libgtk-3-dev
  ```
- **Fedora:**
  ```bash
  sudo dnf install gtk3-devel
  ```
- **Arch Linux:**
  ```bash
  sudo pacman -S gtk3
  ```

### 3. Installing the Application

Clone the source code from GitHub:

```bash
git clone https://github.com/nguyenhhoa03/video-downloader.git
cd video-downloader
```

Then, run the application using Python:

```bash
python3 app.py
```

## Directory Structure

```
video-downloader/
│
├── app.py            # Main source code of the application
├── ui.glade          # Glade file for the user interface
└── README.md         # Installation and usage guide
```

## How to Use

1. **Open the Video Downloader application** from the terminal or via the graphical interface.  
2. **Enter the video URL** you want to download.  
3. **Select video quality** (if available).  
4. **Choose the save location:** Select the folder to save the downloaded video.  
5. **Click "Download"** to start the download process.  

## Notes

- **Under Development:** The application is still under development, so you may encounter bugs or incomplete features.  
- **GTK Pre-installed:** Most Linux distributions already include GTK, so you can use the app out of the box.  
- **Cross-platform Support Coming Soon:** Support for Windows and macOS is planned for future versions.  
- **Source Code Only:** Currently, the source code includes `app.py` and `ui.glade`.  

## Contact

For issues or inquiries, feel free to:

- Open an issue on the [GitHub repository](https://github.com/nguyenhhoa03/video-downloader).  
- Email: **simpleosproject@gmail.com**  
