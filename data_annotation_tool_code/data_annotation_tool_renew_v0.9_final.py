#-*- coding:utf-8 -*-
# coding: utf-8

# # Grading Data Selection Tool
# ---

# * Date: 2021.10.01.
# * Author: Seoung-Ho Choi
# * Description: Data annoatation tool for preprocessed data
'''
parameter description :
- ABP_raw_data #visualization ABP 이미지 파일 경로 저장 리스트 
- ECG_raw_data #visualization ECG 이미지 파일 경로 저장 리스트 
- PPG_raw_data #visualization PPG 이미지 파일 경로 저장 리스트 
- MBP_raw_data #visualization MBP 이미지 파일 경로 저장 리스트 
'''

import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit,QShortcut
import numpy as np
import pandas as pd
import csv

#file path 
file_root_path="E:/opstart_opend_v2/"
file_root_path2="E:/"


ABP_raw_data =[] #visualization ABP 이미지 파일 경로 저장 리스트 
ECG_raw_data =[] #visualization ECG 이미지 파일 경로 저장 리스트 
PPG_raw_data =[] #visualization PPG 이미지 파일 경로 저장 리스트 
MBP_raw_data =[] #visualization MBP 이미지 파일 경로 저장 리스트 

    
ABP_grade_value_list=[]#ABP 이미지 파일 grading 정보 저장 리스트 
ECG_grade_value_list=[]#ECG 이미지 파일 grading 정보 저장 리스트 
PPG_grade_value_list=[]#PPG 이미지 파일 grading 정보 저장 리스트
MBP_grade_value_list=[]#MBP 이미지 파일 grading 정보 저장 리스트 

ABP_grade_data_annotation = 0 #ABP data annotation grading 몇개 됬는지 
ECG_grade_data_annotation = 0 #ECG data annotation grading 몇개 됬는지 
PPG_grade_data_annotation = 0 #PPG data annotation grading 몇개 됬는지 
MBP_grade_data_annotation = 0 #MBP data annotation grading 몇개 됬는지 

Segment_id_data=[] #case_id_list
Case_id_data_total=[]
Segment_id_data_total=[]
Segment_id_data_art=[]
Segment_id_data_mbp=[]
Segment_id_data_ecg=[]
Segment_id_data_ppg=[]
Segment_id_data_art_start_end =[]
Segment_id_data_ecg_start_end =[]
Segment_id_data_ppg_start_end =[]
Segment_id_data_mbp_start_end =[]
ABP_raw_data_index = 0
ECG_raw_data_index = 0
PPG_raw_data_index = 0
MBP_raw_data_index = 0
case_raw_data_index = 0

case_id_data_index_matching=[]
case_id_data_index_matching_full=[]
segment_id_data=[]


data_index_count={}
data_index_count_v2={}
data_index_load_range=[] #load data index range


ABP_grade_value_list_temp = []
ECG_grade_value_list_temp = []
PPG_grade_value_list_temp = []
MBP_grade_value_list_temp = []

abp_count=0
ecg_count=0
ppg_count=0
mbp_count=0
file_open_count =0

#Segment_id read
def segment_id_read():
    global case_id_data_index_matching
    global case_id_data_index_matching_full
    global Case_id_data_total
    global data_index_count
    
    segment_id_data_csv = pd.read_csv(file_root_path2+'segment_id.csv')
    segment_id_data_csv=segment_id_data_csv.values.tolist()
    #print(segment_id_data_csv)
    count1 =0
    for i in range(0,len(segment_id_data_csv[1:])):
        if count1 >=1:
            case_id_data_index_matching.append(segment_id_data_csv[i][0][:-4].zfill(4))
            segment_id_data.append(segment_id_data_csv[i][0][-5:-1])
            case_id_data_index_matching_full.append(segment_id_data_csv[i][0].zfill(8))
        count1= count1+1

    #count duplicate value -> 각각 case 별 data index nubmer
    #print(case_id_data_index_matching)
    for i in case_id_data_index_matching:
        try: data_index_count[i] += 1
        except: data_index_count[i]=1
    #print(data_index_count)
    #카운트가 변화할때 마다 중복된 갯수가 적용 되도
    
    #remove duplicate value
    case_id_data = list(set(case_id_data_index_matching[:]))
    #print(case_id_data)
    case_id_data = sorted(case_id_data)
    #print(len(case_id_data))
    Case_id_data_total=case_id_data
    #print(Case_id_data_total)
    
segment_id_read()

def search(dirname):
    global case_id_list
    global Segment_id_data
    global Segment_id_data_art
    global Segment_id_data_ecg
    global Segment_id_data_ppg
    global Segment_id_data_mbp
    global ABP_raw_data
    global ECG_raw_data
    global PPG_raw_data
    global MBP_raw_data
    global Segment_id_data_art_start_end
    global Segment_id_data_ecg_start_end
    global Segment_id_data_ppg_start_end
    global Segment_id_data_mbp_start_end
    global data_index_count_v2
        
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(full_filename)[-1]
        if ext == '.npy':
            #print(full_filename)
            raw_data.append(full_filename)
        if ext == '.png':
            #print(full_filename)
            aa=full_filename.split('/')
            fname=aa[-1].split('_')
            #print(fname)
            Segment_id_data.append(fname[1])
            if str(fname[0]) == "ART":
                ABP_raw_data.append(full_filename)
                Segment_id_data_art.append(fname[1])
                Segment_id_data_art_start_end.append([fname[1],fname[2]])#start
                Segment_id_data_art_start_end.append([fname[1],fname[3]])#end
            elif str(fname[0]) == "ECG":
                ECG_raw_data.append(full_filename)
                Segment_id_data_ecg.append(fname[1])
                Segment_id_data_ecg_start_end.append([fname[1],fname[2]])#start
                Segment_id_data_ecg_start_end.append([fname[1],fname[3]])#end
            elif str(fname[0]) == "PLETH":
                PPG_raw_data.append(full_filename)
                Segment_id_data_ppg.append(fname[1])
                Segment_id_data_ppg_start_end.append([fname[1],fname[2]])#start
                Segment_id_data_ppg_start_end.append([fname[1],fname[3]])#end
            elif str(fname[0]) == "MBP":
                MBP_raw_data.append(full_filename)
                Segment_id_data_mbp.append(fname[1])
                Segment_id_data_mbp_start_end.append([fname[1],fname[2]])#start
                Segment_id_data_mbp_start_end.append([fname[1],fname[3]])#end
            else :
                print('no name')
    #print(Segment_id_data_mbp_start_end) # 총 데이터 갯수 만큼 불러와짐 / (케이스 수*2) 
    #print(Segment_id_data_ppg_start_end)
    
    
    #case id duplicate remove
    #print(Segment_id_data)
    for i in Segment_id_data:
        try: data_index_count_v2[i] += 1
        except: data_index_count_v2[i]=1
    #print(data_index_count_v2)#ART / PPG / EEG / MBP 

    global data_index_load_range
    aa=list(data_index_count_v2.values())
    for i in range(0,len(aa)):
        data_index_load_range.append(int(aa[i]/4))
    print(data_index_load_range)#[5,2,2]
    #print('chchchchchchchc')

    Segment_id_data=list(set(Segment_id_data))
    Segment_id_data = sorted(Segment_id_data)
    Segment_id_data_art = sorted(Segment_id_data_art)
    ABP_raw_data=sorted(ABP_raw_data)
    #print(Segment_id_data_art)
    Segment_id_data_ecg = sorted(Segment_id_data_ecg)
    ECG_raw_data=sorted(ECG_raw_data)
    #print(Segment_id_data_ecg)
    Segment_id_data_ppg = sorted(Segment_id_data_ppg)
    PPG_raw_data=sorted(PPG_raw_data)
    #print(Segment_id_data_ppg)
    Segment_id_data_mbp = sorted(Segment_id_data_mbp)
    MBP_raw_data=sorted(MBP_raw_data)
    
    
    Segment_id_data_art_start_end=sorted(Segment_id_data_art_start_end)
    Segment_id_data_ecg_start_end=sorted(Segment_id_data_ecg_start_end)
    Segment_id_data_ppg_start_end=sorted(Segment_id_data_ppg_start_end)
    Segment_id_data_mbp_start_end=sorted(Segment_id_data_mbp_start_end)


#Annotation tool에 사용할 수 있는 정보로 가공하기
#Caseid / index 번호
# Data index 와 grade 가 쌍으로 저장되도록해야함

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QScrollBar, QFileDialog, QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence
import matplotlib.pyplot as plt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ABP_raw_data_index_number=0
        self.ECG_raw_data_index_number=0
        self.PPG_raw_data_index_number=0
        self.MBP_raw_data_index_number=0
        self.initUI()

    #Text Box
    def edit_onChanged1(self, text):
        layout_scale_factor = 1.85
        
        self.label17.setText(text)
        self.label17.adjustSize()
        print('ART Grade',text)
        '''
        Full Case id Segment id 가지고 있는 것 , 현재 상태 case id / segment id matching
        '''
        global case_id_data_index_matching_full
        global Case_id_data_total
        global ABP_raw_data_index
        global Segment_id_data
        global case_raw_data_index
        global ABP_grade_value_list
        
        ABP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ABP_raw_data_index).zfill(4))
        print('ABP_raw_data_index',ABP_raw_index)
        #ART insert
        ABP_grade_value_list[ABP_raw_index][0]= text
        self.qle.setText(str(ABP_grade_value_list[ABP_raw_index][0]))
        self.qle.move(700*layout_scale_factor, 100*layout_scale_factor)
        self.qle.repaint()
        print(ABP_grade_value_list[ABP_raw_index][0])


    def edit_onChanged2(self, text):
        layout_scale_factor = 1.85
        self.label16.setText(text)
        self.label16.adjustSize()
        print('ECG Grade',text)
        
        global case_id_data_index_matching_full
        global Case_id_data_total
        global ECG_raw_data_index
        global Segment_id_data
        global case_raw_data_index
        global ECG_grade_value_list
        ECG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ECG_raw_data_index).zfill(4))
        print('ECG_raw_data_index',ECG_raw_index)
        #Grade insert
        ECG_grade_value_list[ECG_raw_index][0]= text
        print(ECG_grade_value_list[ECG_raw_index][0])
        self.qle1.setText(str(ECG_grade_value_list[ECG_raw_index][0]))
        self.qle1.move(700*layout_scale_factor, 200*layout_scale_factor)
        self.qle1.repaint()

    def edit_onChanged3(self, text):
        layout_scale_factor = 1.85
        self.label15.setText(text)
        self.label15.adjustSize()
        print('PPG Grade',text)
        
        global case_id_data_index_matching_full
        global Case_id_data_total
        global PPG_raw_data_index
        global Segment_id_data
        global case_raw_data_index
        global PPG_grade_value_list
        PPG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(PPG_raw_data_index).zfill(4))
        print('PPG_raw_data_index',PPG_raw_index)
        #Grade insert
        PPG_grade_value_list[PPG_raw_index][0]= text
        print(PPG_grade_value_list[PPG_raw_index][0])
        self.qle2.setText(str(PPG_grade_value_list[PPG_raw_index][0]))
        self.qle2.move(700*layout_scale_factor, 300*layout_scale_factor)
        self.qle2.repaint()
        
    def edit_onChanged4(self, text):
        layout_scale_factor = 1.85
        self.label14.setText(text)
        self.label14.adjustSize()
        print('MBP Grade',text)
        global case_id_data_index_matching_full
        global Case_id_data_total
        global MBP_raw_data_index
        global Segment_id_data
        global case_raw_data_index
        global MBP_grade_value_list
        
        MBP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(MBP_raw_data_index).zfill(4))
        print('MBP_raw_data_index',MBP_raw_index)
        #Grade insert
        MBP_grade_value_list[MBP_raw_index][0]= text
        print(MBP_grade_value_list[MBP_raw_index][0])
        self.qle3.setText(str(MBP_grade_value_list[MBP_raw_index][0]))
        self.qle3.move(700*layout_scale_factor, 420*layout_scale_factor)
        self.qle3.repaint()
        
    def filedialog_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '','All File(*);; Image File(*.png *.jpg)')
        if fname[0]:
            # QPixmap 객체
            pixmap = QPixmap(fname[0])
            self.label.setPixmap(pixmap)  # 이미지 세팅
            self.label.setContentsMargins(10, 50, 10, 10)
            self.label.resize(pixmap.width(), pixmap.height())
            # 이미지의 크기에 맞게 Resize
            self.resize(pixmap.width(), pixmap.height())
        else:
            QMessageBox.about(self, 'Warning', '파일을 선택하지 않았습니다.')
            
    def btnRun_clicked1(self,value):
        global ABP_raw_data_index
        global ECG_raw_data_index
        global PPG_raw_data_index
        global MBP_raw_data_index
        global case_raw_data_index
        
        global Segment_id_data
        global Segment_id_data_art
        global Segment_id_data_ecg
        global Segment_id_data_ppg
        global Segment_id_data_mbp
        
        global Segment_id_data_art_start_end
        global Segment_id_data_ecg_start_end
        global Segment_id_data_ppg_start_end
        global Segment_id_data_mbp_start_end
        
        global Case_id_data_total
        global data_index_count

        global case_raw_data_index
        global data_index_load_range
        global Segment_id_data_mbp_start_end

        global ABP_grade_value_list
        global ECG_grade_value_list
        global PPG_grade_value_list
        global MBP_grade_value_list
        case_raw_data_index = case_raw_data_index-1

        #self.slider.setValue(0)
        if ABP_raw_data_index < 0:
            ABP_raw_data_index = 0
        if ECG_raw_data_index < 0:
            ECG_raw_data_index = 0
        if PPG_raw_data_index < 0:
            PPG_raw_data_index = 0
        if MBP_raw_data_index < 0:
            MBP_raw_data_index = 0                        
        if case_raw_data_index <0:
            case_raw_data_index = 0
        
        if case_raw_data_index >= len(Segment_id_data):
            case_raw_data_index = len(Segment_id_data) -1
            
        print('Caculation data index boundary')
        print('Segment id', Segment_id_data[case_raw_data_index])
        print('data index count', data_index_count[Segment_id_data[case_raw_data_index]])


        self.ABP_raw_data_index_number = ABP_raw_data_index
        self.ECG_raw_data_index_number = ECG_raw_data_index
        self.PPG_raw_data_index_number = PPG_raw_data_index
        self.MBP_raw_data_index_number = MBP_raw_data_index
        
        
        #Case id  index
        self.label13.setText(str(Segment_id_data[case_raw_data_index])+'/'+str(len(Segment_id_data)))
        self.label13.adjustSize()
        self.label13.repaint()
        
        self.label12.setText(str(ABP_raw_data_index)+'/'+str(data_index_load_range[case_raw_data_index]-1))
        #self.label12.setText(str(ABP_raw_data_index)+'/'+str(data_index_count[Segment_id_data[case_raw_data_index]]))
        self.label12.adjustSize()
        self.label12.repaint()

        print('annotation count')
        global abp_count
        global ecg_count
        global ppg_count
        global mbp_count
        
        self.label32.setText(str(abp_count))
        self.label32.adjustSize()
        self.label32.repaint()
        
        self.label34.setText(str(ecg_count))
        self.label34.adjustSize()
        self.label34.repaint()
        
        self.label36.setText(str(ppg_count))
        self.label36.adjustSize()
        self.label36.repaint()
        
        self.label38.setText(str(mbp_count))
        self.label38.adjustSize()
        self.label38.repaint()

    
        layout_scale_factor = 1.85
        
        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        self.label21 = QLabel(self)
        print(ABP_raw_data[ABP_raw_data_index])

        #Case
        aa=ABP_raw_data[ABP_raw_data_index].split('/')
        aaa=aa[-1].split('_')
        bb=ECG_raw_data[ECG_raw_data_index].split('/')
        print(bb)
        
        bbb=bb[-1].split('_')
        cc=PPG_raw_data[PPG_raw_data_index].split('/')
        ccc=cc[-1].split('_')
        dd=MBP_raw_data[MBP_raw_data_index].split('/')
        ddd=dd[-1].split('_')


        #현재 케이스 id에 따른 start index / end index
                                        
        #print(Segment_id_data_art_start_end[2*(ABP_raw_data_index)])
        #print(Segment_id_data_art_start_end[2*ABP_raw_data_index+1])
        
        Segment_id_data_ecg_start_end[2*(ABP_raw_data_index)]
        Segment_id_data_ecg_start_end[2*ABP_raw_data_index+1]
        
        Segment_id_data_ppg_start_end[2*(ABP_raw_data_index)]
        Segment_id_data_ppg_start_end[2*ABP_raw_data_index+1]
        
        Segment_id_data_mbp_start_end[2*(ABP_raw_data_index)]
        Segment_id_data_mbp_start_end[2*ABP_raw_data_index+1]

        #print(Segment_id_data_art_start_end)
        #print(Segment_id_data_ecg_start_end)
        #print(Segment_id_data_ppg_start_end)
        #print(Segment_id_data_mbp_start_end)
        #start point
        #end point

        print('ccc index')
        index_aa=0
        #print(ABP_raw_data_index)
        if case_raw_data_index ==0:
            index_aa = ABP_raw_data_index
        else:
            for i in range(0,len(data_index_load_range[:case_raw_data_index])):
                index_aa=index_aa+int(data_index_load_range[i])+ABP_raw_data_index
        print('sum of the index',index_aa)
        if index_aa*2 == len(Segment_id_data_art_start_end):
            index_aa = index_aa -1
        print(len(Segment_id_data_art_start_end))
        #print(data_index_load_range[case_raw_data_index]*case_raw_data_index+ABP_raw_data_index) #[5,2,2]

        Abp_change_path = aaa[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_art_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_art_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Abp_change_path = file_root_path+Abp_change_path
        Ecg_change_path = bbb[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ecg_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_ecg_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Ecg_change_path = file_root_path+Ecg_change_path
        Ppg_change_path = ccc[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ppg_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_ppg_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Ppg_change_path = file_root_path+Ppg_change_path
        Mbp_change_path = ddd[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_mbp_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_mbp_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Mbp_change_path = file_root_path+Mbp_change_path
        
        print('check 1')
        
        print(Abp_change_path)
        print(Ecg_change_path)
        print(Ppg_change_path)
        print(Mbp_change_path)
        
        ## To DO case id 변경 햇을때 이미지 적용하는 것
        self.ABP_image=QtGui.QPixmap(Abp_change_path)
        #self.ABP_image=QtGui.QPixmap(ABP_raw_data[ABP_raw_data_index])
        self.ABP_image_resized = self.ABP_image.scaled(width_size, height_size)
        self.label21.setPixmap(self.ABP_image_resized)
        self.label21.adjustSize()
        self.label21.setGeometry(QtCore.QRect(40*layout_scale_factor, 80*layout_scale_factor, width_size, height_size))

        
        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        #print(ECG_raw_data[ECG_raw_data_index])
        ## To DO case id 변경 햇을때 이미지 적용하는 것
        
        #print(ECG_raw_data[ECG_raw_data_index])
        self.ECG_image=QtGui.QPixmap(Ecg_change_path)
        #self.ECG_image=QtGui.QPixmap(ECG_raw_data[ECG_raw_data_index])
        self.ECG_image_resized = self.ECG_image.scaled(width_size, height_size)
        self.label22.setPixmap(self.ECG_image_resized)
        self.label22.adjustSize()
        self.label22.setGeometry(QtCore.QRect(40*layout_scale_factor, 180*layout_scale_factor, width_size, height_size))

                
        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        #print(PPG_raw_data[PPG_raw_data_index])
        ## To DO case id 변경 햇을때 이미지 적용하는 것
        
        self.PPG_image=QtGui.QPixmap(Ppg_change_path)
        #self.PPG_image=QtGui.QPixmap(PPG_raw_data[PPG_raw_data_index])
        self.PPG_image_resized = self.PPG_image.scaled(width_size, height_size)
        self.label23.setPixmap(self.PPG_image_resized)
        self.label23.adjustSize()
        self.label23.setGeometry(QtCore.QRect(40*layout_scale_factor, 280*layout_scale_factor, width_size, height_size))
        
        width_size = 550*1.18*layout_scale_factor
        height_size = 90*layout_scale_factor
        #print(MBP_raw_data[MBP_raw_data_index])
        ## To DO case id 변경 햇을때 이미지 적용하는 것
                
        self.MBP_image=QtGui.QPixmap(Mbp_change_path)
        #self.MBP_image=QtGui.QPixmap(MBP_raw_data[MBP_raw_data_index])
        self.MBP_image_resized = self.MBP_image.scaled(width_size, height_size)
        self.label24.setPixmap(self.MBP_image_resized)
        self.label24.adjustSize()
        self.label24.setGeometry(QtCore.QRect(40*layout_scale_factor, 405*layout_scale_factor, width_size, height_size))
        
        self.label21.update()
        self.label22.update()
        self.label23.update()
        self.label24.update()
        self.label21.show()
        self.label22.show()
        self.label23.show()
        self.label24.show()


        ABP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ABP_raw_data_index).zfill(4))
        #print('ABP_raw_index',ABP_raw_index)
        ECG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ECG_raw_data_index).zfill(4))
        #print('ECG_raw_index',ECG_raw_index)
        PPG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(PPG_raw_data_index).zfill(4))
        #print('PPG_raw_index',PPG_raw_index)        
        MBP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(MBP_raw_data_index).zfill(4))
        #print('MBP_raw_index',MBP_raw_index)

        self.qle.setText(str(ABP_grade_value_list[ABP_raw_index][0]))
        self.qle.move(700*layout_scale_factor, 100*layout_scale_factor)
        self.qle.repaint()
        
        self.qle1.setText(str(ECG_grade_value_list[ECG_raw_index][0]))
        self.qle1.move(700*layout_scale_factor, 200*layout_scale_factor)
        self.qle1.repaint()
        
        self.qle2.setText(str(PPG_grade_value_list[PPG_raw_index][0]))
        self.qle2.move(700*layout_scale_factor, 300*layout_scale_factor)
        self.qle2.repaint()
                
        self.qle3.setText(str(MBP_grade_value_list[MBP_raw_index][0]))
        self.qle3.move(700*layout_scale_factor, 420*layout_scale_factor)
        self.qle3.repaint()
        
        #Segment id and ART segment id ECG segment id PPG segment id MBP segment id update
        Segment_id = str(Segment_id_data[case_raw_data_index])+str(ABP_raw_data_index).zfill(4)
        
        ABP_segment_id=str(Segment_id_data[case_raw_data_index])+str(ABP_raw_data_index).zfill(4)+'A'
        ECG_segment_id=str(Segment_id_data[case_raw_data_index])+str(ECG_raw_data_index).zfill(4)+'E'
        PPG_segment_id=str(Segment_id_data[case_raw_data_index])+str(PPG_raw_data_index).zfill(4)+'P'
        MBP_segment_id=str(Segment_id_data[case_raw_data_index])+str(MBP_raw_data_index).zfill(4)+'M'
        
        self.label1_1.setText(ABP_segment_id)
        self.label1_1.adjustSize()
        self.label1_1.repaint()
        
        self.label2_1.setText(ECG_segment_id)
        self.label2_1.adjustSize()
        self.label2_1.repaint()
        
        self.label3_1.setText(PPG_segment_id)
        self.label3_1.adjustSize()
        self.label3_1.repaint()
        
        self.label4_1.setText(MBP_segment_id)
        self.label4_1.adjustSize()
        self.label4_1.repaint()
        
        self.label9_2.setText(Segment_id)
        self.label9_2.adjustSize()
        self.label9_2.repaint()
        
        #save grade
        #self.btnRun_clicked5_1()


    def btnRun_clicked2(self,value):
        global ABP_raw_data_index
        global ECG_raw_data_index
        global PPG_raw_data_index
        global MBP_raw_data_index
        
        global Segment_id_data
        global case_raw_data_index
        global Segment_id_data_art
        global Segment_id_data_ecg
        global Segment_id_data_ppg
        global Segment_id_data_mbp
        
        global Case_id_data_total
        global data_index_count

        global case_raw_data_index
        global data_index_load_range
        global Segment_id_data_mbp_start_end

        global ABP_grade_value_list
        global ECG_grade_value_list
        global PPG_grade_value_list
        global MBP_grade_value_list

        case_raw_data_index = case_raw_data_index + 1
                
        if ABP_raw_data_index < 0:
            ABP_raw_data_index = 0
        if ECG_raw_data_index < 0:
            ECG_raw_data_index = 0
        if PPG_raw_data_index < 0:
            PPG_raw_data_index = 0
        if MBP_raw_data_index < 0:
            MBP_raw_data_index = 0
        if case_raw_data_index <0:
            case_raw_data_index = 0
            
        if case_raw_data_index >= len(Segment_id_data):
            case_raw_data_index = len(Segment_id_data) -1

        #print('Caculation data index boundary')
        #print('Segment id', Segment_id_data[case_raw_data_index])
        #print('data index count', data_index_count[Segment_id_data[case_raw_data_index]]) # 기존 전체 data index count
        '''        
        if ABP_raw_data_index >= data_index_count[Segment_id_data[case_raw_data_index]]:
            ABP_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]]  -1
        if ECG_raw_data_index  >= data_index_count[Segment_id_data[case_raw_data_index]]:
            ECG_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]]  -1
        if PPG_raw_data_index  >= data_index_count[Segment_id_data[case_raw_data_index]]:
            PPG_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]] -1
        if MBP_raw_data_index  >= data_index_count[Segment_id_data[case_raw_data_index]]:
            MBP_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]] -1
        '''
        global data_index_load_range
        #print('data index load file count', data_index_load_range[case_raw_data_index]) # load data index count
        if ABP_raw_data_index >=  data_index_load_range[case_raw_data_index]:
            ABP_raw_data_index =  data_index_load_range[case_raw_data_index]  -1
        if ECG_raw_data_index  >=  data_index_load_range[case_raw_data_index]:
            ECG_raw_data_index =  data_index_load_range[case_raw_data_index]  -1
        if PPG_raw_data_index  >=  data_index_load_range[case_raw_data_index]:
            PPG_raw_data_index =  data_index_load_range[case_raw_data_index]-1
        if MBP_raw_data_index  >=  data_index_load_range[case_raw_data_index]:
            MBP_raw_data_index =  data_index_load_range[case_raw_data_index] -1

        
        self.ABP_raw_data_index_number = ABP_raw_data_index
        self.ECG_raw_data_index_number = ECG_raw_data_index
        self.PPG_raw_data_index_number = PPG_raw_data_index
        self.MBP_raw_data_index_number = MBP_raw_data_index
        
                
        self.label13.setText(str(Segment_id_data[case_raw_data_index])+'/'+str(len(Segment_id_data)))
        self.label13.adjustSize()
        self.label13.repaint()
        self.label13.update()

        self.label12.setText(str(ABP_raw_data_index)+'/'+str(data_index_load_range[case_raw_data_index]-1))
        #self.label12.setText(str(ABP_raw_data_index)+'/'+str(data_index_count[Segment_id_data[case_raw_data_index]]))
        self.label12.adjustSize()
        self.label12.repaint()
        
        layout_scale_factor = 1.85
        
        #Case
        aa=ABP_raw_data[ABP_raw_data_index].split('/')
        aaa=aa[-1].split('_')
        bb=ECG_raw_data[ECG_raw_data_index].split('/')
        bbb=bb[-1].split('_')
        cc=PPG_raw_data[PPG_raw_data_index].split('/')
        ccc=cc[-1].split('_')
        dd=MBP_raw_data[MBP_raw_data_index].split('/')
        ddd=dd[-1].split('_')


        #현재 케이스 id에 따른 start index / end index
                                        
        #print(case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]) #start index
        #print(case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+1) #end index
        #print(Segment_id_data_mbp_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]])#start value
        #print(Segment_id_data_mbp_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+1]) #end value

        #start point
        #end point
        global file_root_path
        
        '''
        Abp_change_path = aaa[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_art_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]][1])+'_'+str(Segment_id_data_art_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+1][1])+'_'+aaa[4]
        Abp_change_path = file_root_path+Abp_change_path
        Ecg_change_path = bbb[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ecg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]][1])+'_'+str(Segment_id_data_ecg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+1][1])+'_'+aaa[4]
        Ecg_change_path = file_root_path+Ecg_change_path
        Ppg_change_path = ccc[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ppg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]][1])+'_'+str(Segment_id_data_ppg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+1][1])+'_'+aaa[4]
        Ppg_change_path = file_root_path+Ppg_change_path
        Mbp_change_path = ddd[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_mbp_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]][1])+'_'+str(Segment_id_data_mbp_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+1][1])+'_'+aaa[4]
        Mbp_change_path = file_root_path+Mbp_change_path
        print('ccc index')
        index_aa=0
        print(ABP_raw_data_index)
        if case_raw_data_index ==0:
            index_aa = ABP_raw_data_index
        else:
            for i in range(0,len(data_index_load_range[:case_raw_data_index])):
                index_aa=index_aa+int(data_index_load_range[i])+ABP_raw_data_index
        print('sum of the index',index_aa)
               
        #print(data_index_load_range[case_raw_data_index]*case_raw_data_index+ABP_raw_data_index) #[5,2,2]
        '''
        
        print('ccc index')
        index_aa=0
        #print(ABP_raw_data_index)
        if case_raw_data_index ==0:
            index_aa = ABP_raw_data_index
        else:
            for i in range(0,len(data_index_load_range[:case_raw_data_index])):
                index_aa=index_aa+int(data_index_load_range[i])+ABP_raw_data_index
        print('sum of the index',index_aa)
        if index_aa*2 == len(Segment_id_data_art_start_end):
            index_aa = index_aa -1
        #print(len(Segment_id_data_art_start_end))
        #print(data_index_load_range[case_raw_data_index]*case_raw_data_index+ABP_raw_data_index) #[5,2,2]
        
        Abp_change_path = aaa[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_art_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_art_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Abp_change_path = file_root_path+Abp_change_path
        Ecg_change_path = bbb[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ecg_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_ecg_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Ecg_change_path = file_root_path+Ecg_change_path
        Ppg_change_path = ccc[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ppg_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_ppg_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Ppg_change_path = file_root_path+Ppg_change_path
        Mbp_change_path = ddd[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_mbp_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_mbp_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Mbp_change_path = file_root_path+Mbp_change_path
        
        print('check 2')
        print(Abp_change_path)
        print(Ecg_change_path)
        print(Ppg_change_path)
        print(Mbp_change_path)
        
        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        
        self.ABP_image=QtGui.QPixmap(Abp_change_path)
        #self.ABP_image=QtGui.QPixmap(ABP_raw_data[ABP_raw_data_index])
        self.ABP_image_resized = self.ABP_image.scaled(width_size, height_size)
        self.label21.setPixmap(self.ABP_image_resized)
        self.label21.adjustSize()
        self.label21.setGeometry(QtCore.QRect(40*layout_scale_factor, 80*layout_scale_factor, width_size, height_size))
        
        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
    
        #print(ECG_raw_data[ECG_raw_data_index])
        self.ECG_image=QtGui.QPixmap(Ecg_change_path)
        #self.ECG_image=QtGui.QPixmap(ECG_raw_data[ECG_raw_data_index])
        self.ECG_image_resized = self.ECG_image.scaled(width_size, height_size)
        self.label22.setPixmap(self.ECG_image_resized)
        self.label22.adjustSize()
        self.label22.setGeometry(QtCore.QRect(40*layout_scale_factor, 180*layout_scale_factor, width_size, height_size))

        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor

        #print(PPG_raw_data[PPG_raw_data_index])
        self.PPG_image=QtGui.QPixmap(Ppg_change_path)
        #self.PPG_image=QtGui.QPixmap(PPG_raw_data[PPG_raw_data_index])
        self.PPG_image_resized = self.PPG_image.scaled(width_size, height_size)
        self.label23.setPixmap(self.PPG_image_resized)
        self.label23.adjustSize()
        self.label23.setGeometry(QtCore.QRect(40*layout_scale_factor, 280*layout_scale_factor, width_size, height_size))
        
        width_size = 550*1.18*layout_scale_factor
        height_size = 90*layout_scale_factor
        #print(MBP_raw_data[MBP_raw_data_index])
        
        self.MBP_image=QtGui.QPixmap(Mbp_change_path)
        #self.MBP_image=QtGui.QPixmap(MBP_raw_data[MBP_raw_data_index])
        self.MBP_image_resized = self.MBP_image.scaled(width_size, height_size)
        self.label24.setPixmap(self.MBP_image_resized)
        self.label24.adjustSize()
        self.label24.setGeometry(QtCore.QRect(40*layout_scale_factor, 405*layout_scale_factor, width_size, height_size))
        
        self.label21.update()
        self.label22.update()
        self.label23.update()
        self.label24.update()
        self.label21.show()
        self.label22.show()
        self.label23.show()
        self.label24.show()
        
        ABP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ABP_raw_data_index).zfill(4))
        #print('ABP_raw_index',ABP_raw_index)
        ECG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ECG_raw_data_index).zfill(4))
        #print('ECG_raw_index',ECG_raw_index)
        PPG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(PPG_raw_data_index).zfill(4))
        #print('PPG_raw_index',PPG_raw_index)        
        MBP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(MBP_raw_data_index).zfill(4))
        #print('MBP_raw_index',MBP_raw_index)

        self.qle.setText(str(ABP_grade_value_list[ABP_raw_index][0]))
        self.qle.move(700*layout_scale_factor, 100*layout_scale_factor)
        self.qle.repaint()
        
        self.qle1.setText(str(ECG_grade_value_list[ECG_raw_index][0]))
        self.qle1.move(700*layout_scale_factor, 200*layout_scale_factor)
        self.qle1.repaint()
        
        self.qle2.setText(str(PPG_grade_value_list[PPG_raw_index][0]))
        self.qle2.move(700*layout_scale_factor, 300*layout_scale_factor)
        self.qle2.repaint()
                
        self.qle3.setText(str(MBP_grade_value_list[MBP_raw_index][0]))
        self.qle3.move(700*layout_scale_factor, 420*layout_scale_factor)
        self.qle3.repaint()
        
        #Segment id and ART segment id ECG segment id  segment id MBP segment id update
        Segment_id = str(Segment_id_data[case_raw_data_index])+str(ABP_raw_data_index).zfill(4)
        
        ABP_segment_id = str(Segment_id_data[case_raw_data_index])+str(ABP_raw_data_index).zfill(4)+'A'
        ECG_segment_id = str(Segment_id_data[case_raw_data_index])+str(ECG_raw_data_index).zfill(4)+'E'
        PPG_segment_id = str(Segment_id_data[case_raw_data_index])+str(PPG_raw_data_index).zfill(4)+'P'
        MBP_segment_id = str(Segment_id_data[case_raw_data_index])+str(MBP_raw_data_index).zfill(4)+'M'
        
        self.label1_1.setText(ABP_segment_id)
        self.label1_1.adjustSize()
        self.label1_1.repaint()
        
        self.label2_1.setText(ECG_segment_id)
        self.label2_1.adjustSize()
        self.label2_1.repaint()
        
        self.label3_1.setText(PPG_segment_id)
        self.label3_1.adjustSize()
        self.label3_1.repaint()
        
        self.label4_1.setText(MBP_segment_id)
        self.label4_1.adjustSize()
        self.label4_1.repaint()
        
        self.label9_2.setText(Segment_id)
        self.label9_2.adjustSize()
        self.label9_2.repaint()
        
        #save grade
        #self.btnRun_clicked5_1()

    
    def btnRun_clicked7(self,value):
        #file value open to grade data load and repaint value
        global ABP_grade_value_list
        global ECG_grade_value_list
        global PPG_grade_value_list
        global MBP_grade_value_list
        global MBP_raw_data_index
        global PPG_raw_data_index
        global ECG_raw_data_index
        global ABP_raw_data_index
        global file_open_count
            
        layout_scale_factor = 1.85
        
        print('file open')
        FileFolder = QFileDialog.getOpenFileName(self,'Find Folder')
        f = open(FileFolder[0], 'r', encoding='utf-8')
        rdr = csv.reader(f)
        count = 1
        #print(len(ABP_grade_value_list)) #402451
        #print(len(ECG_grade_value_list)) #402451
        #print(len(PPG_grade_value_list)) #402451
        #print(len(MBP_grade_value_list)) #402451
                
        for line in rdr:
            #csv index 와 리스트 인덱스 차이가 2개 
            ABP_grade_value_list[count-2][0]=line[1]
            ECG_grade_value_list[count-2][0]=line[2]
            PPG_grade_value_list[count-2][0]=line[3]
            MBP_grade_value_list[count-2][0]=line[4]
            count = count +1
            
        #count initialization
        count=0
        f.close()

        #print('value check 1')
        #print(ABP_grade_value_list[122302])
        #print(ECG_grade_value_list[122302])
        #print(PPG_grade_value_list[122302])
        #print(MBP_grade_value_list[122302])
        print('load done')
        
        global case_id_data_index_matching_full
        global Case_id_data_total
        global ABP_raw_data_index
        global Segment_id_data
        global case_raw_data_index
        
        ABP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ABP_raw_data_index).zfill(4))
        ECG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ECG_raw_data_index).zfill(4))
        PPG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(PPG_raw_data_index).zfill(4))
        MBP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(MBP_raw_data_index).zfill(4))
        
        print('load value repaint')
        self.qle.setText(str(ABP_grade_value_list[ABP_raw_index][0]))
        self.qle.adjustSize()
        self.qle.repaint()
        self.qle1.setText(str(ECG_grade_value_list[ECG_raw_index][0]))
        self.qle1.adjustSize()
        self.qle1.repaint()
        self.qle2.setText(str(PPG_grade_value_list[PPG_raw_index][0]))
        self.qle2.adjustSize()
        self.qle2.repaint()
        self.qle3.setText(str(MBP_grade_value_list[MBP_raw_index][0]))
        self.qle3.adjustSize()
        self.qle3.repaint()

        ABP_grade_value_list_temp=[]
        ECG_grade_value_list_temp=[]
        PPG_grade_value_list_temp=[]
        MBP_grade_value_list_temp=[]
        global abp_count
        global ecg_count
        global ppg_count
        global mbp_count
        
        #Annotation Count remain function part
        for i in range(0,len(ABP_grade_value_list)-1):
            #print(ABP_grade_value_list[i][0])
            #print(type(ABP_grade_value_list[i][0]))
            ABP_grade_value_list_temp.append(int(ABP_grade_value_list[i][0]))
            ECG_grade_value_list_temp.append(int(ECG_grade_value_list[i][0]))
            PPG_grade_value_list_temp.append(int(PPG_grade_value_list[i][0]))
            MBP_grade_value_list_temp.append(int(MBP_grade_value_list[i][0]))
        #print(ABP_grade_value_list_temp)
        abp_count_array=np.array(ABP_grade_value_list_temp)
        ecg_count_array=np.array(ECG_grade_value_list_temp)
        ppg_count_array=np.array(PPG_grade_value_list_temp)
        mbp_count_array=np.array(MBP_grade_value_list_temp)
        abp_count=np.count_nonzero(abp_count_array)
        ecg_count=np.count_nonzero(ecg_count_array)
        ppg_count=np.count_nonzero(ppg_count_array)
        mbp_count=np.count_nonzero(mbp_count_array)
        print('annotation count')
        print(abp_count)
        print(ecg_count)
        print(ppg_count)
        print(mbp_count)
        
        self.label32.setText(str(abp_count))
        self.label32.adjustSize()
        self.label32.repaint()
        
        self.label34.setText(str(ecg_count))
        self.label34.adjustSize()
        self.label34.repaint()
        
        self.label36.setText(str(ppg_count))
        self.label36.adjustSize()
        self.label36.repaint()
        
        self.label38.setText(str(mbp_count))
        self.label38.adjustSize()
        self.label38.repaint()
        file_open_count = file_open_count+1
    
    def btnRun_clicked3(self,value):
        print('move button clicked <-')
        global ABP_raw_data_index
        global ECG_raw_data_index
        global PPG_raw_data_index
        global MBP_raw_data_index
        global case_raw_data_index
        
        global Segment_id_data
        global Segment_id_data_art
        global Segment_id_data_ecg
        global Segment_id_data_ppg
        global Segment_id_data_mbp
        
        global ABP_grade_value_list
        global ECG_grade_value_list
        global PPG_grade_value_list
        global MBP_grade_value_list

        global ABP_grade_data_annotation
        global ECG_grade_data_annotation
        global PPG_grade_data_annotation
        global MBP_grade_data_annotation

        global Case_id_data_total
        global case_raw_data_index
        global data_index_load_range
        global Segment_id_data_mbp_start_end
        
        letter = ""
        if isinstance(self.sender(), QtWidgets.QPushButton):
            letter = self.sender().text()
            print('button',letter)
        elif isinstance(self.sender(), QtWidgets.QShortcut):
            letter = self.sender().key().toString(QtGui.QKeySequence.NativeText)
            print('shortcut',letter)
       
        #self.slider.setValue(0)
        ABP_raw_data_index = ABP_raw_data_index -1
        ECG_raw_data_index = ECG_raw_data_index -1
        PPG_raw_data_index = PPG_raw_data_index -1
        MBP_raw_data_index = MBP_raw_data_index -1

        if ABP_raw_data_index < 0:
            ABP_raw_data_index = 0
        if ECG_raw_data_index < 0:
            ECG_raw_data_index = 0
        if PPG_raw_data_index < 0:
            PPG_raw_data_index = 0
        if MBP_raw_data_index < 0:
            MBP_raw_data_index = 0
        if case_raw_data_index <0:
            case_raw_data_index = 0
        '''
        if ABP_raw_data_index >= data_index_count[Segment_id_data[case_raw_data_index]]:
            ABP_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]]  -1
        if ECG_raw_data_index  >= data_index_count[Segment_id_data[case_raw_data_index]]:
            ECG_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]]  -1
        if PPG_raw_data_index  >= data_index_count[Segment_id_data[case_raw_data_index]]:
            PPG_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]] -1
        if MBP_raw_data_index  >= data_index_count[Segment_id_data[case_raw_data_index]]:
            MBP_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]] -1
        '''

        print('data index load file count', data_index_load_range[case_raw_data_index]) # load data index count
        if ABP_raw_data_index >=  data_index_load_range[case_raw_data_index]:
            ABP_raw_data_index =  data_index_load_range[case_raw_data_index]  -1
        if ECG_raw_data_index  >=  data_index_load_range[case_raw_data_index]:
            ECG_raw_data_index =  data_index_load_range[case_raw_data_index]  -1
        if PPG_raw_data_index  >=  data_index_load_range[case_raw_data_index]:
            PPG_raw_data_index =  data_index_load_range[case_raw_data_index]-1
        if MBP_raw_data_index  >=  data_index_load_range[case_raw_data_index]:
            MBP_raw_data_index =  data_index_load_range[case_raw_data_index] -1

        
        #To Do : Left button moving ABP_raw_data_annotation & ABP_raw_data_annotation & ABP_raw_data_annotation & ABP_raw_data_annotation count 유지
        #0이 아닌 값을 체크해서 annotation 갯수로 보여주면됨
        #print(len(ABP_grade_value_list))
        #print(ABP_grade_value_list[ABP_raw_data_index][0])
        #print(len(ECG_grade_value_list))
        #print(ECG_grade_value_list[ECG_raw_data_index][1])
        #print(len(PPG_grade_value_list))
        #print(PPG_grade_value_list[PPG_raw_data_index][2])
        #print(len(MBP_grade_value_list))
        #print(MBP_grade_value_list[MBP_raw_data_index][3])
        
        self.ABP_raw_data_index_number = ABP_grade_data_annotation
        self.ECG_raw_data_index_number = ECG_grade_data_annotation
        self.PPG_raw_data_index_number = PPG_grade_data_annotation
        self.MBP_raw_data_index_number = MBP_grade_data_annotation

        self.label12.setText(str(ABP_raw_data_index)+'/'+str(data_index_load_range[case_raw_data_index]-1))
        #self.label12.setText(str(ABP_raw_data_index)+'/'+str(data_index_count[Segment_id_data[case_raw_data_index]]))
        self.label12.adjustSize()
        self.label12.repaint()

        print('annotation count')
        global abp_count
        global ecg_count
        global ppg_count
        global mbp_count
        
        self.label32.setText(str(abp_count))
        self.label32.adjustSize()
        self.label32.repaint()
        
        self.label34.setText(str(ecg_count))
        self.label34.adjustSize()
        self.label34.repaint()
        
        self.label36.setText(str(ppg_count))
        self.label36.adjustSize()
        self.label36.repaint()
        
        self.label38.setText(str(mbp_count))
        self.label38.adjustSize()
        self.label38.repaint()
            
        layout_scale_factor = 1.85
        
        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        #print(ABP_raw_data[ABP_raw_data_index])
        
        #Case
        aa=ABP_raw_data[ABP_raw_data_index].split('/')
        aaa=aa[-1].split('_')
        bb=ECG_raw_data[ECG_raw_data_index].split('/')
        bbb=bb[-1].split('_')
        cc=PPG_raw_data[PPG_raw_data_index].split('/')
        ccc=cc[-1].split('_')
        dd=MBP_raw_data[MBP_raw_data_index].split('/')
        ddd=dd[-1].split('_')


        #현재 케이스 id에 따른 start index / end index
                                        
        #print(Segment_id_data_art_start_end[2*(ABP_raw_data_index)])
        #print(Segment_id_data_art_start_end[2*ABP_raw_data_index+1])
        
        Segment_id_data_ecg_start_end[2*(ABP_raw_data_index)]
        Segment_id_data_ecg_start_end[2*ABP_raw_data_index+1]
        
        Segment_id_data_ppg_start_end[2*(ABP_raw_data_index)]
        Segment_id_data_ppg_start_end[2*ABP_raw_data_index+1]
        
        Segment_id_data_mbp_start_end[2*(ABP_raw_data_index)]
        Segment_id_data_mbp_start_end[2*ABP_raw_data_index+1]
        
        #start point
        #end point
        print('index check here left move (<-)')
        #print(case_raw_data_index)
        #print(ABP_raw_data_index)
        global file_root_path
        print(str(Segment_id_data_art_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2][1])+'_'+str(Segment_id_data_art_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2+1][1]))
        '''
        Abp_change_path = aaa[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_art_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]][1])+'_'+str(Segment_id_data_art_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+1][1])+'_'+aaa[4]
        Abp_change_path = file_root_path+Abp_change_path
        Ecg_change_path = bbb[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ecg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]][1])+'_'+str(Segment_id_data_ecg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+1][1])+'_'+aaa[4]
        Ecg_change_path = file_root_path+Ecg_change_path
        Ppg_change_path = ccc[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ppg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]][1])+'_'+str(Segment_id_data_ppg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+1][1])+'_'+aaa[4]
        Ppg_change_path = file_root_path+Ppg_change_path
        Mbp_change_path = ddd[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_mbp_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]][1])+'_'+str(Segment_id_data_mbp_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+1][1])+'_'+aaa[4]
        Mbp_change_path = file_root_path+Mbp_change_path

        '''
        print('ccc index')
        index_aa=0
        #print(ABP_raw_data_index)
        if case_raw_data_index ==0:
            index_aa = ABP_raw_data_index
        else:
            for i in range(0,len(data_index_load_range[:case_raw_data_index])):
                index_aa=index_aa+int(data_index_load_range[i])+ABP_raw_data_index
        print('sum of the index',index_aa)
        if index_aa*2 == len(Segment_id_data_art_start_end):
            index_aa = index_aa -1
        print(len(Segment_id_data_art_start_end))

        
        #print(data_index_load_range[case_raw_data_index]*case_raw_data_index+ABP_raw_data_index) #[5,2,2]

        Abp_change_path = aaa[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_art_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_art_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Abp_change_path = file_root_path+Abp_change_path
        Ecg_change_path = bbb[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ecg_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_ecg_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Ecg_change_path = file_root_path+Ecg_change_path
        Ppg_change_path = ccc[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ppg_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_ppg_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Ppg_change_path = file_root_path+Ppg_change_path
        Mbp_change_path = ddd[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_mbp_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_mbp_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Mbp_change_path = file_root_path+Mbp_change_path
        
        print('check 3')
        print(Abp_change_path)
        print(Ecg_change_path)
        print(Ppg_change_path)
        print(Mbp_change_path)
        
        self.ABP_image=QtGui.QPixmap(Abp_change_path)
        #self.ABP_image=QtGui.QPixmap(ABP_raw_data[ABP_raw_data_index])
        self.ABP_image_resized = self.ABP_image.scaled(width_size, height_size)
        self.label21.setPixmap(self.ABP_image_resized)
        self.label21.adjustSize()
        self.label21.setGeometry(QtCore.QRect(40*layout_scale_factor, 80*layout_scale_factor, width_size, height_size))
        
        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        #print(ECG_raw_data[ECG_raw_data_index])
        
        self.ECG_image=QtGui.QPixmap(Ecg_change_path)
        #self.ECG_image=QtGui.QPixmap(ECG_raw_data[ECG_raw_data_index])
        self.ECG_image_resized = self.ECG_image.scaled(width_size, height_size)
        self.label22.setPixmap(self.ECG_image_resized)
        self.label22.adjustSize()
        self.label22.setGeometry(QtCore.QRect(40*layout_scale_factor, 180*layout_scale_factor, width_size, height_size))
                
        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        #print(PPG_raw_data[PPG_raw_data_index])
        
        self.PPG_image=QtGui.QPixmap(Ppg_change_path)
        #self.PPG_image=QtGui.QPixmap(PPG_raw_data[PPG_raw_data_index])
        self.PPG_image_resized = self.PPG_image.scaled(width_size, height_size)
        self.label23.setPixmap(self.PPG_image_resized)
        self.label23.adjustSize()
        self.label23.setGeometry(QtCore.QRect(40*layout_scale_factor, 280*layout_scale_factor, width_size, height_size))

        width_size = 550*1.18*layout_scale_factor
        height_size = 90*layout_scale_factor
        #print(MBP_raw_data[MBP_raw_data_index])
        
        self.MBP_image=QtGui.QPixmap(Mbp_change_path)
        #self.MBP_image=QtGui.QPixmap(MBP_raw_data[MBP_raw_data_index])
        self.MBP_image_resized = self.MBP_image.scaled(width_size, height_size)
        self.label24.setPixmap(self.MBP_image_resized)
        self.label24.setGeometry(QtCore.QRect(40*layout_scale_factor, 405*layout_scale_factor, width_size, height_size))

        self.label21.update()
        self.label22.update()
        self.label23.update()
        self.label24.update()
        self.label21.show()
        self.label22.show()
        self.label23.show()
        self.label24.show()
                
        ABP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ABP_raw_data_index).zfill(4))
        print('ABP_raw_index',ABP_raw_index)
        ECG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ECG_raw_data_index).zfill(4))
        print('ECG_raw_index',ECG_raw_index)
        PPG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(PPG_raw_data_index).zfill(4))
        print('PPG_raw_index',PPG_raw_index)        
        MBP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(MBP_raw_data_index).zfill(4))
        print('MBP_raw_index',MBP_raw_index)

        self.qle.setText(str(ABP_grade_value_list[ABP_raw_index][0]))
        self.qle.move(700*layout_scale_factor, 100*layout_scale_factor)
        self.qle.repaint()
        
        self.qle1.setText(str(ECG_grade_value_list[ECG_raw_index][0]))
        self.qle1.move(700*layout_scale_factor, 200*layout_scale_factor)
        self.qle1.repaint()
        
        self.qle2.setText(str(PPG_grade_value_list[PPG_raw_index][0]))
        self.qle2.move(700*layout_scale_factor, 300*layout_scale_factor)
        self.qle2.repaint()
                
        self.qle3.setText(str(MBP_grade_value_list[MBP_raw_index][0]))
        self.qle3.move(700*layout_scale_factor, 420*layout_scale_factor)
        self.qle3.repaint()
        
        #Segment id and ART segment id ECG segment id PPG segment id MBP segment id update
        Segment_id = str(Segment_id_data[case_raw_data_index])+str(ABP_raw_data_index).zfill(4)
        ABP_segment_id=str(Segment_id_data[case_raw_data_index])+str(ABP_raw_data_index).zfill(4)+'A'
        ECG_segment_id=str(Segment_id_data[case_raw_data_index])+str(ECG_raw_data_index).zfill(4)+'E'
        PPG_segment_id=str(Segment_id_data[case_raw_data_index])+str(PPG_raw_data_index).zfill(4)+'P'
        MBP_segment_id=str(Segment_id_data[case_raw_data_index])+str(MBP_raw_data_index).zfill(4)+'M'
        
        self.label1_1.setText(ABP_segment_id)
        self.label1_1.adjustSize()
        self.label1_1.repaint()
        
        self.label2_1.setText(ECG_segment_id)
        self.label2_1.adjustSize()
        self.label2_1.repaint()
        
        self.label3_1.setText(PPG_segment_id)
        self.label3_1.adjustSize()
        self.label3_1.repaint()
        
        self.label4_1.setText(MBP_segment_id)
        self.label4_1.adjustSize()
        self.label4_1.repaint()

        self.label9_2.setText(Segment_id)
        self.label9_2.adjustSize()
        self.label9_2.repaint()
        
        #save grade
        #self.btnRun_clicked5_1()

    #move button clicked ->
    def btnRun_clicked4(self,value):
        print('move button clicked ->')
    
        #print('slider value 2')
        #print(value)
        global ABP_raw_data_index
        global ECG_raw_data_index
        global PPG_raw_data_index
        global MBP_raw_data_index
        global case_raw_data_index
        
        global Segment_id_data
        global Segment_id_data_art
        global Segment_id_data_ecg
        global Segment_id_data_ppg
        global Segment_id_data_mbp
        
        global ABP_grade_value_list
        global ECG_grade_value_list
        global PPG_grade_value_list
        global MBP_grade_value_list

        global ABP_grade_data_annotation
        global ECG_grade_data_annotation
        global PPG_grade_data_annotation
        global MBP_grade_data_annotation

        global Case_id_data_total
        global case_raw_data_index
        global data_index_load_range
        global Segment_id_data_mbp_start_end
        
        
        letter = ""
        if isinstance(self.sender(), QtWidgets.QPushButton):
            letter = self.sender().text()
            print('button',letter)
        elif isinstance(self.sender(), QtWidgets.QShortcut):
            letter = self.sender().key().toString(QtGui.QKeySequence.NativeText)
            print('shortcut',letter)
        
        #self.slider.setValue(0)
        ABP_raw_data_index = ABP_raw_data_index +1
        ECG_raw_data_index = ECG_raw_data_index +1
        PPG_raw_data_index = PPG_raw_data_index +1
        MBP_raw_data_index = MBP_raw_data_index +1

        if ABP_raw_data_index < 0:
            ABP_raw_data_index = 0
        if ECG_raw_data_index < 0:
            ECG_raw_data_index = 0
        if PPG_raw_data_index < 0:
            PPG_raw_data_index = 0
        if MBP_raw_data_index < 0:
            MBP_raw_data_index = 0
            
        '''
        if ABP_raw_data_index >= data_index_count[Segment_id_data[case_raw_data_index]]:
            ABP_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]]  -1
        if ECG_raw_data_index  >= data_index_count[Segment_id_data[case_raw_data_index]]:
            ECG_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]]  -1
        if PPG_raw_data_index  >= data_index_count[Segment_id_data[case_raw_data_index]]:
            PPG_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]] -1
        if MBP_raw_data_index  >= data_index_count[Segment_id_data[case_raw_data_index]]:
            MBP_raw_data_index = data_index_count[Segment_id_data[case_raw_data_index]] -1
        '''
        global data_index_load_range
        print('data index load file count', data_index_load_range[case_raw_data_index]) # load data index count
        if ABP_raw_data_index >=  data_index_load_range[case_raw_data_index]:
            ABP_raw_data_index =  data_index_load_range[case_raw_data_index]  -1
        if ECG_raw_data_index  >=  data_index_load_range[case_raw_data_index]:
            ECG_raw_data_index =  data_index_load_range[case_raw_data_index]  -1
        if PPG_raw_data_index  >=  data_index_load_range[case_raw_data_index]:
            PPG_raw_data_index =  data_index_load_range[case_raw_data_index]-1
        if MBP_raw_data_index  >=  data_index_load_range[case_raw_data_index]:
            MBP_raw_data_index =  data_index_load_range[case_raw_data_index] -1

        
        self.ABP_raw_data_index_number = ABP_grade_data_annotation
        self.ECG_raw_data_index_number = ECG_grade_data_annotation
        self.PPG_raw_data_index_number = PPG_grade_data_annotation
        self.MBP_raw_data_index_number = MBP_grade_data_annotation

        self.label12.setText(str(ABP_raw_data_index)+'/'+str(data_index_load_range[case_raw_data_index]-1))
        #self.label12.setText(str(ABP_raw_data_index)+'/'+str(data_index_count[Segment_id_data[case_raw_data_index]]))
        self.label12.adjustSize()
        self.label12.repaint()

        print('annotation count')
        global abp_count
        global ecg_count
        global ppg_count
        global mbp_count
        
        self.label32.setText(str(abp_count))
        self.label32.adjustSize()
        self.label32.repaint()
        
        self.label34.setText(str(ecg_count))
        self.label34.adjustSize()
        self.label34.repaint()
        
        self.label36.setText(str(ppg_count))
        self.label36.adjustSize()
        self.label36.repaint()
        
        self.label38.setText(str(mbp_count))
        self.label38.adjustSize()
        self.label38.repaint()

                
        #Case
        aa=ABP_raw_data[ABP_raw_data_index].split('/')
        aaa=aa[-1].split('_')
        bb=ECG_raw_data[ECG_raw_data_index].split('/')
        bbb=bb[-1].split('_')
        cc=PPG_raw_data[PPG_raw_data_index].split('/')
        ccc=cc[-1].split('_')
        dd=MBP_raw_data[MBP_raw_data_index].split('/')
        ddd=dd[-1].split('_')


        #현재 케이스 id에 따른 start index / end index
        
        #start point
        #end point
        global file_root_path
        #print('case_raw_data_index', case_raw_data_index)

        #print('index check here')
        #print(case_raw_data_index)
        #print(ABP_raw_data_index)
        #print(ECG_raw_data_index)
        #print(PPG_raw_data_index)
        #print(MBP_raw_data_index)

        print(str(Segment_id_data_art_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2][1])+'_'+str(Segment_id_data_art_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2+1][1]))
        '''
        Abp_change_path = aaa[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_art_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2][1])+'_'+str(Segment_id_data_art_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2+1][1])+'_'+aaa[4]
        Abp_change_path = file_root_path+Abp_change_path
        Ecg_change_path = bbb[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ecg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2][1])+'_'+str(Segment_id_data_ecg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2+1][1])+'_'+aaa[4]
        Ecg_change_path = file_root_path+Ecg_change_path
        Ppg_change_path = ccc[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ppg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2][1])+'_'+str(Segment_id_data_ppg_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2+1][1])+'_'+aaa[4]
        Ppg_change_path = file_root_path+Ppg_change_path
        Mbp_change_path = ddd[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_mbp_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2][1])+'_'+str(Segment_id_data_mbp_start_end[case_raw_data_index*2*data_index_load_range[case_raw_data_index-1]+2+1][1])+'_'+aaa[4]
        Mbp_change_path = file_root_path+Mbp_change_path
        '''
        print('ccc index')
        index_aa=0
        print(ABP_raw_data_index)
        if case_raw_data_index ==0:
            index_aa = ABP_raw_data_index
        else:
            for i in range(0,len(data_index_load_range[:case_raw_data_index])):
                index_aa=index_aa+int(data_index_load_range[i])+ABP_raw_data_index
        print('sum of the index',index_aa)
        if index_aa*2 == len(Segment_id_data_art_start_end):
            index_aa = index_aa -1
        
        Abp_change_path = aaa[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_art_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_art_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Abp_change_path = file_root_path+Abp_change_path
        Ecg_change_path = bbb[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ecg_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_ecg_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Ecg_change_path = file_root_path+Ecg_change_path
        Ppg_change_path = ccc[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_ppg_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_ppg_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Ppg_change_path = file_root_path+Ppg_change_path
        Mbp_change_path = ddd[0]+'_'+str(Segment_id_data[case_raw_data_index])+'_'+str(Segment_id_data_mbp_start_end[2*(index_aa)][1])+'_'+str(Segment_id_data_mbp_start_end[2*(index_aa)+1][1])+'_'+aaa[4]
        Mbp_change_path = file_root_path+Mbp_change_path
        
        #print(data_index_load_range[case_raw_data_index]*case_raw_data_index+ABP_raw_data_index) #[5,2,2]

        print('check 4')
        print(Abp_change_path)
        print(Ecg_change_path)
        print(Ppg_change_path)
        print(Mbp_change_path)
        
        layout_scale_factor = 1.85
        
        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor

        self.ABP_image=QtGui.QPixmap(Abp_change_path)
        #self.ABP_image=QtGui.QPixmap(ABP_raw_data[ABP_raw_data_index])
        self.ABP_image_resized = self.ABP_image.scaled(width_size, height_size)
        self.label21.setPixmap(self.ABP_image_resized)
        self.label21.setGeometry(QtCore.QRect(40*layout_scale_factor, 80*layout_scale_factor, width_size, height_size))
        self.label21.update()
        self.label21.show()

        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        
        self.ECG_image=QtGui.QPixmap(Ecg_change_path)
        #self.ECG_image=QtGui.QPixmap(ECG_raw_data[ECG_raw_data_index])
        self.ECG_image_resized = self.ECG_image.scaled(width_size, height_size)
        self.label22.setPixmap(self.ECG_image_resized)
        self.label22.setGeometry(QtCore.QRect(40*layout_scale_factor, 180*layout_scale_factor, width_size, height_size))
        self.label22.update()
        self.label22.show()

        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        
        self.PPG_image=QtGui.QPixmap(Ppg_change_path)
        #self.PPG_image=QtGui.QPixmap(PPG_raw_data[PPG_raw_data_index])
        self.PPG_image_resized = self.PPG_image.scaled(width_size, height_size)
        self.label23.setPixmap(self.PPG_image_resized)
        self.label23.setGeometry(QtCore.QRect(40*layout_scale_factor, 280*layout_scale_factor, width_size, height_size))
        self.label23.update()
        self.label23.show()

        width_size = 550*1.18*layout_scale_factor
        height_size = 90*layout_scale_factor
        
        self.MBP_image=QtGui.QPixmap(Mbp_change_path)
        #self.MBP_image=QtGui.QPixmap(MBP_raw_data[MBP_raw_data_index])
        self.MBP_image_resized = self.MBP_image.scaled(width_size, height_size)
        self.label24.setPixmap(self.MBP_image_resized)
        self.label24.setGeometry(QtCore.QRect(40*layout_scale_factor, 405*layout_scale_factor, width_size, height_size))
        self.label24.update()
        self.label24.show()
                    
        ABP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ABP_raw_data_index).zfill(4))
        print('ABP_raw_index',ABP_raw_index)
        ECG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(ECG_raw_data_index).zfill(4))
        print('ECG_raw_index',ECG_raw_index)
        PPG_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(PPG_raw_data_index).zfill(4))
        print('PPG_raw_index',PPG_raw_index)        
        MBP_raw_index=case_id_data_index_matching_full.index(Segment_id_data[case_raw_data_index]+str(MBP_raw_data_index).zfill(4))
        print('MBP_raw_index',MBP_raw_index)

        self.qle.setText(str(ABP_grade_value_list[ABP_raw_index][0]))
        self.qle.move(700*layout_scale_factor, 100*layout_scale_factor)
        self.qle.repaint()
        
        self.qle1.setText(str(ECG_grade_value_list[ECG_raw_index][0]))
        self.qle1.move(700*layout_scale_factor, 200*layout_scale_factor)
        self.qle1.repaint()
        
        self.qle2.setText(str(PPG_grade_value_list[PPG_raw_index][0]))
        self.qle2.move(700*layout_scale_factor, 300*layout_scale_factor)
        self.qle2.repaint()
                
        self.qle3.setText(str(MBP_grade_value_list[MBP_raw_index][0]))
        self.qle3.move(700*layout_scale_factor, 420*layout_scale_factor)
        self.qle3.repaint()
        
        #Segment id and ART segment id ECG segment id PPG segment id MBP segment id update
        Segment_id = str(Segment_id_data[case_raw_data_index])+str(ABP_raw_data_index).zfill(4)
        ABP_segment_id=str(Segment_id_data[case_raw_data_index])+str(ABP_raw_data_index).zfill(4)+'A'
        ECG_segment_id=str(Segment_id_data[case_raw_data_index])+str(ECG_raw_data_index).zfill(4)+'E'
        PPG_segment_id=str(Segment_id_data[case_raw_data_index])+str(PPG_raw_data_index).zfill(4)+'P'
        MBP_segment_id=str(Segment_id_data[case_raw_data_index])+str(MBP_raw_data_index).zfill(4)+'M'
        
        self.label1_1.setText(ABP_segment_id)
        self.label1_1.adjustSize()
        self.label1_1.repaint()
        
        self.label2_1.setText(ECG_segment_id)
        self.label2_1.adjustSize()
        self.label2_1.repaint()
        
        self.label3_1.setText(PPG_segment_id)
        self.label3_1.adjustSize()
        self.label3_1.repaint()
        
        self.label4_1.setText(MBP_segment_id)
        self.label4_1.adjustSize()
        self.label4_1.repaint()

        self.label9_2.setText(Segment_id)
        self.label9_2.adjustSize()
        self.label9_2.repaint()
        
        #save grade
        #self.btnRun_clicked5_1()

    def btnRun_clicked5(self):
        #save button event
        print('save_grade')
        import pandas as pd
        #global grade_value_list
                            
        global ABP_grade_value_list
        global ECG_grade_value_list
        global PPG_grade_value_list
        global MBP_grade_value_list

        global ABP_raw_data_index
        global ECG_raw_data_index
        global PPG_raw_data_index
        global MBP_raw_data_index
        global case_raw_data_index
        
        global ABP_grade_data_annotation
        global ECG_grade_data_annotation
        global PPG_grade_data_annotation
        global MBP_grade_data_annotation
    
        global concat_grade_value_list
        global case_id_data_index_matching_full

        global Case_id_data_total
        global case_raw_data_index
        global data_index_load_range
        global Segment_id_data_mbp_start_end


        global abp_count
        global ecg_count
        global ppg_count
        global mbp_count
        global file_open_count

        if file_open_count>=1:
            print('ccccccccccccccccccccaaaaaaaaaaaaa')
            abp_count=0
            ecg_count=0
            ppg_count=0
            mbp_count=0
            print(len(case_id_data_index_matching_full))
            print(len(ABP_grade_value_list))
            
            ABP_temp=[]
            for i in range(0,len(case_id_data_index_matching_full)-1):
                ABP_temp.append([case_id_data_index_matching_full[i],ABP_grade_value_list[i][0]])
                        
            a = [x + y for x, y in zip(ABP_temp,ECG_grade_value_list)]
            b = [x + y for x, y in zip(PPG_grade_value_list,MBP_grade_value_list)]
            concat_grade = [x + y for x, y in zip(a,b)]
            #print(c[0])
            df = pd.DataFrame(concat_grade,columns=['Segment_id','ART_Grade','ECG_Grade','PPG_Grade',
            'MBP_Grade'])
            df.to_csv(file_root_path2+'data_grade_save.csv', index=False, encoding='cp949')

            #Annotation Count remain function part
            print(file_open_count)
            ABP_grade_value_list_temp=[]
            ECG_grade_value_list_temp=[]
            PPG_grade_value_list_temp=[]
            MBP_grade_value_list_temp=[]
        
            for i in range(0,len(ABP_grade_value_list)-1):
                ABP_grade_value_list_temp.append(int(ABP_grade_value_list[i][0]))
                ECG_grade_value_list_temp.append(int(ECG_grade_value_list[i][0]))
                PPG_grade_value_list_temp.append(int(PPG_grade_value_list[i][0]))
                MBP_grade_value_list_temp.append(int(MBP_grade_value_list[i][0]))
            abp_count_array=np.array(ABP_grade_value_list_temp)
            ecg_count_array=np.array(ECG_grade_value_list_temp)
            ppg_count_array=np.array(PPG_grade_value_list_temp)
            mbp_count_array=np.array(MBP_grade_value_list_temp)
            abp_count=np.count_nonzero(abp_count_array)
            ecg_count=np.count_nonzero(ecg_count_array)
            ppg_count=np.count_nonzero(ppg_count_array)
            mbp_count=np.count_nonzero(mbp_count_array)
            print(abp_count)
            print(ecg_count)
            print(ppg_count)
            print(mbp_count)
        else:
            print('ccccccccccccccccccccbbbb')
            print(len(case_id_data_index_matching_full))
            print(len(ABP_grade_value_list))
            
            ABP_temp=[]
            for i in range(0,len(case_id_data_index_matching_full)-1):
                ABP_temp.append([case_id_data_index_matching_full[i],ABP_grade_value_list[i][0]])
                        
            a = [x + y for x, y in zip(ABP_temp,ECG_grade_value_list)]
            b = [x + y for x, y in zip(PPG_grade_value_list,MBP_grade_value_list)]
            concat_grade = [x + y for x, y in zip(a,b)]
            #print(c[0])
            df = pd.DataFrame(concat_grade,columns=['Segment_id','ART_Grade','ECG_Grade','PPG_Grade','MBP_Grade'])
            df.to_csv(file_root_path2+'data_grade_save.csv', index=False, encoding='cp949')

            #Annotation Count remain function part
            #print(file_open_count)
            ABP_grade_value_list_temp=[]
            ECG_grade_value_list_temp=[]
            PPG_grade_value_list_temp=[]
            MBP_grade_value_list_temp=[]
        
            for i in range(0,len(ABP_grade_value_list)-1):
                ABP_grade_value_list_temp.append(int(ABP_grade_value_list[i][0]))
                ECG_grade_value_list_temp.append(int(ECG_grade_value_list[i][0]))
                PPG_grade_value_list_temp.append(int(PPG_grade_value_list[i][0]))
                MBP_grade_value_list_temp.append(int(MBP_grade_value_list[i][0]))
            #print(ABP_grade_value_list_temp)
            #print(len(ABP_grade_value_list_temp))
            abp_count_array=np.array(ABP_grade_value_list_temp)
            ecg_count_array=np.array(ECG_grade_value_list_temp)
            ppg_count_array=np.array(PPG_grade_value_list_temp)
            mbp_count_array=np.array(MBP_grade_value_list_temp)
         
            abp_count=np.count_nonzero(abp_count_array)
            ecg_count=np.count_nonzero(ecg_count_array)
            ppg_count=np.count_nonzero(ppg_count_array)
            mbp_count=np.count_nonzero(mbp_count_array)
            print(abp_count)
            print(ecg_count)
            print(ppg_count)
            print(mbp_count)

        self.label32.setText(str(abp_count))
        self.label32.adjustSize()
        self.label32.repaint()
        
        self.label34.setText(str(ecg_count))
        self.label34.adjustSize()
        self.label34.repaint()
        
        self.label36.setText(str(ppg_count))
        self.label36.adjustSize()
        self.label36.repaint()
        
        self.label38.setText(str(mbp_count))
        self.label38.adjustSize()
        self.label38.repaint()
        print('---')#Annotation Count remain function part


    def btnRun_clicked6(self):
        '''
        another path save button event
        Save as button
        '''
        print('save_as grade')
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', './')
        #print(FileSave[0]) data path and name
        import pandas as pd
                            
        global ABP_grade_value_list
        global ECG_grade_value_list
        global PPG_grade_value_list
        global MBP_grade_value_list

        global ABP_raw_data_index
        global ECG_raw_data_index
        global PPG_raw_data_index
        global MBP_raw_data_index
        global case_raw_data_index
        
        global ABP_grade_data_annotation
        global ECG_grade_data_annotation
        global PPG_grade_data_annotation
        global MBP_grade_data_annotation
    
        global concat_grade_value_list
        global case_id_data_index_matching_full

        global Case_id_data_total
        global case_raw_data_index
        global data_index_load_range
        global Segment_id_data_mbp_start_end

        global abp_count
        global ecg_count
        global ppg_count
        global mbp_count
        global file_open_count
        
        ABP_temp=[]
        for i in range(0,len(case_id_data_index_matching_full)-1):
            ABP_temp.append([case_id_data_index_matching_full[i],ABP_grade_value_list[i][0]])
                    
        a = [x + y for x, y in zip(ABP_temp,ECG_grade_value_list)]
        b = [x + y for x, y in zip(PPG_grade_value_list,MBP_grade_value_list)]
        concat_grade = [x + y for x, y in zip(a,b)]
        #print(c[0])
        df = pd.DataFrame(concat_grade,columns=['Segment_id','ART_Grade','ECG_Grade','PPG_Grade',
        'MBP_Grade'])
        df.to_csv(str(FileSave[0]), index=False, encoding='cp949')
        
        #Annotation Count remain function part
        ABP_grade_value_list_temp=[]
        ECG_grade_value_list_temp=[]
        PPG_grade_value_list_temp=[]
        MBP_grade_value_list_temp=[]

        #print(ABP_grade_value_list_temp)
        for i in range(0,len(ABP_grade_value_list)-1):
            ABP_grade_value_list_temp.append(int(ABP_grade_value_list[i][0]))
            ECG_grade_value_list_temp.append(int(ECG_grade_value_list[i][0]))
            PPG_grade_value_list_temp.append(int(PPG_grade_value_list[i][0]))
            MBP_grade_value_list_temp.append(int(MBP_grade_value_list[i][0]))
        abp_count_array=np.array(ABP_grade_value_list_temp)
        ecg_count_array=np.array(ECG_grade_value_list_temp)
        ppg_count_array=np.array(PPG_grade_value_list_temp)
        mbp_count_array=np.array(MBP_grade_value_list_temp)
        abp_count=np.count_nonzero(abp_count_array)
        ecg_count=np.count_nonzero(ecg_count_array)
        ppg_count=np.count_nonzero(ppg_count_array)
        mbp_count=np.count_nonzero(mbp_count_array)
        print(abp_count)
        print(ecg_count)
        print(ppg_count)
        print(mbp_count)
        
        self.label32.setText(str(abp_count))
        self.label32.adjustSize()
        self.label32.repaint()
        
        self.label34.setText(str(ecg_count))
        self.label34.adjustSize()
        self.label34.repaint()
        
        self.label36.setText(str(ppg_count))
        self.label36.adjustSize()
        self.label36.repaint()
        
        self.label38.setText(str(mbp_count))
        self.label38.adjustSize()
        self.label38.repaint()
        print('---')#Annotation Count remain function part


    def keyPressEvent(self, e):
        
        #방향키 이벤트 적용한 것
        
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_F13:
            print("Key A")
            #self.showFullScreen()
            self.btnRun_clicked1(self)
            #self.btn1.clicked.connect(self.btnRun_clicked1)
        elif e.key() == Qt.Key_F14:
            print("Key D")
            #self.showNormal()
            self.btnRun_clicked2(self)
            #self.btn2.clicked.connect(self.btnRun_clicked2)
        elif e.key() == Qt.Key_F15:
            print("Key Z")
            #self.showFullScreen()
            #self.btn3.clicked.connect(self.btnRun_clicked3)
            self.btnRun_clicked3(self)
        elif e.key() == Qt.Key_F16:
            print("Key C")
            #self.showNormal()
            self.btnRun_clicked4(self)
            #self.btn4.clicked.connect(self.btnRun_clicked4)
            

    def value_changed_case_index(self, value):
        print(value) #case index
        print('slider value 1')
        global case_raw_data_index
        case_raw_data_index=(value-1)
        
    def value_changed_data_index(self, value):
        print(value) #Data id index
        print('slider value 2')
        global ABP_raw_data_index
        global ECG_raw_data_index
        global PPG_raw_data_index
        global MBP_raw_data_index
        ABP_raw_data_index=(value-1)
        ECG_raw_data_index=(value-1)
        PPG_raw_data_index=(value-1)
        MBP_raw_data_index=(value-1)

    
    def initUI(self):
        global case_raw_data_index
        
        global ABP_grade_value_list
        global ECG_grade_value_list
        global PPG_grade_value_list
        global MBP_grade_value_list
        
        global Segment_id_data_total
        global Case_id_data_total
        global data_index_load_range

        #Grade value initalizaiton
        temp=[]
        print(len(case_id_data_index_matching_full))
        for i in range(0,len(case_id_data_index_matching_full)):
            ABP_grade_value_list.append([0])
            ECG_grade_value_list.append([0])
            PPG_grade_value_list.append([0])
            MBP_grade_value_list.append([0])
            temp.append([case_id_data_index_matching_full[i],0])
            
        a = [x + y for x, y in zip(temp,ECG_grade_value_list)]
        b = [x + y for x, y in zip(PPG_grade_value_list,MBP_grade_value_list)]
        concat_grade = [x + y for x, y in zip(a,b)]
                    
        df = pd.DataFrame(concat_grade,columns=['Segment_id','ART_Grade','ECG_Grade','PPG_Grade',
        'MBP_Grade'])
        df.to_csv(file_root_path2+'data_grade_initalization.csv', index=False, encoding='cp949')
        
        layout_scale_factor = 1.85
        
        label1 = QLabel('ART', self)
        label1.move(5, 80*layout_scale_factor)
        label2 = QLabel('ECG', self)
        label2.move(5, 180*layout_scale_factor)
        label3 = QLabel('PPG', self)
        label3.move(5, 280*layout_scale_factor)
        label4 = QLabel('MBP', self)
        label4.move(5, 405*layout_scale_factor)

        #Case id 만 적용 index id 만들어야 함 (아직 index id 적용되어 있지 않음)
        Segment_id = str(Segment_id_data[case_raw_data_index])+str(ABP_raw_data_index).zfill(4)
        ABP_segment_id=str(Segment_id_data[ABP_raw_data_index])+str(ABP_raw_data_index).zfill(4)+'A'
        ECG_segment_id=str(Segment_id_data[ECG_raw_data_index])+str(ECG_raw_data_index).zfill(4)+'E'
        PPG_segment_id=str(Segment_id_data[PPG_raw_data_index])+str(PPG_raw_data_index).zfill(4)+'P'
        MBP_segment_id=str(Segment_id_data[MBP_raw_data_index])+str(MBP_raw_data_index).zfill(4)+'M'
    
        self.label1_1 = QLabel(ABP_segment_id, self)
        self.label1_1.move(5, 90*layout_scale_factor)
        self.label2_1 = QLabel(ECG_segment_id, self)
        self.label2_1.move(5, 190*layout_scale_factor)
        self.label3_1 = QLabel(PPG_segment_id, self)
        self.label3_1.move(5, 290*layout_scale_factor)
        self.label4_1 = QLabel(MBP_segment_id, self)
        self.label4_1.move(5, 415*layout_scale_factor)
        
        self.label31 = QLabel('ART Grade', self)
        self.label31.move(700*layout_scale_factor, 80*layout_scale_factor)
        
        self.label32 = QLabel(str(self.ABP_raw_data_index_number), self)
        self.label32.move(700*layout_scale_factor, 130*layout_scale_factor)
        
        self.label33 = QLabel('ECG Grade', self)
        self.label33.move(700*layout_scale_factor, 180*layout_scale_factor)
        
        self.label34 = QLabel(str(self.ECG_raw_data_index_number), self)
        self.label34.move(700*layout_scale_factor, 230*layout_scale_factor)
        
        self.label35 = QLabel('PPG Grade', self)
        self.label35.move(700*layout_scale_factor, 280*layout_scale_factor)

        self.label36 = QLabel(str(self.PPG_raw_data_index_number), self)
        self.label36.move(700*layout_scale_factor, 330*layout_scale_factor)
        
        self.label37 = QLabel('MBP Grade', self)
        self.label37.move(700*layout_scale_factor, 400*layout_scale_factor)
        
        self.label38 = QLabel(str(self.MBP_raw_data_index_number), self)
        self.label38.move(700*layout_scale_factor, 440*layout_scale_factor)


        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        self.label21 = QLabel(self)
        self.ABP_image=QtGui.QPixmap(ABP_raw_data[ABP_raw_data_index])
        #self.ABP_image=QtGui.QPixmap("./opstart_opend/ART_1914_780000_810000_split.png")
        #self.ABP_image_resized = self.ABP_image.scaled(width_size, height_size, QtCore.Qt.KeepAspectRatio)
        self.ABP_image_resized = self.ABP_image.scaled(width_size, height_size)
        self.label21.setPixmap(self.ABP_image_resized)
        self.label21.setGeometry(QtCore.QRect(44*layout_scale_factor, 80*layout_scale_factor, width_size, height_size))

        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        self.label22 = QLabel(self)
        self.ECG_image=QtGui.QPixmap(ECG_raw_data[ECG_raw_data_index])
        #self.ECG_image=QtGui.QPixmap("./opstart_opend/ECG_1914_780000_810000_split.png")
        #self.ECG_image_resized = self.ECG_image.scaled(width_size, height_size, QtCore.Qt.KeepAspectRatio)
        self.ECG_image_resized = self.ECG_image.scaled(width_size, height_size)
        self.label22.setPixmap(self.ECG_image_resized)
        self.label22.setGeometry(QtCore.QRect(44*layout_scale_factor, 180*layout_scale_factor, width_size, height_size))
        
        width_size = 550*1.18*layout_scale_factor
        height_size = 98*layout_scale_factor
        self.label23 = QLabel(self)
        self.PPG_image=QtGui.QPixmap(PPG_raw_data[PPG_raw_data_index])
        #self.PPG_image=QtGui.QPixmap("./opstart_opend/PLETH_1914_780000_810000_split.png")
        #self.PPG_image_resized = self.PPG_image.scaled(width_size, height_size, QtCore.Qt.KeepAspectRatio)
        self.PPG_image_resized = self.PPG_image.scaled(width_size, height_size)
        self.label23.setPixmap(self.PPG_image_resized)
        self.label23.setGeometry(QtCore.QRect(44*layout_scale_factor, 280*layout_scale_factor, width_size, height_size))
        
        width_size = 550*1.18*layout_scale_factor
        height_size = 90*layout_scale_factor
        self.label24 = QLabel(self)
        self.MBP_image=QtGui.QPixmap(MBP_raw_data[MBP_raw_data_index])
        #self.MBP_image=QtGui.QPixmap("./opstart_opend/MBP_1914_780_810_split.png")
        self.MBP_image_resized = self.MBP_image.scaled(width_size, height_size)
        self.label24.setPixmap(self.MBP_image_resized)
        self.label24.setGeometry(QtCore.QRect(44*layout_scale_factor, 405*layout_scale_factor, width_size, height_size))
        
        #Segment ID
        self.label9_1 = QLabel('Segment ID:', self)
        self.label9_1.move(600*layout_scale_factor, 10)
        self.label9_2 = QLabel(Segment_id, self)
        self.label9_2.move(650*layout_scale_factor, 10)
                
        
        #Move Button
        self.btn1 = QPushButton('<-', self)
        self.btn1.move(700*layout_scale_factor, 20*layout_scale_factor)
        self.btn1.clicked.connect(self.btnRun_clicked1)
        
        self.btn2 = QPushButton('->', self)
        self.btn2.move(730*layout_scale_factor, 20*layout_scale_factor)
        self.btn2.clicked.connect(self.btnRun_clicked2)
        
        self.label9 = QLabel('Move Button 1', self)
        self.label9.move(700*layout_scale_factor, 10*layout_scale_factor)

        self.btn3 = QPushButton('<-', self)
        self.btn3.move(700*layout_scale_factor, 45*layout_scale_factor)
        self.btn3.clicked.connect(self.btnRun_clicked3)
        
        self.btn4 = QPushButton('->', self)
        self.btn4.move(730*layout_scale_factor, 45*layout_scale_factor)
        self.btn4.clicked.connect(self.btnRun_clicked4)
        
        #Move Button
        self.label9 = QLabel('Move Button 2', self)
        self.label9.move(700*layout_scale_factor, 35*layout_scale_factor)
            
        self.label17 = QLabel(str(concat_grade[0][1]), self)
        self.label17.move(680*layout_scale_factor, 120*layout_scale_factor)
        self.qle = QLineEdit(self)
        self.qle.textChanged[str].connect(self.edit_onChanged1)
        self.qle.move(700*layout_scale_factor, 100*layout_scale_factor)

        self.label16 = QLabel(str(concat_grade[0][2]), self)
        self.label16.move(680*layout_scale_factor, 220*layout_scale_factor)
        self.qle1 = QLineEdit(self)
        self.qle1.textChanged[str].connect(self.edit_onChanged2)
        self.qle1.move(700*layout_scale_factor, 200*layout_scale_factor)

        self.label15 = QLabel(str(concat_grade[0][3]), self)
        self.label15.move(680*layout_scale_factor, 320*layout_scale_factor)
        self.qle2 = QLineEdit(self)
        self.qle2.textChanged[str].connect(self.edit_onChanged3)
        self.qle2.move(700*layout_scale_factor, 300*layout_scale_factor)

        self.label14 = QLabel(str(concat_grade[0][4]), self)
        self.label14.move(680*layout_scale_factor, 420*layout_scale_factor)
        self.qle3 = QLineEdit(self)
        self.qle3.textChanged[str].connect(self.edit_onChanged4)
        self.qle3.move(700*layout_scale_factor, 420*layout_scale_factor)
        
    
        #self.slider.valueChanged.connect(self.button_clicked4)
        #self.slider.valueChanged[str].connect(self.button_clicked4)
        #self.slider.valueChanged.connect(self.button_clicked2)
        
        #Data index range
        self.slider = QScrollBar(Qt.Horizontal, self)
        self.slider.move(30, 30)
        #case id min max
        self.slider.setRange(0,int(len(Segment_id_data)-1))
        self.slider.setSingleStep(1)
        self.slider.setSliderPosition(0)

        
        #self.slider.setTickInterval(1)
        #self.slider.valueChanged[int].connect(self.btnRun_clicked1)
        #print(self.slider.setTickPosition(QSlider.TicksAbove))
        self.slider.valueChanged.connect(self.value_changed_case_index)
        self.slider.valueChanged[int].connect(self.btnRun_clicked2)
        self.slider.setGeometry(80, 20, 630*layout_scale_factor, 50) #x,y,w,h
        
  
        
        print('Caculation data index boundary')
        print('Segment id', Segment_id_data[case_raw_data_index])
        print('data index count', data_index_count[Segment_id_data[case_raw_data_index]])

        print(str(len(Segment_id_data[:])))
        #print(Segment_id_data)
        self.label10 = QLabel('Case ID:', self)
        self.label10.move(10, 40)
        self.label13 = QLabel(str(Segment_id_data[case_raw_data_index])+'/'+str(len(Segment_id_data)), self)
        self.label13.move(1250, 40)
        
        self.slider2 = QScrollBar(Qt.Horizontal, self)
        self.slider2.move(30, 30)
        #case id slider min max
        self.slider2.setRange(0,int(data_index_load_range[case_raw_data_index]-1))
        self.slider2.setSingleStep(1)
        #self.slider2.setTickInterval(1)
        #print(self.slider2.setTickPosition(QSlider.TicksAbove))
        self.slider2.setSliderPosition(0)
        #print(self.slider2.setTickPosition(QSlider.TicksAbove))
        self.slider2.valueChanged.connect(self.value_changed_data_index)
        
        #self.label = QLabel('0',self)
        #self.label.move(30,100)
        #self.slider2.valueChanged[int].connect(self.btnRun_clicked3)
        self.slider2.valueChanged[int].connect(self.btnRun_clicked4)
        self.slider2.setGeometry(80, 50, 630*layout_scale_factor, 35*layout_scale_factor)#x,y,w,h
        
        '''
        self.slider2 = QSlider(Qt.Horizontal, self)
        self.slider2.setGeometry(10, 50, 630*layout_scale_factor, 35*layout_scale_factor)#x,y,w,h
        self.slider2.move(80, 50)
        self.slider2.setRange(0, 6000)
        self.slider2.setValue(0)
        self.slider2.setTickInterval(30)
        self.slider2.setTickPosition(QSlider.TicksBelow)
        self.slider2.valueChanged.connect(self.button_clicked_slider)
        self.slider2.valueChanged[str].connect(self.button_clicked)
        '''
        #self.slider2.valueChanged.connect(self.button_clicked2)

        
        self.label11 = QLabel('Data Index:', self)
        self.label11.move(10, 70)
        

        
        self.label12 = QLabel(str(ABP_raw_data_index)+'/'+str(data_index_load_range[case_raw_data_index]-1),self)
        #self.label12 = QLabel('0'+'/'+str(data_index_count[Segment_id_data[case_raw_data_index]]), self)
        self.label12.move(1250, 70)
        #self.image1=self.filedialog_open()
        #label20 = QLabel(self.image1)
        #label20.move(300, 50)
        
        self.btn5 = QPushButton('save', self)
        self.btn5.move(690*layout_scale_factor, 465*layout_scale_factor)
        self.btn5.clicked.connect(self.btnRun_clicked5)

        self.btn5 = QPushButton('save as', self)
        self.btn5.move(730*layout_scale_factor, 465*layout_scale_factor)
        self.btn5.clicked.connect(self.btnRun_clicked6)
        
        self.btn5 = QPushButton('open', self)
        self.btn5.move(730*layout_scale_factor, 480*layout_scale_factor)
        self.btn5.clicked.connect(self.btnRun_clicked7)
        
        self.setWindowTitle('ABP, ECG, PPG data annotation tool')
        #self.setGeometry(900*1.85, 500*1.85, 900*1.85, 500*1.85)
        self.setGeometry(780*layout_scale_factor, 500*layout_scale_factor, 780*layout_scale_factor, 500*layout_scale_factor)
        self.show()

if __name__ == '__main__':
    search(file_root_path)
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    while True:    
       if keyboard.read_key() == "p":    
          print('p')
