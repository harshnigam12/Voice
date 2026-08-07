"""

Robot Configuration File

Contains:
1. Link lengths
2. Servo offsets
3. Servo limits
4. Home position
5. Handover position
6. Gripper settings


"""

# ======================================================
# LINK LENGTHS (millimeters)
# ======================================================

BASE_HEIGHT = 85

UPPER_ARM = 130      # Shoulder → Elbow

FOREARM = 150      # Elbow → Wrist

WRIST = 100      # Wrist → Gripper


# ======================================================
# HOME POSITION
# ======================================================

HOME_POSITION = {

    "base": 90,

    "shoulder": 90,

    "elbow": 90,

    "wrist": 90,

    "gripper": 20

}


# ======================================================
# USER HANDOVER POSITION
# ======================================================

# Relative to robot base

HANDOVER_POSITION = (

250,     # X (mm)

180,     # Y (mm)

120      # Z (mm)

)


# ======================================================
# GRIPPER
# ======================================================

GRIPPER_OPEN = 20

GRIPPER_CLOSE = 70


# ======================================================
# SERVO OFFSETS
# Used after calibration
# ======================================================

BASE_OFFSET = 0

SHOULDER_OFFSET = 0

ELBOW_OFFSET = 0

WRIST_OFFSET = 0

GRIPPER_OFFSET = 0


# ======================================================
# SERVO LIMITS
# ======================================================

BASE_MIN = 0
BASE_MAX = 180

SHOULDER_MIN = 15
SHOULDER_MAX = 165

ELBOW_MIN = 0
ELBOW_MAX = 180

WRIST_MIN = 0
WRIST_MAX = 180

GRIPPER_MIN = 10
GRIPPER_MAX = 80


# ======================================================
# CAMERA
# ======================================================

CAMERA_INDEX = 1

FRAME_WIDTH = 640

FRAME_HEIGHT = 480


# ======================================================
# SERIAL COMMUNICATION
# ======================================================

SERIAL_PORT = "COM3"

BAUDRATE = 115200


# ======================================================
# YOLO MODEL
# ======================================================

MODEL_PATH = "models/best.pt"


# ======================================================
# DETECTION
# ======================================================

CONFIDENCE_THRESHOLD = 0.25


# ======================================================
# ROBOT SPEED
# ======================================================

SERVO_DELAY = 10        # milliseconds

MOVE_DELAY = 1.5        # seconds


# ======================================================
# VOICE COMMANDS
# ======================================================

VOICE_COMMANDS = [

    "pick fruit",

    "home",

    "stop",

    "release"

]