Search.setIndex({docnames:["index","modules","src","src.Utils","src.cluster","src.corpus","src.expression","src.master","src.singletons","src.temp","src.wrappers"],envversion:53,filenames:["index.rst","modules.rst","src.rst","src.Utils.rst","src.cluster.rst","src.corpus.rst","src.expression.rst","src.master.rst","src.singletons.rst","src.temp.rst","src.wrappers.rst"],objects:{"":{check_alcohol_limit:[0,0,1,""],complete_query:[0,0,1,""],enumerate:[0,0,1,""],src:[2,1,0,"-"]},"src.SKU_Match":{build_sku_list:[2,0,1,""],cleanSKUData:[2,0,1,""],computeMatchWeight:[2,0,1,""],curateData:[2,0,1,""],extractFromString:[2,0,1,""],extractWords:[2,0,1,""],extract_number_from_string:[2,0,1,""],extract_skus_from_name_dict:[2,0,1,""],find_min_char_index:[2,0,1,""],getAlternate:[2,0,1,""],getCSV:[2,0,1,""],getCustomOrderFormDataFromFile:[2,0,1,""],getData:[2,0,1,""],getDistance:[2,0,1,""],getInfoFromOrder:[2,0,1,""],getLinearSpan:[2,0,1,""],getLower:[2,0,1,""],getMatch:[2,0,1,""],getOrderFormDataFromFile:[2,0,1,""],getSKUMatch:[2,0,1,""],getTypoCSV:[2,0,1,""],getTypos:[2,0,1,""],get_alcohol_data:[2,0,1,""],get_better_from_best:[2,0,1,""],get_class_dict_from_name_dict:[2,0,1,""],get_corresponding_sku_object:[2,0,1,""],get_decay:[2,0,1,""],get_info_from_order_form:[2,0,1,""],get_match:[2,0,1,""],get_name_dict_from_class_dict:[2,0,1,""],get_sku_list:[2,0,1,""],get_sku_list_csv:[2,0,1,""],have_similar_length:[2,0,1,""],helperGetElligiblePair:[2,0,1,""],helper_typo_distance:[2,0,1,""],importBigBasketDataFromFile:[2,0,1,""],importSKUDataFromFile:[2,0,1,""],import_madhuloka_data:[2,0,1,""],isVowel:[2,0,1,""],is_good_match:[2,0,1,""],load_english_words:[2,0,1,""],main:[2,0,1,""],match_item_to_raw_data:[2,0,1,""],match_item_to_sku:[2,0,1,""],merge_list_of_lists:[2,0,1,""],minimalSimilarity:[2,0,1,""],populate:[2,0,1,""],printPercentage:[2,0,1,""],printVector:[2,0,1,""],sort_sku_list:[2,0,1,""],tag_and_score:[2,0,1,""],test_cluster_popularity:[2,0,1,""],test_pickled_data:[2,0,1,""],typo_distance:[2,0,1,""]},"src.Utils":{Pickler:[3,1,0,"-"],logger:[3,1,0,"-"],scorer:[3,1,0,"-"],scoring_utils:[3,1,0,"-"],sku_utils:[3,1,0,"-"]},"src.Utils.Pickler":{pickle_data:[3,0,1,""],pickle_dict:[3,0,1,""],unpickle_data:[3,0,1,""],unpickle_dict:[3,0,1,""]},"src.Utils.scorer":{Scorer:[3,2,1,""]},"src.Utils.scorer.Scorer":{decay:[3,3,1,""],increment:[3,3,1,""],score:[3,3,1,""]},"src.Utils.scoring_utils":{get_brand_word_score:[3,0,1,""],get_match_ratio_score:[3,0,1,""],get_meta_match_score:[3,0,1,""],get_root_words_score:[3,0,1,""],get_score:[3,0,1,""],get_sequential_score:[3,0,1,""],get_user_query_score:[3,0,1,""]},"src.Utils.sku_utils":{clean_item:[3,0,1,""],clean_item_with_meta:[3,0,1,""],clean_word:[3,0,1,""],clean_words:[3,0,1,""],compute_edit_distance:[3,0,1,""],extract_alcohol_liquid_quantity:[3,0,1,""],flipper:[3,0,1,""],get_linear_span:[3,0,1,""],get_min_item_edit_distance:[3,0,1,""],get_min_word_edit_distance:[3,0,1,""],get_str_from_vec:[3,0,1,""],helper_eligible_pair:[3,0,1,""],is_eligible_pair:[3,0,1,""],is_invalid_word:[3,0,1,""],is_liquid_unit:[3,0,1,""],is_valid_word:[3,0,1,""],meets_match_count_threshold:[3,0,1,""],remove_special_symbols:[3,0,1,""],separate_meta_data:[3,0,1,""]},"src.cluster":{Cluster:[4,1,0,"-"],Cluster_Test:[4,1,0,"-"],cluster_utils:[4,1,0,"-"]},"src.cluster.Cluster":{Cluster:[4,2,1,""]},"src.cluster.Cluster.Cluster":{add_leader:[4,4,1,""],add_term:[4,4,1,""],add_to_trie:[4,4,1,""],fuzzy_match_score:[4,4,1,""],get_sorted_terms:[4,4,1,""],has_term:[4,4,1,""],is_in_trie:[4,4,1,""],is_leader:[4,4,1,""],match_score:[4,4,1,""],name:[4,3,1,""],quick_match_score:[4,4,1,""],update_leader:[4,4,1,""]},"src.cluster.Cluster_Test":{test_whether_a_term_is_getting_added_to_the_term_cache_when_add_term_is_called_and_its_score_is_likewise_updated:[4,0,1,""],test_whether_add_leader_adds_to_prefix_trie:[4,0,1,""],test_whether_cluster_leader_update_is_working:[4,0,1,""],test_whether_quick_match_score_is_correct:[4,0,1,""],test_whether_the_add_term_is_adding_appropriately_to_prefix_trie:[4,0,1,""]},"src.cluster.cluster_utils":{match_score:[4,0,1,""]},"src.corpus":{Corpus:[5,1,0,"-"],Corpus_Test:[5,1,0,"-"]},"src.corpus.Corpus":{Corpus:[5,2,1,""]},"src.corpus.Corpus.Corpus":{add_cluster:[5,4,1,""],add_leader:[5,4,1,""],add_leader_list:[5,4,1,""],add_term:[5,4,1,""],add_term_list:[5,4,1,""],add_term_to_cluster:[5,4,1,""],create_cluster:[5,4,1,""],fix_cache:[5,4,1,""],get_cached_term_cluster:[5,4,1,""],get_eligible_clusters:[5,4,1,""],get_specific_clusters:[5,4,1,""],has_term:[5,4,1,""],match_term_cluster:[5,4,1,""],pickle_corpus:[5,4,1,""],reset_scores:[5,4,1,""]},"src.corpus.Corpus_Test":{test_whether_add_leader_works_as_intended:[5,0,1,""],test_whether_add_term_to_corpus_works_as_intended:[5,0,1,""],test_whether_match_term_caches_information:[5,0,1,""]},"src.expression":{Item:[6,1,0,"-"],Sku:[6,1,0,"-"]},"src.expression.Item":{Item:[6,2,1,""]},"src.expression.Item.Item":{add_cluster:[6,4,1,""],get_name:[6,4,1,""],get_subtag:[6,4,1,""]},"src.expression.Sku":{Sku:[6,2,1,""]},"src.expression.Sku.Sku":{add_cluster:[6,4,1,""],add_dzer:[6,4,1,""],add_user:[6,4,1,""],get_name:[6,4,1,""],get_subtag:[6,4,1,""],is_eligible:[6,4,1,""],match_distance:[6,4,1,""],setup_popularity:[6,4,1,""],update_count:[6,4,1,""],update_popularity:[6,4,1,""],update_score:[6,4,1,""]},"src.master":{Match:[7,1,0,"-"],Tagger:[7,1,0,"-"]},"src.master.Match":{Match:[7,2,1,""],MatchSku:[7,2,1,""]},"src.master.Match.MatchSku":{add_and_match_item_list:[7,4,1,""],add_corpus:[7,4,1,""],add_item:[7,4,1,""],add_leader_term:[7,4,1,""],add_sku:[7,4,1,""],add_term:[7,4,1,""],batch_update_sku:[7,4,1,""],get_sku_list_from_item_clusters:[7,4,1,""],get_sku_with_clusters_from_term_prefix_clusters:[7,4,1,""],get_term_cluster:[7,4,1,""],match_item:[7,4,1,""],match_term_corpus:[7,4,1,""]},"src.master.Tagger":{Tagger:[7,2,1,""]},"src.master.Tagger.Tagger":{add_cluster:[7,4,1,""],add_term:[7,4,1,""],extract_tag:[7,4,1,""],generic_function_1:[7,4,1,""],generic_function_2:[7,4,1,""],tag_item:[7,4,1,""]},"src.singletons":{sku_match:[8,1,0,"-"]},"src.singletons.sku_match":{SkuSingleton:[8,2,1,""]},"src.singletons.sku_match.SkuSingleton":{get_obj:[8,4,1,""]},"src.temp":{clusterer:[9,1,0,"-"],string_cluster:[9,1,0,"-"]},"src.temp.clusterer":{cleanItem:[9,0,1,""],cleanWord:[9,0,1,""],get_cluster_index:[9,0,1,""],isInvalidWord:[9,0,1,""],isValidWord:[9,0,1,""],is_eligible:[9,0,1,""],remove_special_symbols:[9,0,1,""]},"src.temp.string_cluster":{batch_cluster:[9,0,1,""],get_local_data_for_testing:[9,0,1,""],map_term:[9,0,1,""]},"src.wrappers":{autocomplete:[10,1,0,"-"]},"src.wrappers.autocomplete":{AutoComplete:[10,2,1,""]},"src.wrappers.autocomplete.AutoComplete":{get_cluster_match_score:[10,5,1,""],get_from_cache:[10,4,1,""],get_meta_match_score:[10,5,1,""],hit_query:[10,4,1,""],set_in_cache:[10,4,1,""]},src:{SKU_Match:[2,1,0,"-"],Utils:[3,1,0,"-"],cluster:[4,1,0,"-"],corpus:[5,1,0,"-"],expression:[6,1,0,"-"],master:[7,1,0,"-"],self_test:[2,1,0,"-"],singletons:[8,1,0,"-"],temp:[9,1,0,"-"],wrappers:[10,1,0,"-"]}},objnames:{"0":["py","function","Python function"],"1":["py","module","Python module"],"2":["py","class","Python class"],"3":["py","attribute","Python attribute"],"4":["py","method","Python method"],"5":["py","staticmethod","Python static method"]},objtypes:{"0":"py:function","1":"py:module","2":"py:class","3":"py:attribute","4":"py:method","5":"py:staticmethod"},terms:{"char":2,"class":[3,4,5,6,7,8,10],"function":[0,2,4],"new":4,"return":[0,4],"static":10,"true":[],And:0,The:[],There:0,access:0,add:4,add_and_match_item:[],add_and_match_item_list:7,add_clust:[5,6,7],add_corpu:7,add_dzer:6,add_item:7,add_lead:[4,5],add_leader_list:5,add_leader_term:7,add_sku:7,add_term:[4,5,7],add_term_list:5,add_term_to_clust:5,add_to_tri:4,add_us:6,added:4,adding:4,additional_dict:3,alcohol:[0,1,2],alcohol_limit:[],alcohol_tag:[],alcohollimit:[],alcohollimitbangalor:[],alcohollimitgurgaon:[],alcohollimitpun:[],algorithm:4,also:4,assign:4,autocomplet:[0,1,2],avail:4,base:[3,4,5,6,7,8,10],batch_clust:9,batch_update_sku:7,been:0,befor:4,best:2,best_items_match:2,best_sku_match:2,block:4,bodi:0,build_sku_list:2,call:4,can:0,check:4,check_alcohol_limit:0,check_ord:[],citi:0,city_id:[],class_dict:2,clean_item:3,clean_item_with_meta:3,clean_word:3,cleanitem:9,cleanskudata:2,cleanword:9,cluster:[0,1,2,5,6,7],cluster_lead:9,cluster_test:4,cluster_util:4,complet:4,complete_queri:0,comput:4,compute_edit_dist:3,computematchweight:2,consid:4,contain:[0,4,7],content:1,corpora:7,corpu:[0,1,2,7],corpus_test:5,correct:2,count:2,creat:7,create_clust:5,csv:2,curatedata:2,current:4,data:[2,3,9],decai:3,decay_factor:3,decay_funct:3,defin:[4,6],describ:[],descript:[],detail:0,dict:2,dictionari:3,directori:0,django:0,docstr:[],doctest:[],dunzo:0,dzer_id:6,each:4,enabl:4,enumer:0,exampl:[],expos:0,express:[0,1,2,7],extract_alcohol_liquid_quant:3,extract_number_from_str:2,extract_skus_from_name_dict:2,extract_tag:7,extractfromstr:2,extractword:2,fals:7,fast:4,filenam:[2,3,5],find_min_char_index:2,first:[],fix_cach:5,flag:3,flipper:3,framework:0,func:2,fuzzy_match_scor:4,generic_function_1:7,generic_function_2:7,get:0,get_alcohol_data:2,get_better_from_best:2,get_brand_word_scor:3,get_cached_result:[],get_cached_term_clust:5,get_class_dict_from_name_dict:2,get_cluster_index:9,get_cluster_match_scor:10,get_corresponding_sku_object:2,get_decai:2,get_eligible_clust:5,get_from_cach:10,get_info_from_order_form:2,get_linear_span:3,get_local_data_for_test:9,get_match:2,get_match_ratio_scor:3,get_meta_match_scor:[3,10],get_min_item_edit_dist:3,get_min_word_edit_dist:3,get_ml:[],get_nam:6,get_name_dict_from_class_dict:2,get_obj:8,get_order_detail:[],get_root_words_scor:3,get_rule_detail:[],get_scor:3,get_sequential_scor:3,get_sku_list:2,get_sku_list_csv:2,get_sku_list_from_item_clust:7,get_sku_with_clusters_from_term_prefix_clust:7,get_sorted_term:4,get_specific_clust:5,get_str_from_vec:3,get_strategi:[],get_subtag:6,get_term_clust:7,get_user_query_scor:3,getaltern:2,getcsv:2,getcustomorderformdatafromfil:2,getdata:2,getdist:2,getinfofromord:2,getlinearspan:2,getlow:2,getmatch:2,getorderformdatafromfil:2,getskumatch:2,gettypo:2,gettypocsv:2,has:0,has_term:[4,5],have_similar_length:2,help:4,helper:4,helper_eligible_pair:3,helper_typo_dist:2,helpergetelligiblepair:2,here:[],highest:4,hit_item:[],hit_ord:[],hit_queri:10,http:0,import_madhuloka_data:2,importbigbasketdatafromfil:2,importskudatafromfil:2,incorrect:2,increment:3,index:[0,2],individu:4,info:0,inform:0,initial_increment:3,initial_scor:3,involv:0,is_elig:[6,9],is_eligible_pair:3,is_good_match:2,is_in_tri:4,is_invalid_word:3,is_lead:4,is_liquid_unit:3,is_valid_word:3,isinvalidword:9,isvalidword:9,isvowel:2,item1:[2,3],item2:[2,3],item:[0,1,2,3,7,9],item_data_tuple_with_uid_dzid_tag:2,item_dict:2,item_list:7,item_nam:6,item_name_tag:2,item_sku_term_map:3,item_subtag:6,itemnam:2,iter:0,kei:10,keyword:2,kind:0,leader:[4,5,7],leader_list:5,leader_term:4,learning_flag:7,limit:[0,1,2],list1:2,list2:2,list:0,list_of_list:2,load_english_word:2,logger:[0,1,2],lower:[],mai:4,main:2,map_term:9,master:[0,1,2],master_dict:9,match:[0,1,4],match_book:10,match_dist:6,match_item:7,match_item_to_raw_data:2,match_item_to_sku:2,match_scor:4,match_term_clust:5,match_term_corpu:7,matchbook:[0,1,2,7],matcher:7,matchsku:7,meets_match_count_threshold:3,merge_list_of_list:2,metric:[],migrat:[],minimalsimilar:2,model:4,modul:[0,1],more:4,name:[4,5,6],name_dict:2,need:[4,7],ner:4,none:[2,3,4],note:[],notebook:7,object:[3,4,5,6,7,8,10],one:4,option1:3,option2:3,order:[0,2],orderform:2,out:7,packag:[0,1],page:0,param:4,paramet:[0,4],paramt:4,pickle_corpu:5,pickle_data:3,pickle_dict:3,pickler:[0,1,2],plai:4,plug:4,popul:2,popular:6,port:0,post:0,prefix:4,prev_decai:2,primari:4,printpercentag:2,printvector:2,probabl:0,product:2,quantiti:6,queri:[0,10],query_clust:10,quick_match_scor:4,readi:4,remove_special_symbol:[3,9],renam:7,request:0,reset_scor:5,reursiv:4,score:[0,1,2,4,5,6],scorer:[0,1,2],scoreself:4,scoring_util:3,search:0,seealso:[],self:[0,1],self_test:[],separ:4,separate_meta_data:3,sequenc:0,set:4,set_in_cach:10,setup_popular:6,similar:2,singleton:[0,1,2],sku:[0,1,3,7,10],sku_count:2,sku_data_tuple_with_tag:2,sku_id:6,sku_item_term_map:3,sku_list:2,sku_match:[2,8],sku_meta:6,sku_nam:[2,6],sku_name_tag:2,sku_subtag:6,sku_util:3,skusingleton:8,some:0,sort_sku_list:2,sourc:[2,3,4,5,6,7,8,9,10],span:3,sphinx:[],src:[3,4,5,6,7,8,9,10],standard:0,start:0,str:9,strategi:[],strict:4,string:[0,1,2,3],string_clust:9,sub:0,subdirectori:0,submodul:[0,1],subpackag:[0,1],subtag:6,tag:7,tag_and_scor:2,tag_item:7,tagger:[0,1,2],temp:9,temporari:[0,1,2],term1:4,term2:4,term:[4,5,6,7,9],term_list:5,test:[0,1,6],test_cluster_popular:2,test_pickled_data:2,test_whether_a_term_is_getting_added_to_the_term_cache_when_add_term_is_called_and_its_score_is_likewise_upd:4,test_whether_add_leader_adds_to_prefix_tri:4,test_whether_add_leader_works_as_intend:5,test_whether_add_term_to_corpus_works_as_intend:5,test_whether_cluster_leader_update_is_work:4,test_whether_match_term_caches_inform:5,test_whether_quick_match_score_is_correct:4,test_whether_the_add_term_is_adding_appropriately_to_prefix_tri:4,text:[],than:4,thei:[4,7],todo:[],total:2,trie:4,tune:4,tupl:0,two:0,type:[],typo_dist:2,unpickle_data:3,unpickle_dict:3,updat:4,update_count:6,update_default_valu:[],update_lead:4,update_popular:6,update_scor:6,update_valu:[],upper:[],used:[0,7],useful:7,user:[0,6],user_id:6,using:0,util:[0,1,2],valu:10,variou:7,vec:[2,3],warn:[],when:0,which:[0,4,7],whose:4,word1:2,word2:2,word:[2,3,4,9],work:4,wrapper:[0,1,2],yield:0},titles:["Welcome to Chai\u2019s documentation!","src","src package","Utils package","cluster package","corpus package","expression package","master package","singletons","temporary","wrappers"],titleterms:{admin:[],alcohol:10,alcohol_limit:[],app:[],autocomplet:10,chai:0,cluster:[4,9],cluster_test:[],cluster_util:[],content:[0,2,3,4,5,6,7,8,9,10],corpu:5,corpus_test:[],django_wrapp:[],document:0,express:[3,6],get_info:[],get_sku:[],item:6,limit:10,logger:3,master:7,match:[2,7],matchbook:8,migrat:[],model:[],modul:[2,3,4,5,6,7,8,9,10],packag:[2,3,4,5,6,7],pickler:3,score:3,scorer:3,scoring_util:[],self:2,self_test:[],set:[],singleton:8,sku:[2,6,8],sku_match:[],sku_util:[],src:[0,1,2],string:9,string_clust:[],submodul:[2,3,4,5,6,7,8,9,10],subpackag:2,tagger:7,temp:[],temporari:9,test:[2,4,5],url:[],util:[3,4],view:[],welcom:0,wrapper:10,wsgi:[]}})