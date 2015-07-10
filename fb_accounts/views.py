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
		serializer.save()
		return Response(serializer.data)
