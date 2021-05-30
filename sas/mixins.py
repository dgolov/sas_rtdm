from django.views.generic import View
import requests


class RequestDataMixin(View):
    def __init__(self):
        super(RequestDataMixin, self).__init__()
        self.host = 'http://217.73.57.195/'
        token = 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vbG9jYWxob3N0L1NBU0xvZ29uL3Rva2VuX2tleXMiLCJraWQiOiJsZWdhY3ktdG9rZW4ta2V5IiwidHlwIjoiSldUIn0.eyJqdGkiOiI4OWUwNzAxNzc5YmE0YWRlOTU2ZTc5Njc4MGJmYWU2ZSIsImV4dF9pZCI6InVpZD1zYXNkZW1vLG91PXBlb3BsZSxkYz1sb2NhbGhvc3QsZGM9bG9jYWxkb21haW4iLCJzdWIiOiJlOTdjYTQ4OS04YTFlLTRiMGItOWFmNi1kMzRkM2FhNmQ4NGEiLCJzY29wZSI6WyJvcGVuaWQiXSwiY2xpZW50X2lkIjoiaGFjazEiLCJjaWQiOiJoYWNrMSIsImF6cCI6ImhhY2sxIiwiZ3JhbnRfdHlwZSI6InBhc3N3b3JkIiwidXNlcl9pZCI6ImU5N2NhNDg5LThhMWUtNGIwYi05YWY2LWQzNGQzYWE2ZDg0YSIsIm9yaWdpbiI6ImxkYXAiLCJ1c2VyX25hbWUiOiJzYXNkZW1vIiwiZW1haWwiOiJzYXNkZW1vQHVzZXIuZnJvbS5sZGFwLmNmIiwiYXV0aF90aW1lIjoxNjIyMjgxMTkxLCJyZXZfc2lnIjoiNGEzMjczZDQiLCJpYXQiOjE2MjIyODExOTEsImV4cCI6MTYyMjMyNDM5MCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdC9TQVNMb2dvbi9vYXV0aC90b2tlbiIsInppZCI6InVhYSIsImF1ZCI6WyJvcGVuaWQiLCJoYWNrMSJdfQ.EqINI6ZZYgJyV6nORSsbg1hJsXWHO_jjPs7LGWX0_Yo0zpT8GTcu6Lccox3Z912txjQblrljp6zik2Dlw4dKttDtGg4GY67HxaXSfN30FlHd1D8r9vNnXMA3Gyly0kHTT9yaX9q8uVVg0HJOks4Q2d3bWJbaOg03U18Ty8eb0Oi4dQH8cQttTN3m9o1Vs1pHnFu21CIT7KCxQbBQ6V9gDlKU36fpzGXTathQaePnn1A_q0GdXrlt4RYI70EF10pFblThDx5hBetO-gUByQCcaKATI2Y9s-H6KTiHQLHgHNFg1-D_OYptISNuUFCmm2f_dZmXYvyY5NIG-dScuWjZaw'
        self.headers = {
            'authorization': 'Bearer ' + token,
            'content-type': "application/json",
        }

    def get_token(self):
        url = 'http://217.73.57.195/SASLogon/oauth/clients/consul?callback=false&serviceId=sas'
        headers = {
            'X-CONSUL-TOKEN': '50a4b0e1-039a-4ef9-ba24-76ffa7e724a8',
        }
        response = requests.post(url, headers)
        access_token = response.text
        print(access_token)
        return access_token
