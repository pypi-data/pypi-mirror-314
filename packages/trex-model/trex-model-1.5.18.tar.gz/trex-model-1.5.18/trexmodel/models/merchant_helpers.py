from trexmodel.models.datastore.pos_models import InvoiceNoGeneration,\
    RoundingSetup, DinningOption, PosPaymentMethod
from trexmodel.models.datastore.merchant_models import ReceiptSetup, Outlet,\
    BannerFile
from trexlib.utils.string_util import is_not_empty
from trexconf import conf
from datetime import datetime
import logging

logger = logging.getLogger('helper')

def construct_merchant_acct_info(merchant_acct):
    account_settings        = {
                                'account_code'  : merchant_acct.account_code,
                                'currency'      : merchant_acct.currency_code,
                                'locale'        : merchant_acct.locale,    
                                }
    
    outlet_list = Outlet.list_by_merchant_acct(merchant_acct)
    outlet_json_list = []
    for o in outlet_list:
        outlet_json_list.append(construct_outlet_info(o))
        
    
    banner_file_listing =  BannerFile.list_by_merchant_acct(merchant_acct)
    banner_listing = []
    if banner_file_listing:
        for banner_file in banner_file_listing:
            banner_listing.append(banner_file.banner_file_public_url)
        
        
    invoice_no_generation   = InvoiceNoGeneration.getByMerchantAcct(merchant_acct)
    
    if invoice_no_generation:
        account_settings['invoice_settings']    = {
                                                     'invoice_no_generators'    : invoice_no_generation.generators_list,
                                                                     
                                                    }
    
    referral_program_settings = merchant_acct.program_settings.get('referral_program', {})
    
    
    
    merchant_news_list=[]
    
    if merchant_acct.published_news_configuration:
        merchant_news_list = merchant_acct.published_news_configuration['news']
    
    published_redemption_catalogue_configuration = merchant_acct.published_redemption_catalogue_configuration
    catalogues_list = []    
    if published_redemption_catalogue_configuration:
        catalogues_list = published_redemption_catalogue_configuration.get('catalogues')
        
        if len(catalogues_list)>0:
            for catalogue in catalogues_list:
                catalogue['items'] = __resolve_catalogue_items_details(catalogue.get('items'), merchant_acct.published_voucher_configuration.get('vouchers'))
    
    info =  {
                'key'                               : merchant_acct.key_in_str,
                'company_name'                      : merchant_acct.company_name,
                'brand_name'                        : merchant_acct.brand_name,
                'website'                           : merchant_acct.website,
                'account_id'                        : merchant_acct.key_in_str,
                'api_key'                           : merchant_acct.api_key,
                'logo_image_url'                    : merchant_acct.logo_public_url,
                'image_default_base_url'            : merchant_acct.image_default_base_url,
                'account_settings'                  : account_settings,
                'outlets'                           : outlet_json_list,
                'banners'                           : banner_listing,
                'merchant_news'                     : merchant_news_list,
                'redemption_catalogues'             : catalogues_list,
                'published_voucher_configuration'   : merchant_acct.published_voucher_configuration,
                
                } 
    if is_not_empty(referral_program_settings):
        
        info['referral_program_settings'] = {
                                                'program_count'             : merchant_acct.effective_referral_program_count,
                                                'referrer_promote_title'    : referral_program_settings.get('referrer_promote_title'),
                                                'referrer_promote_desc'     : referral_program_settings.get('referrer_promote_desc'),
                                                'referrer_promote_image'    : referral_program_settings.get('referrer_promote_image', conf.REFERRAL_DEFAULT_PROMOTE_IMAGE),
                                                'referee_promote_title'     : referral_program_settings.get('referee_promote_title'),
                                                'referee_promote_desc'      : referral_program_settings.get('referee_promote_desc'),
                                                'referee_promote_image'     : referral_program_settings.get('referee_promote_image'),
                                                
                                            }
    
    return info

def __check_is_still_active(catalogue):
    today = datetime.utcnow().date()
    start_date  = datetime.strptime(catalogue.get('start_date'), '%d-%m-%Y').date()
    end_date    = datetime.strptime(catalogue.get('end_date'), '%d-%m-%Y').date()
    
    if today>=start_date and today<=end_date:
        logger.info('catalogue is still valid')
        return True
    else:
        logger.info('catalogue is expired')
        return False
    
def __resolve_catalogue_items_details(catalogue_items_list, vouchers_list):
    resolved_items_list = []
    voucher_dict = __convert_vouchers_list_to_dict(vouchers_list)
    for item in catalogue_items_list:
        voucher = voucher_dict.get(item.get('voucher_key'))
        if voucher:
            resolved_items_list.append(
                    {
                        'voucher_key'           : item.get('voucher_key'),
                        'amount'                : item.get('voucher_amount'),
                        'label'                 : voucher.get('label'),
                        'image_url'             : voucher.get('image_url'),
                        'terms_and_conditions'  : voucher.get('terms_and_conditions'),
                        'redeem_reward_amount'  : item.get('redeem_reward_amount'),
                    }
                
                )
        else:
            resolved_items_list.append(item)
        
    return resolved_items_list    

def __convert_vouchers_list_to_dict(vouchers_list):
    voucher_dict = {}
    for voucher in vouchers_list:
        voucher_dict[voucher.get('voucher_key')] = voucher
    
    return voucher_dict

def construct_outlet_info(outlet):
    geo_location = None
    if outlet.geo_location:
        geo_location = '%s,%s' % (outlet.geo_location.latitude, outlet.geo_location.longitude)
    return {
            'outlet_key'        : outlet.key_in_str,
            'outlet_name'       : outlet.name,
            'address'           : outlet.address,
            'business_hour'     : outlet.business_hour,
            'geo_location'      : geo_location,
            
        }

def construct_setting_by_outlet(outlet, device_setting=None, is_pos_device=False):


    merchant_acct           = outlet.merchant_acct_entity
    invoice_no_generation   = InvoiceNoGeneration.getByMerchantAcct(merchant_acct)
    rounding_setup          = RoundingSetup.get_by_merchant_acct(merchant_acct)
    receipt_setup           = ReceiptSetup.get_by_merchant_acct(merchant_acct)
    dinning_option_json     = []
    dinning_option_list     = DinningOption.list_by_merchant_acct(merchant_acct)
    
    account_settings        = {
                                'account_code'  : merchant_acct.account_code,
                                'currency'      : merchant_acct.currency_code,
                                'locale'        : merchant_acct.locale,    
                                }
    if is_pos_device:
        if dinning_option_list:
            for d in dinning_option_list:
                dinning_option_json.append({
                                            'option_key'                : d.key_in_str,
                                            'option_name'               : d.name,
                                            'option_prefix'             : d.prefix,
                                            'is_default'                : d.is_default,
                                            'is_dinning_input'          : d.is_dinning_input,
                                            'is_delivery_input'         : d.is_delivery_input,
                                            'is_takeaway_input'         : d.is_takeaway_input,
                                            'is_self_order_input'       : d.is_self_order_input,
                                            'is_self_payment_mandatory' : d.is_self_payment_mandatory,
                                            'dinning_table_is_required' : d.dinning_table_is_required,
                                            'assign_queue'              : d.assign_queue,
                                            })
    
    if is_pos_device:
        account_settings['dinning_option_list'] = dinning_option_json
        
    if invoice_no_generation:
        account_settings['invoice_settings']    = {
                                                     'invoice_no_generators'    : invoice_no_generation.generators_list,
                                                                     
                                                    }
    else:
        account_settings['invoice_settings'] = {}
    
    if receipt_setup:
        account_settings['receipt_settings'] = {
                                                'header_data_list': receipt_setup.receipt_header_settings,
                                                'footer_data_list': receipt_setup.receipt_footer_settings or [],
                                                }
    
    if rounding_setup:
        account_settings['rounding_settings']     = {
                                                    'rounding_interval' : rounding_setup.rounding_interval,
                                                    'rounding_rule'     : rounding_setup.rounding_rule,
                                                    }
    pos_payment_method_json = []
    pos_payment_method_list = PosPaymentMethod.list_by_merchant_acct(merchant_acct)
    
    if pos_payment_method_list:
        for d in pos_payment_method_list:
            pos_payment_method_json.append({
                                        'code'                  : d.code,
                                        'key'                   : d.key_in_str,
                                        'label'                 : d.label,
                                        'is_default'            : d.is_default,
                                        'is_rounding_required'  : d.is_rounding_required,
                                        })
    
    account_settings['assigned_service_charge_setup']   = outlet.service_charge_settings
    account_settings['assigned_tax_setup']              = outlet.assigned_tax_setup
    account_settings['dinning_table_list']              = outlet.assigned_dinning_table_list
    account_settings['show_dinning_table_occupied']     = outlet.show_dinning_table_occupied
    account_settings['payment_methods']                 = pos_payment_method_json
    
    
    outlet_details = {
                    'key'                        : outlet.key_in_str,
                    'id'                         : outlet.id,
                    'outlet_name'                : outlet.name,
                    'company_name'               : outlet.company_name,
                    'brand_name'                 : merchant_acct.brand_name,
                    'business_reg_no'            : outlet.business_reg_no,
                    'address'                    : outlet.address,
                    'email'                      : outlet.email,
                    'phone'                      : outlet.office_phone,
                    'website'                    : merchant_acct.website or '',  
                        
                    }
    
    program_configurations = {
                            'prepaid_configuration' : merchant_acct.prepaid_configuration,
                            'days_of_return_policy' : merchant_acct.program_settings.get('days_of_return_policy'),
                            }
    
    setting =  {
                'company_name'                      : merchant_acct.company_name,
                'brand_name'                        : merchant_acct.brand_name,
                'website'                           : merchant_acct.website,
                'account_id'                        : merchant_acct.key_in_str,
                'api_key'                           : merchant_acct.api_key,
                'logo_image_url'                    : merchant_acct.logo_public_url,
                'image_default_base_url'            : merchant_acct.image_default_base_url,
                'account_settings'                  : account_settings,
                'outlet_details'                    : outlet_details,
                'program_configurations'            : program_configurations,
                'membership_configurations'         : merchant_acct.membership_configuration, 
                } 
    if device_setting:
        setting['activation_code']              = device_setting.activation_code
        setting['device_name']                  = device_setting.device_name
        setting['device_id']                    = device_setting.device_id
        setting['enable_lock_screen']           = device_setting.enable_lock_screen
        setting['lock_screen_code']             = device_setting.lock_screen_code
        setting['lock_screen_length_in_second'] = device_setting.lock_screen_length_in_second
        
    return setting