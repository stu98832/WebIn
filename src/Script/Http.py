import requests
import bs4
import json

class HttpResponse:
    def __init__(self, response: requests.Response):
        self._response = response

    @property
    def Status(self) -> int:
        return self._response.status_code

    @property
    def Content(self):
        return self._response.content

    @property
    def Raw(self):
        return self._response

    def ToSoup(self, parser='html.parser') -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(self.Content, parser)

    def ToDict(self) -> dict:
        try:
            return self._response.json()
        except:
            return { }

class Http:
    HEADER = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
    }

    def __init__(self, session=None, allowRedirect = False, varify = False):
        if session:
            self.mSession = session
        else:
            self.mSession = requests.Session()
            self.mSession.headers.update(self.HEADER)
        self.mAllowRedirect = allowRedirect
        self.mVarify        = varify
        self.mDefaultHost   = None
        self.mAuth          = None

    def UpdateHeader(self, header: dict) -> None:
        self.mSession.headers.update(header)

    @property
    def Session(self) -> requests.Session:
        return self.mSession

    def SetDefaultHost(self, host: str) -> None:
        if host != None and not host.startswith('http'):
            raise Exception('invalid url')
        if host == None:
            self.mDefaultHost = None
        else:
            self.mDefaultHost = host.rstrip('/')

    def _MakeRequestHeader(self, url: str, params: dict=None) -> dict:
        header = {
          'url'             : url,
          'params'          : params,
          'allow_redirects' : self.mAllowRedirect
        }
        if self.mDefaultHost and not header['url'].startswith('http'):
            header['url'] = '{}/{}'.format(self.mDefaultHost, url.strip('/'))
        if self.mAuth:
            header['auth'] = self.mAuth
        return header

    def Get(self, url: str, params: dict=None) -> HttpResponse:
        body = self._MakeRequestHeader(url, params)
        return HttpResponse(self.mSession.get(**body))

    def Post(self, url: str, data: dict=None, asjson: bool=False, params: dict=None) -> HttpResponse:
        body = self._MakeRequestHeader(url, params)
        if asjson:
            body['json'] = json.dumps({ 'data':data })
        else:
            body['data'] = data
        return HttpResponse(self.mSession.post(**body))

    def Put(self, url: str, data: dict=None, asjson: bool=False, params: dict=None) -> HttpResponse:
        body = self._MakeRequestHeader(url, params)
        if asjson:
            body['json'] = json.dumps({ 'data':data })
        else:
            body['data'] = data
        return HttpResponse(self.mSession.put(**body))

    def Delete(self, url: str, params: dict=None) -> HttpResponse:
        body = self._MakeRequestHeader(url, params)
        return HttpResponse(self.mSession.delete(**body))
