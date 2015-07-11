from django.contrib import admin

from . import models

@admin.register(models.Guest)
class GuestAdmin(admin.ModelAdmin):

	list_display = ('guest_id', 'user')
	readonly_fields = ('guest_id', 'user', 'create')