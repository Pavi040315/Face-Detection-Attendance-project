# Face Detection Attendance System

This project is an automated attendance system that uses facial recognition. It captures video from a webcam, detects faces, identifies known individuals, and records their attendance in a daily CSV log file.

## Features

*   **Real-time Face Recognition**: Detects and identifies faces from a live webcam feed.
*   **Automatic Attendance Logging**: Marks attendance automatically when a known face is recognized.
*   **Daily Records**: Creates a new CSV file for each day to log attendance, preventing duplicate entries for the same person on the same day.
*   **Image Snapshots**: Captures and saves a snapshot of the person's face at the moment their attendance is recorded.
*   **Dynamic Face Loading**: Automatically learns faces from image files placed in the `images` directory.
*   **Visual & Audio Feedback**: Displays a bounding box around detected faces (green for known, red for unknown) and plays a sound notification upon successful attendance marking.

## How It Works

The system operates through the `program.py` script, which performs the following steps:

1.  **Load Known Faces**: On startup, the script scans the `images/` directory. It loads each image (`.jpg`, `.jpeg`, `.png`, `.webp`) and creates a face encoding. The filename (without the extension) is used as the person's name.
2.  **Initialize Webcam**: It starts capturing video from the default webcam.
3.  **Create/Open Log File**: It checks for or creates a CSV file named with the current date (e.g., `2025-10-20.csv`). It reads existing entries to avoid re-marking attendance.
4.  **Detect and Compare**: In a continuous loop, the script grabs a frame from the webcam, resizes it for faster processing, and detects all faces in it.
5.  **Mark Attendance**: For each detected face, it compares the face encoding against the known encodings. If a match is found and the person has not yet been marked for the day:
    *   The person's name, current time, and a local file path to a new snapshot are written to the daily CSV file.
    *   A snapshot of the face is saved to the `snapshots/` directory.
    *   An audio notification confirms that attendance has been recorded.
6.  **Display Output**: The webcam feed is displayed in a window titled "Attendance System". Bounding boxes are drawn around faces with their names.

## File Structure

```
.
├── program.py              # Main application script
├── images/                 # Directory for storing known face images
│   ├── brad.webp
│   ├── pavi.JPG
│   └── ...
├── snapshots/              # Directory where face snapshots are saved
└── YYYY-MM-DD.csv          # Attendance log files, created daily
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/pavi040315/face-detection-attendance-project.git
    cd face-detection-attendance-project
    ```

2.  **Install dependencies:**
    This project requires Python and the following libraries. You can install them using pip:
    ```bash
    pip install opencv-python face_recognition numpy
    ```
    **Note:** The `winsound` library is used for audio notifications and is available by default on Windows. For other operating systems, you may need to modify or remove the audio feedback code.

## How to Use

1.  **Add Known Faces**: Place image files of the individuals you want to recognize into the `images/` directory. Supported formats are `.jpg`, `.jpeg`, `.png`, and `.webp`. The name of the file (e.g., `pavi.JPG`) will be used as the person's name ("pavi").

2.  **Run the script**:
    ```bash
    python program.py
    ```

3.  **Operation**:
    *   A window will open showing the live feed from your webcam.
    *   Position a known person's face in front of the camera. The system will recognize them and mark their attendance.
    *   The attendance will be logged in `YYYY-MM-DD.csv`.

4.  **Quit the application**:
    *   Press the 'q' key while the webcam window is active to stop the program.
