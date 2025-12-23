
import os
import cv2
import numpy as np

# ---------- 0. 准备工作 ----------
OUT_DIR = 'homework3_output'
os.makedirs(OUT_DIR, exist_ok=True)
IMG_FILE = 'input.jpg'         

img = cv2.imread(IMG_FILE)
if img is None:
    raise FileNotFoundError('把待处理图片命名为 input.jpg 并放在本脚本同级目录！')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ---------- 1. Sobel 梯度 ----------
gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0)
gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1)
gm = cv2.magnitude(gx, gy)
cv2.imwrite(os.path.join(OUT_DIR, '1_sobel.png'),
            np.uint8(255 * gm / gm.max()))

# ---------- 2. 手动 Canny ----------
blur = cv2.GaussianBlur(gray, (0, 0), 1.0)
mag, ang = cv2.cartToPolar(cv2.Sobel(blur, cv2.CV_32F, 1, 0),
                           cv2.Sobel(blur, cv2.CV_32F, 0, 1),
                           angleInDegrees=True)
# 2-1 梯度幅值
cv2.imwrite(os.path.join(OUT_DIR, '2_gradient_mag.png'),
            np.uint8(255 * mag / mag.max()))

# 2-2 NMS
def nms(mag, ang):
    h, w = mag.shape
    out = np.zeros_like(mag)
    ang[ang < 0] += 180
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            a, m = ang[i, j], mag[i, j]
            if (0 <= a < 22.5) or (157.5 <= a <= 180):
                q, r = mag[i, j + 1], mag[i, j - 1]
            elif 22.5 <= a < 67.5:
                q, r = mag[i + 1, j - 1], mag[i - 1, j + 1]
            elif 67.5 <= a < 112.5:
                q, r = mag[i + 1, j], mag[i - 1, j]
            else:
                q, r = mag[i + 1, j + 1], mag[i - 1, j - 1]
            if m >= q and m >= r:
                out[i, j] = m
    return out

nms_map = nms(mag, ang)
cv2.imwrite(os.path.join(OUT_DIR, '2_nms.png'),
            np.uint8(255 * nms_map / nms_map.max()))

# 2-3 双阈值边缘连接
edges = cv2.Canny(np.uint8(blur), 50, 150)
cv2.imwrite(os.path.join(OUT_DIR, '2_canny_final.png'), edges)

# ---------- 3. 手动 Harris ----------
Ix = cv2.Sobel(blur, cv2.CV_32F, 1, 0)
Iy = cv2.Sobel(blur, cv2.CV_32F, 0, 1)
Ixx, Iyy, Ixy = Ix * Ix, Iy * Iy, Ix * Iy

def harris_response(sigma):
    win = 6 * sigma + 1
    Sxx = cv2.GaussianBlur(Ixx, (win, win), sigma)
    Syy = cv2.GaussianBlur(Iyy, (win, win), sigma)
    Sxy = cv2.GaussianBlur(Ixy, (win, win), sigma)
    det = Sxx * Syy - Sxy * Sxy
    trace = Sxx + Syy
    delta = np.sqrt((Sxx - Syy) ** 2 + 4 * Sxy ** 2)
    lambda1 = 0.5 * (trace + delta)
    lambda2 = 0.5 * (trace - delta)
    return np.minimum(lambda1, lambda2)   # Shi-Tomasi

def nms_local(img, radius=3):
    h, w = img.shape
    out = np.zeros_like(img)
    for i in range(radius, h - radius):
        for j in range(radius, w - radius):
            win = img[i - radius:i + radius + 1, j - radius:j + radius + 1]
            if img[i, j] == win.max() and img[i, j] > 0:
                out[i, j] = img[i, j]
    return out

def draw_top_n(out_name, sigma):
    R = harris_response(sigma)
    thr = 0.01 * R.max()
    R[R < thr] = 0
    cnms = nms_local(R, radius=3)
    ys, xs = np.where(cnms > 0)
    cand = [(cnms[y, x], x, y) for x, y in zip(xs, ys)]
    cand.sort(reverse=True, key=lambda x: x[0])
    keep = []
    N, minDist = 150, 10
    for _, x, y in cand:
        if all((x - kx) ** 2 + (y - ky) ** 2 >= minDist ** 2 for _, kx, ky in keep):
            keep.append((_, x, y))
            if len(keep) == N:
                break
    out_img = img.copy()
    for _, x, y in keep:
        cv2.circle(out_img, (x, y), 3, (0, 0, 255), -1)
    cv2.imwrite(os.path.join(OUT_DIR, out_name), out_img)

draw_top_n('3_harris_fixed.png', sigma=2)
for s in [1, 3, 5]:
    draw_top_n(f'3_harris_win{s}_fixed.png', sigma=s)

# ---------- 4. 手动直方图均衡化 ----------
hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
cdf = hist.cumsum()
lut = np.uint8((cdf - cdf.min()) * 255 / (cdf.max() - cdf.min()))
eq = lut[gray]
cv2.imwrite(os.path.join(OUT_DIR, '4_histeq.png'), eq)

print('全部完成！结果已写入文件夹：', os.path.abspath(OUT_DIR))