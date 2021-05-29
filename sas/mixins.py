from django.views.generic import View


class RequestDataMixin(View):
    def __init__(self):
        super(RequestDataMixin, self).__init__()
        self.host = 'http://217.73.57.195/'
        token = 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vbG9jYWxob3N0L1NBU0xvZ29uL3Rva2VuX2tleXMiLCJraWQiOiJsZWdhY3ktdG9rZW4ta2V5IiwidHlwIjoiSldUIn0.eyJqdGkiOiIxYTk5ZGQ5ZmViOTc0MjEyYTZkYWNjNWIzZDUwOGZkMCIsImV4dF9pZCI6InVpZD1zYXNkZW1vLG91PXBlb3BsZSxkYz1sb2NhbGhvc3QsZGM9bG9jYWxkb21haW4iLCJzdWIiOiJlOTdjYTQ4OS04YTFlLTRiMGItOWFmNi1kMzRkM2FhNmQ4NGEiLCJzY29wZSI6WyJvcGVuaWQiXSwiY2xpZW50X2lkIjoic2FzIiwiY2lkIjoic2FzIiwiYXpwIjoic2FzIiwiZ3JhbnRfdHlwZSI6InBhc3N3b3JkIiwidXNlcl9pZCI6ImU5N2NhNDg5LThhMWUtNGIwYi05YWY2LWQzNGQzYWE2ZDg0YSIsIm9yaWdpbiI6ImxkYXAiLCJ1c2VyX25hbWUiOiJzYXNkZW1vIiwiZW1haWwiOiJzYXNkZW1vQHVzZXIuZnJvbS5sZGFwLmNmIiwiYXV0aF90aW1lIjoxNjIyMjM1NjMwLCJyZXZfc2lnIjoiYmZkMjEwZmIiLCJpYXQiOjE2MjIyMzU2MzAsImV4cCI6MTYyMjI3ODgyOSwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdC9TQVNMb2dvbi9vYXV0aC90b2tlbiIsInppZCI6InVhYSIsImF1ZCI6WyJzYXMiLCJvcGVuaWQiXX0.F3xe-olVPpnChiI4PXHmBah7KmCaFeCRiPW70EytT7U7c1IM_ssvDCI6t2PgcFfh1Ot63XLJP5nE-kxHGlF-BKAaiStxKLSxwAFt-MgP-wyRP8-4kyE0RBek1ysM8tin6zVVmHuaNKiEEwRVGU7Q67oCtPqCcpkMwP3YFOiID7MDsBuG9A47aXjOnX52erpv6gCgUaSHOsCUo1ynpMnFLPOp6qBAqxEZ22Cn8QYMQbDOrXzF2k7XPw-iTXP8tRa0F6Q332CL15aQsL91ViGv_bhGw35DIQmPHFuev7mASvC_FN05eRvL6IezedXNT2LAAT0QgINZYHzIN4-QwzTvow'
        self.headers = {
            'authorization': 'Bearer ' + token,
            'content-type': "application/json",
        }
