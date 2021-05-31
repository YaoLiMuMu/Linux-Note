#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/05/31 03:19
# @Auther : yaolimumu
# @Site : Nebula
# @File : bms_resolution.py
# @Version: V0.0.1
# @Software : Python3

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
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# customized function
def BST_Parser(msgstring):
    """
    :param msgstring: fixed parameter, BST message
    :param test1: 固定参数, 默认参数, 不定长参数, 关键字参数
    :return: BST fault
    """
    faultBitList=[['SOC达到目标值', 'SOC不可信', '电压达到设定值', '电压不可信', '单体电压达到限值', '单体电压不可信', '收到充电机中止', 'CST不可信'], \
    ['绝缘故障', '绝缘不可信', '输出连接器过温', '连接器过温不可信', 'BMS元件过温', 'BMS元件不可信', '充电连接器故障', '充电连接器不可信'], \
    ['电池组过温', '电池组温度不可信', '高压继电器故障', '高通继电器不可信', 'CC2检测故障', 'CC2不可信', '其他故障', '其他不可信'], \
    ['电流过大', '电流不可信', '电压异常', '电压不可信']]
    backString = ''
    for i in range(len(faultBitList)):
        for j in range(len(faultBitList[i])):
            if ((int(msgstring[3*i:(3*i+2)], 16)) >> j) & 0x01 == 0x01:
                backString = backString + '<' + faultBitList[i][j]
    return backString
def CST_Parser(msgstring):
    faultBitList=[['充电机达设定条件', '设定条件不可信', '人工中止', '人工中止不可信', '故障中止', '故障中止不可信', '收到BMS中止', 'BST不可信'], \
    ['充电机过温', '充电过温不可信', '充电连接器故障', '连接器故障不可信', '充电机内部过温', '内部过温不可信', '电量无法传送', '电量传送不可信'], \
    ['急停故障', '急停不可信', '其他故障', '其他不可信'], \
    ['电流不匹配', '电流不可信', '电压异常', '电压不可信']]
    backString = ''
    for i in range(len(faultBitList)):
        for j in range(len(faultBitList[i])):
            if ((int(msgstring[3*i:(3*i+2)], 16)) >> j) & 0x01 == 0x01:
                backString = backString + '<' + faultBitList[i][j]
    return backString
def BSM_Parser(msgstring):
    faultBitList=[['单体电压过高', '单体电压过低', 'SOC过高', 'SOC过低', '电池过流', '过流不可信', '电池过温', '过温不可信'], \
    ['绝缘异常', '绝缘不可信', '连接器异常', '连接器不可信', '允许充电']]
    backString = ''
    for i in range(len(faultBitList)):
        for j in range(len(faultBitList[i])):
            if ((int(msgstring[3*i:(3*i+2)], 16)) >> j) & 0x01 == 0x01:
                backString = backString + '<' + faultBitList[i][j]
    return backString
def CEM_Parser(msgstring):
    faultBitList=[['BRM超时', 'BRM不可信'], \
    ['BCP超时', 'BCP不可信', 'BRO超时', 'BRO不可信'], \
    ['BCS超时', 'BCS不可信', 'BCL超时', 'BCL不可信', 'BST超时', 'BST不可信'], \
    ['BSD超时', 'BSD不可信', '其他超时', '其他超时']]
    backString = ''
    for i in range(len(faultBitList)):
        for j in range(len(faultBitList[i])):
            if ((int(msgstring[3*i:(3*i+2)], 16)) >> j) & 0x01 == 0x01:
                backString = backString + '<' + faultBitList[i][j]
    return backString
def BEM_Parser(msgstring):
    faultBitList=[['CRM_00超时', 'CRM_00不可信', 'CRM_AA超时', 'CRM_AA不可信'], \
    ['CML超时', 'CML不可信', 'CRO超时', 'CRO不可信'], \
    ['CCS超时', 'CCS不可信', 'CST超时', 'CST不可信'], \
    ['CSD超时', 'CSD不可信', '其他超时', '其他超时']]
    backString = ''
    for i in range(len(faultBitList)):
        for j in range(len(faultBitList[i])):
            if ((int(msgstring[3*i:(3*i+2)], 16)) >> j) & 0x01 == 0x01:
                backString = backString + '<' + faultBitList[i][j]
    return backString
def Battery_Type(type_index):
    Battery_Type = [ '', '铅酸电池', '镍氢电池', '磷酸铁锂电池', '锰酸锂电池', '钴酸锂电池', '三元材料电池', '聚合物锂离子电池', '钛酸锂电池', '其他电池']
    if type_index > 8:
        return Battery_Type[9]
    else:
        return Battery_Type[type_index]
def str_to_ascii(input_string, index, number):
    outputString = ''
    for i in range(number):
        if int(input_string[3*(index+i):3*(index+i)+2], 16) > 127:
            return 'Invalid'
        outputString = outputString + chr(int(input_string[3*(index+i):3*(index+i)+2], 16))
    return outputString
# configuration variable
path = '.'
MsgDateTime = '*'
MsgType = 2 # Type 1 USBCAN capture CSV, Typy 2 TCU capture CSV
triple_variable = ('SYS_MS', 'MAKE_CAN_ID(HEX)', 'DATA(HEX)')
BHM_FrameID = '*182756f4*'  #[OK]
BCL_FrameID = '*181056f4*'  #[OK]
CCS_FrameID = '*1812f456*'  #[OK]
CML_FrameID = '*1808f456*'  #[OK]
BRO_FrameID = '*100956f4*'  #[OK]
CRO_FrameID = '*100af456*'  #[OK]
CHM_FrameID = '*1826f456*'  #[OK]
CST_FrameID = '*101af456*'  #[OK]
BST_FrameID = '*101956f4*'  #[OK]
CRM_FrameID = '*1801f456*'  #[OK]
CSD_FrameID = '*181df456*'  #[OK]
CEM_FrameID = '*081ff456*'  #[OK]
BEM_FrameID = '*081e56f4*'  #[OK]
BSM_FrameID = '*181356f4*'  #[OK]
BSD_FrameID = '*181c56f4*'  #[OK]
BCP_First_Frame_Data = '10 0d 00 02 ff 00 06 00*'
BCP_End_ACK = '13 0d 00 02 ff 00 06 00*'
BRM_First_Frame_Data = '*00 02 00*'     # compatiable with the old standard
BRM_End_ACK = '13 31 00 07 ff 00 02 00*'
BCS_First_Frame_Data = '10 09 00 02 ff 00 11 00*'
BCS_End_ACK = '13 09 00 02 ff 00 11 00*'
SAJ1939_RTS_FrameID = '*1cec56f4*'
SAJ1939_CTS_FrameID = '*1ceb56f4*'
SAJ1939_EndofMsgAck = '*1cecf456*'
os.makedirs('csvfiles', exist_ok=True) # make directory to store analysis results
# Loop through every file in the current working directory
print('请将解析工具放在.csv文件同目录下, 生成结果与图形自动保存在同目录的csvfiles文件中...')
print('注意!!!csv文件需要包含表头:', triple_variable)
csvfiles = os.listdir(path)
csvfiles.sort() #排序
for file in csvfiles:
    if not file.endswith('.csv'):
        continue # skip non-csv files
    print('>>>> scaning csv file from ' + file + ' ...')
    if match(file.lower(), '*bms*'):
        framebuffer = pd.read_csv(file, names=[triple_variable[0], "id", triple_variable[1], triple_variable[2]], header=None, index_col=False)
        framebuffer.drop('id', inplace=True, axis=1)
    else:
        framebuffer = pd.read_csv(file, usecols=[triple_variable[0], triple_variable[1], triple_variable[2]])
    framebuffer.insert(3,'TEXT1', '') # add a column as TEXT1
    framebuffer['TEXT2'], framebuffer['TEXT3'], framebuffer['Fault'] = ['', '', ''] # add columns as TEXT2, TEXT3 = np.NaN
    buffer= np.array(framebuffer)
    data=[]
    data.append([triple_variable[0], triple_variable[1], triple_variable[2], 'TEXT1', 'TEXT2', 'TEXT3', 'TEXT4']) # add csv header
    BCL_Axis = [[], [], []]     # [0] timestamp [1] voltage [2] current
    CCS_Axis = [[], [], []]     # [0] timestamp [1] voltage [2] current
    MsgBcpDict = [0, 0, 0] # [0] RTS [1] donestep [2] long connect join temp
    MsgBrmDict = [0, 0, 0]
    MsgBcsDict = [0, 0, 0]
    stopStamp = False
    TimeoutFlag = False
    for item in buffer:
        sh = item[0]
        if match(sh, '*Gun*'):
            continue    # filter 'can:0 Gun:00' row
        if match(sh, MsgDateTime): # filter DateTime
            sh = item[1]
            if match(sh.lower(), BCL_FrameID): # filter BCL messages
                BCLVoltage = (int(str(item[2])[3:5], 16)*256 + int(str(item[2])[0:2], 16))/10
                BCLCurrent = 400 - (int(str(item[2])[9:11], 16)*256 + int(str(item[2])[6:8], 16))/10
                timestamp = str(item[0]).strip('[]') # delete []
                BCL_Axis[2].append(BCLCurrent)
                BCL_Axis[1].append(BCLVoltage)
                if match(file.lower(), '*bms*'):
                    BCL_Axis[0].append(datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S'))
                else:
                    BCL_Axis[0].append(datetime.datetime.strptime(timestamp,'%H:%M:%S.%f'))
                item[3] = 'BCL:需求电压=' + str(BCLVoltage) + 'V'
                item[4] = 'BCL:需求电流=' + str(BCLCurrent) + 'A'
            elif match(sh.lower(), CCS_FrameID): # filter CCS messages
                CCSVoltage = (int(str(item[2])[3:5], 16)*256 + int(str(item[2])[0:2], 16))/10
                CCSCurrent = round((400 - (int(str(item[2])[9:11], 16)*256 + int(str(item[2])[6:8], 16))/10), 1)
                timestamp = str(item[0]).strip('[]') # delete []
                CCS_Axis[2].append(CCSCurrent)
                CCS_Axis[1].append(CCSVoltage)
                if match(file.lower(), '*bms*'):
                    CCS_Axis[0].append(datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S'))
                else:
                    CCS_Axis[0].append(datetime.datetime.strptime(timestamp,'%H:%M:%S.%f'))
                item[3] = 'CCS: U=' + str(CCSVoltage) + 'V' 
                item[4] = 'CCS: I=' + str(CCSCurrent) + 'A'
            elif match(sh.lower(), BHM_FrameID): # filter BHM messages
                BHM_Voltage = (int(str(item[2])[3:5], 16)*256 + int(str(item[2])[0:2], 16))/10
                item[3] = 'BHM:自检电压=' + str(BHM_Voltage) + 'V'
                if BHM_Voltage < 200.0:
                    item[6] = 'Fault:BHM最高电压过低'
                    print('<<<< ' + file + item[6])
            elif match(sh.lower(), CML_FrameID): # filter CML messages
                CML_Max_Voltage = (int(str(item[2])[3:5], 16)*256 + int(str(item[2])[0:2], 16))/10
                CML_Min_Voltage = (int(str(item[2])[9:11], 16)*256 + int(str(item[2])[6:8], 16))/10
                CML_Max_Current = 400 - (int(str(item[2])[15:17], 16)*256 + int(str(item[2])[12:14], 16))/10
                CML_Min_Current = 400 - (int(str(item[2])[21:23], 16)*256 + int(str(item[2])[18:20], 16))/10
                item[3] = 'CML:电压范围=' + str(CML_Min_Voltage) + '~' + str(CML_Max_Voltage) + 'V'
                item[4] = 'CML:电流范围=' + str(CML_Min_Current) + '~' + str(CML_Max_Current) + 'A'
            elif match(sh.lower(), SAJ1939_RTS_FrameID):
                if match(item[2], BCP_First_Frame_Data):
                    MsgBcpDict[0] = 1
                    item[3] = 'BCP->RTS...'
                elif match(item[2], BRM_First_Frame_Data):
                    MsgBrmDict[0] = 1
                    item[3] = 'BRM->RTS...'
                elif match(item[2], BCS_First_Frame_Data):
                    MsgBcsDict[0] = 1
                    item[3] = 'BCS->RTS...'
            elif match(sh.lower(), SAJ1939_CTS_FrameID):
                if match(item[2].lower(), '01*') and MsgBcpDict[0] == 1:    # filter BCP messages[1]
                    item[3] = 'BCP:单体上限=' + str((int(str(item[2])[6:8], 16)*256 + int(str(item[2])[3:5], 16))/100) + ' V'
                    item[4] = 'BCP:最大电流=' + str(round((400 - (int(str(item[2])[12:14], 16)*256 + int(str(item[2])[9:11], 16))/10), 1)) + ' A'
                    item[5] = 'BCP:电池能量=' + str((int(str(item[2])[18:20], 16)*256 + int(str(item[2])[15:17], 16))/10) + ' Kwh'
                    if (400 - (int(str(item[2])[12:14], 16)*256 + int(str(item[2])[9:11], 16))/10) <= 0.0:
                        item[6] = 'Fault:BCP最大电流非法'
                        print('<<<< ' + file + item[6])
                    MsgBcpDict[2] = int(str(item[2])[21:23], 16)
                    MsgBcpDict[1] = MsgBcpDict[1] + 1
                elif match(item[2].lower(), '02*') and MsgBcpDict[1] == 1:    # filter BCP messages[2]
                    item[3] = 'BCP:电压上限=' + str((int(str(item[2])[3:5], 16)*256 + MsgBcpDict[2])/10) + 'V'
                    item[4] = 'BCP:当前SOC=' + str(round(((int(str(item[2])[12:14], 16)*256 + int(str(item[2])[9:11], 16))/10), 1)) + '%'
                    item[5] = 'BCP:当前电压=' + str((int(str(item[2])[18:20], 16)*256 + int(str(item[2])[15:17], 16))/10) + 'V'
                elif match(item[2].lower(), '01*') and MsgBcsDict[0] == 1:    # filter BCS messages[1]
                    item[3] = 'BCS:车端电压=' + str((int(str(item[2])[6:8], 16)*256 + int(str(item[2])[3:5], 16))/10) + ' V'
                    item[4] = 'BCS:车端电流=' + str(round((400 - (int(str(item[2])[12:14], 16)*256 + int(str(item[2])[9:11], 16))/10), 1)) + ' A'
                    item[5] = 'BCS:当前SOC=' + str(int(str(item[2])[21:23], 16)) + '%'
                    MsgBcsDict[1] = MsgBcsDict[1] + 1
                elif match(item[2].lower(), '02*') and MsgBcsDict[1] == 1:    # filter BCS messages[2]
                    item[3] = 'BCS:剩余时间=' + str(int(str(item[2])[6:8], 16)*256 + int(str(item[2])[3:5], 16)) + 'min'
                elif match(item[2].lower(), '01*') and MsgBrmDict[0] == 1:    # filter BRM messages[1]
                    item[3] = 'BRM:协议版本=V' + str(int(str(item[2])[3:5], 16)) + '.' + str(int(str(item[2])[6:8], 16)) + str(int(str(item[2])[9:11], 16))
                    item[4] = 'BRM:电池类型=' + Battery_Type(int(str(item[2])[12:14], 16))
                    item[5] = 'BRM:额定容量=' + str((int(str(item[2])[18:20], 16)*256 + int(str(item[2])[15:17], 16))/10) + 'Ah'
                    MsgBrmDict[1] = MsgBrmDict[1] + 1
                elif match(item[2].lower(), '02*') and MsgBrmDict[1] == 1:
                    item[3] = 'BRM:电池产商=' + str_to_ascii(item[2], 2, 4)
                    MsgBrmDict[1] = MsgBrmDict[1] + 1
                elif match(item[2].lower(), '03*') and MsgBrmDict[1] == 2:
                    MsgBrmDict[2] = int(str(item[2])[21:23], 16)*256 + int(str(item[2])[18:20], 16)
                    MsgBrmDict[1] = MsgBrmDict[1] + 1
                elif match(item[2].lower(), '04*') and MsgBrmDict[1] == 3:
                    item[3] = 'BRM:充电次数=' + str(int(item[2][3:5], 16)*16*256 + MsgBrmDict[2])
                    MsgBrmDict[2] = ''
                    MsgBrmDict[2] = MsgBrmDict[2] + str_to_ascii(item[2], 4, 4)
                    MsgBrmDict[1] = MsgBrmDict[1] + 1
                elif match(item[2].lower(), '05*') and MsgBrmDict[1] == 4:
                    MsgBrmDict[2] = MsgBrmDict[2] + str_to_ascii(item[2], 1, 7)
                    MsgBrmDict[1] = MsgBrmDict[1] + 1
                elif match(item[2].lower(), '06*') and MsgBrmDict[1] == 5:
                    MsgBrmDict[2] = MsgBrmDict[2] + str_to_ascii(item[2], 1, 6)
                    if match(MsgBrmDict[2], '*Invalid*'):
                        MsgBrmDict[2] = '无效'
                    item[3] = 'BRM:VIN=' + MsgBrmDict[2]
                    MsgBrmDict[1] = MsgBrmDict[1] + 1
            elif match(sh.lower(), SAJ1939_EndofMsgAck):
                if match(item[2].lower(), BCP_End_ACK):
                    MsgBcpDict[0] = 0
                    MsgBcpDict[1] = 0
                    MsgBcpDict[2] = 0
                if match(item[2].lower(), BRM_End_ACK):
                    if TimeoutFlag == True:
                        item[3] = '通信重连成功[OK]'
                        TimeoutFlag = False
                    MsgBrmDict[0] = 0
                    MsgBrmDict[1] = 0
                    MsgBrmDict[2] = 0
                if match(item[2].lower(), BCS_End_ACK):
                    MsgBcsDict[0] = 0
                    MsgBcsDict[1] = 0
                    MsgBcsDict[2] = 0
            elif match(sh.lower(), BRO_FrameID):
                if match(item[2].lower(), '*aa*'):
                    item[3] = 'BRO:车端准备完成[OK]'
                else:
                    item[3] = 'BRO:车端准备中...'
            elif match(sh.lower(), CRO_FrameID):
                if match(item[2].lower(), '*aa*'):
                    item[3] = 'CRO:桩端准备完成[OK]'
                else:
                    item[3] = 'CRO:桩端准备中...'
            elif match(sh.lower(), CHM_FrameID):
                item[3] = 'CHM:自检版本=V' + str(int(str(item[2])[0:2], 16)) + '.' + str(int(str(item[2])[3:5], 16)) + str(int(str(item[2])[6:8], 16))
            elif match(sh.lower(), BST_FrameID):
                item[4] = 'BST:中止原因' + BST_Parser(item[2])
                if stopStamp == False:
                    item[3] = '车端主动中止->>'
                    stopStamp = True
            elif match(sh.lower(), CST_FrameID):
                item[4] = 'CST:中止原因' + CST_Parser(item[2])
                if stopStamp == False:
                    item[3] = '桩端主动中止...'
                    stopStamp = True
            elif match(sh.lower(), CRM_FrameID):
                if match(item[2].lower(), 'aa*'):
                    item[3] = 'CRM:车辆辨识成功'
                else:
                    item[3] = 'CRM:车辆未能辨识'
                    item[4] = 'CRM:充电机编号:' + str(item[2])[3:14].replace(' ', '') # replace space
                    item[5] = 'CRM:区域编码:' + str_to_ascii(item[2], 5, 3)
            elif match(sh.lower(), CSD_FrameID):
                item[3] = 'CSD:累计时长=' + str(int(str(item[2])[3:5], 16)*256 + int(str(item[2])[0:2], 16)) + 'min'
                item[4] = 'CSD:充电机编号=' + str(item[2])[12:23].replace(' ', '') # replace space
                item[5] = 'CSD:充电量=' + str((int(str(item[2])[9:11], 16)*256 + int(str(item[2])[6:8], 16))/10) + 'Kwh'
            elif match(sh.lower(), BSM_FrameID):
                item[3] = 'BSM:最高温度=' + str(int(str(item[2])[3:5], 16) - 50) + '℃'
                item[4] = 'BSM:最低温度=' + str(int(str(item[2])[9:11], 16) - 50) + '℃'
                item[5] = 'BSM:状态=' + BSM_Parser(item[2][15:20])
            elif match(sh.lower(), BSD_FrameID):
                item[3] = 'BSD:中止SOC=' + str(int(str(item[2])[0:2], 16)) + '%'
                item[4] = 'BSD:单体最高电压=' + str((int(str(item[2])[12:14], 16)*256 + int(str(item[2])[9:11], 16))/100) + 'V'
                item[5] = 'BSD:最高温度=' + str(int(str(item[2])[18:20], 16) - 50) + '℃'
            elif match(sh.lower(), BEM_FrameID):
                item[4] = 'BEM:桩端报文超时=' + BEM_Parser(item[2])
                if TimeoutFlag == False:
                    item[3] = '车端发现超时重连中...'
                    TimeoutFlag == True
            elif match(sh.lower(), CEM_FrameID):
                item[4] = 'CEM:车端报文超时=' + CEM_Parser(item[2])
                if TimeoutFlag == False:
                    item[3] = '桩端发现超时重连中...'
                    TimeoutFlag == True
            data.append(item)
    csvFilesobj = open(os.path.join('csvfiles', file), 'w', newline='') # create copy file in csvfiles direstory
    csvWriter = csv.writer(csvFilesobj)
    for row in data:
        csvWriter.writerow(row)
    csvFilesobj.close()
    # df = pd.read_csv('./csvfiles/5.csv',header=None,names=[triple_variable[0], triple_variable[1], triple_variable[2], 'TEXT1', 'TEXT2', 'TEXT3', '1', '2', '3'])
    # df.to_csv('./csvfiles/5.csv', index=False)
    # y_major_locator=MultipleLocator(10)
    # plt.plot(BCL_Axis[0], BCL_Axis[1], color='red', label='BCL Voltage')
    # plt.plot(CCS_Axis[0], CCS_Axis[1], color='green', label='CCS Voltage')
    # plt.plot(CCS_Axis[0], CCS_Axis[2], color='blue', label='CCS Current')
    # plt.plot(BCL_Axis[0], BCL_Axis[2], color='black', label='BCL Current')

    ChangingFigure = plt.figure()
    DoubleAxis = ChangingFigure.add_subplot(111)
    DoubleAxis.plot(BCL_Axis[0], BCL_Axis[1], color='red', label='BCL Voltage')
    DoubleAxis.plot(CCS_Axis[0], CCS_Axis[1], color='green', label='CCS Voltage')
    Axis2 = DoubleAxis.twinx()
    Axis2.plot(CCS_Axis[0], CCS_Axis[2], color='blue', label='CCS Current')
    Axis2.plot(BCL_Axis[0], BCL_Axis[2], color='black', label='BCL Current')
    # ax=plt.gca()
    # ax.yaxis.set_major_locator(y_major_locator)
    # plt.ylim(0, 750)
    Axis2.set_ylim(0, 250)
    plt.xticks(rotation=45, fontsize=7)
    # plt.yticks(fontsize=7)
    plt.xlabel('X-Time')
    DoubleAxis.set_ylabel('Voltage-V')
    Axis2.set_ylabel('Current-A')
    plt.title('Charging Curve')
    #添加注释 参数名xy：箭头注释中箭头所在位置，参数名xytext：注释文本所在位置，
    #arrowprops在xy和xytext之间绘制箭头, shrink表示注释点与注释文本之间的图标距离
    # DoubleAxis.annotate('i am commment', xy=(CCS_Axis[0][0],680), xytext=(CCS_Axis[0][0], 700),
    #             arrowprops=dict(facecolor='black', shrink=0.01), )
    # DoubleAxis.text(CCS_Axis[0][0], 680, 'Hello', ha='center', va='bottom', fontsize=10)
    Axis2.legend(loc=6)
    DoubleAxis.legend(loc=7)
    plt.savefig(path + '/csvfiles/' + file +'.png') # 在show之前才能保存
    plt.show()
    print ('<<<< ' + path + '/csvfiles/' + file + 'file conversion completed')
# TODO(yaolimumu): double-x axis xticks rotation=45