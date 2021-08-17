import cv2
import numpy as np

window_name = 'test'
large_img = cv2.imread('Gorira.jpg')
small_img = cv2.imread('vivi.jpg')

h, w = small_img.shape[:2]
size = (w, h)
'''
trans2 = cv2.getRotationMatrix2D((int(0.5*small_img.shape[1]),int(0.5*small_img.shape[0])), 45 , scale)
rot_small_img2 = cv2.warpAffine(small_img, trans2, (int(1*small_img.shape[1]),int(1*small_img.shape[0])))
'''
#print(small_img[100][100])

#回転角の指定
angle = 60
angle_rad = angle/180.0*np.pi

# 回転後の画像サイズを計算
w_rot = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
h_rot = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
size_rot = (w_rot, h_rot)

# 元画像の中心を軸に回転する
center_s = (w/2, h/2)
scale = 1
rotation_matrix = cv2.getRotationMatrix2D(center_s, angle, scale)

# 平行移動を加える (rotation + translation)
affine_matrix = rotation_matrix.copy()
affine_matrix[0][2] = affine_matrix[0][2] - w/2 + w_rot/2
affine_matrix[1][2] = affine_matrix[1][2] - h/2 + h_rot/2

rot_small_img = cv2.warpAffine(small_img, affine_matrix, size_rot, flags=cv2.INTER_CUBIC)
print(rot_small_img.shape)
dst_img = large_img
print(dst_img.shape)
rh, rw = rot_small_img.shape[0], rot_small_img.shape[1]
print(rw, rh)
#dst_img[int(48 - (rw/2)) : int(48 + (rw/2)), int(593 - (rh/2)) : int(593 + (rh/2))] = rot_small_img
print((48 + rw) - 48, (593 + rh) -593)
print(dst_img[48 : (48 + 552), 400: (400 + 596)].shape)

dst_img[48 : (48 + rw), 593: (593 + rh)] = rot_small_img


cv2.namedWindow('original', cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
while(1):
    cv2.imshow('original', small_img)
    cv2.imshow(window_name, rot_small_img)
    k = cv2.waitKey(1) #delayは1
    if k == ord('q'):
        cv2.destroyAllWindows()
        break
