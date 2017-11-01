# -*- coding: utf-8 -*-
from django.http import HttpResponse

from .base_view import BaseView
from .models import WxAccounts
from django.db import models
# Create your views here.


class AccountView(BaseView):
    def get(self, request):
        request_dict = self.get_request_data_dict()
        accounts = WxAccounts.list(**request_dict)
        self._response_data_dict['data'] = accounts

