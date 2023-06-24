import os
from shells.shell import Shell
import imutils
import cv2
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# VIDEO_PATH = './video/traffic.mp4'
# VIDEO_PATH = './video/pedestrian.mp4'
# RESULT_PATH = './out/result.mp4'

DEEPSORT_CONFIG_PATH = "./deep_sort/configs/deep_sort.yaml"
YOLOV5_WEIGHT_PATH = './weights/best.pt'


def detect(VIDEO_PATH, RESULT_PATH, VOL_THRESH):
    det = Shell(DEEPSORT_CONFIG_PATH, YOLOV5_WEIGHT_PATH)
    videoWriter = None
    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = int(cap.get(5))
    t = int(1000/fps)
    obj_number = 0
    while True:
        _, frame = cap.read()
        if not _ :
            break
        
        result = det.update(frame, VOL_THRESH)

        pos = result['obj_bboxes']
        result = result['frame']
        if len(pos) != 0:
            obj_number = max(obj_number, pos.pop()[5])

        if result is None:
            break
        result = imutils.resize(result, height=500)
        if videoWriter is None:
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # opencv3.0
            videoWriter = cv2.VideoWriter(RESULT_PATH, fourcc, fps, (result.shape[1], result.shape[0]))
        videoWriter.write(result)

        cv2.imshow("frame", result)
        key = cv2.waitKey(t)
        if key == ord('q'): break

    sec = det.frameCounter / fps
    cv2.destroyAllWindows()
    videoWriter.release()
    cap.release()
    return obj_number, sec


if __name__ == "__main__":
    num, s = detect('./video/MVI_40963.mp4', './video/MVI_40963_result.mp4', 60)
    print(num)