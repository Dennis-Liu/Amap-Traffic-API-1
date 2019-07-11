# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:39:47 2019
@author: xin-yi.song
"""

import json
from urllib.request import urlopen
import time
import sched
import csv

#input your own key. Here is xinyi's key.
ak=r"9f32c962835c771c560ead42368febe7"

#input the coordinates
left_bottom = [121.488254,31.205333] #Should be in Baidu coordinate system
right_top = [121.513445,31.226069] #Should be in Baidu coordinate system

#input your filepath
filepath=r"C:\Users\Xin-yi.Song\Desktop\�ٶ�API\���Ҷ�\�ߵ�13\\" #���ô��·��,�����Ҫ����б�ܣ�����һ����ת���

#input step_length(seconds),data will be collected every step_length
step_length=300

#prefix of gaode API
url0=r"https://restapi.amap.com/v3/traffic/status/rectangle?"
#https://restapi.amap.com/v3/traffic/status/rectangle?key=����key&rectangle=116.351147,39.966309;116.357134,39.968727
############################��ȡ����###########################################

lng1=str(left_bottom[0])
lat1=str(left_bottom[1])
lng2=str(right_top[0])
lat2=str(right_top[1])
#���ζԽ��߲��ܳ���10����

'''
Ĭ��ֵ��level=5 
1������· 
2������·������
3�����ٸ�·
4����Ҫ��· 
5��һ���· 
6��������·
'''

#################�жϿպ���#############################
def valid(arr,key):#�˴��������ж��ֵ�keyֵ�Ƿ����,arrΪ������ֵ�,keyΪ��Ҫ�жϵĹؼ���
    if key in arr.keys():
        return arr[key]
    else:
        return '��ֵΪ��'
    
############################Get road names####################################
def road_names(): #�˴�������road_names()���������ڴ����ļ���д��ͷ
    
    for i in range(1,7):
        url=url0+'key='+ak+'&rectangle='+lng1+','+lat1+';'+lng2+','+lat2+'&extensions=all'+'&level='+str(i)
        res=urlopen(url)
        cet=res.read()
        result=json.loads(cet)
        #print(result)
    
        trafficinfo=result['trafficinfo']
        roads=trafficinfo['roads']
    
        if len(roads)==0:
            print('level=',i,'�������޿ɲ�ѯ��·��')
        else:
            for element in roads:
                road_name=element['name']
                Header = u'��·�ȼ�',u'��·����',u'����',u'ʱ',u'��',u'����ӵ������',u'��ͨ��ռ�ٷֱ�',u'������ռ�ٷֱ�',u'ӵ����ռ�ٷֱ�',u'δ֪·����ռ�ٷֱ�',u'��··��',u'����',u'�Ƕ�',u'�ٶ�',u'��γ��'
                filename = filepath+road_name+'.csv'
                with open(filename, "w", newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerow(Header)
                
        
###########################Get congestion info#################################
def road_congestion(sc):

    start = time.clock()#��¼��ʼʱ�䣬Ϊ�˹۲���ȡһ����Ҫ���
    print('��ʼʱ��Ϊ��',start)    

    for i in range(1,7):
        print('���ڿ�ʼ��ѯlevel=',i)
        url=url0+'key='+ak+'&rectangle='+lng1+','+lat1+';'+lng2+','+lat2+'&extensions=all'+'&level='+str(i)
        res=urlopen(url)
        cet=res.read()
        result=json.loads(cet)
        print(result)
    
        date=(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        h=(time.strftime('%H',time.localtime(time.time())))
        m=(time.strftime('%M',time.localtime(time.time())))
    
        trafficinfo=result['trafficinfo']
        description=trafficinfo['description']#'����ӵ������'
        expedite=trafficinfo['evaluation']['expedite']#'��ͨ��ռ�ٷֱ�'
        congested=trafficinfo['evaluation']['congested']#'������ռ�ٷֱ�'
        blocked=trafficinfo['evaluation']['blocked']#'ӵ����ռ�ٷֱ�'
        unknown=trafficinfo['evaluation']['unknown']#'δ֪��·��ռ�ٷֱ�'
    
        roads=trafficinfo['roads']
 
        if len(roads)==0:
            print('level=',i,'�������޿ɲ�ѯ��·��')
        else:
            for element in roads:
                road_name=element['name']
                filename = filepath+road_name+'.csv'
            
                if len(element)==1:#ֻ����·����������ӵ�����
                    traffic=[i,road_name,date,h,m,description,expedite,congested,blocked,unknown]
                else:
                    status=valid(element,'status')#��··��
                    direction=valid(element,'direction')#'����'
                    angle=valid(element,'angle')#'�Ƕ�'
                    speed=valid(element,'speed')#'�ٶ�'
                    polyline=valid(element,'polyline')#'ƽ��ͨ���ٶ�'
                    traffic=[i,road_name,date,h,m,description,expedite,congested,blocked,unknown,status,direction,angle,speed,polyline]
                
                #print(traffic)
                f = csv.writer(open(filename, "a+",newline=''))
                f.writerow(traffic)

    end = time.clock()#��¼����ʱ��
    print('����ʱ��Ϊ',end)
    
    cost = end-start#�����������ʱ�䣬6��·���ռ��2��
    print("��������ʱ��Ϊ : %.03f seconds" %(cost)) 
    
    sc.enter(step_length, 1, road_congestion, (sc,))

#################��������ʼ#########################      
s = sched.scheduler(time.time, time.sleep)

road_names()#�����ļ�����д��ͷ

s.enter(step_length, 1, road_congestion, (s,)) # ���ú�������ʽΪ(delay, priority, action, argument)
s.run()        
    

