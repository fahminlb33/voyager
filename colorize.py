import torch

import matplotlib.pyplot as plt

# https://github.com/richzhang/colorization
from voyager_reader.eccv16 import eccv16
from voyager_reader.siggraph17 import siggraph17
from voyager_reader.util import load_img, preprocess_img, postprocess_tens


# create model
print("Loading models")
colorizer_eccv16 = eccv16(pretrained=True).eval()
colorizer_siggraph17 = siggraph17(pretrained=True).eval()

# load the original image
print("Loading image")
input_img = load_img('result/processed.jpg')

# preprocess
print("Preprocessing image")
tens_l_orig, tens_l_rs = preprocess_img(input_img)

# process
eccv16_out = colorizer_eccv16(tens_l_rs).cpu()
siggraph17_out = colorizer_siggraph17(tens_l_rs).cpu()

# post process
img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
out_img_eccv16 = postprocess_tens(tens_l_orig, eccv16_out)
out_img_siggraph17 = postprocess_tens(tens_l_orig, siggraph17_out)

plt.imsave('result/colorized_eccv16.png', out_img_eccv16)
plt.imsave('result/colorized_siggraph17.png', out_img_siggraph17)
