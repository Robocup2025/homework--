
import cv2, numpy as np, matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

OUT_DIR = Path("output") / datetime.now().strftime("%m%d_%H%M%S")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------- 工具 ----------
def gaussian_kernel_2d(k: int, s: float):
    if k % 2 == 0:
        raise ValueError("k 必须为奇数")
    h = k // 2
    x, y = np.mgrid[-h : h + 1, -h : h + 1]
    g = np.exp(-(x ** 2 + y ** 2) / (2 * s ** 2))
    return g / g.sum()

def convolve_color(img_bgr, kernel, pad_mode):
    kh, kw = kernel.shape
    pad = kh // 2
    if pad_mode == "zero":
        p = np.pad(img_bgr, ((pad, pad), (pad, pad), (0, 0)), "constant")
    elif pad_mode == "reflect":
        p = np.pad(img_bgr, ((pad, pad), (pad, pad), (0, 0)), "reflect")
    else:
        raise ValueError(pad_mode)
    h, w, c = img_bgr.shape
    out = np.zeros_like(img_bgr, np.float32)
    for ch in range(c):
        for i in range(h):
            for j in range(w):
                out[i, j, ch] = (p[i : i + kh, j : j + kw, ch] * kernel).sum()
    return np.clip(out, 0, 255).astype(np.uint8)

# ---------- 2. 核对比 ----------
def demo_kernel():
    params = [(3, 0.8), (5, 1.0), (7, 2.0)]
    fig, ax = plt.subplots(len(params), 3, figsize=(9, 3 * len(params)))
    if len(params) == 1:
        ax = ax[np.newaxis, :]
    for idx, (k, s) in enumerate(params):
        hand = gaussian_kernel_2d(k, s)
        cv2d = cv2.getGaussianKernel(k, s) @ cv2.getGaussianKernel(k, s).T
        diff = np.abs(hand - cv2d)
        ax[idx, 0].imshow(hand, cmap="gray"); ax[idx, 0].set_title(f"hand k={k} σ={s}")
        ax[idx, 1].imshow(cv2d, cmap="gray"); ax[idx, 1].set_title(f"opencv k={k} σ={s}")
        ax[idx, 2].imshow(diff, cmap="gray"); ax[idx, 2].set_title(f"diff max={diff.max():.4f}")
    for a in ax.ravel():
        a.axis("off")
    fig.tight_layout()
    fn = OUT_DIR / "02_kernel_compare.png"
    fig.savefig(fn, dpi=150)
    print(f" saved  {fn}")

# ---------- 3. 彩色模糊 ----------
def demo_blur(img):
    params = [(3, 0.8), (7, 2.0), (15, 5.0)]
    for k, s in params:
        kernel = gaussian_kernel_2d(k, s)
        out = convolve_color(img, kernel, "reflect")
        fn = OUT_DIR / f"03_blur_k{k}-σ{s}_reflect_color.png"
        cv2.imwrite(str(fn), out)
        print(f" saved  {fn}")

# ---------- 4. 彩色 padding ----------
def demo_pad(img):
    pad = 60
    zero = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), "constant")
    ref = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), "reflect")
    for name, im in [("zero", zero), ("reflect", ref)]:
        fn = OUT_DIR / f"04_pad-{name}_color.png"
        cv2.imwrite(str(fn), im)
        print(f" saved  {fn}")

# ---------- main ----------
if __name__ == "__main__":
    img = cv2.imread("test.jpg")
    if img is None:
        raise FileNotFoundError("test.jpg not found")
    print("output dir:", OUT_DIR)
    demo_kernel()
    demo_blur(img)
    demo_pad(img)
    print("全部完成！")