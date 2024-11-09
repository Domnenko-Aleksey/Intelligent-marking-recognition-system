import json
import os
from pathlib import Path
import time
from PIL import Image, ImageDraw
import cv2
import numpy as np
import pandas as pd


def ajax(CORE):
    CORE.debug('PATH: /webapp/ajax.py -> ajax()')

    file = CORE.post['file'].file.read()
    post_file_name = CORE.post['file'].filename.lower()
    # ext = post_file_name.split('.')[-1] 
    # file_name = uuid.uuid4().hex + '.' + ext


    # Сохраняем файл
    file_path = 'files/' + post_file_name
    with open(file_path, 'wb') as f:
        f.write(file)

    result = predict(CORE, post_file_name)
    if not result:
        answer = {'answer': 'error', 'message': 'Изображение не распознаноы'}

    # [Наименование, извлечённый текст, соответствие]
    print('RESULT', result)

    answer = {'answer': 'success', 'file': result[0], 'ext_text': result[1], 'marking': result[2]}
    return {'ajax': json.dumps(answer)}


def predict(CORE, file_name):
    CORE.debug('PATH: /webapp/ajax.py -> predict()')
    print('file_name', file_name)
    time_start = time.time()
    img = Image.open('files/' + file_name)
    print('IMAGE SIZE;', img.size)
    name = file_name.split('.')[0]
    predict = CORE.yolo.model(img)
    for p in predict:     
        im_np = p.plot()
        im_orig = p.orig_img
        print('IM ORIG, SHAPE', im_orig.shape)
        print('BBOX:', p.boxes)
        bbox = p.boxes.xyxyn.data.detach().cpu().numpy()

        # Внимание! Изображежие x, y, 3, arr => y, x, 3
        x1 = round(im_orig.shape[1]*bbox[0][0])
        y1 = round(im_orig.shape[0]*bbox[0][1])
        x2 = round(im_orig.shape[1]*bbox[0][2])
        y2 = round(im_orig.shape[0]*bbox[0][3])
        
        # print('COORD', x1, x2, y1, y2)

        crop = p.orig_img[y1:y2,x1:x2,:]  
        # cropped_img_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        im_crop = Image.fromarray(crop)  # RGB PIL image
        im_crop.save('files/crop.png')

        # OCR
        img_crop = 'files/crop.png'
        result = CORE.ocr.ocr(img_crop, cls=True) 
        
        print('RESULT', result)

        recognized_text = []
        for line in result:
            for word_info in line:
                text = word_info[1][0]  # Извлечение текста
                recognized_text.append(text)
        extracted_text = ' '.join(recognized_text)
        print('EXTRACTED TEXT', extracted_text)

        emb = CORE.model_emb.encode(extracted_text)
        # print("Распознанный текст:", extracted_text)
        D, I = CORE.faiss.search(emb)

        print(D[0])
        print(I[0][0])
        idx = I[0][0]

        print('IDX', idx)

        row = CORE.faiss.df.iloc[idx]
        
        delta_time = time.time() - time_start
        print('DELTA TIME', delta_time)

        print("###############################\n")
        print('ИЗОБРАЖЕНИЕ:',  file_name, 'ИЗВЛЕЧЁННЫЙ ТЕКСТ:', extracted_text, 'СООТВЕТСТВИЕ:', row[1])
        print("###############################\n")
    return [file_name, extracted_text, row[1]]