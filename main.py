import ui
import pymysql
from PyQt5.QtGui import QImage, QPixmap
import camera2
import align.compare as cp
import align.align_dataset_mtcnn as adm
import tensorflow as tf
import align.detect_face as detect_face
import numpy as np
import align.facenet as facenet
import cv2
import matplotlib.image as mpimg
import time

with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, None)
            facenet.load_model('20180402-114759')
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

db = pymysql.connect("localhost", "root", "", "Students",passwd = 'XIAOLAN12conan')
matrix = []
sid = []

cursor = db.cursor()
sql = "select matrix,studentId from students"
cursor.execute(sql)
result = cursor.fetchall()
for i in result:
	h = np.frombuffer(i[0],dtype = np.float64)
		#h = np.array(h)
	matrix.append(h)
	print(h)
	print(np.shape(h))
	sid.append(i[1])
matrix = np.array(matrix)


def capture():
	frame = camera.captureCroped()
	ui.captured_photo.setMatrix(frame)
	#image = cp.load_and_align_data(frame, 160, 44, 1.0, pnet, onet, rnet)
	time_start=time.time()
	image = adm.align(frame,pnet,onet,rnet)

	if isinstance(image,int):
		ui.console.info("Cannot detect face, try again!")
		ui.student_name.setText('')
		ui.student_id.setText('')
		ui.similarity.setText('')
		ui.stored_photo.load('')
	else:
		ui.console.info("Generating feature vector...")
		
		feed_dict = {images_placeholder: image, phase_train_placeholder:False }
		emb = sess.run(embeddings, feed_dict=feed_dict)
		#dot product
		final = np.matmul(emb,matrix.T)
				
		#for top 1 dot product
		maximum = np.argmax(final)
		if final[0][maximum] > 0.5:
			sel = "select studentName from students where studentId = " + sid[maximum]
			cursor.execute(sel)
			name = cursor.fetchone()
			print(name)
			ui.student_name.setText(name[0])
			ui.student_id.setText(sid[maximum])
			photo = 'photos/'+sid[maximum]+'.png'
			print(photo)
			p = cv2.imread(photo)
			p = cv2.cvtColor(p,cv2.COLOR_BGR2RGB)  
			ui.stored_photo.setMatrix(p) #need to load photo!!!
			print(final[0][maximum])
			similarity = str(final[0][maximum])
			ui.similarity.setText(similarity)
		else:
			ui.console.error('Not in database')

		time_end=time.time()
		ui.console.info(str(time_end-time_start))

		
	



ui.init()
ui.console.info('UI Initilized Successfully')
camera = camera2.Camera(cameraNumber=0, cropWidth=180, cropHeight=255)
camera.startDisplayOnQLabel(ui.video)
ui.capture_button.clicked.connect(capture)
ui.console.ok('Camera Initilized Successfully')




'''
ui.student_name.setText('Yichen Liu')
ui.student_id.setText('20031446')
ui.stored_photo.load('icon/no_photo.png')
ui.similarity.setText('95.6%')
'''




ui.console.error('Cannot load main module.')


ui.app.exec_()

camera.release()
print('Exited')
