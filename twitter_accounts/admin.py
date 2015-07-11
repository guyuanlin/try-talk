from django.contrib import admin

from . import models

@admin.register(models.TwitterID)
class TwitterIDAdmin(admin.ModelAdmin):

	list_display = ('twitter_id', 'user')
	readonly_fields = ('twitter_id', 'user', 'create')