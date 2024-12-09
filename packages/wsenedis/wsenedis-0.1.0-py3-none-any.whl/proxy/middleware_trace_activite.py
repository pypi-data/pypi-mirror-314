from proxy.models import TraceActivite
import json
import logging



class EnregistreurActivite:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if len(request.body) == 0:
            return self.get_response(request)
        body = json.loads(request.body.decode("utf-8"))
        trace = TraceActivite()
        trace.service_concerne = request.path
        trace.demandeur = body['serveur']
        if 'pointId' in body['donnees']:
            trace.RAE_concerne = body['donnees']['pointId']
        trace.save()
        # print("rapport: ", copie.path, body['serveur'], trace.RAE_concerne)
        # print("on a cette entrée dans la BDD",TraceActivite.objects.get(id=1).service_concerne, TraceActivite.objects.get(id=1).demandeur, TraceActivite.objects.get(id=1).RAE_concerne, TraceActivite.objects.get(id=1).horodate)
        return self.get_response(request)
