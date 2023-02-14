# IYPT 2022/23 Problem #17 Arrester Bed.
# Tracker for the centers of moving objects with
# writing the results into a file and building a chart.
#
# Made by @topIXItop 14.02.2023 for BNTU Lyceum team.
# Under the GNU General Public License v3.0

import cv2
import ox_graph


filename = 'src_vids/new/big/8_215.mp4'
out_centers = 'out/centers/' + filename.split('/')[-1] + '.txt'
out_graph = 'out/graphs/' + filename.split('/')[-1] + '.png'

cap = cv2.VideoCapture(filename)
fps = cap.get(cv2.CAP_PROP_FPS)

_, img = cap.read()

try:
    with open(filename + '.bbox.txt', 'r'):
        bbox = [int(x) for x in open(
            filename + '.bbox.txt', 'r').read().split()]
        print('Using bbox from file', filename + '.bbox.txt')
except FileNotFoundError:
    bbox = cv2.selectROI('Tracking', img)
    with open(filename + '.bbox.txt', 'w') as f:
        f.write(' '.join([str(x) for x in bbox]))
        print('Saved bbox to file', filename + '.bbox.txt')

tracker = cv2.legacy.TrackerBoosting_create()
tracker.init(img, bbox)

centers = []
while True:
    suc, frame = cap.read()
    try:
        height, width, _ = frame.shape
    except AttributeError:
        break

    suc, bbox = tracker.update(frame)

    if suc:
        x, y, w, h = [int(x) for x in bbox]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
        center = (x + w // 2, y + h // 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        # If the cylinder has stopped and his position is not changing
        # then don't add it to the list for the graph
        if len(centers) > 3:
            average = sum([x for x, _ in centers[-3:]]) / 3
            if abs(center[0] - average) < 2.7:
                cv2.putText(frame, 'STOPPED', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            else:
                centers.append(center)

        else:
            centers.append(center)

    else:
        cv2.putText(frame, 'Lost', (100, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow('Tracking', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break


with open(out_centers, 'w') as f:
    txt = ''
    for center in centers:
        txt += (' '.join([str(x) for x in center]) + '\n')
    f.write(txt)
    print('Centers saved to', out_centers)

ox_graph.build_x_graph(centers, out_graph)
print('Graph saved to', out_graph)

cap.release()
cv2.destroyAllWindows()
