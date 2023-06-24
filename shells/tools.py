import cv2
import numpy as np


def plot_bboxes(image, bboxes, vol_thresh, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(
        0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # line/font thickness
    list_pts = []
    point_radius = 4

    for (x1, y1, x2, y2, cls_id, pos_id, speed) in bboxes:
        # if cls_id in ['car', 'bus', 'truck']:
        #    color = (0, 0, 255)
        # else:
        #    color = (0, 255, 255)
        color = (0, 0, 255)

        # check whether hit line
        check_point_x = x1
        check_point_y = int(y1 + ((y2 - y1) * 0.6))

        c1, c2 = (x1, y1), (x2, y2)
        tf = max(tl - 1, 1)  # font thickness
        if speed <= vol_thresh:
            cv2.rectangle(image, c1, c2, [0, 255, 255], thickness=tl, lineType=cv2.LINE_AA)
            # cv2.putText(image, '{}'.format(pos_id), (c1[0], c1[1] - 2), 0, tl / 3,
                        # [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
        else:
            cv2.rectangle(image, c1, c2, [0, 0, 255], thickness=tl, lineType=cv2.LINE_AA)
            cv2.putText(image, 'speeding'.format(pos_id), (c1[0], c1[1] - 2), 0, tl / 3,
                        [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
        if speed and y2 < 520:
            cv2.putText(image, 'speed:{}km/h'.format(speed), (c1[0], c1[1] + y2 - y1), 0, tl / 6,
                        [0, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

        list_pts.append([check_point_x - point_radius, check_point_y - point_radius])
        list_pts.append([check_point_x - point_radius, check_point_y + point_radius])
        list_pts.append([check_point_x + point_radius, check_point_y + point_radius])
        list_pts.append([check_point_x + point_radius, check_point_y - point_radius])

        ndarray_pts = np.array(list_pts, np.int32)
        cv2.fillPoly(image, [ndarray_pts], color=(0, 0, 255))
        list_pts.clear()
    return image