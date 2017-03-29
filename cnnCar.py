import cv2                 # working with, mainly resizing, images
import numpy as np       
import os                  
from random import shuffle 
from tqdm import tqdm      


class CarCNN_Count:

    global TRAIN_DIR1
    global TRAIN_DIR2 
    global IMG_SIZE 
    global LR 


    def __init__(self,AreaCode, Blockcode):

        
        TRAIN_DIR1 = './nohouse'
        TRAIN_DIR2 = './house'
        IMG_SIZE = 50
        LR = 1e-3


        MODEL_NAME = 'car_detection-{}-{}.model'.format(LR, '2conv-basic')

        def label_img1(img):
            return [0,1] #for no house images
        def label_img2(img):
            return [1,0] #for house images


            
        def create_train_data2():
            training_data = []
            for img in tqdm(os.listdir(TRAIN_DIR1)):
                label = label_img1(img)
                path = os.path.join(TRAIN_DIR1,img)
                img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
                training_data.append([np.array(img),np.array(label)])
            for img in tqdm(os.listdir(TRAIN_DIR2)):
                label = label_img2(img)
                path = os.path.join(TRAIN_DIR2,img)
                img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
                training_data.append([np.array(img),np.array(label)])
            
            shuffle(training_data)
            np.save('train_data2.npy', training_data)
            return training_data


        import tflearn
        from tflearn.layers.conv import conv_2d, max_pool_2d
        from tflearn.layers.core import input_data, dropout, fully_connected
        from tflearn.layers.estimator import regression
        import tensorflow as tf
        tf.reset_default_graph()
        convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 1], name='input')

        convnet = conv_2d(convnet, 32, 5, activation='relu')
        convnet = max_pool_2d(convnet, 5)

        convnet = conv_2d(convnet, 64, 5, activation='relu')
        convnet = max_pool_2d(convnet, 5)

        convnet = conv_2d(convnet, 128, 5, activation='relu')
        convnet = max_pool_2d(convnet, 5)

        convnet = conv_2d(convnet, 64, 5, activation='relu')
        convnet = max_pool_2d(convnet, 5)

        convnet = conv_2d(convnet, 32, 5, activation='relu')
        convnet = max_pool_2d(convnet, 5)

        convnet = fully_connected(convnet, 1024, activation='sigmoid')
        convnet = dropout(convnet, 0.8)

        convnet = fully_connected(convnet, 2, activation='softmax')
        convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')


        model = tflearn.DNN(convnet, tensorboard_dir='log')

        if os.path.exists('{}.meta'.format(MODEL_NAME)):
            model.load(MODEL_NAME)
            print('model loaded!')
           
        train_data = create_train_data2()
        train = train_data[:-20]
        test = train_data[-20:]

        X = np.array([i[0] for i in train]).reshape(-1,IMG_SIZE,IMG_SIZE,1)
        Y = [i[1] for i in train]

        test_x = np.array([i[0] for i in test]).reshape(-1,IMG_SIZE,IMG_SIZE,1)
        test_y = [i[1] for i in test]
        model.fit({'input': X}, {'targets': Y}, n_epoch=3, validation_set=({'input': test_x}, {'targets': test_y}), 
            snapshot_step=500, show_metric=True, run_id=MODEL_NAME)
        model.save(MODEL_NAME)

        from PIL import Image
        x = input('please enter the zip code of your areaS')
        y = input('please enter the block code of your area')
        img_data = cv2.imread("./area_zip" +str(x) + "/" + "img"+str(y)+".jpg",cv2.IMREAD_GRAYSCALE)
        k = IMG_SIZE/3
        l = IMG_SIZE/3
        count = 0
        for i in range(0,IMG_SIZE-l,l):
        	for j in range(0,IMG_SIZE-k,k):
        		img2 = img_data[i: i + l, j : j + k]
        		img2 = cv2.resize(img2, (IMG_SIZE,IMG_SIZE))
        		img2 = img2.reshape(IMG_SIZE,IMG_SIZE,1)
        		model_out = model.predict([img2])[0]
        		if np.argmax(model_out) == 1:
        			count = count + 1
        print count   
           
        data = cv2.resize(img_data, (IMG_SIZE,IMG_SIZE))
        data = data.reshape(IMG_SIZE,IMG_SIZE,1)
        #model_out = model.predict([data])[0]
        model_out = model.predict([data])[0]
        str_label = 'p'    
        if np.argmax(model_out) == 1:
        	 str_label='House'
        else: 
        	 str_label='NoHouse'

        print str_label
