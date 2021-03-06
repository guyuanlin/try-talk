# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.contrib.gis.geos import fromstr
from django.utils.translation import ugettext as _
from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.renderers import JSONRenderer

from . import models, serializers, tasks

class QuestionViewSet(mixins.CreateModelMixin,
					  mixins.ListModelMixin,
					  mixins.DestroyModelMixin,
					  viewsets.GenericViewSet):

	model = models.Question
	queryset = models.Question.objects.active()
	serializer_class = serializers.QuestionSerializer
	filter_backends = (filters.OrderingFilter,)
	ordering_fields = ('update', 'reply_count')

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

		# add push notification task for the created question
		renderer = JSONRenderer()
		question_data = renderer.render(data=serializer.data)
		tasks.push_question.delay(question_data)

	def create(self, request, *args, **kwargs):
		"""
		新增問題
		
		可於 Request Header 設定以下其中一種 Content-Type 發送 Request

		1. application/json，範例如下：
		<pre>
{
  "category": "food",
  "content": "問題內容",
  "location": "POINT(121.517553 25.046283)",
  "tags": ["tag1", "tag2", "tag3", "tag4"]
}
		</pre>


		2. application/x-www-form-urlencoded，範例如下：
		
		category=food&content=%E5%95%8F%E9%A1%8C%E5%85%A7%E5%AE%B9&location=POINT(121.517553+25.046283)&tags=tag1&tags=tag2&tags=tag3&tags=tag4
		---
		response_serializer: serializers.QuestionSerializer

		parameters:
			- name: category
			  description: 問題分類
			  required: True
			  type: choice
			  enum: ['food', 'shop', 'location', 'other']
			  paramType: form
			- name: content
			  description: 問題內容(字數上限為 500 字)
			  required: True
			  type: string
			  paramType: form
			- name: location
			  description: 發問位置，字串格式為"POINT($longtitude $latitude)"，例如 POINT(121.517553 25.046283)
			  defaultValue: POINT(121.517553 25.046283)
			  required: True
			  type: string
			  paramType: form
			- name: tags
			  description: 關鍵字，若有多個關鍵字，送出 request 時，可送出多個以 "tags" 為 key 的欄位，最多 4 個關鍵字
			  required: False
			  type: string
			  paramType: form

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報
		"""
		return super(QuestionViewSet, self).create(request, *args, **kwargs)

	def list(self, request, *args, **kwargs):
		"""
		問題列表
		
		---
		response_serializer: serializers.QuestionSerializer

		parameters:
			- name: location
			  description: 使用者所在位置，字串格式為"POINT($longtitude $latitude)"，例如 POINT(121.517553 25.046283)
			  defaultValue: POINT(121.517553 25.046283)
			  required: True
			  type: string
			  paramType: query
			- name: offset
			  description: 資料起始 index，從 0 開始
			  defaultValue: 0
			  required: false
			  type: integer
			  paramType: query
			- name: limit
			  description: 每次撈取的問題數量
			  defaultValue: 20
			  required: false
			  type: integer
			  paramType: query
			- name: ordering
			  defaultValue: distance
			  description: 排序方法：distance(距離排序), -update(更新時間排序), -reply_count(回覆數排序)
			  required: false
			  enum: [distance, -update, -reply_count]
			  type: string
			  paramType: query

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報
		"""
		if serializers.USER_LOCATION_KEY not in request.query_params:
			errors = {
				'detail': _(u'必須設定 location 參數')
			}
			return Response(errors, status=status.HTTP_400_BAD_REQUEST)
			
		ordering = self.request.query_params.get('ordering', 'distance')
		user_location = None
		try:
			user_location = fromstr(self.request.query_params[serializers.USER_LOCATION_KEY])
			# store user location
			models.UserLocationHistory.objects.create(
				user=request.user,
				location=user_location,
			)

			if ordering == 'distance':
				queryset = models.Question.objects.active().distance(user_location).order_by('distance')
			else:
				queryset = self.filter_queryset(self.get_queryset())

			page = self.paginate_queryset(queryset)
			if page is not None:
				serializer = self.get_serializer(page, many=True)
				return self.get_paginated_response(serializer.data)

			serializer = self.get_serializer(queryset, many=True)
			return Response(serializer.data)
		except:
			errors = {
				'detail': _(u'location 格式錯誤，正確格式為 POINT($longtitude $latitude)')
			}
			return Response(errors, status=status.HTTP_400_BAD_REQUEST)

	@detail_route(methods=['get'])
	def replys(self, request, *args, **kwargs):
		"""
		回覆列表
		
		---
		response_serializer: serializers.ReplySerializer

		parameters:
			- name: pk
			  description: 問題 ID
			  required: True
			  type: integer
			  paramType: path
			- name: offset
			  description: 資料起始 index，從 0 開始
			  defaultValue: 0
			  required: false
			  type: integer
			  paramType: query
			- name: limit
			  description: 每次撈取的問題數量
			  defaultValue: 20
			  required: false
			  type: integer
			  paramType: query

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報
		"""
		question = self.get_object()
		queryset = question.replys.all().order_by('id')

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = serializers.ReplySerializer(
				page,
				many=True,
				context={
					'request': request
				}
			)
			return self.get_paginated_response(serializer.data)

		serializer = serializers.ReplySerializer(
			queryset,
			many=True,
			context={
				'request': request
			}
		)
		return Response(serializer.data)

	@detail_route(methods=['post'])
	def reply(self, request, *args, **kwargs):
		"""
		新增回覆
		---
		serializer: serializers.ReplySerializer

		parameters:
			- name: pk
			  description: 問題 ID
			  required: True
			  type: integer
			  paramType: path
			- name: content
			  description: 回覆內容
			  required: True
			  type: string
			  paramType: form
			- name: location
			  description: 發問位置，字串格式為"POINT($longtitude $latitude)"，例如 POINT(121.517553 25.046283)
			  defaultValue: POINT(121.517553 25.046283)
			  required: True
			  type: string
			  paramType: form

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報
		"""
		question = self.get_object()
		serializer = serializers.ReplySerializer(
			data=request.data,
			context={
				'request': request
			}
		)
		serializer.is_valid(raise_exception=True)
		serializer.save(
			user=request.user,
			question=question,
		)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def destroy(self, request, *args, **kwargs):
		"""
		刪除問題
		---
		omit_serializer: True

		parameters:
			- name: pk
			  description: 問題 ID
			  required: True
			  type: integer
			  paramType: path

		responseMessages:
			- code: 204
			  message: 刪除成功
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報
			- code: 404
			  message: 問題 ID 不存在
		"""
		question = self.get_object()
		if question.owner.pk != request.user.pk:
			errors = {
				'detail': _(u'您無權限刪除此問題')
			}
			return Response(errors, status=status.HTTP_400_BAD_REQUEST)

		return super(QuestionViewSet, self).destroy(request, *args, **kwargs)

	@list_route(methods=['get'])
	def history(self, request, *args, **kwargs):
		"""
		我的提問
		---
		response_serializer: serializers.QuestionSerializer

		parameters:
			- name: offset
			  description: 資料起始 index，從 0 開始
			  defaultValue: 0
			  required: false
			  type: integer
			  paramType: query
			- name: limit
			  description: 每次撈取的問題數量
			  defaultValue: 20
			  required: false
			  type: integer
			  paramType: query

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報
		"""
		queryset = models.Question.objects.filter(
			owner=request.user
		).order_by('-update')
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	@list_route(methods=['get'])
	def replied(self, request, *args, **kwargs):
		"""
		我的解答
		---
		response_serializer: serializers.QuestionSerializer

		parameters:
			- name: offset
			  description: 資料起始 index，從 0 開始
			  defaultValue: 0
			  required: false
			  type: integer
			  paramType: query
			- name: limit
			  description: 每次撈取的問題數量
			  defaultValue: 20
			  required: false
			  type: integer
			  paramType: query

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報
		"""
		queryset = models.Question.objects.filter(
			id__in=models.Question.objects.filter(replys__user=request.user).distinct()
		).order_by('-update')
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


class ReplyViewSet(mixins.DestroyModelMixin,
				   viewsets.GenericViewSet):

	model = models.Reply
	queryset = models.Reply.objects.active()
	serializer_class = serializers.ReplySerializer

	def destroy(self, request, *args, **kwargs):
		"""
		刪除回覆
		---
		omit_serializer: True

		parameters:
			- name: pk
			  description: 回覆 ID
			  required: True
			  type: integer
			  paramType: path

		responseMessages:
			- code: 204
			  message: 刪除成功
			- code: 400
			  message: 輸入的參數有錯誤，將有錯誤的欄位與訊息個別回報
			- code: 404
			  message: 回覆 ID 不存在
		"""
		reply = self.get_object()
		if reply.question.owner.pk != request.user.pk and reply.user.pk != request.user.pk:
			errors = {
				'detail': _(u'您無權限刪除此回覆')
			}
			return Response(errors, status=status.HTTP_400_BAD_REQUEST)

		return super(ReplyViewSet, self).destroy(request, *args, **kwargs)

	@detail_route(methods=['post'])
	def like(self, request, *args, **kwargs):
		"""
		回覆按讚
		---
		response_serializer: serializers.ReplySerializer

		omit_parameters:
        	- form
		parameters:
			- name: pk
			  description: 回覆 ID
			  required: True
			  type: integer
			  paramType: path

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 404
			  message: 回覆 ID 不存在
		"""
		reply = self.get_object()
		reply.likes.add(request.user)
		serializer = serializers.ReplySerializer(
			reply,
			context={
				'request': request
			}
		)
		return Response(serializer.data)

	@detail_route(methods=['post'])
	def cancel_like(self, request, *args, **kwargs):
		"""
		回覆取消按讚
		---
		response_serializer: serializers.ReplySerializer

		omit_parameters:
        	- form
		parameters:
			- name: pk
			  description: 回覆 ID
			  required: True
			  type: integer
			  paramType: path

		responseMessages:
			- code: 200
			  message: 執行成功
			- code: 404
			  message: 回覆 ID 不存在
		"""
		reply = self.get_object()
		reply.likes.remove(request.user)
		serializer = serializers.ReplySerializer(
			reply,
			context={
				'request': request
			}
		)
		return Response(serializer.data)