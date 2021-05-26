#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bms message(.csv files) automatic analysis script
from numpy.core.arrayprint import ComplexFloatingFormat
import pandas as pd
import numpy as np
import os
import csv
import datetime
import matplotlib.pyplot as plt
from fnmatch import fnmatchcase as match # grep compare
from matplotlib.pyplot import MultipleLocator, tripcolor
# configuration variable
path = '.'
MsgDateTime = '*'
triple_variable = ('SYS_MS', 'MAKE_CAN_ID(HEX)', 'DATA(HEX)')
BHM_FrameID = '*182756f4*'
BCL_FrameID = '*181056f4*'
CCS_FrameID = '*1812f456*'
CML_FrameID = '*1808f456*'
SAJ1939_RTS_FrameID = '*1cec56f4*'
SAJ1939_CTS_FrameID = '*1ceb56f4*'
EndofMsgAck = '*1cecf456*'
os.makedirs('csvfiles', exist_ok=True) # make directory to store analysis results
# Loop through every file in the current working directory
csvfiles = os.listdir(path)
csvfiles.sort() #排序
for file in csvfiles:
    if not file.endswith('.csv'):
        continue # skip non-csv files
    print('scaning csv file from ' + file + ' ...')
    framebuffer = pd.read_csv(file, usecols=[triple_variable[0], triple_variable[1], triple_variable[2]])
    framebuffer.insert(3,'TEXT1', '') # add a column as TEXT1
    framebuffer['TEXT2'], framebuffer['TEXT3'], framebuffer['TEXT4'] = ['', '', ''] # add columns as TEXT2, TEXT3 = np.NaN
    buffer= np.array(framebuffer)
    data=[]
    print(buffer[0])
    data.append([triple_variable[0], triple_variable[1], triple_variable[2], 'TEXT1', 'TEXT2', 'TEXT3', 'TEXT4']) # add csv header
    BCL_Axis = [[], [], []]
    CCS_Axis = [[], [], []]
    MsgBcpDict = [0, 0, 0]
    for item in buffer:
        sh = item[0]
        if match(sh, MsgDateTime): # filter DateTime
            sh = item[1]
            if match(sh.lower(), BCL_FrameID): # filter BCL messages
                BCLVoltage = (int(str(item[2])[3:5], 16)*256 + int(str(item[2])[0:2], 16))/10
                BCLCurrent = 400 - (int(str(item[2])[9:11], 16)*256 + int(str(item[2])[6:8], 16))/10
                timestamp = str(item[0]).strip('[]') # delete []
                BCL_Axis[2].append(BCLCurrent)
                BCL_Axis[1].append(BCLVoltage)
                BCL_Axis[0].append(datetime.datetime.strptime(timestamp,'%H:%M:%S.%f'))
                item[3] = '需求 U = ' + str(BCLVoltage)
                item[4] = '需求 I = ' + str(BCLCurrent)
                data.append(item)
            elif match(sh.lower(), CCS_FrameID): # filter CCS messages
                CCSVoltage = (int(str(item[2])[3:5], 16)*256 + int(str(item[2])[0:2], 16))/10
                CCSCurrent = round((400 - (int(str(item[2])[9:11], 16)*256 + int(str(item[2])[6:8], 16))/10), 1)
                timestamp = str(item[0]).strip('[]') # delete []
                CCS_Axis[2].append(CCSCurrent)
                CCS_Axis[1].append(CCSVoltage)
                CCS_Axis[0].append(datetime.datetime.strptime(timestamp,'%H:%M:%S.%f'))
                item[3] = '输出 U = ' + str(CCSVoltage)
                item[4] = '输出 I = ' + str(CCSCurrent)
                data.append(item)
            elif match(sh.lower(), BHM_FrameID): # filter BHM messages
                BHM_Voltage = (int(str(item[2])[3:5], 16)*256 + int(str(item[2])[0:2], 16))/10
                item[3] = '最高允许电压 U = ' + str(BHM_Voltage) + ' V'
                data.append(item)
            elif match(sh.lower(), CML_FrameID): # filter CML messages
                CML_Max_Voltage = (int(str(item[2])[3:5], 16)*256 + int(str(item[2])[0:2], 16))/10
                CML_Min_Voltage = (int(str(item[2])[9:11], 16)*256 + int(str(item[2])[6:8], 16))/10
                CML_Max_Current = 400 - (int(str(item[2])[15:17], 16)*256 + int(str(item[2])[12:14], 16))/10
                CML_Min_Current = 400 - (int(str(item[2])[21:23], 16)*256 + int(str(item[2])[18:20], 16))/10
                item[3] = 'Max U = ' + str(CML_Max_Voltage)
                item[4] = 'Min U = ' + str(CML_Min_Voltage)
                item[5] = 'Max I = ' + str(CML_Max_Current)
                item[6] = 'Min I = ' + str(CML_Min_Current)
                data.append(item)
            elif match(sh.lower(), SAJ1939_RTS_FrameID):
                if match(item[2], '10 0d 00 02 ff 00 06 00*'):
                    MsgBcpDict[0] = 1
            elif match(sh.lower(), SAJ1939_CTS_FrameID):
                if match(item[2], '01*') and MsgBcpDict[0] == 1:    # filter BCP messages
                    item[3] = 'Max Ucell = ' + str((int(str(item[2])[6:8], 16)*256 + int(str(item[2])[3:5], 16))/100) + ' V'
                    item[4] = 'Max I = ' + str(round((400 - (int(str(item[2])[12:14], 16)*256 + int(str(item[2])[9:11], 16))/10), 1)) + ' A'
                    item[5] = 'Cap = ' + str((int(str(item[2])[18:20], 16)*256 + int(str(item[2])[15:17], 16))/10) + ' Kwh'
                    MsgBcpDict[1] = int(str(item[2])[21:23], 16)
                    data.append(item)
                if match(item[2].lower(), '02*') and MsgBcpDict[0] == 1 :
                    item[3] = 'Max U = ' + str((int(str(item[2])[3:5], 16)*256 + MsgBcpDict[1])/10) + ' V'
                    item[4] = 'SOC = ' + str(round(((int(str(item[2])[12:14], 16)*256 + int(str(item[2])[9:11], 16))/10), 1)) + '%'
                    item[5] = 'Now U = ' + str((int(str(item[2])[18:20], 16)*256 + int(str(item[2])[15:17], 16))/10) + ' V'
                    data.append(item)
            elif match(sh.lower(), EndofMsgAck) and match(item[2].lower(), '*13 0d 00 02 ff 00 06 00*'):
                    MsgBcpDict[0] = 0
                    MsgBcpDict[1] = 0
    csvFilesobj = open(os.path.join('csvfiles', file), 'w', newline='') # create copy file in csvfiles direstory
    csvWriter = csv.writer(csvFilesobj)
    for row in data:
        csvWriter.writerow(row)
    csvFilesobj.close()
    # df = pd.read_csv('./csvfiles/5.csv',header=None,names=[triple_variable[0], triple_variable[1], triple_variable[2], 'TEXT1', 'TEXT2', 'TEXT3', '1', '2', '3'])
    # df.to_csv('./csvfiles/5.csv', index=False)
    # y_major_locator=MultipleLocator(10)
    plt.plot(BCL_Axis[0], BCL_Axis[1], color='red', label='BCL Voltage')
    plt.plot(CCS_Axis[0], CCS_Axis[1], color='green', label='CCS Voltage')
    plt.plot(CCS_Axis[0], CCS_Axis[2], color='blue', label='CCS Current')
    plt.plot(BCL_Axis[0], BCL_Axis[2], color='black', label='BCL Current')
    # ax=plt.gca()
    # ax.yaxis.set_major_locator(y_major_locator)
    # plt.ylim(0, 750)
    plt.xticks(rotation=45, fontsize=7)
    plt.yticks(fontsize=7)
    plt.xlabel('X-Time')
    plt.ylabel('Y-Voltage')
    plt.title('Charging Curve')
    #添加注释 参数名xy：箭头注释中箭头所在位置，参数名xytext：注释文本所在位置，
    #arrowprops在xy和xytext之间绘制箭头, shrink表示注释点与注释文本之间的图标距离

    plt.annotate('i am commment', xy=(2,680), xytext=(2, 680),
                arrowprops=dict(facecolor='black', shrink=0.01), )
    plt.legend()
    plt.savefig(path + '/csvfiles/' + file +'.png') # 在show之前才能保存
    plt.show()
    print ("all picture is starting")