from pdf2image import convert_from_path
import os

pdf_path = 'pdf_files/MX-C3582R_20070505_214441.pdf'
path = './jpg_files'

images = convert_from_path(pdf_path, dpi=800)

if not os.path.exists(path):
    os.makedirs(path)
# save images as jpegs.
for i, image in enumerate(images):
    image.save(f'{path}/{pdf_path.split("/")[-1].split(".")[0]}_page_{i}.jpg', 'JPEG')