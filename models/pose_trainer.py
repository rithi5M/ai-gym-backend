import cv2
import numpy as np
import mediapipe as mp
from typing import Dict

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a); b = np.array(b); c = np.array(c)
    ba = a - b; bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba)*np.linalg.norm(bc) + 1e-8)
    angle = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))
    return angle

def analyze_squat(image_bytes: bytes) -> Dict:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            return {"detected": False, "message": "No person detected."}

        h, w, _ = img.shape
        lm = results.pose_landmarks.landmark

        def get_point(i): return [lm[i].x * w, lm[i].y * h]

        hip = get_point(mp_pose.PoseLandmark.RIGHT_HIP.value)
        knee = get_point(mp_pose.PoseLandmark.RIGHT_KNEE.value)
        ankle = get_point(mp_pose.PoseLandmark.RIGHT_ANKLE.value)

        angle = calculate_angle(hip, knee, ankle)

        if angle < 80:
            fb = "Good squat depth!"
        elif angle < 140:
            fb = "Try going lower."
        else:
            fb = "Bend your knees more."

        return {
            "detected": True,
            "exercise": "squat",
            "knee_angle": round(angle, 2),
            "feedback": fb
        }
