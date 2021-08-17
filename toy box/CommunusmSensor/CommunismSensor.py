import cv2
import numpy as np
import pygame as pg
    
def RedCapture():
    
    #変数初期化
    flag_detected = 0    
    most_large_area = 0
    most_large_area_x = 0
    most_large_area_y = 0
    most_large_area_w = 0
    most_large_area_h = 0
    window_name = 'frame'
    global g_area

    #フレームを取得
    ret, frame = cap.read()

    #フレームをBGRからHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #取得する色の範囲を指定する
    lower = np.array([0, 70, 70])
    upper = np.array([20, 255, 255])

    #指定した色に基づいたマスク画像の生成
    img_mask = cv2.inRange(hsv, lower, upper)

    #輪郭抽出
    contours, hierarchy = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #抽出したすべての輪郭から、条件に合うものを一つ取り出す
    for i in range(0, len(contours)):

        #輪郭の領域
        area = cv2.contourArea(contours[i])

        #ノイズ除去（大きすぎたり小さすぎたりする領域の輪郭は除去）
        
        if area < 2e3 or area > 1e5:
            continue

        #条件に合う輪郭が一つでも見つかればフラグを立てる
        flag_detected = 1

        #外接矩形の座標算出（輪郭が存在するとき）
        if len(contours[i]) > 0:
            rect = contours[i]
            x, y, w, h = cv2.boundingRect(rect)
            area = w * h #矩形の面積を算出
            #print(contours[i])

            #前回に比べて面積が増えたときに更新
            if area > most_large_area:
                most_large_area = area
                most_large_area_x = x
                most_large_area_y = y
                most_large_area_w = w
                most_large_area_h = h

    g_area = most_large_area
    
    if flag_detected:
        #最大面積の短形を描画
        cv2.rectangle(frame, (most_large_area_x, most_large_area_y), (most_large_area_x + most_large_area_w, most_large_area_y + most_large_area_h), 3)
        
    cv2.imshow(window_name, img_mask)
    cv2.imshow(window_name, frame)
    

def music_init():
    pg.mixer.init(frequency = 22050)
    pg.mixer.music.load("USSR_Anthem.mp3")

def main():
    global g_area
    std_lower = 1e3
    #std_upper = 1e6
    flag = True
    
    music_init()
   
    while(cap.isOpened()):

        RedCapture()

        if g_area > std_lower:
            if flag:
                pg.mixer.music.play(-1)
            flag = False
        else:
            if not flag:
                pg.mixer.music.stop()
            flag = True
        
        #qを押したら終了
        k = cv2.waitKey(1) #delayは1
        if k == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            pg.mixer.music.stop()
            break

'''
ここからメインプログラム
'''

#↓インポートした時に実行しない
if __name__ == "__main__":
    cam_id = 1 #カメラIDによって変更（PC内蔵カメラ：0, USBカメラ：接続順に1,2,3...）
    cap = cv2.VideoCapture(cam_id)
    cap.set(cv2.CAP_PROP_FPS, 10)
    main()
