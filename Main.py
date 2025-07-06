# Main.py
import traceback
from yolo_loader import load_model
from detector import run_detection
from my_utils import should_start_monitoring

def main():
    if should_start_monitoring():
        model = load_model()
        run_detection(model)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        traceback.print_exc()
        # エラーログをDiscordに送信するなどの処理を追加できます
        # send_discord_notify(f"エラーが発生しました: {e}")