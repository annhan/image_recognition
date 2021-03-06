#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import os
import xml.etree.ElementTree as ET

class init_camera:
    def __init__(self,image_sizeW=640,image_sizeH = 480):
        self.image_sizeW = image_sizeW
        self.image_sizeH = image_sizeH
        self.matrix = np.zeros((3, 3), np.float)
        self.new_camera_matrix = np.zeros((3, 3), np.float)
        self.dist = np.zeros((1, 5))
        self.roi = np.zeros(4, np.int)

    def load_params(self, param_file:str='./calibcamera/output/camera_params.xml'):
        if not os.path.exists(param_file):
            print("File {} does not exist.",format(param_file))
            exit(-1)
        tree = ET.parse(param_file)
        root = tree.getroot()
        mat_data = root.find('camera_matrix')
        matrix = dict()
        if mat_data:
            for data in mat_data.iter():
                matrix[data.tag] = data.text
            for i in range(9):
                self.matrix[i // 3][i % 3] = float(matrix['data{}'.format(i)])
        else:
            print('No element named camera_matrix was found in {}'.format(param_file))

        new_camera_matrix = dict()
        new_data = root.find('new_camera_matrix')
        if new_data:
            for data in new_data.iter():
                new_camera_matrix[data.tag] = data.text
            for i in range(9):
                self.new_camera_matrix[i // 3][i % 3] = float(new_camera_matrix['data{}'.format(i)])
        else:
            print('No element named new_camera_matrix was found in {}'.format(param_file))

        dist = dict()
        dist_data = root.find('camera_distortion')
        if dist_data:
            for data in dist_data.iter():
                dist[data.tag] = data.text
            for i in range(5):
                self.dist[0][i]= float(dist['data{}'.format(i)])
        else:
            print('No element named camera_distortion was found in {}'.format(param_file))

        roi = dict()
        roi_data = root.find('roi')
        if roi_data:
            for data in roi_data.iter():
                roi[data.tag] = data.text
            for i in range(4):
                self.roi[i] = int(roi['data{}'.format(i)])
        else:
            print('No element named roi was found in {}'.format(param_file))

    def rectify_image(self, img):
        #if not isinstance(img, np.ndarray):
        #    AssertionError("Image type '{}' is not numpy.ndarray.".format(type(img)))
        dst = cv2.undistort(img, self.matrix, self.dist, self.new_camera_matrix)
        x, y, w, h = self.roi
        dst = dst[y:y + h, x:x + w]
        dst = cv2.resize(dst, (self.image_sizeW, self.image_sizeH))
        return dst


if __name__ == '__main__':
    init_camera = init_camera()
    init_camera.load_params()