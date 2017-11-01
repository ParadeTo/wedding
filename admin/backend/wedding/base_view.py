# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.views import View

OK_MSG = 'ok'
OK_CODE = 0

class BaseView(View):
    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self._request_method = None
        self._request = None
        self._status_code = 200
        self._request_data_dict = {}
        self._response_data_dict = {
            'msg': OK_MSG,
            'ret': OK_CODE,
            'data': {}
        }

    def get_request_data_dict(self):
        return self._request_data_dict

    def dispatch(self, request, *args, **kwargs):
        # try:
        request_method = request.method.lower()
        self._request_method = request_method
        self._request = request

        processor = getattr(self, request_method, None)
        if not processor:
            return self.http_method_not_allowed(request, *args, **kwargs)
        return self.build_response(processor, *args, **kwargs)
        # except Exception as e:
        #     return self.raise_exc(e)


    def _fetch_body_data(self, request, *args, **kwargs):
        json_data = request.body
        if not json_data:
            return {}
        try:
            params_dict = json.loads(json_data)
            return params_dict
        except ValueError:
            # when js call $.ajax(data: JSON.stringify({xxxx}))
            # request.POST will be
            # <QueryDict: {u'{"date":"2014-9-20"}': [u'']}>
            return {}
            # raise ParamError(code_tuple=Code.PARAM_VALUE_INVALID, msg='json_params_invalid')

    def _fetch_get_data(self, request, *args, **kwargs):
        # params_dict = dict([(key.encode('utf8', 'replace'), value)
        params_dict = dict([(key, value)
                           for key, value in
                           request.GET.items()])
        for key, value in params_dict.items():
            if isinstance(value, list) and len(value) == 1:
                params_dict[key] = value[0]
        return params_dict or {}

    def _fetch_post_data(self, request, *args, **kwargs):
        params_dict = dict([(key.encode('utf8', 'replace'), value)
                           for key, value in
                           request.POST.items()])
        for key, value in params_dict.items():
            if isinstance(value, list) and len(value) == 1:
                params_dict[key] = value[0]
        return params_dict or {}

    def format_request(self, request, *args, **kwargs):
        if self._request_method == 'get':
            self._request_data_dict.update(
                self._fetch_get_data(request, *args, **kwargs)
            )
        elif self._request_method in ['post', 'put']:
            body_dict = self._fetch_body_data(request, *args, **kwargs)
            if body_dict:
                self._request_data_dict.update(
                    self._fetch_body_data(request, *args, **kwargs)
                )
            else:
                self._request_data_dict.update(
                    self._fetch_post_data(request, *args, **kwargs)
                )
        elif self._request_method == 'delete':
            if request.GET:
                self._request_data_dict.update(
                    self._fetch_get_data(request, *args, **kwargs)
                )
            else:
                self._request_data_dict.update(
                    self._fetch_body_data(request, *args, **kwargs)
                )
        self._request_data_dict.update(kwargs)

    def build_response(self, processor, *args, **kwargs):
        self.format_request(self._request, *args, **kwargs)

        result = processor(self._request)

        # 兼容原来的json数据返回,也支持template返回
        if result is None:
            return self._render_response()
        # 如果get/post/delete/put有返回,则使用其返回方式
        else:
            return result

    def _render_response(self):
        response_json_data = json.dumps(self._response_data_dict)
        print(self._response_data_dict)
        callback = self._request_data_dict.get('_jsonp', '')
        if callback:
            jsonp = u'%s(%s)' % (callback, response_json_data)
            return HttpResponse(jsonp, status=self._status_code)
        else:
            response = HttpResponse(
                response_json_data,
                content_type='application/json',
                status=self._status_code,
            )
        if self._status_code == 401:
            response['WWW-Authenticate'] = 'Basic realm="USER LOGIN"'
        return response

    def raise_exc(self, e, *args, **kwargs):
        self.pre_handler_error(e)
        self._handler_error(e)
        self.post_handler_error(e)
        return self._render_response()

    def pre_handler_error(self, e):
        pass

    def post_handler_error(self, e):
        pass

    def _handler_error(self, e):
        # if isinstance(e, AuthError):
        #     self.set_status(401)
        # elif isinstance(e, ForbiddenError):
        #     self.set_status(403)
        # else:
        #     self.set_status(400)
        # data = getattr(e, 'data', None)
        # if data:
        #     self.write_data({'tips': data})
        self._response_data_dict.update({
            'msg': str(e),
            'ret': '-1',
        })