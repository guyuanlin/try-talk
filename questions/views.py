# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from rest_framework import viewsets, mixins

from . import models, serializers

class QuestionViewSet(mixins.CreateModelMixin,
				 	  viewsets.GenericViewSet):

	model = models.Question
	queryset = models.Question.objects.active()
	serializer_class = serializers.QuestionSerializer