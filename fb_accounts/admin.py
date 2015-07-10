from django.contrib import admin

from . import models

@admin.register(models.FacebookID)
class FacebookIDAdmin(admin.ModelAdmin):

	list_display = ('fb_id', 'user')
	readonly_fields = ('fb_id', 'user')