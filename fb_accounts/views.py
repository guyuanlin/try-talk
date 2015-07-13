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
		Facebook 登入(不需Token)
		
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
		"""
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)
