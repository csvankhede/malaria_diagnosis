import cv2
import numpy as np
import os
from lxml import etree

def create_patches(img,size):
    patches = []
    
    h,w,c = img.shape
    
    max_y = 0 
    while max_y+size < h:
        max_x = 0 
        while max_x+size < w:
            left = max_x
            right = max_x+size
            top = max_y 
            bottom = max_y + size
            
            patch = img[top:bottom,left:right]
            patches.append(patch.copy())
            max_x += size
        max_y += size
    return patches
	
def create_patches_from_annotation(image_dir,annotation_dir,size):
    pos = []
    neg = []
    
    for image in os.listdir(image_dir)[:200]:
        annotation_filename = annotation_dir + image[:-3] + 'xml'
        
        bounding_boxes = get_bounding_boxes(annotation_filename)
        
        img = cv2.imread(image_dir+image)#,cv2.IMREAD_GRAYSCALE)
       
        img_pos = get_img_pos(img,bounding_boxes,size)
        
        
        pos.append(img_pos)
       
        img_neg = get_img_neg(img,bounding_boxes,size)
        neg.append(img_neg)
        
        
    pos = [img for subimg in pos for img in subimg]
    neg = [img for subimg in neg for img in subimg]
    
    patches = pos+neg
    
    index = np.arange(len(patches))
    np_labels = [0]*len(index)
    np_patches = [0]*len(index)
    
    
    max_pos = len(pos)
    for i,j in zip(index,range(len(index))):
        if i < max_pos:
            #pdb.set_trace()
            np_patches[j] = np.ndarray.flatten(pos[i])
            np_labels[j] = 1
        else:
            np_patches[j] = np.ndarray.flatten(neg[i-max_pos])
            np_labels[j] = 0
            
    np_labels = np.array(np_labels,dtype=np.uint8)
    
    return np_patches,np_labels


def get_bounding_boxes(annotation_file):
    file_exist = os.path.exists(annotation_file)
    bounding_boxes = []
    
    if file_exist:
        data = etree.parse(annotation_file)
            
        object = data.findall("object")
        for obj in object:
                xmin = round(float(obj.find("bndbox/xmin").text))
                ymin = round(float(obj.find("bndbox/ymin").text))
                xmax = round(float(obj.find("bndbox/xmax").text))
                ymax = round(float(obj.find("bndbox/ymax").text))
                xmin,xmax,ymin,ymax = int(xmin),int(xmax),int(ymin),int(ymax)
                bounding_boxes.append((xmin,xmax,ymin,ymax))

        
        if len(bounding_boxes) == 0:
            return np.array([])
        return np.vstack(bounding_boxes)


def get_img_pos(img,bb_box,size):
    patches = []
    
    for bb in bb_box:
        patch = img[bb[0]:bb[1],bb[2]:bb[3]]
        
        s = patch.shape
        
        
        if s[0]<size or s[1]<size:
            continue
        patches.append(patch)
   
    return patches
  
def get_img_neg(img,bb_box,size):
    patches = []
    h,w,c = img.shape
   
    
    max_y = 0 
    while max_y+size < h:
        max_x = 0 
        while max_x+size < w:
            if np.random.rand()>0.90 and len(patches)<11:
                left = max_x
                right = max_x+size
                top = max_y 
                bottom = max_y + size
           
                pos = False
                for bb in bb_box:
                    if overlap([left,right,top,bottom],bb):
                      pos = True
                if not pos:      
                  patch = img[top:bottom,left:right]
                  patches.append(patch.copy())
            max_x += size
        max_y += size
    return patches
            

def overlap(bb1,bb2):
    return (bb1[0] <= bb2[1] and bb2[0] <= bb1[1]) and (bb1[2] <= bb2[3] and bb2[2] <= bb1[3])
        

            