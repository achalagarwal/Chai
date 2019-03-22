from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from urllib.parse import unquote
from src.Utils.logger import logger
from src.expression.Sku import Sku
from src.singletons import sku_match
from src.Utils.Pickler import pickle_data
import os
sku_matcher_singleton = sku_match.SkuSingleton()


def add_sku(request):

    try:
        logger.info("REQUEST: %s", str(request))
        assert request.GET

        sku_name = unquote(request.GET['name'])
        sku_id = unquote(request.GET['id'])
        sku_subtag = unquote(request.GET['tag'])
        sku_meta = unquote(request.GET['meta'])

        new_sku = Sku(sku_name=sku_name, sku_meta=sku_meta, sku_id=sku_id, sku_subtag=sku_subtag)
        sku_matchbook = sku_matcher_singleton.get_obj()
        sku_matchbook.add_sku(new_sku)

        return JsonResponse({'code': 200})
    except Exception as e:
        return JsonResponse({'code': 400, 'error': str(e)})


def pickle_and_backup(request):

    try:
        logger.info("REQUEST: %s", str(request))
        assert request.GET

        key = request.GET['key']

        if not key == 'data':
            return JsonResponse({'code': 400, 'error': "Unwarranted Access"})
        sku_matchbook = sku_matcher_singleton.get_obj()
    
        os.rename(os.getcwd()+'/src/sku_matchbook.pickle', os.getcwd()+'/src/old_sku_matchbook.pickle')

        pickle_data(sku_matchbook, './src/sku_matchbook.pickle')

        return JsonResponse({'code': 200})

    except Exception as e:
        return JsonResponse({'code': 400, 'error': str(e)})

