# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import math
import simplejson
from django.db import models


class CheckinStatus(models.Model):
    accountid = models.IntegerField(db_column='accountID')  # Field name made lowercase.
    status = models.CharField(max_length=7)
    createtime = models.DateTimeField(db_column='createTime')  # Field name made lowercase.
    lastupdatetime = models.DateTimeField(db_column='lastUpdateTime')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'checkin_status'


class Feeds(models.Model):
    accountid = models.IntegerField(db_column='accountID')  # Field name made lowercase.
    nickname = models.CharField(db_column='nickName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    headimgurl = models.CharField(db_column='headImgUrl', max_length=300, blank=True, null=True)  # Field name made lowercase.
    msgtype = models.IntegerField(db_column='msgType', blank=True, null=True)  # Field name made lowercase.
    msg = models.TextField(blank=True, null=True)
    visible = models.IntegerField()
    createtime = models.DateTimeField(db_column='createTime')  # Field name made lowercase.
    lastupdatetime = models.DateTimeField(db_column='lastUpdateTime')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'feeds'


class WxAccounts(models.Model):
    accountid = models.IntegerField(db_column='accountID', primary_key=True)  # Field name made lowercase.
    openid = models.CharField(db_column='openID', unique=True, max_length=50)  # Field name made lowercase.
    nickname = models.CharField(db_column='nickName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sex = models.IntegerField(blank=True, null=True)
    province = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    headimgurl = models.CharField(db_column='headImgUrl', max_length=300, blank=True, null=True)  # Field name made lowercase.
    privilege = models.TextField(blank=True, null=True)
    accesstoken = models.CharField(db_column='accessToken', max_length=500)  # Field name made lowercase.
    refreshtoken = models.CharField(db_column='refreshToken', max_length=500)  # Field name made lowercase.
    expirein = models.IntegerField(db_column='expireIn')  # Field name made lowercase.
    tokentime = models.DateTimeField(db_column='tokenTime', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='createTime')  # Field name made lowercase.
    lastupdatetime = models.DateTimeField(db_column='lastUpdateTime')  # Field name made lowercase.
    lastcheckinstatus = models.CharField(db_column='lastCheckinStatus', max_length=7, blank=True, null=True)  # Field name made lowercase.

    # def __str__(self):
    #     print(self.nickname)
    #     return self.nickname

    @staticmethod
    def list(page, limit):
        page = int(page)
        limit = int(limit)
        total_items = WxAccounts.objects.count()
        total_page = math.ceil(total_items / limit)
        list = []

        if page <= total_page:
            offset = (page - 1) * limit
            query_set = WxAccounts.objects.all()[offset : offset + limit]
            for item in query_set:
                print(item)
                d = {
                    "nickname": item.nickname,
                    "sex": item.sex,
                    "province": item.province
                }
                list.append(d)
        return list


    class Meta:
        # managed = False
        db_table = 'wx_accounts'


class TestTable(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()