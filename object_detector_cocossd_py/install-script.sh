#!/bin/sh

cd $(dirname $0)

wget -O VGG_coco_SSD_300x300_iter_400000.caffemodel https://getfile.dokpub.com/yandex/get/https://yadi.sk/d/lZNdWhChLNmhcw

wget -O res10_300x300_ssd_iter_140000_fp16_Faces.caffemodel https://github.com/opencv/opencv_3rdparty/raw/19512576c112aa2c7b6328cb0e8d589a4a90a26d/res10_300x300_ssd_iter_140000_fp16.caffemodel
