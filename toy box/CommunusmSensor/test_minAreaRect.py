#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:51:44 2020

@author: yuki_enomoto
"""

import numpy as np
import cv2

'''
cam_id = 0
cap = cv2.VideoCapture(cam_id)
cap.set(cv2.CAP_PROP_FPS, 10)
'''
window_name = 'test'

large_img = cv2.imread('Gorira.jpg')
dst_img = large_img
small_img = cv2.imread('vivi.jpg')
#small_img = cv2.resize(small_img , (int(small_img.shape[0]*0.5), int(small_img.shape[1]*0.5)))
h, w = small_img.shape[:2]
size = (w, h)

#フレームを取得
frame = large_img

#フレームをBGRからHSVに変換
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#取得する色の範囲を指定する
lower = np.array([0, 0, 0])
upper = np.array([255, 255, 50])

#指定した色に基づいたマスク画像の生成
img_mask = cv2.inRange(hsv, lower, upper)

#輪郭抽出
contours, hierarchy = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#抽出したすべての輪郭から、条件に合うものを一つ取り出す
for i in range(0, len(contours)):
    
    flag_detected = 0

    #輪郭の領域面積
    area = cv2.contourArea(contours[i])

    #ノイズ除去（大きすぎたり小さすぎたりする領域の輪郭は除去）
    
    if area < 2e3 or area > 1e5:
        continue
    
    
    #条件に合う輪郭が一つでも見つかればフラグを立てる
    flag_detected = 1

    #外接矩形の座標算出（輪郭が存在するとき）
    if len(contours[i]) > 0:
        
        rect = cv2.minAreaRect(contours[i])
        center = np.int0(rect[0][0]), np.int0(rect[0][1])
        size = np.int0(rect[1])
        width, height = np.int0(size[0]), np.int0(size[1])
        angle = np.int0(rect[2])
        cache = 0
        #print('rect')
        #print(rect) #((x,y), (w,h), angle)
        #print(len(rect)) #3
        box = cv2.boxPoints(rect)
        #print('box')
        #print(box)
        box = np.int0(box)
        
        if angle > -45:
            angle += 90
            
            cache = width
            width = height
            height = cache

        #合成画像を最小外接矩形に合わせてresize
        small_img = cv2.resize(small_img, (width, height))
        #print(type(center), type(angle), type(scale))

        #回転角の指定
        angle_rad = angle/180.0*np.pi

        # 回転後の画像サイズを計算
        w_rot = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
        h_rot = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
        size_rot = (w_rot, h_rot)

        # 元画像の中心を軸に回転する
        center_s = (w/2, h/2)
        scale = 1.0
        rotation_matrix = cv2.getRotationMatrix2D(center_s, angle, scale)

        # 平行移動を加える (rotation + translation)
        affine_matrix = rotation_matrix.copy()
        affine_matrix[0][2] = affine_matrix[0][2] -w/2 + w_rot/2
        affine_matrix[1][2] = affine_matrix[1][2] -h/2 + h_rot/2

        rot_small_img = cv2.warpAffine(small_img, affine_matrix, size_rot, flags=cv2.INTER_CUBIC)
        dst_img = large_img

        print(w, h)
        print(center[0], center[1])
        print(large_img.shape)
        print(rot_small_img.shape)
        '''
        dst_img = large_img
        for  x in range(w):
            for y in range(h):
                x2, y2 = (x + center[0] - (w/2) , y + center[1] - (h/2))
                print(x2, y2)
                b, g, r = rot_small_img[x, y]
                if not (0<=b<=0 and 0<=g<=0 and 0<=r<=0):
                    dst_img[x2, y2] = rot_small_img[x, y]
        
        #print(box[i][0], box[i][1])
        #offset_x, offset_y = box[i][0], box[i][1]
        #print(small_img.shape[0], small_img.shape[1])
        '''
        dst_img[int(center[0] - (w/2)) : int(center[0] + (w/2)), int(center[1] - (h/2)) : int(center[1] + (h/2))] = rot_small_img
        
    #if flag_detected:
        #frame = cv2.drawContours(frame,[box],0, (0, 0, 255), 2)
        #frame[offset_y:offset_y+small_img.shape[0], offset_x:offset_x+small_img.shape[1]] = small_img
        
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
while(1):
    cv2.imshow(window_name, dst_img)
    k = cv2.waitKey(1) #delayは1
    if k == ord('q'):
        cv2.destroyAllWindows()
        break
