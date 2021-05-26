#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bms message(.csv files) automatic analysis script
import pandas as pd
import numpy as np
import os
import csv
import datetime
import matplotlib.pyplot as plt
from fnmatch import fnmatchcase as match # grep compare
from matplotlib.pyplot import MultipleLocator

path = '.'
MsgDate = '*05-24*'
BCL_FrameID = '*181056f4*'
CCS_FrameID = '*1812f456*'
SAJ1939_RTS_FrameID = '*1cec56f4*'
SAJ1939_CTS_FrameID = '*1ceb56f4*'
EndofMsgAck = '*1cecf456*'
FrameData = '11 22'
os.makedirs('csvfiles', exist_ok=True)
# Loop through every file in the current working directory
csvfiles =os.listdir(path)
csvfiles.sort() #排序
for file in csvfiles:
    if not file.endswith('.csv'):
        continue # skip non-csv files
    print('scaning csv file from ' + file + ' ...')
    file1=pd.read_csv(file)
    file1=np.array(file1)
    data=[]
    ybcl = []
    yccs = []
    timeaxix = []
    timeaxix_ccs = []
    MsgBcpDict = [0, 0, 0]
    for item in file1:
        sh = item[0]
        if match(sh, MsgDate):
            sh = item[13]
            if match(sh, BCL_FrameID):
                BCLVoltage = (int(str(item[20])[3:5], 16)*256 + int(str(item[20])[0:2], 16))/10
                BCLCurrent = (int(str(item[20])[9:11], 16)*256 + int(str(item[20])[6:8], 16))/10 - 400
                timestamp = str(item[10]).strip('[]') # delete []
                ybcl.append(BCLVoltage)
                timeaxix.append(datetime.datetime.strptime(timestamp,'%H:%M:%S.%f'))
                temp = np.pad(item, (0,2), 'constant', constant_values=('0'))
                temp[21] = '需求 U = ' + str(BCLVoltage)
                temp[22] = '需求 I = ' + str(BCLCurrent)
                data.append(temp)
                csvFilesobj = open(os.path.join('csvfiles', file), 'w', newline='') # create copy file in csvfiles direstory
                csvWriter = csv.writer(csvFilesobj)
                for row in data:
                    csvWriter.writerow(row)
                csvFilesobj.close()
            elif match(sh, CCS_FrameID):
                CCSVoltage = (int(str(item[20])[3:5], 16)*256 + int(str(item[20])[0:2], 16))/10
                CCSCurrent = round(((int(str(item[20])[9:11], 16)*256 + int(str(item[20])[6:8], 16))/10 - 400), 1)
                timestamp = str(item[10]).strip('[]') # delete []
                yccs.append(CCSVoltage)
                timeaxix_ccs.append(datetime.datetime.strptime(timestamp,'%H:%M:%S.%f'))
                temp = np.pad(item, (0,2), 'constant', constant_values=('0'))
                temp[21] = '输出 U = ' + str(CCSVoltage)
                temp[22] = '输出 I = ' + str(CCSCurrent)
                data.append(temp)
                csvFilesobj = open(os.path.join('csvfiles', file), 'w', newline='') # create copy file in csvfiles direstory
                csvWriter = csv.writer(csvFilesobj)
                for row in data:
                    csvWriter.writerow(row)
                csvFilesobj.close()
            elif match(sh, SAJ1939_RTS_FrameID):
                if match(item[20], '10 0d 00 02 ff 00 06 00*'):
                    MsgBcpDict[0] = 1
            elif match(sh.lower(), SAJ1939_CTS_FrameID):
                if match(item[20], '01*'):
                    if MsgBcpDict[0] == 1:
                        print ('test for bcp receive')
                        temp = np.pad(item, (0,3), 'constant', constant_values=('0'))
                        temp[21] = 'Max Ucell = ' + str((int(str(item[20])[6:8], 16)*256 + int(str(item[20])[3:5], 16))/100) + ' V'
                        temp[22] = 'Max I = ' + str(round(((int(str(item[20])[12:14], 16)*256 + int(str(item[20])[9:11], 16))/10 - 400), 1)) + ' A'
                        temp[23] = 'Cap = ' + str((int(str(item[20])[18:20], 16)*256 + int(str(item[20])[15:17], 16))/10) + ' Kwh'
                        MsgBcpDict[1] = int(str(item[20])[21:23], 16)
                        data.append(temp)
                        csvFilesobj = open(os.path.join('csvfiles', file), 'w', newline='') # create copy file in csvfiles direstory
                        csvWriter = csv.writer(csvFilesobj)
                        for row in data:
                            csvWriter.writerow(row)
                        csvFilesobj.close()
                if match(item[20].lower(), '02*'):
                    if MsgBcpDict[0] == 1:
                        temp = np.pad(item, (0,3), 'constant', constant_values=('0'))
                        temp[21] = 'Max U = ' + str((int(str(item[20])[3:5], 16)*256 + MsgBcpDict[1])/10) + ' V'
                        temp[22] = 'SOC = ' + str(round(((int(str(item[20])[12:14], 16)*256 + int(str(item[20])[9:11], 16))/10), 1)) + '%'
                        temp[23] = 'Now U = ' + str((int(str(item[20])[18:20], 16)*256 + int(str(item[20])[15:17], 16))/10) + ' V'
                        data.append(temp)
                        csvFilesobj = open(os.path.join('csvfiles', file), 'w', newline='') # create copy file in csvfiles direstory
                        csvWriter = csv.writer(csvFilesobj)
                        for row in data:
                            csvWriter.writerow(row)
                        csvFilesobj.close()
            elif match(sh, EndofMsgAck):
                if match(item[20], '*13 0d 00 02 ff 00 06 00*'):
                    MsgBcpDict[0] = 0
                    MsgBcpDict[1] = 0
    # y_major_locator=MultipleLocator(10)
    plt.plot(timeaxix, ybcl, color='red', label='testing accuracy')
    plt.plot(timeaxix_ccs, yccs, color='green', label='training accuracy')
    ax=plt.gca()
    # ax.yaxis.set_major_locator(y_major_locator)
    # plt.ylim(0, 750)
    # plt.yticks([])
    plt.xlabel('x axxxx')
    #y轴文本
    plt.ylabel('y byyyy')
    #标题
    plt.title('1234567')
    #添加注释 参数名xy：箭头注释中箭头所在位置，参数名xytext：注释文本所在位置，
    #arrowprops在xy和xytext之间绘制箭头, shrink表示注释点与注释文本之间的图标距离

    plt.annotate('i am commment', xy=(2,5), xytext=(2, 10),
                arrowprops=dict(facecolor='black', shrink=0.01),
                )
    plt.legend()
    plt.savefig(file +'.png') # 在show之前才能保存
    plt.show()
    print ("all picture is starting")