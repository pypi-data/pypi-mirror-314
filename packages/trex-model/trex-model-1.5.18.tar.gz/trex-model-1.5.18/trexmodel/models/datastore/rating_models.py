'''
Created on 29 Nov 2023

@author: jacklok
'''
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel
from google.cloud import ndb
from trexmodel.models.datastore.merchant_models import MerchantAcct, Outlet
from trexmodel.models.datastore.user_models import User
from trexconf import conf
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('model')

class RatingBase(BaseNModel, DictModel):
    user_acct                           = ndb.KeyProperty(name="user_acct", kind=User)
    modified_datetime                   = ndb.DateTimeProperty(required=True, auto_now=True)
    updated                             = ndb.BooleanProperty(required=True, default=False)

class OutletRating(RatingBase):
    outlet                              = ndb.KeyProperty(name="outlet", kind=Outlet)
    merchant_acct                       = ndb.KeyProperty(name="merchant_acct", kind=MerchantAcct)
    
    service_rating                      = ndb.FloatProperty(required=True, default=.0)
    ambience_rating                      = ndb.FloatProperty(required=True, default=.0)
    food_rating                         = ndb.FloatProperty(required=True, default=.0)
    value_rating                        = ndb.FloatProperty(required=True, default=.0)
    
    previous_service_rating             = ndb.FloatProperty(required=True, default=.0)
    previous_ambience_rating             = ndb.FloatProperty(required=True, default=.0)
    previous_food_rating                = ndb.FloatProperty(required=True, default=.0)
    previous_value_rating               = ndb.FloatProperty(required=True, default=.0)
    
    dict_properties         = ['service_rating', 'ambience_rating', 'food_rating','value_rating',
                               'previous_service_rating', 'previous_ambience_rating', 'previous_food_rating','previous_value_rating',
                               ]
    
    @staticmethod
    def get_user_rating_by_outlet(user_acct, outlet):
        return OutletRating.query(ndb.AND(OutletRating.user_acct==user_acct.create_ndb_key(), OutletRating.outlet==outlet.create_ndb_key())).get()
    
    @staticmethod
    def list_by_outlet(outlet):
        return OutletRating.query(ndb.AND(OutletRating.outlet==outlet.create_ndb_key())).fetch(limit=conf.MAX_FETCH_RECORD)
    
    @staticmethod
    def list_new_rating_by_outlet(outlet, checking_datetime_from):
        return OutletRating.query(ndb.AND(OutletRating.outlet==outlet.create_ndb_key(), OutletRating.updated==False, OutletRating.modified_datetime>checking_datetime_from)).fetch(limit=conf.MAX_FETCH_RECORD)
    
    @staticmethod
    def list_updated_rating_by_outlet(outlet, checking_datetime_from):
        return OutletRating.query(ndb.AND(OutletRating.outlet==outlet.create_ndb_key(), OutletRating.updated==True, OutletRating.modified_datetime>checking_datetime_from)).fetch(limit=conf.MAX_FETCH_RECORD)
    
    @staticmethod
    def list_by_merchant(merchant_acct):
        return OutletRating.query(ndb.AND(OutletRating.merchant_acct==merchant_acct.create_ndb_key())).fetch(limit=conf.MAX_FETCH_RECORD)
    
    @staticmethod
    def list_new_rating_by_merchant(merchant_acct, checking_datetime_from):
        return OutletRating.query(ndb.AND(OutletRating.merchant_acct==merchant_acct.create_ndb_key(), OutletRating.updated==False, OutletRating.modified_datetime>checking_datetime_from)).fetch(limit=conf.MAX_FETCH_RECORD)
    
    @staticmethod
    def list_updated_rating_by_merchant(merchant_acct, checking_datetime_from):
        return OutletRating.query(ndb.AND(OutletRating.merchant_acct==merchant_acct.create_ndb_key(), OutletRating.updated==True, OutletRating.modified_datetime>checking_datetime_from)).fetch(limit=conf.MAX_FETCH_RECORD)
    
    @staticmethod
    def create(user_acct, outlet, service_rating=.5, ambience_rating=.5, food_rating=.5, value_rating=.5):
        outlet_rating = OutletRating.get_user_rating_by_outlet(user_acct, outlet)
        if outlet_rating is None:
            merchant_acct   = outlet.merchant_acct_entity
            outlet_rating       = OutletRating(
                                            user_acct           = user_acct.create_ndb_key(),
                                            merchant_acct       = merchant_acct.create_ndb_key(),
                                            outlet              = outlet.create_ndb_key(),
                                            service_rating      = service_rating,
                                            ambience_rating     = ambience_rating,
                                            food_rating         = food_rating,
                                            value_rating        = value_rating,
                                            
                                            )
        else:
            outlet_rating.previous_service_rating    = outlet_rating.service_rating
            outlet_rating.previous_ambience_rating    = outlet_rating.ambience_rating
            outlet_rating.previous_food_rating       = outlet_rating.food_rating
            outlet_rating.previous_value_rating      = outlet_rating.value_rating
            
            outlet_rating.service_rating    = service_rating
            outlet_rating.ambience_rating    = ambience_rating
            outlet_rating.food_rating       = food_rating
            outlet_rating.value_rating      = value_rating
            #outlet_rating.updated           = True
            
        
        outlet_rating.put()
    
    @staticmethod
    def __calculate_rating(rating_list):
        
        service_rating      = .0
        ambience_rating      = .0
        food_rating         = .0
        value_rating        = .0
        total_rating_count  = len(rating_list)
        
        for r in rating_list:
            service_rating  +=r.service_rating
            ambience_rating  +=r.ambience_rating
            food_rating     +=r.food_rating
            value_rating    +=r.value_rating
            
        service_average_rating  = service_rating/total_rating_count
        ambience_average_rating  = ambience_rating/total_rating_count
        food_average_rating     = food_rating/total_rating_count
        value_average_rating    = value_rating/total_rating_count
            
        return {
                'service_rating'    : service_average_rating,
                'ambience_rating'    : ambience_average_rating,
                'food_rating'       : food_average_rating,
                'value_rating'      : value_average_rating,
                }
    
    @staticmethod    
    def get_outlet_rating(outlet):
        outlet_rating_list = OutletRating.list_by_outlet(outlet)
        
        return OutletRating.__calculate_rating(outlet_rating_list)
    
    @staticmethod    
    def get_merchant_rating(merchant_acct):
        merchant_rating_list = OutletRating.list_by_outlet(merchant_acct)
        
        return OutletRating.__calculate_rating(merchant_rating_list)

class RatingResult(BaseNModel, DictModel):
    total_rating_count      = ndb.IntegerProperty(required=True, default=0)
    rating_result           = ndb.JsonProperty()
    modified_datetime       = ndb.DateTimeProperty(required=True, auto_now=True)
    

class OutletRatingResult(RatingResult):
    outlet                  = ndb.KeyProperty(name="outlet", kind=Outlet)
    
    
    dict_properties         = ['total_rating_count', 'rating_result', 'modified_datetime',]
    
    @staticmethod
    def get_by_outlet(outlet):
        return OutletRatingResult.query(ndb.AND(OutletRatingResult.outlet==outlet.create_ndb_key())).get()
    
    @staticmethod
    def update(outlet, updated_datetime_from=None):
        outlet_rating_result = OutletRatingResult.query(ndb.AND(OutletRatingResult.outlet==outlet.create_ndb_key())).get()
        existing_total_rating_count = 0
        if updated_datetime_from is None:
            updated_datetime_from = datetime.utcnow() - timedelta(days=1)
        
        if outlet_rating_result is None:
            outlet_rating_result = OutletRatingResult(
                                        outlet = outlet.create_ndb_key(),
                                        )
            rating_result = {
                            'service_rating'    : .0,
                            'ambience_rating'    : .0,
                            'food_rating'       : .0,
                            'value_rating'      : .0,
                            
                            }
        else:
            rating_result = outlet_rating_result.rating_result
            existing_total_rating_count = outlet_rating_result.total_rating_count
        
        new_rating_list             = OutletRating.list_new_rating_by_outlet(outlet, updated_datetime_from)
        total_new_rating_count      = len(new_rating_list)
        
        new_service_rating      = .0
        new_ambience_rating      = .0
        new_food_rating         = .0
        new_value_rating        = .0
        
        for r in new_rating_list:
            new_service_rating  +=r.service_rating
            new_ambience_rating  +=r.ambience_rating
            new_food_rating     +=r.food_rating
            new_value_rating    +=r.value_rating
            
        
        updated_rating_list         = OutletRating.list_updated_rating_by_outlet(outlet, updated_datetime_from)
        #total_updated_rating_count  = len(updated_rating_list)
        
        updated_service_rating      = rating_result.get('service_rating')   * existing_total_rating_count
        updated_ambience_rating      = rating_result.get('ambience_rating')   * existing_total_rating_count
        updated_food_rating         = rating_result.get('food_rating')      * existing_total_rating_count
        updated_value_rating        = rating_result.get('value_rating')     * existing_total_rating_count
        
        for r in updated_rating_list:
            updated_service_rating  +=(r.service_rating-r.previous_service_rating)
            updated_ambience_rating  +=(r.ambience_rating-r.previous_ambience_rating)
            updated_food_rating     +=(r.food_rating-r.previous_food_rating)
            updated_value_rating    +=(r.value_rating-r.previous_value_rating)
        
        latest_service_rating      = (new_service_rating + updated_service_rating)  / (existing_total_rating_count + total_new_rating_count)
        latest_ambience_rating      = (new_ambience_rating + updated_ambience_rating)  / (existing_total_rating_count + total_new_rating_count)
        latest_food_rating         = (new_food_rating    + updated_food_rating)     / (existing_total_rating_count + total_new_rating_count)
        latest_value_rating        = (new_value_rating   + updated_value_rating)    / (existing_total_rating_count + total_new_rating_count)
        
        
        score = (latest_service_rating + latest_ambience_rating + latest_food_rating + latest_value_rating)/4
        outlet_rating_result.total_rating_count = existing_total_rating_count + total_new_rating_count
        outlet_rating_result.rating_result = {
                                                'reviews_details':{
                                                                    'service_rating'    : latest_service_rating,
                                                                    'ambience_rating'   : latest_ambience_rating,
                                                                    'food_rating'       : latest_food_rating,
                                                                    'value_rating'      : latest_value_rating,
                                                                    },
                                                'total_reviews'     : outlet_rating_result.total_rating_count,
                                                'score'             : score,
                                                }
        
        outlet_rating_result.put()
    
class MerchantRatingResult(RatingResult):
    merchant_acct           = ndb.KeyProperty(name="merchant_acct", kind=MerchantAcct)
    
    
    dict_properties         = ['total_rating_count', 'rating_result', 'modified_datetime',]
    
    @staticmethod
    def get_by_merchant_acct(merchant_acct):
        return MerchantRatingResult.query(ndb.AND(MerchantRatingResult.merchant_acct==merchant_acct.create_ndb_key())).get()
    
    @staticmethod
    def update(merchant_acct, updated_datetime_from=None):
        
        logger.info('updated_datetime_from=%s', updated_datetime_from)
        
        merchant_rating_result = MerchantRatingResult.query(ndb.AND(MerchantRatingResult.merchant_acct==merchant_acct.create_ndb_key())).get()
        existing_total_rating_count = 0
        #if updated_datetime_from is None:
        #    updated_datetime_from = datetime.utcnow() - timedelta(days=1)
        is_new_rating_result = False
        if merchant_rating_result is None:
            merchant_rating_result = MerchantRatingResult(
                                        merchant_acct = merchant_acct.create_ndb_key(),
                                        )
            rating_result = {
                            'reviews_details':{
                                                'service_rating'    : .0,
                                                'ambience_rating'   : .0,
                                                'food_rating'       : .0,
                                                'value_rating'      : .0,
                                                
                                                }
                            }
            is_new_rating_result = True
            
            if updated_datetime_from is None:
                updated_datetime_from = merchant_acct.registered_datetime
            
        else:
            rating_result = merchant_rating_result.rating_result
            existing_total_rating_count = merchant_rating_result.total_rating_count
            
            if updated_datetime_from is None:
                updated_datetime_from = merchant_rating_result.modified_datetime
        
        logger.info('rating_result=%s', rating_result)
        
        logger.info('updated_datetime_from=%s', updated_datetime_from)
        
        new_rating_list             = OutletRating.list_new_rating_by_merchant(merchant_acct, updated_datetime_from)
        updated_rating_list         = OutletRating.list_updated_rating_by_merchant(merchant_acct, updated_datetime_from)
        
        total_new_rating_count      = len(new_rating_list)
        total_updated_rating_count  = len(updated_rating_list)
        
        logger.info('total_new_rating_count=%s', total_new_rating_count)
        logger.info('total_updated_rating_count=%s', total_updated_rating_count)
        logger.info('existing_total_rating_count=%s', existing_total_rating_count)
        
        new_service_rating      = .0
        new_ambience_rating     = .0
        new_food_rating         = .0
        new_value_rating        = .0
        
        for r in new_rating_list:
            new_service_rating      +=r.service_rating
            new_ambience_rating     +=r.ambience_rating
            new_food_rating         +=r.food_rating
            new_value_rating        +=r.value_rating
            
            r.updated = True
        
        ndb.put_multi(new_rating_list)    
            
        
        logger.info('new_service_rating=%s', new_service_rating)
        logger.info('new_ambience_rating=%s', new_ambience_rating)
        logger.info('new_food_rating=%s', new_food_rating)
        logger.info('new_value_rating=%s', new_value_rating)
        
        
        
        updated_service_rating      = rating_result.get('reviews_details').get('service_rating', 0)   * existing_total_rating_count
        updated_ambience_rating     = rating_result.get('reviews_details').get('ambience_rating', 0)   * existing_total_rating_count
        updated_food_rating         = rating_result.get('reviews_details').get('food_rating', 0)      * existing_total_rating_count
        updated_value_rating        = rating_result.get('reviews_details').get('value_rating', 0)     * existing_total_rating_count
        
        logger.info('updated_service_rating b4=%s', updated_service_rating)
        logger.info('updated_ambience_rating b4=%s', updated_ambience_rating)
        logger.info('updated_food_rating b4=%s', updated_food_rating)
        logger.info('updated_value_rating b4=%s', updated_value_rating)
        
        for r in updated_rating_list:
            logger.debug('updated rating = %s', r)
            if is_new_rating_result:
                updated_service_rating  +=r.service_rating
                updated_ambience_rating +=r.ambience_rating
                updated_food_rating     +=r.food_rating
                updated_value_rating    +=r.value_rating
            else:
                updated_service_rating  +=(r.service_rating-r.previous_service_rating)
                updated_ambience_rating +=(r.ambience_rating-r.previous_ambience_rating)
                updated_food_rating     +=(r.food_rating-r.previous_food_rating)
                updated_value_rating    +=(r.value_rating-r.previous_value_rating)
        
        logger.info('updated_service_rating after=%s', updated_service_rating)
        logger.info('updated_ambience_rating after=%s', updated_ambience_rating)
        logger.info('updated_food_rating after=%s', updated_food_rating)
        logger.info('updated_value_rating after=%s', updated_value_rating)
        
        if is_new_rating_result:
            latest_service_rating      = (new_service_rating    + updated_service_rating)   / (total_updated_rating_count + total_new_rating_count)
            latest_ambience_rating     = (new_ambience_rating   + updated_ambience_rating)  / (total_updated_rating_count + total_new_rating_count)
            latest_food_rating         = (new_food_rating       + updated_food_rating)      / (total_updated_rating_count + total_new_rating_count)
            latest_value_rating        = (new_value_rating      + updated_value_rating)     / (total_updated_rating_count + total_new_rating_count)
            
            merchant_rating_result.total_rating_count = total_updated_rating_count + total_new_rating_count
            
        else:
            latest_service_rating      = (new_service_rating    + updated_service_rating)   / (existing_total_rating_count + total_new_rating_count)
            latest_ambience_rating     = (new_ambience_rating   + updated_ambience_rating)  / (existing_total_rating_count + total_new_rating_count)
            latest_food_rating         = (new_food_rating       + updated_food_rating)      / (existing_total_rating_count + total_new_rating_count)
            latest_value_rating        = (new_value_rating      + updated_value_rating)     / (existing_total_rating_count + total_new_rating_count)
            
            merchant_rating_result.total_rating_count = existing_total_rating_count + total_new_rating_count
        
        
        score = (latest_service_rating + latest_ambience_rating + latest_food_rating + latest_value_rating)/4
        
        logger.info('latest_service_rating=%s', latest_service_rating)
        logger.info('latest_ambience_rating=%s', latest_ambience_rating)
        logger.info('latest_food_rating=%s', latest_food_rating)
        logger.info('latest_value_rating=%s', latest_value_rating)
        
        logger.info('score=%s', score)
        
        
        merchant_rating_result.rating_result = {
                                                'reviews_details':{
                                                                    'service_rating'    : latest_service_rating,
                                                                    'ambience_rating'   : latest_ambience_rating,
                                                                    'food_rating'       : latest_food_rating,
                                                                    'value_rating'      : latest_value_rating,
                                                                    },
                                                'total_reviews'     : merchant_rating_result.total_rating_count,
                                                'score'             : score,
                                                
                                                }
        
        merchant_rating_result.put()
        
        
        
            
        
            
        
        
    
    
    