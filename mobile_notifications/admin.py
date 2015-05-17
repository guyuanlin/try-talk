from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import IOSDevice, AndroidDevice, History


def make_testing_device(modeladmin, request, queryset):
    queryset.update(testing=True)
make_testing_device.short_description = _(
    'Mark selected devices as testing devices'
)


def make_none_testing_devices(modeladmin, request, queryset):
    queryset.update(testing=False)
make_none_testing_devices.short_description = _(
    'Mark selected devices as none-testing devices'
)


class DeviceAdmin(admin.ModelAdmin):

    fields = ('user', 'reg_id', 'testing')
    list_display = ('reg_id', 'user', 'testing')
    raw_id_fields = ('user',)
    actions = [
        make_testing_device,
        make_none_testing_devices
    ]

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class IOSDeviceAdmin(DeviceAdmin):
    pass


class AndroidDeviceAdmin(DeviceAdmin):
    pass


class HistoryAdmin(admin.ModelAdmin):

    list_display = ('content', 'send_time')
    readonly_fields = ('content', 'send_time')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(IOSDevice, IOSDeviceAdmin)
admin.site.register(AndroidDevice, AndroidDeviceAdmin)
admin.site.register(History, HistoryAdmin)
