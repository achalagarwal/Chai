#
# # coding: utf-8
#
# # In[74]:
# #
# #
# # get_ipython().run_line_magic('load_ext', 'autoreload')
# # get_ipython().run_line_magic('autoreload', '2')
# #
#
# # In[75]:
#
#
# from tqdm import tqdm as progress
#
#
# # In[76]:
#
#
# from SKU_Match import cleanSKUData, importSKUDataFromFile, getCustomOrderFormDataFromFile
#
#
# # In[77]:
#
#
# from expression import Sku, Item
#
#
# # In[78]:
#
#
# from match import Match
#
#
# # In[79]:
#
#
# from corpus import Corpus
#
#
# # In[80]:
#
#
# sku_corpus = Corpus.Corpus('sku')
#
#
# # In[81]:
#
#
# sku_matcher = Match.MatchSku()
#
#
# # In[82]:
#
#
# sku_matcher.add_corpus(sku_corpus)
#
#
# # In[83]:
#
#
# raw_sku_list = cleanSKUData(importSKUDataFromFile('./../auto.json'))
#
#
# # In[84]:
#
#
# raw_sku_list
#
#
# # In[85]:
#
#
# sku_list = []
# for raw_sku in raw_sku_list:
#     sku_list.append(Sku.Sku(raw_sku[0], raw_sku[1]))
#
#
# # In[86]:
# parle_skus = list(filter(lambda x: 'parle' in x.terms, sku_list))
#
#
# for sku in progress(parle_skus):
#     sku_matcher.add_sku(sku)
#
# for sku in progress(sku_list):
#     sku_matcher.add_sku(sku)
#
#
# # In[87]:
#
#
# corpus = sku_matcher.corpora[0]
#
#
# # In[88]:
#
#
# corpus.clusters
#
#
# # In[89]:
#
#
# corpus.unused_dict
#
#
# # In[90]:
#
#
# # items = getCustomOrderFormDataFromFile('/Users/achal/Dunzo/Data/dunzo_tasks_raised_1stJan_dump.csv')
# items = getCustomOrderFormDataFromFile('/Users/achal/Work/DunzoVE/orderform.csv')
#
#
# # In[91]:
#
#
# item_list = []
# for item in progress(items):
#     item_list.append(Item.Item(item[0], item[1], item[2], item[3], item[4]))
#
#
# # In[92]:
#
# parle_g_items = list(filter(lambda x: 'parle g' in x.name, item_list))
#
# for item in progress(parle_g_items):
#     sku_matcher.add_item(item)
#
# for item in progress(item_list):
#     sku_matcher.add_item(item)
#
#
# # In[93]:
#
#
# corpus.clusters
#
#
# # In[94]:
#
#
# len(corpus.clusters)
#
#
# # In[95]:
#
#
# # for item in sku_matcher.item_list:
# #     print(item.name, item.term_cluster)
#
#
# # In[96]:
#
#
# for item in progress(item_list):
#     l = sku_matcher.match_item(item)
#     if not l:
#         continue
#     l = list(map(lambda x: (x[0]._name, x[1]), l))
#     l.sort(key=(lambda x: x[1]), reverse=True)
#     print(item.name, l)
#     print("**********")
#
#
# # In[99]:
#
#
# parle_g_items = list(filter(lambda x: 'parle g' in x.name, item_list))
#
#
# # In[122]:
#
#
# parle_g_items[0].term_cluster.get('parle')
#
#
# # In[119]:
#
#
# parle_skus = list(filter(lambda x: 'parle' in x.terms, sku_list))
#
#
# # In[124]:
#
#
# for parle_sku in parle_skus:
#     print(parle_sku.cluster_terms)
#
#
# # In[118]:
#
#
# sku_matcher.match_item(parle_g_items[0])
#
#
# # In[ ]:
#
#
#
# # In[28]:
#
#
# sku_list_names = list(map(lambda x: x._name, sku_list))
#
#
# # In[29]:
#
#
# sku_list_names
#
