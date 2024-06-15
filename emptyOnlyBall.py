from ultralytics import YOLO
import cv2

# モデル読み込み
model = YOLO(R"/Users/hiratasoma/happyPython/yolov8x.pt")

# カメラ読み込み
cap = cv2.VideoCapture(2)

while True:
    # カメラから1フレーム読み込み
    ret, frame = cap.read()

    # YOLOv8で物体検出
    results = model.predict(frame,task='segment', show=True)

    # 結果を表示
    for result in results:
        for xyxy in result.boxes.xyxy:
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 0, 255), 2)
            num_objects = len(results[0])
            cv2.putText(frame,
                str(num_objects),
                org=(15
                     ,20),
                fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                fontScale=1.0,
                color=(0,255,0),
                thickness=2,
                lineType=cv2.LINE_4
            )
    cv2.imshow('frame', frame)

    if cv2.waitKey(10) == ord('s'):
        cv2.imwrite(R"C:\Users\hirat\Documents\OpenCV\Picture\camera_binary.bmp", frame)
    # qキーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 後処理
cap.release()
cv2.destroyAllWindows()
