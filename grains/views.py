from django.core import serializers
from django.http import HttpResponse
from grains.models import GrainData

def get_data(request):

    if not request.GET.get("from"):
        where_clause=""
    else:
        from_date=request.GET.get("from")+" 00:00:00 +0000"
        to_date=request.GET.get("to")+" 00:00:00 +0000"
        where_clause = "WHERE c.date BETWEEN '"+from_date+"' AND '"+to_date+"'" 

    table='public.'+request.GET.get("crop")+'_data'

    raw_query = "SELECT c.id, c.date, c.price, c.stock ,d.value as usdx_value  FROM "+table+" AS c INNER JOIN public.usdx_data as d on d.date = c.date "+where_clause+"  ORDER BY date;"
    data=list(GrainData.objects.raw(raw_query))
    serialized = serializers.serialize("json", data, fields=("id", "date","price","stock","usdx_value"))
    return HttpResponse(serialized,content_type="application/json")


