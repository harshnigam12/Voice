# 🍎 Real-Time Object Detection and World Coordinate Estimation using YOLOv8 and ArUco Markers

A complete computer vision pipeline for **real-time object detection** and **world coordinate estimation** using **YOLOv8**, **camera calibration**, and **ArUco marker-based pose estimation**.

The project detects objects from a webcam, determines the center of the detected object, and converts its pixel coordinates into real-world coordinates, making it suitable for robotics and autonomous pick-and-place applications.

---

# 📖 Project Overview

This project integrates multiple computer vision techniques into a single pipeline.

The workflow consists of:

- Camera Calibration
- YOLOv8 Object Detection
- ArUco Marker Pose Estimation
- Pixel-to-World Coordinate Conversion
- Real-Time Webcam Detection

The estimated world coordinates can be directly used for robotic arm applications and autonomous object manipulation.

---

# ✨ Features

- Custom YOLOv8 object detector
- Camera calibration using chessboard images
- ArUco marker pose estimation
- Pixel-to-world coordinate transformation
- Real-time webcam detection
- Real-world coordinate estimation
- Modular project structure
- Easily extendable for robotic arm applications

---

# 🛠 Technologies Used

| Category | Technology |
|-----------|------------|
| Language | Python |
| Object Detection | YOLOv8 |
| Computer Vision | OpenCV |
| Numerical Computing | NumPy |
| Visualization | Matplotlib |
| Annotation Format | Pascal VOC XML |
| IDE | Visual Studio Code |

---

# 📂 Project Structure

```text
Fruit_Detection_3D_Localization

│
├── dataset/
├── images/
├── models/
│     └── best.pt
│
├── test_data/
├── train_data/
│
├── vision/
│     ├── aruco/
│     ├── calibration/
│     └── utils/
│
├── inference.py
├── main.py
├── webcam.py
├── train.py
├── data.yaml
├── requirements.txt
└── README.md
```

---

---

# 🔄 System Pipeline

```text
Camera
   │
   ▼
Image Acquisition
   │
   ▼
YOLOv8 Object Detection
   │
   ▼
Bounding Box Center Extraction
   │
   ▼
Camera Calibration
   │
   ▼
ArUco Marker Pose Estimation
   │
   ▼
Pixel-to-World Coordinate Transformation
   │
   ▼
Real-World Coordinates (X, Y, Z)
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Fruit_Detection_3D_Localization.git
```

## 2. Move into the project directory

```bash
cd Fruit_Detection_3D_Localization
```

## 3. Create a virtual environment

```bash
python -m venv venv
```

## 4. Activate the virtual environment

### Windows

```bash
.\venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 5. Install the dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ How to Run

## 1. Camera Calibration

Capture chessboard images:

```bash
python vision/calibration/capture_images.py
```

Calibrate the camera:

```bash
python vision/calibration/calibrate.py
```

---

## 2. Train the YOLOv8 Model

```bash
python train.py
```

---

## 3. Test on an Image

```bash
python inference.py
```

---

## 4. Real-Time Webcam Detection

```bash
python webcam.py
```

---

## 5. Estimate World Coordinates

```bash
python main.py
```

---

# 📸 Results

## Camera Calibration

![Camera Calibration](results/calibration.png)

---

## Object Detection

![Object Detection](results/apple_detection.png)

---

## World Coordinate Estimation

![World Coordinates](results/world_coordinates.png)

---

# 🚀 Future Improvements

- Multi-object localization
- Robotic arm pick-and-place integration
- Raspberry Pi deployment
- ROS2 integration
- Depth camera support
- TensorRT optimization

---

# 👨‍💻 Author

**Vidhi Rajput**

B.Tech in Electronics and Communication Engineering

### Areas of Interest

- Computer Vision
- Robotics
- Machine Learning
- Artificial Intelligence

If you found this project helpful, consider giving it a ⭐ on GitHub.