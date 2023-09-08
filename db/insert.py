import pymysql
import os
import cv2
import numpy as np
import align.compare as cp
import align.align_dataset_mtcnn as adm
import tensorflow as tf
import align.detect_face as detect_face
import numpy
import align.facenet as facenet

with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, None)
            facenet.load_model('20180402-114759')
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

db = pymysql.connect("localhost", "root", "", "Students",passwd='XIAOLAN12conan')
cursor = db.cursor()

img = cv2.imread("/Users/qiaoshuangshuang/Desktop/db/Victoria.png")
judge = adm.align(img,pnet,onet,rnet)
if not isinstance(judge,int):
	feed_dict = {images_placeholder: judge, phase_train_placeholder:False }
	emb = sess.run(embeddings, feed_dict=feed_dict)
	print(type(emb))

#vector = k[0].split(',')
#list_to_float = np.array(list(map(lambda x:float(x),vector)))
	number = '6522059'
	name ='Shuying Qiao'

#bytes_feature = list_to_float.tostring()
	cursor.execute('insert into Students values(%s,%s,%s)',(number,name,emb)) 
	db.commit()