from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from rest_framework import routers
from accounts import views as accounts_views
from fb_accounts import views as fb_accounts_views
from twitter_accounts import views as twitter_accounts_views
from mobile_notifications import views as mobile_notifications_views
from questions import views as questions_views

router = routers.DefaultRouter()
router.register(r'accounts/guest', accounts_views.GuestUserViewSet)
router.register(r'accounts/facebook', fb_accounts_views.FacebookUserViewSet)
router.register(r'accounts/twitter', twitter_accounts_views.TwitterUserViewSet)
router.register(r'mobile_notifications/ios', mobile_notifications_views.IOSDeviceViewSet)
router.register(r'questions', questions_views.QuestionViewSet)
router.register(r'replys', questions_views.ReplyViewSet)

urlpatterns = patterns(
	'',
	url(r'^api/', include(router.urls)),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/docs/', include('rest_framework_swagger.urls')),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
