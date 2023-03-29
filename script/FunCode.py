import cv2
import numpy as np
import random

# 動画作成に必要な情報
fps = 30
frame_size = (1280, 720)
frame_count = 300
font = cv2.FONT_HERSHEY_SIMPLEX
text_size = 2
text_thickness = 3
text_color = (0, 0, 0)
background_color = (255, 255, 255)

# 文字列のリスト
vertical_texts = ["縦書き1", "縦書き2", "縦書き3"]
horizontal_texts = ["横書き1", "横書き2", "横書き3"]

# 動画作成の準備
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter('output.mp4', fourcc, fps, frame_size)

for i in range(frame_count):
    # 白背景の画像を作成
    image = np.zeros((*frame_size, 3), np.uint8)
    image[:, :] = background_color

    # ランダムに縦書き文字を描画
    for j, text in enumerate(vertical_texts):
        text_position = (random.randint(0, frame_size[0] - 1), random.randint(0, frame_size[1] - len(text) * text_size))
        for k, char in enumerate(text):
            char_position = (text_position[0], text_position[1] + k * text_size)
            cv2.putText(image, char, char_position, font, text_size, text_color, text_thickness, cv2.LINE_AA, True)

    # ランダムに横書き文字を描画
    for j, text in enumerate(horizontal_texts):
        text_position = (random.randint(0, frame_size[0] - len(text) * text_size), random.randint(0, frame_size[1] - 1))
        for k, char in enumerate(text):
            char_position = (text_position[0] + k * text_size, text_position[1])
            cv2.putText(image, char, char_position, font, text_size, text_color, text_thickness, cv2.LINE_AA, False)

    # 画面中央Z軸方向に文字を徐々に消していく
    for j in range(frame_size[1]):
        alpha = 1 - j / frame_size[1]
        image = cv2.putText(image, " ", (int(frame_size[0] / 2), int(frame_size[1] / 2) - j), font, text_size, text_color, text_thickness, cv2.LINE_AA, False, alpha)

    # 動画にフレームを追加
    video_writer.write(image)

# 動画を保存して終了
video_writer.release()