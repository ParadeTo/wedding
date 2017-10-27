from django.contrib import admin

# Register your models here.
from .models import CheckinStatus, Feeds, WxAccounts

admin.site.register(CheckinStatus)
admin.site.register(Feeds)
admin.site.register(WxAccounts)