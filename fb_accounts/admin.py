from django.contrib import admin

from . import models

@admin.register(models.FacebookID)
class FacebookIDAdmin(admin.ModelAdmin):

	list_display = ('user', 'fb_id')
	fields = ('user', 'fb_id')