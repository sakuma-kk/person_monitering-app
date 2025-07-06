# detector.py
import cv2
import time
from notifier import send_discord_notify
from my_utils import draw_boxes
from face_checker import FaceChecker


def run_detection(model):
    print("映像チェック開始")
    # 内臓カメラを使用
    cap = cv2.VideoCapture(0)
    # カメラが開けなかった場合
    if not cap.isOpened():
        print("カメラが見つからりません。")
        return

    print("カメラ初期化OK")
    # アプリ開始を通知
    send_discord_notify("起動開始")

    # 顔チェックの初期化
    face_checker = FaceChecker()
    last_face_check_time = time.time()
    face_check_interval = 5  # 顔チェックの間隔(秒)

    # 初期化
    prev_count = 0
    notified = False
    last_check_time = time.time()

    interval = 90  # インターバル時間はここで設定(分単位)
    start_delay = 10  # 開始からの無通知時間(秒)


    send_discord_notify(f"インターバル: {interval}s / 無通知時間: {start_delay}s")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("フレーム取得失敗")
                break

            now = time.time()

            # 顔認証による自動終了
            # 一定時間ごとに顔認証を行う
            if now - last_face_check_time >= face_check_interval:
                if face_checker.is_user_present(frame):
                    print("顔が検出されました")
                    send_discord_notify("顔認識:アプリ使用者を確認。アプリケーションを終了します.")
                    break
                last_face_check_time = now # 顔チェックの時間を更新

            # YOLOv8での人数検出
            results = model(frame[..., ::-1])
            detections = results.pandas().xyxy[0]
            person_count = len(detections[detections['name'] == 'person']) # 人だけをカウント


            # 起動直後の遅延処理
            if now - last_check_time < start_delay: 
                person_count = 0
            elif not notified:
                send_discord_notify(f"監視を開始.現在の人数：{person_count}人.")
                notified = True
            

            # インターバルによる人数通知
            if now - last_check_time >= interval:
                print(f"現在の人数: {person_count}人")
                if person_count != prev_count:
                    send_discord_notify(f"人数の変化を検知：{prev_count}人 → {person_count}人.")
                    prev_count = person_count
                else:
                    send_discord_notify(f"人数変化なし：{person_count}人.")
                last_check_time = now

            # デバッグ用表示処理
            draw_boxes(frame, detections)
            cv2.imshow('監視カメラ', frame)

            # 終了条件
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("手動終了")
                break
    
    finally:
        # 後処理(アプリ終了を通知)
        cap.release()
        cv2.destroyAllWindows()
        send_discord_notify("監視終了")
