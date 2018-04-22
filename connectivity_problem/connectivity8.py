import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
def eight_connectivity(img):
	img1 = cv2.imread(img)
	_,_,channel = img1.shape
	if channel==3:
		gray = img1[:,:,1]
	else:
		gray = img1
	 

	ret,image = cv2.threshold(gray,128,255,cv2.THRESH_BINARY)
	img = np.uint16(image) # convert image to int16 if label is greater than 256


	h,w  = img.shape

	label = 0
	# find 8 label
	for r in range(0,h):
		for c in range(0,w):
			if img[r,c]!=0:
				if c>0 and img[r,c-1]!=0:
					img[r,c] = img[r,c-1]
				elif r>0 and img[r-1,c]!=0:
					img[r,c] = img[r-1,c]
				elif r>0 and c>0 and img[r-1,c-1]!=0:
					img[r,c] = img[r-1,c-1] 
				else:	
					label += 1
					img[r,c] = label



	arr = dict()
	key = 1
	# transitive closure
	for r in range(0,h): 
		for c in range(0,w):
			if img[r,c] in [x for v in arr.values() for x in v]: # check if label is in dict or not if present merge two label else create new entry in dict
				if r>0 and c >0 and img[r,c]!=0 and (img[r-1,c]!=0 and img[r,c-1]!=0):
					if img[r-1,c] != img[r,c-1]:
						for key_v in arr.keys():
							if img[r-1,c] in arr[key_v]:
								key_1 = key_v
								break
						for key_v in arr.keys():
							if img[r,c-1] in arr[key_v]:
								key_2 = key_v
								break	
						if key_1 !=key_2:
							arr[key_1] = arr[key_1]+arr[key_2]
							del arr[key_2]



							
			elif img[r,c]!=0:
				
				flag = 0
				for key_v in arr.keys():
					if img[r-1,c] in arr[key_v]:
						flag =1
				if flag!=1:
					arr[key] = []
					arr[key].append(img[r,c])
					key +=1

	#print np.where(img==1)
	#group all values which belong to same key in one label
	label =1
	keylist = arr.keys()
	key_pair = dict()
	for key in sorted(keylist):
		for value in arr[key]:
			img[img==value] = label
		arr[key] = label
		key_pair[label] = label
		label+=1


	bounding_box = {}
	#initialize variable
	for i in range(1,len(keylist)+1):
		bounding_box[i] = {
			'count':0,
			'rectangle':{
			'r_min':0,
			'r_max':0,
			'c_min':0,
			'c_max':0
			},
			'centre':{
			'x':0,
			'y':0
			}
		}

	for i in key_pair.keys():
		labels = np.where(img==key_pair[i])
		c_min = labels[0][0]
		c_max = labels[0][-1]
		r_min = labels[1][labels[1].argmin()]
		r_max =labels[1][labels[1].argmax()]
		bounding_box[i]['count']=len(labels[0])
		bounding_box[i]['rectangle']['r_min'] = labels[1][labels[1].argmin()]
		bounding_box[i]['rectangle']['r_max'] = labels[1][labels[1].argmax()]
		bounding_box[i]['rectangle']['c_max'] = labels[0][0]
		bounding_box[i]['rectangle']['c_max'] = labels[0][-1]
		bounding_box[i]['centre']['x'] = (r_max - r_min)/2
		bounding_box[i]['centre']['y'] = (c_max - c_min)/2
		cv2.rectangle(img,(r_min,c_min),(r_max,c_max),(255,255),1)
		
	if len(bounding_box)>10:
		new_list = sorted(bounding_box.iteritems(), key=lambda (x, y): y['count']) ## sort largest pixels 
		new_list = new_list[:-11:-1] ## take 10 largest connected component
		new_dict = dict(new_list)
	else:
		new_dict = bounding_box

	for key in new_dict.keys():
		print "Label",key
		print "Number of pixel : ",bounding_box[i]['count']
		print 'Bounding rectangle Size : ' ,(bounding_box[i]['rectangle']['r_max']-bounding_box[i]['rectangle']['r_min'])*(bounding_box[i]['rectangle']['c_max']-bounding_box[i]['rectangle']['c_min'])
		print 'Bounding rectangle centre : ' , bounding_box[i]['centre']['x'] , bounding_box[i]['centre']['y']	

	img = np.uint8(img)
	cv2.imshow('image',img)
	cv2.waitKey(0)


if __name__ == "__main__":
	try:
	    eight_connectivity(sys.argv[1])
	except Exception as e:
		print 'Provide image path While running program'

	 