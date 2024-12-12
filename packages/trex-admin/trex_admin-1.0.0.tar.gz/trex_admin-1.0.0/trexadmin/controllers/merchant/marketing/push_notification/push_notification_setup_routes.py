'''
Created on 5 Jan 2024

@author: jacklok
'''
from flask import Blueprint, request, url_for
import logging
from trexadmin.libs.flask.decorator.security_decorators import login_required
from trexadmin.libs.flask.utils.flask_helper import get_loggedin_merchant_user_account
from trexmodel.utils.model.model_util import create_db_client
from trexmodel.models.datastore.merchant_models import MerchantAcct,\
    MerchantUser
from flask.templating import render_template
from flask_babel import gettext
from trexadmin.forms.merchant.marketing.push_notification_setup_forms import PushNotificationSetupForm
from trexlib.utils.log_util import get_tracelog
from trexadmin.libs.http import StatusCode, create_rest_message
from trexmodel.models.datastore.marketing_models import PushNotificationSetup,\
    MarketingImage
from trexlib.utils.common.common_util import sort_list
from trexlib.utils.string_util import is_not_empty, is_empty, truncate_string
import jinja2
from datetime import datetime
from trexadmin.controllers.system.system_route_helpers import get_push_notification_content_type_label
from trexadmin.conf import DEFAULT_TIMEZONE, IS_LOCAL
from trexlib.utils.google.cloud_tasks_util import create_task
from trexconf.conf import SYSTEM_TASK_SERVICE_CREDENTIAL_PATH, SYSTEM_TASK_GCLOUD_PROJECT_ID, SYSTEM_TASK_GCLOUD_LOCATION, SYSTEM_TASK_SERVICE_ACCOUNT_EMAIL
from trexconf import conf
from trexadmin.controllers.merchant.marketing.push_notification.push_notification_task_routes import send_push_notification

push_notification_setup_bp = Blueprint('push_notification_setup_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/merchant/marketing/messaging/push_notification')


logger = logging.getLogger('controller')


@jinja2.contextfilter
@push_notification_setup_bp.app_template_filter()
def push_notification_content_type_label(context, content_type):
    label = get_push_notification_content_type_label(content_type)
    if is_empty(label):
        return '-'
    else:
        return label


'''
Blueprint settings here
'''
@push_notification_setup_bp.context_processor
def messaging_setup_bp_inject_settings():
    
    return dict(

    )

def get_marketing_image_list():
    logged_in_merchant_user         = get_loggedin_merchant_user_account()
    db_client = create_db_client(caller_info="show_push_notification_setup_listing")
    
    marketing_images_list = []
    
    with db_client.context():
        merchant_acct   = MerchantAcct.fetch(logged_in_merchant_user.get('merchant_acct_key'))
        images_list = MarketingImage.list_by_merchant_acct(merchant_acct)
        marketing_images_list.append(object)
    
@push_notification_setup_bp.route('/list', methods=['GET'])
@login_required
def manage_push_notification_setup(): 
    return show_push_notification_setup_listing(
                'merchant/marketing/push_notification/manage_push_notification.html',
                
                )



def show_push_notification_setup_listing(template_name, show_page_title=True, is_archived=False): 
    logged_in_merchant_user         = get_loggedin_merchant_user_account()
    push_notification_setup_list        = []
    
    logger.debug('template_name=%s', template_name)
    logger.debug('show_page_title=%s', show_page_title)
    logger.debug('is_archived=%s', is_archived)
    
    db_client = create_db_client(caller_info="show_push_notification_setup_listing")
    try:
        if logged_in_merchant_user:
            with db_client.context():
                merchant_acct   = MerchantAcct.fetch(logged_in_merchant_user.get('merchant_acct_key'))
                #logger.debug('merchant_acct=%s', merchant_acct)
                if is_archived:
                    _push_notification_setup_list  = sort_list(PushNotificationSetup.list_archived_by_merchant_acct(merchant_acct), 'created_datetime', reverse_order=True)
                else:
                    _push_notification_setup_list  = sort_list(PushNotificationSetup.list_by_merchant_acct(merchant_acct), 'created_datetime', reverse_order=True)
                
                for mp in _push_notification_setup_list:
                    push_notification_setup_list.append(mp.to_dict())
            
    except:
        logger.error('Fail to list push notification setup due to %s', get_tracelog())
           
    
    logger.debug('push notification setup list count=%d', len(push_notification_setup_list))
    
    return render_template(template_name,
                           page_title = gettext('Manage Push Notification') if show_page_title else None,
                           push_notification_setup_list = push_notification_setup_list,
                           )

@push_notification_setup_bp.route('/create', methods=['GET'])    
def create_push_notification_setup():
    return render_template('merchant/marketing/push_notification/setup/create_push_notification_setup.html',
                           page_title                                           = gettext('Push Notification Setup'),
                           reload_push_notification_setup_listing_content_url   = url_for('push_notification_setup_bp.push_notification_setup_listing_content'),
                           archived_push_notification_setup_listing_url         = url_for('push_notification_setup_bp.archived_push_notification_setup_listing'),
                           create_push_notification_setup_url                   = url_for('push_notification_setup_bp.create_push_notification_setup_post'),
                           is_edit_push_notification_setup                      = True,
                           )
    
@push_notification_setup_bp.route('/create', methods=['post'])
def create_push_notification_setup_post():
    logger.debug('--- create_push_notification_setup_post ---')
    
    logged_in_merchant_user = get_loggedin_merchant_user_account()
    
    push_notification_setup_data = request.form
    
    logger.debug('push_notification_setup_data=%s', push_notification_setup_data)
    
    push_notification_setup_form = PushNotificationSetupForm(push_notification_setup_data)
    
    db_client = create_db_client(caller_info="create_push_notification_setup_post")
    
    is_send_now = False
    
    try:
        with db_client.context():
            merchant_acct   = MerchantAcct.fetch(logged_in_merchant_user.get('merchant_acct_key'))
            merchant_user   = MerchantUser.get_by_user_id(logged_in_merchant_user.get('user_id'))
            
            #title           = push_notification_setup_form.title.data
            title           = truncate_string(merchant_acct.brand_name, 65)
            desc            = push_notification_setup_form.desc.data
            send_mode       = push_notification_setup_form.send_mode.data
            schedule_date   = push_notification_setup_form.schedule_date.data
            schedule_time   = push_notification_setup_form.schedule_time.data
            content_type    = push_notification_setup_form.content_type.data
            action_link     = push_notification_setup_form.action_link.data
            image_content   = push_notification_setup_form.image_content.data
            text_content    = push_notification_setup_form.text_content.data
            
            
            
            if send_mode == 'send_schedule':
                schedule_date_str = schedule_date.strftime('%d-%m-%Y')
            
                schedule_datetime =  datetime.strptime('%s %s' % (schedule_date_str, schedule_time), '%d-%m-%Y %H:%M')
                
                logger.debug('schedule_datetime=%s', schedule_datetime)
                
                import pytz
                
                gmt_timezone = pytz.timezone(DEFAULT_TIMEZONE)
                if is_not_empty(merchant_acct.timezone):
                    gmt_timezone = pytz.timezone(merchant_acct.timezone)
                
                localized_datetime  = gmt_timezone.localize(schedule_datetime)
                
                logger.debug('localized_datetime=%s', localized_datetime)
                
                schedule_datetime = (localized_datetime - localized_datetime.utcoffset()).replace(tzinfo=None)
            else:
                schedule_datetime = datetime.utcnow()
                is_send_now = True
                
            logger.debug('title=%s', title)
            logger.debug('desc=%s', desc)
            logger.debug('send_mode=%s', send_mode)
            logger.debug('schedule_datetime=%s', schedule_datetime)    
            logger.debug('content_type=%s', content_type)
            logger.debug('action_link=%s', action_link)
            logger.debug('image_content=%s', image_content)
            logger.debug('text_content=%s', text_content)
            
            content_settings = {}
            
            if content_type == 'text':
                content_settings = {
                                    'content_type':content_type,
                                    'content_value':text_content, 
                                    }
            elif content_type =='action_link':
                content_settings = {
                                    'content_type':content_type,
                                    'content_value':action_link, 
                                    }
            elif content_type=='image':
                content_settings = {
                                    'content_type':content_type,
                                    'content_value':image_content, 
                                    }    
            
            logger.debug('content_settings=%s', content_settings)
            
            push_notification_setup = PushNotificationSetup.create(merchant_acct, 
                                         title              = title, 
                                         desc               = desc, 
                                         send_mode          = send_mode,
                                         schedule_datetime  = schedule_datetime, 
                                         content_settings   = content_settings,
                                         created_by         = merchant_user,
                                         )
            
            logger.debug('push_notification_setup=%s', push_notification_setup)
            
        if is_send_now:
            if IS_LOCAL:
                return send_push_notification(push_notification_setup.key_in_str)
            else:
                task_url        = '%s/push-notification/task/setup/%s' % (conf.APPLICATION_BASE_URL ,push_notification_setup.key_in_str)
                create_task(task_url, 'default', in_seconds=1, 
                            http_method     = 'GET',
                            credential_path = SYSTEM_TASK_SERVICE_CREDENTIAL_PATH, 
                            project_id      = SYSTEM_TASK_GCLOUD_PROJECT_ID,
                            location        = SYSTEM_TASK_GCLOUD_LOCATION,
                            service_email   = SYSTEM_TASK_SERVICE_ACCOUNT_EMAIL
                            )
        
        return create_rest_message(status_code=StatusCode.OK)
            
    except:
        logger.error('Failed due to %s', get_tracelog())
        
        return create_rest_message(gettext('Failed to create push notification'), status_code=StatusCode.BAD_REQUEST)
    

@push_notification_setup_bp.route('/list/content', methods=['GET'])
def push_notification_setup_listing_content():
    return show_push_notification_setup_listing(
                'merchant/marketing/push_notification/latest_push_notification_setup_listing_content.html',
                )

@push_notification_setup_bp.route('/list/archived', methods=['GET'])
def archived_push_notification_setup_listing():
    return show_push_notification_setup_listing(
                'merchant/marketing/push_notification/archived_push_notification_setup_listing.html',
                show_page_title = False,
                is_archived = True
                )  

@push_notification_setup_bp.route('/read/<push_notification_setup_key>', methods=['get'])
def view_push_notification_setup(push_notification_setup_key):
    logger.debug('--- view_push_notification_setup ---')
    db_client = create_db_client(caller_info="archive_push_notification_setup")
    
    try:
        with db_client.context():
            push_notification_setup     = PushNotificationSetup.fetch(push_notification_setup_key)
            if push_notification_setup:
                push_notification_setup = push_notification_setup.to_dict()
            
        
        return render_template('merchant/marketing/push_notification/setup/create_push_notification_setup.html',
                           page_title                                           = gettext('Push Notification Setup'),
                           push_notification_setup                              = push_notification_setup,
                           create_push_notification_setup_url                   = url_for('push_notification_setup_bp.create_push_notification_setup_post'),
                           is_edit_push_notification_setup                      = False,
                           
                           )
    except:
        logger.error('Failed due to %s', get_tracelog())
        
        return create_rest_message(gettext('Failed to create push notification'), status_code=StatusCode.BAD_REQUEST)
    
    
    
@push_notification_setup_bp.route('/archive/<push_notification_setup_key>', methods=['post','get'])
def archive_push_notification_setup(push_notification_setup_key):
    logger.debug('--- archive_push_notification_setup ---')
    
    logged_in_merchant_user = get_loggedin_merchant_user_account()
    
    db_client = create_db_client(caller_info="archive_push_notification_setup")
    
    try:
        with db_client.context():
            push_notification_setup     = PushNotificationSetup.fetch(push_notification_setup_key)
            merchant_user               = MerchantUser.get_by_user_id(logged_in_merchant_user.get('user_id'))
            
            if push_notification_setup:
                push_notification_setup.archived(merchant_user)
            
            return create_rest_message(status_code=StatusCode.OK)
    except:
        logger.error('Failed due to %s', get_tracelog())
        
        return create_rest_message(gettext('Failed to archive push notification'), status_code=StatusCode.BAD_REQUEST)                
