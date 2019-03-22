from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import json
from src.expression.Item import Item
from src.singletons import sku_match
from urllib.parse import unquote
from src.wrappers import autocomplete
from src.Utils.logger import logger

sku_matcher_singleton = sku_match.SkuSingleton()



def modify_format(index, title, id='noskuidavailable', source_string='good'):

    return {'type': 'fuzzy', 'idx': index, 'title': title, 'skuId': id, 'sourceString': source_string}


def complete_query(request):
    try:
        logger.info("REQUEST: %s", str(request))
        assert request.GET

        user_search_query = request.GET['text']
        user_search_query = unquote(user_search_query)

        sku_matcher = sku_matcher_singleton.get_obj()
        autocompleter = autocomplete.AutoComplete(sku_matcher)

        sku_suggestions = autocompleter.hit_query(user_search_query.lower())

        response = {'code': 200, 'data': {'results': []}}

        for i in range(len(sku_suggestions)):
            sku = sku_suggestions[i]
            response['data']['results'].append(modify_format(index=i, title=sku[0].get_name(), id=sku[0]._id, source_string=user_search_query))

        # print(a.add_and_match_item(Item(name='maggi noodles', subtag='Alcohol')))
        return JsonResponse(response)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'code': 400, 'data': {'results': []}, 'error': str(e)})


def get_sku_data(request):
    try:
        logger.info(request)
        assert request.GET
        key = request.GET['key']
        if not (key == 'data' or key=='dataless') :
            return JsonResponse({'code': 400, 'error': 'Unwarranted Request'})
        sku_matcher = sku_matcher_singleton.get_obj()
        if key == 'dataless':
            data = [('Sku Id', 'Sku Name', 'Sku Popularity')]
            for sku in sku_matcher.sku_set:
                data.append((sku._id, sku.get_name(), sku._subtag, sku._popularity))
            return JsonResponse({'code': 200, 'data': data})
        data = [('Sku Id', 'Sku Name', 'Sku Subtag', 'Sku Popularity', 'Sku Dzerids', 'Sku Users')]
        for sku in sku_matcher.sku_set:
            data.append((sku._id, sku.get_name(), sku._subtag, int(sku._popularity), json.dumps(sku._dzer_ids), str(sku._user_ids)))

        return JsonResponse({'code': 200, 'data': data})
    except Exception as e:
        return JsonResponse({'code': 200, 'error': str(e)})


