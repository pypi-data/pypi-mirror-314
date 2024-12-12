'''
Created on 10 Dec 2020

@author: jacklok
'''

from flask import Blueprint, render_template, session, current_app, abort, request
from trexadmin.libs.flask.decorator.security_decorators import login_required, login_required_rest, account_activated
from trexadmin.menu import merchant_menu 
from trexadmin.libs.flask.utils.flask_helper import check_is_menu_accessable, get_loggedin_merchant_user_account, get_preferred_language
from flask_babel import gettext
from flask.helpers import url_for
import logging
import jinja2
from trexmodel.utils.model.model_util import create_db_client
from trexadmin.analytics_conf import MERCHANT_CUSTOMER_GROWTH_CHART_DATA_URL, MERCHANT_SALES_GROWTH_CHART_DATA_URL,\
    MERCHANT_CUSTOMER_COUNT_BY_DATE_RANGE_DATA_URL,\
    MERCHANT_SALES_YEARLY_DATE_RANGE_DATA_URL,\
    MERCHANT_TRANSACTION_COUNT_YEARLY_DATE_RANGE_DATA_URL,\
    MERCHANT_CUSTOMER_GENDER_BY_DATE_RANGE_DATA_URL,\
    MERCHANT_CUSTOMER_AGE_GROUP_BY_DATE_RANGE_DATA_URL
from trexmodel.models.datastore.customer_models import Customer
from datetime import datetime, timedelta
from trexlib.utils.log_util import get_tracelog
from flask.json import jsonify
from trexlib.utils.common.date_util import last_day_of_month
from datetime import date
from trexmodel.models.datastore.merchant_models import MerchantAcct
from werkzeug.utils import redirect

merchant_bp = Blueprint('merchant_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/merchant')

logger = logging.getLogger('controller')

'''
Blueprint settings here
'''
@merchant_bp.context_processor
def merchant_bp_inject_settings():
    return {
            
            }


@jinja2.contextfilter
@merchant_bp.app_template_filter()
def is_menu_accessable(context, menu_config):
    return check_is_menu_accessable(menu_config, 'merchant_bp')

@merchant_bp.route('/dashboard')
@account_activated
@login_required
def dashboard_page(): 
    
    return prepare_dashboard('merchant/dashboard/merchant_dashboard_index.html')

@merchant_bp.route('/guide')
def guide_page(): 
    
    return render_template(
                    'merchant/help/merchant_guide_page.html', 
                    page_title    = gettext('Guide'),
                    )             

    
@merchant_bp.route('/dashboard-content')
def dashboard_content(): 
    
    return prepare_dashboard('merchant/dashboard/merchant_dashboard.html', show_page_title=False, show_menu_config=False)                
    

def prepare_dashboard(template_path, show_page_title=True, show_menu_config=True):
    
    try:
        logged_in_user_id   = session.get('logged_in_user_id')
        is_merchant_user    = session.get('is_merchant_user')
        
        logger.debug('dashboard_page: logged_in_user_id=%s', logged_in_user_id)
        logger.debug('dashboard_page: is_merchant_user=%s', is_merchant_user)
    
        if is_merchant_user:
            menu_config  = merchant_menu.menu_items
        else:
            menu_config  = []
            
        application_logo_url        = None
        logged_in_merchant_user     = get_loggedin_merchant_user_account()
        
        if logged_in_merchant_user is None:
            abort(400)
        
        db_client                   = create_db_client(caller_info="dashboard_page")
        merchant_company_name       = None
        today                       = datetime.today()
        start_joined_year           = today.year
        
            
        with db_client.context():
            
            merchant_acct   = MerchantAcct.fetch(logged_in_merchant_user.get('merchant_acct_key'))
        
        if merchant_acct:
            account_code            = merchant_acct.account_code
            merchant_key            = merchant_acct.key_in_str
            start_joined_year       = merchant_acct.plan_start_date.year
            merchant_company_name   = merchant_acct.company_name
            
            if merchant_acct.logo_public_url:
                application_logo_url    = merchant_acct.logo_public_url
                
    
            this_year   = today.year
            year_range_list =  []
            
            for year in range(start_joined_year, this_year+1):
                year_range_list.append(year)
            
            sorted_year_range_list = sorted(year_range_list, reverse=True)
            year_range_list = sorted_year_range_list
                
            given_date                  = datetime.today().date()
            first_date_of_year          = date(given_date.year, 1, 1)
            
            first_date_of_month         = given_date - timedelta(days = int(given_date.strftime("%d"))-1)
            last_date_of_month          = last_day_of_month(given_date)
            
            merchant_plan_start_date    = merchant_acct.plan_start_date
            
            
            return render_template(template_path, 
                                   page_title                       = gettext('Dashboard') if show_page_title else None,
                                   menu_config                      = menu_config if show_menu_config else None,
                                   #page_url                         = url_for('merchant_bp.dashboard_content') if show_page_title else None,
                                   application_logo_url             = application_logo_url,
                                   merchant_key                     = merchant_key,
                                   merchant_company_name            = merchant_company_name,
                                   
                                   year                             = today.year,
                                   month                            = today.month,
                                   year_range_list                  = year_range_list,
                                   get_stat_details_url             = url_for('merchant_analytic_bp.get_merchant_stat_details'),
                                   
                                   #stat widget data url
                                   get_customer_count_data_url      = MERCHANT_CUSTOMER_COUNT_BY_DATE_RANGE_DATA_URL+"?account_code="+account_code+'&date_range_from='+first_date_of_month.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),
                                   get_sales_data_url               = MERCHANT_SALES_YEARLY_DATE_RANGE_DATA_URL+"?account_code="+account_code+'&date_range_from='+first_date_of_month.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),
                                   get_transaction_count_data_url   = MERCHANT_TRANSACTION_COUNT_YEARLY_DATE_RANGE_DATA_URL+"?account_code="+account_code+'&date_range_from='+first_date_of_month.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),
                                   
                                   #dashboard chart data url
                                   customer_growth_chart_data_url   = MERCHANT_CUSTOMER_GROWTH_CHART_DATA_URL+"?account_code="+account_code+'&date_range_from='+first_date_of_year.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),
                                   customer_gender_data_url         = MERCHANT_CUSTOMER_GENDER_BY_DATE_RANGE_DATA_URL+"?account_code="+account_code+'&date_range_from='+merchant_plan_start_date.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),
                                   customer_age_group_data_url      = MERCHANT_CUSTOMER_AGE_GROUP_BY_DATE_RANGE_DATA_URL+"?account_code="+account_code+'&date_range_from='+merchant_plan_start_date.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),
                                   
                                   sales_growth_chart_data_url      = MERCHANT_SALES_GROWTH_CHART_DATA_URL+"?account_code="+account_code+'&date_range_from='+first_date_of_month.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),
                                   sales_growth_chart_data_base_url = MERCHANT_SALES_GROWTH_CHART_DATA_URL+"?account_code="+account_code
                                   
                                   )
        else:
            was_once_logged_in  = session.get('was_once_logged_in')
        
            logger.debug('was_once_logged_in=%s', was_once_logged_in)
            
            if was_once_logged_in:
                user_type = session.get('user_type')
                
                logger.debug('user_type=%s', user_type)
                
                if user_type == 'admin':
                    return redirect(url_for('admin_bp.dashboard_page'))
            else:
                return redirect(url_for('security_bp.merchant_signin_page'))
            
    except:
        logger.error('Failed due to %s', get_tracelog())
        
        abort(400)

def stat_widget(template_path):
    try:
        logged_in_user_id   = session.get('logged_in_user_id')
        is_merchant_user    = session.get('is_merchant_user')
        
        logger.debug('dashboard_page: logged_in_user_id=%s', logged_in_user_id)
        logger.debug('dashboard_page: is_merchant_user=%s', is_merchant_user)
    
        if is_merchant_user:
            menu_config  = merchant_menu.menu_items
        else:
            menu_config  = []
            
        logged_in_merchant_user     = get_loggedin_merchant_user_account()
        
        if logged_in_merchant_user is None:
            abort(400)
        
        db_client                   = create_db_client(caller_info="dashboard_page")
        
        
            
        with db_client.context():
            
            merchant_acct   = MerchantAcct.fetch(logged_in_merchant_user.get('merchant_acct_key'))
        
        if merchant_acct:
            account_code    = merchant_acct.account_code
            
            if merchant_acct.logo_public_url:
                start_joined_year       = merchant_acct.plan_start_date.year
    
            today       = datetime.today()
            this_year   = today.year
            year_range_list =  []
            
            for year in range(start_joined_year, this_year+1):
                year_range_list.append(year)
            
            sorted_year_range_list = sorted(year_range_list, reverse=True)
            year_range_list = sorted_year_range_list
                
            given_date                  = datetime.today().date()
            first_date_of_year          = date(given_date.year, 1, 1)
            
            first_date_of_month         = given_date - timedelta(days = int(given_date.strftime("%d"))-1)
            last_date_of_month          = last_day_of_month(given_date)
            
            merchant_plan_start_date    = merchant_acct.plan_start_date
            
            now = datetime.now()
            
        return render_template(template_path, 
                                   year                             = now.year,
                                   month                            = now.month,
                                   year_range_list                  = year_range_list,
                                   
                                   customer_growth_chart_data_url   = MERCHANT_CUSTOMER_GROWTH_CHART_DATA_URL+"?account_code="+account_code+'&date_range_from='+first_date_of_year.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),  
                                   customer_gender_data_url         = MERCHANT_CUSTOMER_GENDER_BY_DATE_RANGE_DATA_URL+"?account_code="+account_code+'&date_range_from='+merchant_plan_start_date.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),
                                   customer_age_group_data_url      = MERCHANT_CUSTOMER_AGE_GROUP_BY_DATE_RANGE_DATA_URL+"?account_code="+account_code+'&date_range_from='+merchant_plan_start_date.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),
                                   
                                   sales_growth_chart_data_url      = MERCHANT_SALES_GROWTH_CHART_DATA_URL+"?account_code="+account_code+'&date_range_from='+first_date_of_month.strftime('%Y%m%d')+'&date_range_to='+last_date_of_month.strftime('%Y%m%d'),
                                   sales_growth_chart_data_base_url = MERCHANT_SALES_GROWTH_CHART_DATA_URL+"?account_code="+account_code,
                                   show_full                        = True,    
                                   )
     
    except:
        logger.error('Failed due to %s', get_tracelog())
        
        abort(400)  
            
@merchant_bp.route('/gender-group-stat')
@account_activated
@login_required
def gender_group_stat():
    
    return stat_widget('merchant/dashboard/merchant_gender_group_stat_widget.html') 

@merchant_bp.route('/age-group-stat')
@account_activated
@login_required
def age_group_stat():
    
    return stat_widget('merchant/dashboard/merchant_age_group_stat_widget.html') 


#@merchant_bp.route('/<merchant_account_key>/logo-url')
#def merchant_logo_url(merchant_account_key):
    
    