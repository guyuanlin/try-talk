# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.utils.translation import ugettext as _
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import IOSDeviceSerializer, AndroidDeviceSerializer
from .models import IOSDevice, AndroidDevice
from .senders import GCMNotification, gcm_send, APNSNotification, apns_send


class DeviceViewSet(mixins.CreateModelMixin,
					viewsets.GenericViewSet):

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class IOSDeviceViewSet(DeviceViewSet):

	queryset = IOSDevice.objects.all()
	serializer_class = IOSDeviceSerializer

	def create(self, request):
		"""
		註冊 iOS 裝置推播序號<br>
		"""
		try:
			reg_id = request.data.get('reg_id', None)
			instance = IOSDevice.objects.get(reg_id=reg_id)
			serializer = self.get_serializer(
				instance=instance,
				data=request.data
			)
			serializer.is_valid(raise_exception=True)
			serializer.save(user=request.user)
			return Response(serializer.data)
		except IOSDevice.DoesNotExist:
			return super(IOSDeviceViewSet, self).create(request)

	@parser_classes((JSONParser,))
	@list_route(methods=['post'])
	def push(self, request):
		"""
		針對特定裝置序號進行推播(測試用)<br />

		本 API 須於 Header 中設定 Content-Type 為 application/json<br />
		使用 JSON Object 格式字串輸入 request body 中執行<br />

		request 範例：
		<pre>
{
  "reg_id": "target device registration id",
  "use_sandbox": true,
  "data": {
    "alert": "this is alert message",
    "badge": 1,
    "content_available": 0,
    "custom": {
      "type": "test_type",
      "pk": -1
    }
  }
}
		</pre>
		各欄位說明如下：<br />
		<pre>
reg_id(string) : 測試裝置推播序號
use_sandbox(boolean) : 是否為 use_sandbox 模式發送(與設為 true)
data(object) : 推播詳細資料
	alert(string) : 推播顯示訊息
	badge(integer) : 提醒數字
	content_available(integer) : 設定 content-available 參數
	custom(object) : 客製化推播內容，針對不同 APP 會有不同的內容，以下為範例說明
		type(string) : 標示需開啟何種功能頁面
		pk(integer) : 此 pk(primary key) 搭配 type 可決定需開啟哪個項目的頁面，若不需開啟特定項目頁面，則此欄位為 -1
		</pre>
		---
		omit_serializer: true

		omit_parameters:
			- form

		parameters:
			- name: Content-Type
			  description: 指定 request 的資料型態，必須為 application/json
			  paramType: header
			  required: true
			  allowMultiple: false
			  enum: ["application/json"]
			- name: body
			  description: 推播內容，使用 JSON 格式
			  required: True
			  type: string
			  paramType: body

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 400
			  message: 當輸入 JSON 格式錯誤時 
			- code: 403
			  message: HTTP Header 沒有 token 或是 token 不正確，認證失敗
		"""
		reg_id = request.data.get('reg_id', None)
		if reg_id:
			device = IOSDevice(
				id=1,
				reg_id=reg_id
			)
			use_sandbox = request.data.get('use_sandbox', True)
			data = request.data.get('data')
			alert = data.get('alert', 'this is alert message')
			badge = data.get('badge', 1)
			content_available = data.get('content_available', 0)
			custom = data.get('custom', {})
			notification = APNSNotification(
				device=device,
				alert=alert,
				badge=badge,
				content_available=bool(content_available),
				custom=custom
			)
			apns_send(
				notifications=[notification],
				use_sandbox=use_sandbox
			)
			data = {
				'detail': _(u'已成功發送推播')
			}
			return Response(data)
		else:
			errors = {
				'detail': _(u'未指定推播裝置序號')
			}
			return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class AndroidDeviceViewSet(DeviceViewSet):

	queryset = AndroidDevice.objects.all()
	serializer_class = AndroidDeviceSerializer

	def create(self, request):
		"""
		註冊 Android 裝置推播序號
		"""
		try:
			reg_id = request.data.get('reg_id', None)
			instance = AndroidDevice.objects.get(reg_id=reg_id)
			serializer = self.get_serializer(
				instance=instance,
				data=request.data
			)
			serializer.is_valid(raise_exception=True)
			serializer.save(user=request.user)
			return Response(serializer.data)
		except AndroidDevice.DoesNotExist:
			return super(AndroidDeviceViewSet, self).create(request)

	@parser_classes((JSONParser,))
	@list_route(methods=['post'])
	def push(self, request):
		"""
		針對特定裝置序號進行推播(測試用)<br />

		本 API 須於 Header 中設定 Content-Type 為 application/json<br />
		使用 JSON Object 格式字串輸入 request body 中執行<br />

		request 範例：
		<pre>
{
  "reg_ids": ["裝置序號1", "裝置序號2"],
  "collapse_key": "test",
  "data": {
    "title": "this is title",
    "content": "this is content",
    "custom": {
      "type": "test",
      "pk": -1
    }
  }
}
		</pre>
		各欄位說明如下：<br />
		<pre>
reg_ids(array) : 註冊序號列表
collapse_key(string) : GCM 分類名稱，每種 collapse_key 只會在 GCM Server 保留最新的推播資料，若有相同 collapse_key 的推播，則舊的會被刪除
data(object) : 推播詳細資料
	title(string) : 標題，顯示於推播標題欄位
	content(string) : 推播內容
	custom(object) : 點擊推播後開啟對應頁面的必要資訊
		type(string) : 標示需開啟何種功能頁面(尚未定義)
		pk(integer) : 此 pk(primary key) 搭配 type 可決定需開啟哪個項目的頁面，若不需開啟特定項目頁面，則此欄位為 -1
		</pre>
		---
		omit_serializer: true

		omit_parameters:
			- form

		parameters:
			- name: Content-Type
			  description: 指定 request 的資料型態，必須為 application/json
			  paramType: header
			  required: true
			  allowMultiple: false
			  enum: ["application/json"]
			- name: body
			  description: 推播內容，使用 JSON 格式
			  required: True
			  type: string
			  paramType: body

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 400
			  message: 當輸入 JSON 格式錯誤時 
			- code: 403
			  message: HTTP Header 沒有 token 或是 token 不正確，認證失敗
		"""
		reg_ids = request.data.get('reg_ids', [])
		if reg_ids:
			collapse_key = request.data.get('collapse_key', None)
			data = request.data.get('data')
			notification = GCMNotification(
				reg_ids=reg_ids,
				data=data,
				collapse_key=collapse_key
			)
			gcm_send(notification)
		return Response(None)