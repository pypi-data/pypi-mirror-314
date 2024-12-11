def convert_yolo_bbox(
    data_key: str, annotations: list, classes: list, width: int, height: int
):
    converted_annotations = []
    for anno in annotations:
        class_number, x_norm, y_norm, w_norm, h_norm = (
            anno[0],
            anno[1],
            anno[2],
            anno[3],
            anno[4],
        )
        class_name = classes[int(class_number)]
        # Check normalization
        if any(value > 1 for value in (x_norm, y_norm, w_norm, h_norm)):
            print(
                f"[WARNING] [Invalid zip file] {data_key}.txt\n"
                + f"[[Class index] [x_center] [y_center] [width] [height]]: [{int(class_number)} {x_norm} {y_norm} {w_norm} {h_norm}]\n"
                + f" YOLO format coordinates, width, and height must be normalized (0 - 1)."
            )
            return []

        w = w_norm * width
        h = h_norm * height
        x = x_norm * width - w / 2
        y = y_norm * height - h / 2
        converted_annotations.append([class_name, [x, y, w, h]])

    return converted_annotations
