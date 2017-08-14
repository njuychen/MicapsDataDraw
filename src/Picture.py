# -*- coding: utf-8 -*-
#
#     Author:     Liu xianyao
#     Email:      flashlxy@qq.com
#     Update:     2017-04-11
#     Copyright:  ©江西省气象台 2017
#     Version:    2.0.20170411
from __future__ import print_function

import os

from matplotlib.transforms import Bbox

from Projection import Projection


class Picture:
    def __init__(self, root, clipborders):
        p = root.find("Picture")
        # 生成的图片宽度
        self.width = Projection.leaf_to_float(p, "PicWidth", 10)

        # 生成的图片高度
        self.height = Projection.leaf_to_float(p, "PicHeight", 10)

        # dpi
        self.dpi = Projection.leaf_to_int(p, "Dpi", 72)

        # 高宽比
        self.widthshrink = Projection.leaf_to_float(p, "WidthShrink", 1.0)

        # 绘图区外延
        self.margin = Projection.leaf_to_list(p, "Margin", [0, 0, 0, 0])
		
        # 绘图区内边距
        self.pad = Projection.leaf_to_float(p, "Pad", 0.0)

        # 绘图区域

        extents = p.find("Extents").text.strip()
        if extents is None or extents == '':
            if len(clipborders) < 1 or clipborders[0].path is None or (not clipborders[0].using):
                self.extents = None
            else:
                jxextend = clipborders[0].path.get_extents()
                delta = self.margin
                xmax = jxextend.xmax + delta[2]
                xmin = jxextend.xmin - delta[0]
                ymax = jxextend.ymax + delta[1]
                ymin = jxextend.ymin - delta[3]
                self.extents = Bbox.from_extents(xmin, ymin, xmax, ymax)
        else:
            self.extents = Projection.leaf_to_list(p, "Extents", None)

        # 画布透明度
        self.opacity = Projection.leaf_to_float(p, 'Opacity', 1)
        if self.opacity < 0 or self.opacity > 1:
            self.opacity = 1

        # 生成的图片文件存放路径
        self.picfile = Projection.leaf_to_string(p, 'PicFile', 'mytest.png')
        self.checkFilename()


        return

    @staticmethod
    def savePicture(fig, filename):
        # 存图
        fig.savefig(filename, format='png', transparent=False)
        # return

    def checkFilename(self):
        """
        创建数据文件夹
        :param filepath: 文件路径
        :return: 
        """
        try:
            path = os.path.dirname(self.picfile)
            if not os.path.isdir(path):
                os.makedirs(path)
        except:
            self.picfile = 'mytest.png'

