#!/usr/bin/env python
# coding: utf-8

# In[19]:


import json
import urllib
from urllib.request import Request, urlopen
import requests


# In[43]:


class NabverLocalAPI:

    def __init__(self, client_id, client_secret):
        """
        Rest API키 초기화 및 기능 별 URL 설정
        """

        # REST API 키 설정
        self.client_id = client_id
        self.client_secret = client_secret

        # 서비스 별 URL 설정

        # 01. 주소 -> 위경도 추출
        self.URL_01 = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query="
        # 02. 위경도 활용 경로 찾기(자가용 기준) 
        self.URL_02 = "https://naveropenapi.apigw.ntruss.com/map-direction-15/v1/driving?"



    # 주소에 geocoding 적용하는 함수를 작성.
    def get_location(self, loc) :
        """
        01.주소 활용 위경도 추출
        """

       # url = self.URL_01 + urllib.parse.quote(loc)

        # 주소 변환
        request = Request(self.URL_01 + urllib.parse.quote(loc))
        request.add_header('X-NCP-APIGW-API-KEY-ID', self.client_id)
        request.add_header('X-NCP-APIGW-API-KEY', self.client_secret)

        response = urlopen(request)
        res = response.getcode()

        if (res == 200) : # 응답이 정상적으로 완료되면 200을 return한다
            response_body = response.read().decode('utf-8')
            response_body = json.loads(response_body)
            #print(response_body)
            # 주소가 존재할 경우 total count == 1이 반환됨.
            if response_body['meta']['totalCount'] == 1 : 
                # 위도, 경도 좌표를 받아와서 return해 줌.
                lat = response_body['addresses'][0]['y']
                lon = response_body['addresses'][0]['x']
                return (lon, lat)
            else :
                print('location not exist')

        else :
            print('ERROR')



    # *-- Directions 5 활용 코드 --*
    option = ''
    # option : 탐색옵션 [최대 3개, traoptimal(기본 옵션) 
    # / trafast, tracomfort, traavoidtoll, traavoidcaronly]

    def get_optimal_route(self, start, goal, waypoints=['',''], option=option ) :
        """
        02.위경도 활용 경로 찾기(자가용 기준) 
        option : 탐색옵션 [최대 3개, traoptimal(기본 옵션) 
        [trafast, tracomfort, traavoidtoll, traavoidcaronly]
        """

        # start=/goal=/(waypoint=)/(option=) 순으로 request parameter 지정
        url = f"{self.URL_02}start={start[0]},{start[1]}&goal={goal[0]},{goal[1]}"

        request = urllib.request.Request(url)
        request.add_header('X-NCP-APIGW-API-KEY-ID', self.client_id)
        request.add_header('X-NCP-APIGW-API-KEY', self.client_secret)


        response = urllib.request.urlopen(request)
        res = response.getcode()

        if (res == 200) :
            response_body = response.read().decode('utf-8')
            return json.loads(response_body)

        else :
            print('ERROR')


# In[ ]:





# In[ ]:




