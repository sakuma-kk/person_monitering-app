# my_utils.py
import cv2

def draw_boxes(frame, detections):
    for _, det in detections.iterrows():
        if det['name'] == 'person':
            x1, y1, x2, y2 = map(int, [det['xmin'], det['ymin'], det['xmax'], det['ymax']])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame

def should_start_monitoring():
    # 仮でTrue、後にGUIボタンで切り替え可能
    return True
