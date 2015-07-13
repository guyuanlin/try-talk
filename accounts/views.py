# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from rest_framework import viewsets, mixins, status, permissions
from django.contrib.auth import get_user_model
from rest_framework.decorators import (
	list_route, authentication_classes, permission_classes
)
from rest_framework.response import Response
from django.utils.translation import ugettext as _

from . import serializers, models


class GuestUserViewSet(viewsets.GenericViewSet):

	throttle_classes = ()
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	model = get_user_model()
	queryset = get_user_model().objects.all()
	serializer_class = serializers.LoginSerializer

	@list_route(methods=['post'])
	def login(self, request):
		"""
		試用者登入(不需Token)

		首次登入時 guest_id 請填入空值，登入後，後端會生成一組唯一 ID 用來識別此試用者<br>
		若登出後，再次使用試用者身份登入的話，請將前次取得的 guest_id 輸入 guest_id<br>
		以便讓後台可是別此使用者，將他先前輸入的資料撈出來呈現<br> 
		---
		response_serializer: serializers.LoginSerializer
		parameters:
			- name: guest_id
			  description: 試用者 ID(首次登入請填空值，登出後若要再次登入才需要填入前次從後端取得的 ID)
			  required: False
			  type: string
			  paramType: form

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報，會回傳的 keys 為 guest_id
		"""
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)