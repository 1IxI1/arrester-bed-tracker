# Write a graph of center's x corrdinate over time
# All videos are recorded at ~120 fps
import matplotlib.pyplot as plt


PIXELS_PER_CM = 1060 / 18  # scaling
ZERO_POINT_PX = 1700  # cylinder moving left, so x is decreasing
FRAME_TIME = 1 / 119  # 119 fps
plt.style.use('Solarize_Light2')


def build_x_graph(centers: list[tuple[int, int]],
                  filename: str | None = None) -> None:
    xs = []
    ys = []
    time = 0
    for cordinate_x, _ in centers:
        distance_cm = (ZERO_POINT_PX - float(cordinate_x)) / PIXELS_PER_CM
        ys.append(distance_cm)
        xs.append(time)
        time += FRAME_TIME

    plt.plot(xs, ys, marker='o', markersize=4)
    plt.xlabel('Time (s)')
    plt.ylabel('Distance from null point by X (cm)')

    if filename:
        plt.savefig(filename, dpi=250)
    else:
        plt.show()


if __name__ == '__main__':
    centers = []
    with open('out/centers/8_215.mp4.txt', 'r') as f:
        for line in f.readlines():
            centers.append(line.split())
    build_x_graph(centers)
