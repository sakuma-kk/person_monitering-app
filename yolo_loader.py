# yolo_loader.py
import torch
from pathlib import Path

def load_model():
    # 毎回モデルをダウンロードするのは非効率なので
    # ローカルに保存されているか確認
    # もしなければダウンロードする
    model_path = Path("yolov5n.pt")  # モデルのパス
    if not model_path.exists():
        print("モデルが見つかりません。今からダウンロードします。")
        return

    # YOLOv5のモデルをロード  (精度と速度のバランスが良いyolov5nを使用) 
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
    model.conf = 0.4  # 検出信頼度
    return model
