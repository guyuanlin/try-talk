from django.contrib import admin

from . import models


class ReplyInline(admin.TabularInline):

	model = models.Reply
	fields = (
		'user', 'content', 'like_count', 'is_active', 'create'
	)
	# readonly_fields = (
	# 	'user', 'content', 'like_count', 'create'
	# )
	readonly_fields = ('like_count', 'create')

	# def has_add_permission(self, request):
	# 	return False


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):

	list_display = ('content', 'category', 'create')
	fields = (
		'owner', 'category', 'content', 'location',
		'tags', 'create', 'update', 'is_active',
	)
	# readonly_fields = (
	# 	'owner', 'category', 'content', 'location',
	# 	'tags', 'create', 'update', 'is_active',
	# )
	readonly_fields = ('create', 'update')
	date_hierarchy = 'create'
	filter_horizontal = ('tags',)
	list_filter = ('category',)
	search_fields = ('content',)
	inlines = (ReplyInline,)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):

	list_display = ('name',)
	fields = ('name',)
	search_fields = ('name',)
