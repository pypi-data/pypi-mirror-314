
# SPDConv

This is a custom SPDConv module for YOLO models, designed to improve performance on specific tasks.
一种新的卷积神经网络构建SPD-Conv，旨在解决低分辨率或小目标任务中的性能下降问题。通过替换步幅卷积和池化层，SPD-Conv保持了细粒度信息，提高了特征学习效率

# WTConv

This is a custom WTConv module for YOLO models, designed to improve performance on specific tasks.
引入了小波卷积模块，旨在扩大卷积的感受野并有效捕捉图像中的低频信息。其对多尺度问题和小目标问题上有很好的效果

## Installation

You can install the SPDConv module via pip:

```bash
pip install xl_yolo_pkg
