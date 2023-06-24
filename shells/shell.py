import torch

from shells.deepsortor import Deepsortor
from shells.detector import Detector
from shells import tools
import math


class Shell(object):
    def __init__(self, deepsort_config_path, yolo_weight_path):
        self.deepsortor = Deepsortor(configFile=deepsort_config_path)
        self.detector = Detector(yolo_weight_path, imgSize=640, threshould=0.3, stride=1)
        self.frameCounter = 0
        self.last_bbox = []

    def update(self, im, vol_thresh):
        retDict = {
            'frame': None,
            'list_of_ids': None,
            'obj_bboxes': []
        }

        self.frameCounter += 1

        # yolov5
        _, bboxes = self.detector.detect(im)
        bbox_xywh = []
        confs = []

        if len(bboxes):
            # Adapt detections to deep sort input format
            for x1, y1, x2, y2, _, conf in bboxes:
                obj = [
                    int((x1 + x2) / 2), int((y1 + y2) / 2),
                    x2 - x1, y2 - y1
                ]
                bbox_xywh.append(obj)
                confs.append(conf)
            xywhs = torch.Tensor(bbox_xywh)
            confss = torch.Tensor(confs)

            im, obj_bboxes = self.deepsortor.update(xywhs, confss, im)

            if self.last_bbox:
                for i in range(0, len(self.last_bbox)):
                    for j in range(0, len(obj_bboxes)):
                        if self.last_bbox[i][5] == obj_bboxes[j][5]:
                            x1 = (self.last_bbox[i][0] + self.last_bbox[i][2]) / 2
                            y1 = (self.last_bbox[i][1] + self.last_bbox[i][3]) / 2
                            x2 = (obj_bboxes[j][0] + obj_bboxes[j][2]) / 2
                            y2 = (obj_bboxes[j][1] + obj_bboxes[j][3]) / 2
                            d = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
                            speed = d*108*(80/960-96*y2/960/540)
                            obj_bboxes[j].append(round(speed, 0))
                for i in range(0, len(obj_bboxes)):
                    if len(obj_bboxes[i]) == 6:
                        obj_bboxes[i].append(0)
            else:
                for i in range(0, len(obj_bboxes)):
                    obj_bboxes[i].append(0)
            self.last_bbox = obj_bboxes[:]
            # 绘制 deepsort 结果
            image = tools.plot_bboxes(im, obj_bboxes, vol_thresh)

            retDict['frame'] = image
            retDict['obj_bboxes'] = obj_bboxes

        return retDict
