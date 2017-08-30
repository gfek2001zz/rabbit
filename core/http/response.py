#!/usr/bin/python
from http.client import responses
from core.context import applicationContext

class HttpReponse:
    status_code = 200

    def __init__(self, content, content_type = None, status = None, status_name = None, charset=None):
        self._headers = {}
        self.content = content

        if status is not None:
            try:
                self.status_code = int(status)
            except(ValueError, TypeError):
                raise TypeError('HTTP状态码必须为数字')

            if not 100 <= self.status_code <= 599:
                raise ValueError("HTTP状态码不规范")

        self._status_name = status_name

        self._charset = charset
        if content_type is None:
            content_type = applicationContext.DEFAULT_CONTENT_TYPE

        content_type = '%s; charset=%s' % (content_type, self.charset)

        self['Content-Type'] = content_type
        self['Content-Length'] = str(len(content))

    @property
    def status_name(self):
        if self._status_name is not None:
            return self._status_name

        return responses.get(self.status_code, 'Unknown Status Code')   

    @status_name.setter
    def status_name(self, value):
        self._status_name = value    

    @property
    def charset(self):
        if self._charset is not None:
            return self._charset

        return applicationContext.DEFAULT_CHARSET

    @charset.setter
    def charset(self, value):
        self._charset = value

    def __setitem__(self, header, value):
        self._headers[header.lower()] = (header, value)

    def __delitem__(self, header):
        with suppress(KeyError):
            del self._headers[header.lower()]

    def __getitem__(self, header):
        return self._headers[header.lower()][1]
    
    def items(self):
        return self._headers.values() 
        
    


class JSONResponse(HttpReponse):
    def __init__(self, entity):
        super().__init__(entity, 'application/json')


class XMLResponse(HttpReponse):
    def __init__(self, entity):

        super().__init__(entity, 'application/xml')

class TemplateResponse(HttpReponse):
    def __init__(self, template_dir, **kwargs):

        super().__init__(template_dir, 'text/html')


class Response404(HttpReponse):
    def __init__(self, **kwargs):
        super().__init__('page dose not exists', 'text/plain', 404)
