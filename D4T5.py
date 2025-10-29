import random, pathlib
img_dir = pathlib.Path(__file__).resolve().parent / 'img'
png_files = list(img_dir.glob('*.png'))
to_rename = random.sample(png_files, k=min(50, len(png_files)))
for old_path in to_rename:
    new_path = old_path.with_suffix('.jpg')
    old_path.rename(new_path)