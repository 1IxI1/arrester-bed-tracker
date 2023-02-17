FRAME_TIME = 1 / 119  # 119 fps
PIXELS_PER_CM = 1060 / 18  # scaling
ZERO_POINT_PX = 1700  # cylinder moving left, so x is decreasing


def format_file_to_csv(in_fn: str, out_fn: str | None = None):
    with open(in_fn, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            x = line.split()[0]
            x_cm = (ZERO_POINT_PX - int(x)) / PIXELS_PER_CM
            lines[i] = str(i * FRAME_TIME) + ',' + str(x_cm)

    out_fn = out_fn or in_fn.replace('.txt', '.csv').replace('centers', 'csv')

    with open(out_fn, 'w') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    format_file_to_csv(f'out/centers/2_50.mp4.txt')
