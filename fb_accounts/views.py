# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from rest_framework import viewsets, mixins, status, permissions
from django.contrib.auth import get_user_model
from rest_framework.decorators import (list_route, api_view, detail_route,
									   authentication_classes, permission_classes)
from rest_framework.response import Response
from django.utils.translation import ugettext as _

from . import serializers, models
from accounts.utils import send_auth_code_sms

FB_ID_KEY = 'fb_id'


class FacebookUserViewSet(viewsets.GenericViewSet):

	throttle_classes = ()
	permission_classes = (
		permissions.AllowAny,
	)
	authentication_classes = ()
	model = get_user_model()
	queryset = get_user_model().objects.all()
	serializer_class = serializers.LoginSerializer

	@list_route(methods=['post'])
	def login(self, request):
		"""
		Facebook 會員登入(不需 Token)<br>

		若 status code 為 200，需注意以下兩種情況：<br>
		<ul>
			<li>is_registered = False : 表示此 Facebook ID 尚未註冊，請進入會員資料填寫頁面</li>
			<li>is_registered = True, auth_token = null : 表示已註冊，但尚未通過認證，請進入認證碼頁面</li>
		</ul>
		---
		response_serializer: serializers.LoginSerializer
		parameters:
			- name: fb_id
			  description: 使用者的 Facebook ID
			  required: True
			  type: string
			  paramType: form

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報，會回傳的 keys 為 fb_id 
			  		   與 non_field_errors(密碼錯誤時會使用此欄位顯示)
		"""
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		is_registered = serializer.data['is_registered']
		if is_registered:
			serializer.save()
		return Response(serializer.data)

	@list_route(methods=['post'])
	def register(self, request):
		"""
		Facebook 會員註冊(不需 Token)<br>

		當完成註冊後，請呼叫 mobile_notifications/ios/ 或 mobile_notifications/android/ 註冊裝置序號<br>
		(因為登入時若此 FB ID 尚未註冊，輸入的裝置序號不會記錄到資料庫中)<br>
		---
		serializer: serializers.RegisterSerializer
		omit_serializer: false

		parameters:
			- name: fb_id
			  description: 使用者的 Facebook ID
			  required: true
			  type: string
			  paramType: form
			- name: first_name
			  description: 名稱，30 個字元以下，可輸入任意字元
			  required: true
			  type: string
			  paramType: form
			- name: birthday
			  description: 生日，格式為 ISO-8601 日期標準，例如 1985-01-01
			  required: True
			  type: string
			  paramType: form

		responseMessages:
			- code: 201
			  message: 成功新增會員
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報，會回傳的 keys 為 username, 
			  		   email, first_name, password, phone, address 與 non_field_errors(當錯誤訊息是跨多欄位時，使用此 key 顯示錯誤)
		"""
		if (FB_ID_KEY not in request.data) or (not request.data[FB_ID_KEY]):
			errors = {
				FB_ID_KEY: _(u'此欄位是必須的。')
			}
			return Response(errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			fb_id = request.data[FB_ID_KEY]
			exists = models.FacebookID.objects.filter(
				fb_id=fb_id
			).exists()
			if exists:
				errors = {
					'detail': _(u'Facebook ID 已存在')
				}
				return Response(errors, status=status.HTTP_400_BAD_REQUEST)

			serializer = serializers.RegisterSerializer(
				data=request.data
			)
			serializer.is_valid(raise_exception=True)
			user = serializer.save(
				fb_id=fb_id
			)
			send_auth_code_sms(user)
			return Response(serializer.data)
