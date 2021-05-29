from django.shortcuts import HttpResponse, render
import requests
from django.views import View
from .mixins import RequestDataMixin


class DetailDecisionsView(RequestDataMixin, View):
    """ Get -запрос, который позволяет по sourceURI определить подробные параметры решения.
    """
    def __init__(self):
        super(DetailDecisionsView, self).__init__()
        self.sourceURI = '9c529dea-6b72-4fee-bffb-368a75bc07a3/revisions/164159ad-b9df-423b-b304-389c5bbe3859'

    def get(self, request, *args, **kwargs):
        response_SAS = requests.get(
            self.host + 'decisions/flows/' + self.sourceURI,
            headers=self.headers)
        content = response_SAS.json()
        # for signature in content['signature']:
        #     print('\nNEW SIGNATURE:')
        #     for key, value in signature.items():
        #         print(key, value)

        context = {'title': "Подробные параметры решения", 'content': content['signature']}
        return render(request, 'sas_rtdm/detail-decisions.html', context)
        # return HttpResponse(content)
