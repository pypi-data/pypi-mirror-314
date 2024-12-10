'''
Created on 1 Apr 2021

@author: jacklok
'''

from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.customer_models import Customer,\
    CustomerMembership
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.merchant_models import MerchantAcct, Outlet,\
    MerchantUser
import logging
from trexconf import conf, program_conf 
from datetime import datetime, timedelta
from trexmodel.utils.model.model_util import generate_transaction_id
from trexmodel.models.datastore.membership_models import MerchantMembership,\
    MerchantTierMembership

logger = logging.getLogger('model')

class SalesTransaction(BaseNModel, DictModel):
    transact_merchant           = ndb.KeyProperty(name="transact_merchant", kind=MerchantAcct)
    transact_outlet             = ndb.KeyProperty(name="transact_outlet", kind=Outlet)
    
    transact_datetime           = ndb.DateTimeProperty(required=True)
    created_datetime            = ndb.DateTimeProperty(required=True, auto_now=True)
    
    reverted_datetime           = ndb.DateTimeProperty(required=False)
    reverted_by                 = ndb.KeyProperty(name="reverted_by", kind=MerchantUser)
    reverted_by_username        = ndb.StringProperty(required=False)
    
    transact_timestamp          = ndb.FloatProperty(required=False)
    
    transaction_id              = ndb.StringProperty(required=True)
    invoice_id                  = ndb.StringProperty(required=False)
    remarks                     = ndb.StringProperty(required=False)
    system_remarks              = ndb.StringProperty(required=False)
    
    tax_amount                  = ndb.FloatProperty(required=False, default=.0)
    transact_amount             = ndb.FloatProperty(required=True)
    
    transact_by                 = ndb.KeyProperty(name="created_by", kind=MerchantUser)
    transact_by_username        = ndb.StringProperty(required=False)
    
    sales_channel               = ndb.StringProperty(required=False)
    
    is_revert                   = ndb.BooleanProperty(required=False, default=False)
    is_sales_transaction        = ndb.BooleanProperty(required=False, default=True)
    allow_to_revert             = ndb.BooleanProperty(required=False, default=True)
    used                        = ndb.BooleanProperty(required=False, default=False)
    
    reward_expiry_date          = ndb.DateProperty(required=False)
    
    dict_properties         = [
                               'transaction_id', 'invoice_id', 'remarks', 'system_remarks', 'tax_amount', 'transact_amount', 
                               'transact_outlet_entity', 'transact_merchant_acct_entity',
                               'transact_datetime', 'created_datetime',  'transact_outlet_key', 
                               'is_sales_transaction', 'allow_to_revert', 'reward_expiry_date',
                               'transact_by', 'transact_by_username', 'used',
                               
                               ]
    
    @property
    def transact_customer_key(self):
        return ''
    
    @property
    def transact_merchant_acct(self):
        return MerchantAcct.fetch(self.transact_merchant.urlsafe())
    
    @property
    def transact_outlet_key(self):
        if self.transact_outlet:
            return self.transact_outlet.urlsafe().decode('utf-8')
        
    @property
    def transact_outlet_entity(self):
        if self.transact_outlet:
            return Outlet.fetch(self.transact_outlet.urlsafe())    
    
    @property
    def transact_merchant_acct_key(self):
        return self.transact_merchant.urlsafe().decode('utf-8')
    
    @property
    def transact_merchant_acct_entity(self):
        return MerchantAcct.fetch(self.transact_merchant.urlsafe())

    @property
    def transact_by_user(self):
        if self.transact_by:
            return MerchantUser.fetch(self.transact_by.urlsafe())
        
    @property
    def transact_by_user_acct_key(self):
        return self.transact_by.urlsafe()
        
    @property
    def after_deduct_tax_sales_amount(self):
        if self.tax_amount:
            return self.transact_amount - self.tax_amount
        else:
            return self.transact_amount
        
    @classmethod
    def get_by_invoice_id(cls, invoice_id):
        return cls.query(cls.invoice_id==invoice_id).get()
    
    @classmethod
    def get_by_transaction_id(cls, transaction_id):
        return cls.query(cls.transaction_id==transaction_id).get()
    
    @staticmethod
    def create(transact_amount=.0, tax_amount=.0, invoice_id=None, remarks=None, system_remarks=None,
               transact_outlet=None, transact_by=None, transact_datetime=None, 
               
               ):
        
        transact_by_username = None
        
        if is_not_empty(transact_by):
            if isinstance(transact_by, MerchantUser):
                transact_by_username = transact_by.username

        
        transaction_id = generate_transaction_id()
        
        if transact_datetime is None:
            transact_datetime = datetime.utcnow()
        
        logger.debug('generated transaction_id=%s', transaction_id)
        logger.debug('invoice_id=%s', invoice_id)
        logger.debug('tax_amount=%s', tax_amount)
        logger.debug('transact_amount=%s', transact_amount)
        logger.debug('transact_datetime=%s', transact_datetime)
        logger.debug('transact_by_username=%s', transact_by_username)
        logger.debug('system_remarks=%s', system_remarks)
        
        customer_transaction = SalesTransaction(
                                transact_merchant               = transact_outlet.merchant_acct_entity.create_ndb_key(),
                                transact_outlet                 = transact_outlet.create_ndb_key() if transact_outlet else None,
                                
                                tax_amount                      = tax_amount,
                                transact_amount                 = transact_amount,
                                
                                transaction_id                  = transaction_id,
                                invoice_id                      = invoice_id,
                                remarks                         = remarks,
                                system_remarks                  = system_remarks,
                                
                                transact_by                     = transact_by.create_ndb_key() if transact_by else None,
                                transact_by_username            = transact_by_username,
                                
                                transact_datetime               = transact_datetime,
                                
                                is_sales_transaction            = True,
                                allow_to_revert                 = True,
                                
                                )
        
        customer_transaction.put()
        #customer.put()
        
        return customer_transaction
    
        
    
class CustomerTransaction(SalesTransaction):
    '''
    Customer as ancestor
    '''
    
    entitled_reward_summary             = ndb.JsonProperty()
    entitled_voucher_summary            = ndb.JsonProperty()
    entitled_prepaid_summary            = ndb.JsonProperty()
    entitled_program_summary            = ndb.JsonProperty()
    entitled_lucky_draw_ticket_summary  = ndb.JsonProperty(required=False)
    
    reward_giveaway_method      = ndb.StringProperty(required=False, default=program_conf.PROGRAM_REWARD_GIVEAWAY_METHOD_SYSTEM)
    
    
    
    is_from_instant_transaction = ndb.BooleanProperty(required=False, default=False)
    is_reward_redeemed          = ndb.BooleanProperty(required=False, default=False)
    
    
    
    is_membership_purchase      = ndb.BooleanProperty(required=False, default=False)
    is_membership_renew         = ndb.BooleanProperty(required=False, default=False)
    
    is_tier_membership_upgraded = ndb.BooleanProperty(required=False, default=False)
    
    upgraded_merchant_tier_membership   = ndb.KeyProperty(name="upgraded_merchant_tier_membership", kind=MerchantTierMembership)
    
    purchased_merchant_membership        = ndb.KeyProperty(name="purchased_merchant_membership", kind=MerchantMembership)
    purchased_customer_membership        = ndb.KeyProperty(name="purchased_customer_membership", kind=CustomerMembership)
    
    dict_properties         = ['transaction_id', 'invoice_id', 'remarks', 'system_remarks', 'tax_amount', 'transact_amount', 'reward_giveaway_method',
                               'entitled_reward_summary', 'entitled_voucher_summary', 'entitled_prepaid_summary', 'entitled_lucky_draw_ticket_summary',
                               'transact_customer_acct', 'transact_outlet_details', 'transact_merchant_acct',
                               'transact_datetime', 'created_datetime',  'transact_outlet_key', 'is_revert', 'reverted_datetime', 'reverted_by_username',
                               'transact_by', 'transact_by_username', 'is_reward_redeemed', 'is_sales_transaction', 'allow_to_revert',
                               'is_membership_purchase', 'purchased_merchant_membership_key', 'is_tier_membership_upgraded', 'upgraded_merchant_tier_membership_key',
                               ]
    
    def to_transaction_details_json(self):
        pass
    
    @property
    def is_point_reward_entitled(self):
        if is_not_empty(self.entitled_reward_summary):
            if program_conf.REWARD_FORMAT_POINT in self.entitled_reward_summary:
                return True
        return False
    
    @property
    def is_stamp_reward_entitled(self):
        if is_not_empty(self.entitled_reward_summary):
            if program_conf.REWARD_FORMAT_STAMP in self.entitled_reward_summary:
                return True
        return False
    
    @property
    def is_voucher_reward_entitled(self):
        if is_not_empty(self.entitled_voucher_summary):
            return True
        return False
    
    @property
    def is_prepaid_reward_entitled(self):
        if is_not_empty(self.entitled_prepaid_summary):
            return True
        return False
    
    @property
    def transact_customer_acct(self):
        return Customer.fetch(self.key.parent().urlsafe())
    
    @property
    def transact_user_acct(self):
        return self.transact_customer_acct.registered_user_acct
    
    @property
    def transact_user_acct_key(self):
        return self.transact_user_acct.key_in_str
    
    @property
    def transact_customer_key(self):
        return self.key.parent().urlsafe().decode('utf-8')
    
    @property
    def transact_outlet_details(self):
        if self.transact_outlet:
            return Outlet.fetch(self.transact_outlet.urlsafe())
    
    
    @property
    def purchased_merchant_membership_key(self):
        if self.purchased_merchant_membership:
            return self.purchased_merchant_membership.urlsafe().decode('utf-8')
        
    @property
    def purchased_merchant_membership_entity(self):
        if self.purchased_merchant_membership:
            return MerchantMembership.fetch(self.purchased_merchant_membership.urlsafe())    
    
    @property
    def purchased_customer_membership_entity(self):
        if self.purchased_customer_membership:
            return CustomerMembership.fetch(self.purchased_customer_membership.urlsafe())
    
    @property
    def upgraded_merchant_tier_membership_key(self):
        if self.upgraded_merchant_tier_membership:
            return self.upgraded_merchant_tier_membership.urlsafe().decode('utf-8')
    
    def update_entitled_lucky_draw_ticket_summary(self, entitled_lucky_draw_entries_list):
        if self.entitled_lucky_draw_ticket_summary is None:
            self.entitled_lucky_draw_ticket_summary = {}
        
        self.entitled_lucky_draw_ticket_summary['entries']   = entitled_lucky_draw_entries_list
        self.entitled_lucky_draw_ticket_summary['count']     = len(entitled_lucky_draw_entries_list)
        self.put()
    
    @staticmethod
    def update_transaction_reward_have_been_redeemed(transaction_id, redeem_transaction_id, redeem_voucher_details_dict=None):
        
        logger.debug('Update customer transaction reward have been redeemed by transaction id=%s', transaction_id)
        
        if transaction_id:
            customer_transaction = CustomerTransaction.get_by_transaction_id(transaction_id)
            if customer_transaction:
                customer_transaction.is_reward_redeemed = True
                
                if redeem_voucher_details_dict:
                    # voucher key -[list of voucher redeem code]
                    entitled_voucher_summary = customer_transaction.entitled_voucher_summary
                    for voucher_key, redeem_code_list in redeem_voucher_details_dict.items():
                        if entitled_voucher_summary.get(voucher_key):
                            for redeem_info in entitled_voucher_summary.get(voucher_key).get('redeem_info_list'):
                                if redeem_info.get('redeem_code') in redeem_code_list:
                                    redeem_info['is_redeem'] = True
                                    redeem_info['redeem_transaction_id'] = redeem_transaction_id
                    
                
                customer_transaction.put()
    
    @staticmethod
    def create_membership_purchase_transaction(customer, purchased_customer_membership, 
                                               remarks=None, system_remarks=None, transact_outlet=None, 
                                               transact_by=None, transact_datetime=None, 
                                               allow_to_revert=True,):
         
        return CustomerTransaction.create_system_transaction(customer, remarks=remarks, system_remarks=system_remarks, transact_outlet=transact_outlet, transact_by=transact_by, 
                                   transact_datetime=transact_datetime, reward_giveaway_method=program_conf.PROGRAM_REWARD_GIVEAWAY_METHOD_MANUAL,
                                   is_sales_transaction = False, allow_to_revert=allow_to_revert, is_membership_purchase=True, is_membership_renew=False,
                                   purchased_customer_membership=purchased_customer_membership, 
                                   )
        
    @staticmethod
    def create_manual_transaction(customer, remarks=None, system_remarks=None, transact_outlet=None, transact_by=None, transact_datetime=None, is_sales_transaction=False, 
                                  allow_to_revert=True, is_membership_purchase=False, is_membership_renew=False): 
        return CustomerTransaction.create_system_transaction(customer, remarks=remarks, system_remarks=system_remarks, transact_outlet=transact_outlet, transact_by=transact_by, 
                                   transact_datetime=transact_datetime, reward_giveaway_method=program_conf.PROGRAM_REWARD_GIVEAWAY_METHOD_MANUAL,
                                   is_sales_transaction = is_sales_transaction, allow_to_revert=allow_to_revert, 
                                   is_membership_purchase=is_membership_purchase, is_membership_renew=is_membership_renew,
                                   )
        
    @staticmethod
    def create_referral_transaction(customer, transact_outlet=None, transact_datetime=None, ): 
        return CustomerTransaction.create_system_transaction(customer, transact_outlet=transact_outlet, 
                                   transact_datetime=transact_datetime, reward_giveaway_method=program_conf.PROGRAM_REWARD_GIVEAWAY_METHOD_REFERRAL,
                                   allow_to_revert=False,
                                   )        
    
    @staticmethod
    def create_from_sales_transaction(customer, sales_transaction):
        if sales_transaction:
            customer_transaction = CustomerTransaction(
                                                        parent                          = customer.create_ndb_key(),
                                                        
                                                        transact_merchant               = customer.registered_merchant_acct.create_ndb_key(),
                                                        transact_outlet                 = sales_transaction.transact_outlet,
                                                        
                                                        tax_amount                      = sales_transaction.tax_amount,
                                                        transact_amount                 = sales_transaction.transact_amount,
                                                        
                                                        transaction_id                  = sales_transaction.transaction_id,
                                                        invoice_id                      = sales_transaction.invoice_id,
                                                        remarks                         = sales_transaction.remarks,
                                                        system_remarks                  = sales_transaction.system_remarks,
                                                        
                                                        transact_by                     = sales_transaction.transact_by,
                                                        transact_by_username            = sales_transaction.transact_by_username,
                                                        
                                                        transact_datetime               = sales_transaction.transact_datetime,
                                                        is_from_instant_transaction     = True,
                                                        
                                                        #is_sales_transaction            = True,
                                                        #allow_to_revert                 = True,
                                                        #is_membership_purchase          = False,
                                                        #is_membership_renew             = False,
                                                        #purchased_merchant_membership   = False,
                                                        #purchased_customer_membership   = False,
                                                        )
        
        
            customer_transaction.put()
            sales_transaction.used = True
            sales_transaction.put()
            return customer_transaction
    
    @staticmethod
    def create_system_transaction(customer, transact_amount=.0, tax_amount=.0, invoice_id=None, remarks=None, system_remarks=None,
               transact_outlet=None, transact_by=None, transact_datetime=None, reward_giveaway_method=program_conf.PROGRAM_REWARD_GIVEAWAY_METHOD_SYSTEM,
               is_sales_transaction = False, allow_to_revert=True, is_membership_purchase=False, is_membership_renew=False, purchased_customer_membership=None,
               ):
        
        transact_by_username = None
        
        if is_not_empty(transact_by):
            if isinstance(transact_by, MerchantUser):
                transact_by_username = transact_by.username

        
        transaction_id = generate_transaction_id()
        
        if transact_datetime is None:
            transact_datetime = datetime.utcnow()
        
        logger.debug('generated transaction_id=%s', transaction_id)
        logger.debug('invoice_id=%s', invoice_id)
        logger.debug('tax_amount=%s', tax_amount)
        logger.debug('transact_amount=%s', transact_amount)
        logger.debug('transact_datetime=%s', transact_datetime)
        logger.debug('transact_by_username=%s', transact_by_username)
        logger.debug('system_remarks=%s', system_remarks)
        
        customer_transaction = CustomerTransaction(
                                                    parent                          = customer.create_ndb_key(),
                                                    
                                                    transact_merchant               = customer.registered_merchant_acct.create_ndb_key(),
                                                    transact_outlet                 = transact_outlet.create_ndb_key() if transact_outlet else None,
                                                    
                                                    tax_amount                      = tax_amount,
                                                    transact_amount                 = transact_amount,
                                                    
                                                    transaction_id                  = transaction_id,
                                                    invoice_id                      = invoice_id,
                                                    remarks                         = remarks,
                                                    system_remarks                  = system_remarks,
                                                    
                                                    transact_by                     = transact_by.create_ndb_key() if transact_by else None,
                                                    transact_by_username            = transact_by_username,
                                                    
                                                    transact_datetime               = transact_datetime,
                                                    reward_giveaway_method          = reward_giveaway_method,
                                                    
                                                    is_sales_transaction            = is_sales_transaction,
                                                    allow_to_revert                 = allow_to_revert,
                                                    is_membership_purchase          = is_membership_purchase,
                                                    is_membership_renew             = is_membership_renew,
                                                    purchased_merchant_membership   = purchased_customer_membership.merchant_membership_entity.create_ndb_key() if purchased_customer_membership else None,
                                                    purchased_customer_membership   = purchased_customer_membership.create_ndb_key() if purchased_customer_membership else None,
                                                    )
        
        customer_transaction.put()
        #customer.put()
        
        return customer_transaction
    '''
    def revert(self, customer_acct, reverted_by):
        transaction_id = self.transaction_id
        
        entitled_point_details_list     = CustomerPointReward.list_by_transaction_id(transaction_id)
        
        entitled_stamp_details_list     = CustomerStampReward.list_by_transaction_id(transaction_id)
        
        entiteld_vouchers_list          = CustomerEntitledVoucher.list_by_transaction_id(transaction_id)
        
        entitled_prepaid_list           = CustomerPrepaidReward.list_by_transaction_id(transaction_id)
        
        is_transaction_reward_used      = False
        
        customer_reward_summary     = customer_acct.reward_summary or {}
        entitled_voucher_summary    = customer_acct.entitled_voucher_summary or {}
        
        logger.debug('revert: transaction_id=%s', transaction_id)
        logger.debug('revert: entitled_point_details_list count=%s', len(entitled_point_details_list))
        logger.debug('revert: entitled_stamp_details_list count=%s', len(entitled_stamp_details_list))
        logger.debug('revert: entiteld_vouchers_list count=%s', len(entiteld_vouchers_list))
        
        for p in entitled_point_details_list:
            if p.is_used:
                is_transaction_reward_used = True
                break
        
        if is_transaction_reward_used is False:
            for p in entitled_stamp_details_list:
                if p.is_used:
                    is_transaction_reward_used = True
                    break
                
        if is_transaction_reward_used is False:
            for p in entiteld_vouchers_list:
                if p.is_used:
                    is_transaction_reward_used = True
                    break
        
        logger.debug('revert: is_transaction_reward_used=%s', is_transaction_reward_used)
        
        if is_transaction_reward_used is False:
            
            logger.debug('Going to revert transqction')
            reverted_by_key                 = reverted_by.create_ndb_key()
            
            reverted_datetime               = datetime.now()
            self.is_revert                  = True
            self.reverted_datetime          = reverted_datetime
            self.reverted_by                = reverted_by_key
            self.reverted_by_username       = reverted_by.username
            self.put()
            
            for p in entitled_point_details_list:
                if p.is_valid:
                    customer_reward_summary = update_reward_summary_with_reverted_reward(customer_reward_summary, p.to_reward_summary())
                    p.status                        = program_conf.REWARD_STATUS_REVERTED
                    p.reverted_datetime             = reverted_datetime
                    p.reverted_by                   = reverted_by_key
                    p.reverted_by_username          = reverted_by.username
                    p.put()
                    
                
            for p in entitled_stamp_details_list:
                if p.is_valid:
                    customer_reward_summary = update_reward_summary_with_reverted_reward(customer_reward_summary, p.to_reward_summary())
                    p.status                        = program_conf.REWARD_STATUS_REVERTED
                    p.reverted_datetime             = reverted_datetime
                    p.reverted_by                   = reverted_by_key
                    p.reverted_by_username          = reverted_by.username
                    p.put()
                
            for p in entiteld_vouchers_list:
                if p.is_valid:
                    p.status                        = program_conf.REWARD_STATUS_REVERTED
                    p.reverted_datetime             = reverted_datetime
                    p.reverted_by                   = reverted_by_key
                    p.reverted_by_username          = reverted_by.username
                    p.put()
                    
                    entitled_voucher_summary = update_customer_entiteld_voucher_summary_after_reverted_voucher(entitled_voucher_summary, p)
            
            updated_voucher_summary = {}
            
            logger.debug('revert transaction debug: entitled_voucher_summary=%s', entitled_voucher_summary)
            
            for voucher_key, details in entitled_voucher_summary.items():
                if len(details.get('redeem_info_list'))>0:
                    updated_voucher_summary[voucher_key] = details
                
            customer_acct.reward_summary            = customer_reward_summary
            customer_acct.entitled_voucher_summary  = updated_voucher_summary or {}
            customer_acct.put()
            
            return True
        
        else:
            raise Exception('Transaction reward have been used')
    '''
    @staticmethod
    def list_customer_transaction(customer_acct, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False, reverse_order=True, keys_only=False):
        if keys_only:
            query = CustomerTransaction.query(ancestor = customer_acct.create_ndb_key())
            return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, keys_only=True)
        else:
            if reverse_order:
                query = CustomerTransaction.query(ancestor = customer_acct.create_ndb_key()).order(-CustomerTransaction.transact_datetime)
            else:
                query = CustomerTransaction.query(ancestor = customer_acct.create_ndb_key()).order(CustomerTransaction.transact_datetime)
            
            return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def delete_all_by_customer(customer_acct):
        query = CustomerTransaction.query(ancestor = customer_acct.create_ndb_key())
        CustomerTransaction.delete_multiples(query)
    
    @staticmethod
    def list(offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False, reverse_order=True):
        if reverse_order:
            query = CustomerTransaction.query().order(-CustomerTransaction.transact_datetime)
        else:
            query = CustomerTransaction.query().order(CustomerTransaction.transact_datetime)
        
        return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def list_outlet_transaction(transact_outlet, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False, reverse_order=True):
        if reverse_order:
            query = CustomerTransaction.query(ndb.AND(CustomerTransaction.transact_outlet==transact_outlet.create_ndb_key())).order(-CustomerTransaction.transact_datetime)
        else:
            query = CustomerTransaction.query(ndb.AND(CustomerTransaction.transact_outlet==transact_outlet.create_ndb_key())).order(CustomerTransaction.transact_datetime)
        
        return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def list_merchant_transaction(transact_merchant, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False, reverse_order=True):
        if reverse_order:
            query = CustomerTransaction.query(ndb.AND(CustomerTransaction.transact_merchant==transact_merchant.create_ndb_key()))
        else:
            query = CustomerTransaction.query(ndb.AND(CustomerTransaction.transact_merchant==transact_merchant.create_ndb_key()))
        
        return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def count_valid_customer_transaction(customer_acct, limit=conf.MAX_FETCH_RECORD):
        query = CustomerTransaction.query(ndb.AND(CustomerTransaction.is_revert==False), ancestor = customer_acct.create_ndb_key())
        
        return   CustomerTransaction.count_with_condition_query(query, limit=limit)
    
    @staticmethod
    def count_outlet_transaction(transact_outlet, limit=conf.MAX_FETCH_RECORD):
        query = CustomerTransaction.query(ndb.AND(CustomerTransaction.transact_outlet==transact_outlet.create_ndb_key()))
        
        return   CustomerTransaction.count_with_condition_query(query, limit=limit)
    
    @staticmethod
    def list_valid_customer_transaction(customer_acct, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False):
        
        query = CustomerTransaction.query(ndb.AND(CustomerTransaction.is_revert==False), ancestor = customer_acct.create_ndb_key())
        
        if return_with_cursor:
            return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
        else:
            return  CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
        
        
            
    
    @staticmethod
    def list_customer_transaction_by_transact_timestamp(customer_acct, transact_timestamp_from=None, transact_timestamp_to=None):
        return CustomerTransaction.query(ndb.AND(
                                                    CustomerTransaction.transact_timestamp>transact_timestamp_from,
                                                    CustomerTransaction.transact_timestamp<=transact_timestamp_to
                                                  ),ancestor = customer_acct.create_ndb_key()).fetch(limit=conf.MAX_FETCH_RECORD)
        
    @staticmethod
    def list_customer_transaction_by_transact_datetime(customer_acct, transact_datetime_from=None, transact_datetime_to=None):
        return CustomerTransaction.query(ndb.AND(
                                                    CustomerTransaction.transact_datetime>=transact_datetime_from,
                                                    CustomerTransaction.transact_datetime<transact_datetime_to
                                                  ),ancestor = customer_acct.create_ndb_key()).fetch(limit=conf.MAX_FETCH_RECORD)    
    
    @staticmethod
    def get_by_transaction_id(transaction_id):
        return CustomerTransaction.query(CustomerTransaction.transaction_id==transaction_id).get()
    
    @staticmethod
    def list_transaction_by_date(transact_date, transact_outlet=None, including_reverted_transaction=True, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False):
        
        transact_datetime           = datetime.combine(transact_date, datetime.min.time())
        next_day_transact_datetime  = transact_datetime + timedelta(days=1)
        
        logger.debug('transact_datetime=%s',transact_datetime)
        logger.debug('next_day_transact_datetime=%s',next_day_transact_datetime)
        
        if transact_outlet:
            if including_reverted_transaction:
                query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    CustomerTransaction.transact_outlet == transact_outlet.create_ndb_key(),
                                    )).order(-CustomerTransaction.transact_datetime)
            else:
                query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    CustomerTransaction.transact_outlet == transact_outlet.create_ndb_key(),
                                    CustomerTransaction.is_revert == False,
                                    )).order(-CustomerTransaction.transact_datetime)
        else:
            if including_reverted_transaction:
                query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    )).order(-CustomerTransaction.transact_datetime)
            else:
                query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    CustomerTransaction.is_revert == False,
                                    )).order(-CustomerTransaction.transact_datetime)
        
        return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def list_all(offset=0, limit=conf.MAX_FETCH_RECORD):
        
        query = CustomerTransaction.query()
        
        return CustomerTransaction.list_all_with_condition_query(query, offset=offset, limit=limit)
    
    @staticmethod
    def count_customer_transaction(customer_acct, limit=conf.MAX_FETCH_RECORD):
        query = CustomerTransaction.query(ancestor = customer_acct.create_ndb_key())
        
        return CustomerTransaction.count_with_condition_query(query, limit=limit)
    
    @staticmethod
    def count_merchant_transaction(merchant_acct, limit=conf.MAX_FETCH_RECORD):
        query = CustomerTransaction.query(ndb.AND(CustomerTransaction.transact_merchant==merchant_acct.create_ndb_key()))
        
        return CustomerTransaction.count_with_condition_query(query, limit=limit)
    
    @staticmethod
    def count_transaction_by_date(transact_date, including_reverted_transaction=True, transact_outlet=None, limit=conf.MAX_FETCH_RECORD):
        
        transact_datetime           = datetime.combine(transact_date, datetime.min.time())
        next_day_transact_datetime  = transact_datetime + timedelta(days=1)
        
        logger.debug('transact_datetime=%s',transact_datetime)
        logger.debug('next_day_transact_datetime=%s',next_day_transact_datetime)
        
        if transact_outlet:
            if including_reverted_transaction:
                query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    CustomerTransaction.transact_outlet == transact_outlet.create_ndb_key()
                                    ))
            else:
                query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    CustomerTransaction.transact_outlet == transact_outlet.create_ndb_key(),
                                    CustomerTransaction.is_revert == False,
                                    ))
        else:
            if including_reverted_transaction:
                query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    ))
            else:
                query = CustomerTransaction.query(ndb.AND(
                                    CustomerTransaction.transact_datetime  >= transact_datetime,
                                    CustomerTransaction.transact_datetime  <  next_day_transact_datetime,
                                    CustomerTransaction.is_revert == False,
                                    ))
        
        return CustomerTransaction.count_with_condition_query(query, limit=limit)


    
class CustomerTransactionWithRewardDetails(object):    
    
    def __init__(self, transaction_details, reward_details):
        self.transact_customer_key          = transaction_details.transact_customer_key
        self.transact_merchant_acct_key     = transaction_details.transact_merchant_acct_key
        self.transact_outlet_key            = transaction_details.transact_outlet_key
        self.transact_datetime              = transaction_details.transact_datetime
        self.transaction_id                 = transaction_details.transaction_id
        self.transact_amount                = transaction_details.transact_amount
        self.is_revert                      = transaction_details.is_revert
        self.reverted_datetime              = transaction_details.reverted_datetime
        self.reward_format                  = reward_details.reward_format
        self.reward_amount                  = reward_details.reward_amount
        self.expiry_date                    = reward_details.expiry_date
        self.rewarded_datetime              = reward_details.rewarded_datetime 
        self.reward_format_key              = reward_details.reward_format_key
        
    
class CustomerTransactionWithPrepaidDetails(object):    
    
    def __init__(self, transaction_details, prepaid_details):
        self.transact_customer_key          = transaction_details.transact_customer_key
        self.transact_merchant_acct_key     = transaction_details.transact_merchant_acct_key
        self.transact_outlet_key            = transaction_details.transact_outlet_key
        self.transact_datetime              = transaction_details.transact_datetime
        self.transaction_id                 = transaction_details.transaction_id
        self.transact_amount                = transaction_details.transact_amount
        self.is_revert                      = transaction_details.is_revert
        self.reverted_datetime              = transaction_details.reverted_datetime
        self.topup_amount                   = prepaid_details.topup_amount
        self.prepaid_amount                 = prepaid_details.prepaid_amount
        self.topup_datetime                 = prepaid_details.topup_datetime 
            
    
        
        
      
        
        
    
        