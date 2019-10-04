import os
import xml.etree.ElementTree as ET


def get_data(input_path):
    all_imgs = []

    classes_count = {}

    class_mapping = {}

    idx = 0
    for file in os.listdir(input_path):
        idx += 1
        full_path = input_path + "\\" + file

        et = ET.parse(full_path)
        element = et.getroot()

        element_objs = element.findall('object')
        element_filename = element.find('filename').text
        element_width = int(element.find('size').find('width').text)
        element_height = int(element.find('size').find('height').text)

        image_path = element.find('path').text

        if len(element_objs) > 0:
            annotation_data = {'filepath': image_path, 'width': element_width,
                               'height': element_height, 'bboxes': []}

        for element_obj in element_objs:
            class_name = element_obj.find('name').text
            if class_name not in classes_count:
                classes_count[class_name] = 1
            else:
                classes_count[class_name] += 1

            if class_name not in class_mapping:
                class_mapping[class_name] = len(class_mapping)

            obj_bbox = element_obj.find('bndbox')
            x1 = int(round(float(obj_bbox.find('xmin').text)))
            y1 = int(round(float(obj_bbox.find('ymin').text)))
            x2 = int(round(float(obj_bbox.find('xmax').text)))
            y2 = int(round(float(obj_bbox.find('ymax').text)))
            difficulty = int(element_obj.find('difficult').text) == 1
            annotation_data['bboxes'].append(
                {'class': class_name, 'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2, 'difficult': difficulty})
        all_imgs.append(annotation_data)

        print()

    return all_imgs, classes_count, class_mapping


all_imgs, classes_count, class_mapping = get_data("E:\\ImageData\\color_data\\1_annotations")
