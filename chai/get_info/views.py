from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from src.wrappers import alcohol_limit
from src.singletons import sku_match
import json
from src.expression import Item
from src.Utils.logger import logger
sku_matcher_singleton = sku_match.SkuSingleton()


def check_alcohol_limit(request):
    try:
        logger.info("REQUEST", request)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order_form = body.get('items', [])
        city_id = body.get('cityId', 1)
        logger.info(order_form, city_id)
        order_flag, rule_details, order_details, order_bound, broad_order_bound = \
            alcohol_limit.hit_order(order_form, city_id)

        return JsonResponse({'code': 200,
                             'alcohol_within_limits': order_flag,
                             'category_rules': rule_details,
                             'category_bounds': broad_order_bound,
                             'order_details': order_details,
                             'order_bounds': order_bound})
    except Exception as e:
        return JsonResponse({'code': 400, 'error': str(e), 'alcohol_within_limits': True})


def get_top_unmatched(request):

    try:
        logger.info(request)
        assert request.GET

        key = request.GET['key']

        if not key == 'data':
            return JsonResponse({'code': 400, 'error': 'Unwarranted Request'})

        sku_matchbook = sku_matcher_singleton.get_obj()
        # sku_corpus = sku_matchbook.corpora[0]

        unused_list = list(sku_matchbook.unused_dict.items())

        unused_list.sort(key=lambda x: x[1], reverse=True)

        unused_list = unused_list[0:100]

        return JsonResponse({'code': 200, 'data': unused_list})

    except Exception as e:

        return JsonResponse({'code': 400, 'error': str(e)})





