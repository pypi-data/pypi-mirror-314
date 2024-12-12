'''
Created on 24 Mar 2023

@author: jacklok
'''

from flask import Blueprint, request, render_template, jsonify, Response
from trexmodel.utils.model.model_util import create_db_client 
import logging
from trexlib.utils.string_util import is_not_empty, is_empty
from flask.helpers import url_for
from trexmodel.models.datastore.customer_models import Customer,\
    CustomerMembership
from trexmodel.models.datastore.transaction_models import CustomerTransaction
from flask_restful import Api
from trexlib.libs.controllers.task_base_routes import TriggerTaskBaseResource,\
    InitTaskBaseResource, TaskBaseResource
from trexmodel.models.datastore.redeem_models import CustomerRedemption
from trexadmin.controllers.report.merchant import customer
from trexmodel.models.datastore.merchant_models import MerchantAcct
from trexanalytics.bigquery_upstream_data_config import create_merchant_registered_customer_upstream_for_merchant,\
    create_registered_customer_upstream_for_system,\
    create_merchant_customer_transaction_upstream_for_merchant,\
    create_customer_membership_upstream_for_merchant
from trexanalytics.helper.bigquery_upstream_helpers import create_transction_reward_upstream,\
    create_redemption_upstream
from flask_restful import Resource
from trexlib.utils.google.bigquery_util import create_bigquery_client
from trexconf import conf


upstream_maintenance_bp = Blueprint('upstream_maintenance_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/maint/upstream')


#logger = logging.getLogger('controller')
logger = logging.getLogger('debug')

upstream_maintenance_setup_bp_api = Api(upstream_maintenance_bp)

@upstream_maintenance_bp.route('/ping', methods=['get'])
def ping():
    return "pong", 200

@upstream_maintenance_bp.route('/dataset/<dataset_name>/table-name-prefix/<table_name_prefix>/list-dataset-table', methods=['get'])
def list_dataset_table_partition(dataset_name, table_name_prefix):
    bg_client       = create_bigquery_client(credential_filepath=conf.BIGQUERY_SERVICE_CREDENTIAL_PATH, project_id=conf.BIGQUERY_GCLOUD_PROJECT_ID)
    dataset_ref     = bg_client.dataset(dataset_name)
    tables          = bg_client.list_tables(dataset_ref)
    tables_list     = []
    final_table_prefix = '%s' % (table_name_prefix)
    for table in tables:
        if table.table_id.startswith(final_table_prefix):
            tables_list.append(table.table_id)
            
    return jsonify(tables_list)

@upstream_maintenance_bp.route('/dataset/<dataset_name>/table-name-prefix/<table_name_prefix>/merchant-account-code/<merchant_account_code>/list-dataset-table', methods=['get'])
def list_dataset_table_partition_by_merchant_code(dataset_name, table_name_prefix, merchant_account_code):
    bg_client       = create_bigquery_client(credential_filepath=conf.BIGQUERY_SERVICE_CREDENTIAL_PATH, project_id=conf.BIGQUERY_GCLOUD_PROJECT_ID)
    dataset_ref     = bg_client.dataset(dataset_name)
    tables          = bg_client.list_tables(dataset_ref)
    tables_list     = []
    final_table_prefix = '%s_%s' % (table_name_prefix, merchant_account_code.replace('-',''))
    
    logger.debug('final_table_prefix=%s', final_table_prefix)
    
    for table in tables:
        #logger.debug('table.table_id=%s', table.table_id)
        if table.table_id.startswith(final_table_prefix):
            tables_list.append(table.table_id)
            logger.debug('table.table_id=%s', table.table_id)
            
    return jsonify(tables_list)

@upstream_maintenance_bp.route('/dataset/<dataset_name>/table-name-prefix/<table_name_prefix>/merchant-account-code/<merchant_account_code>/delete-dataset-table', methods=['get'])
def delete_dataset_table_partition(dataset_name, table_name_prefix, merchant_account_code):
    bg_client       = create_bigquery_client(credential_filepath=conf.BIGQUERY_SERVICE_CREDENTIAL_PATH, project_id=conf.BIGQUERY_GCLOUD_PROJECT_ID)
    dataset_ref     = bg_client.dataset(dataset_name)
    tables          = bg_client.list_tables(dataset_ref)
    tables_list     = []
    final_table_prefix = '%s_%s' % (table_name_prefix, merchant_account_code.replace('-',''))
    for table in tables:
        if table.table_id.startswith(final_table_prefix):
            tables_list.append(str(table.table_id))
    
    for table_id in tables_list:
        table_ref = bg_client.dataset(dataset_name).table(table_id)

        # Delete the table
        bg_client.delete_table(table_ref)
            
    return jsonify(tables_list)


class ModuleIndexResource(Resource):
    
    def output_html(self, content, code=200, headers=None):
        resp = Response(content, mimetype='text/html', headers=headers)
        resp.status_code = code
        return resp
    
    def post(self):
        return self.get()
    
    def get(self):
        return self.output_html("Upstream maintenance module")



class TriggerCreateMerchantRegisteredCustomerUpstream(TriggerTaskBaseResource):
    
    def get_task_url(self):
        return '/maint/upstream/init-merchant-registered-customer-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
        
    def get_data_payload(self):
        merchant_key=request.args.get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }    
        
class InitCreateMerchantRegisteredCustomerUpstream(InitTaskBaseResource):
    def get_task_count(self, **kwargs):
        count = 0
        merchant_key = kwargs.get('merchant_key')
        
        
        db_client = create_db_client(caller_info="InitCreateMerchantRegisteredCustomerUpstrea")
    
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            
        
            count = Customer.count_merchant_customer(merchant_acct)
        
        return count
    
    def get_task_batch_size(self):
        return 50
    
    def get_task_url(self):
        return '/maint/upstream/merchant-registered-customer-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
    
    def get_data_payload(self):
        merchant_key=request.get_json().get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }
    
class ExecuteCreateMerchantRegisteredCustomerUpstream(TaskBaseResource):
    def execute_task(self, offset, limit, **kwargs):
        merchant_key    = kwargs.get('merchant_key')
        start_cursor    = kwargs.get('start_cursor')
        task_index      = int(kwargs.get('task_index'))
        next_cursor     = None
        
        logger.debug('execute_task debug: merchant_key=%s task_index=%d, offset=%d, limit=%d', merchant_key, task_index, offset, limit)
        
        db_client = create_db_client(caller_info="ExecuteCreateMerchantRegisteredCustomer")
    
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            
            if merchant_acct:
                
                (result, next_cursor) = Customer.list_merchant_customer(merchant_acct, start_cursor, limit=50, return_with_cursor=True) 
                                                                                            
                logger.debug('=================>>>>>> ExecuteCreateMerchantRegisteredCustomerUpstream debug: result count=%s, next_cursor=%s', len(result), next_cursor)
                if result:
                    for customer in result:
                        logger.debug('going to create upstream for customer name=%s', customer.name)
                        
                        create_merchant_registered_customer_upstream_for_merchant(customer)
                        create_registered_customer_upstream_for_system(customer)
                    
                    
                
        return next_cursor
        
    def get_task_queue(self):
        return 'upstream-maint'   
    
    def get_task_url(self):
        return '/maint/upstream/merchant-registered-customer-upstream'
    
    def get_data_payload(self):
        merchant_key=request.get_json().get('merchant_key')
        return {
                'merchant_key': merchant_key,
            } 
        
class TriggerCreateCustomerMembershipUpstream(TriggerTaskBaseResource):
    
    def get_task_url(self):
        return '/maint/upstream/init-customer-membership-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
        
    def get_data_payload(self):
        merchant_key=request.args.get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }    
        
class InitCreateCustomerMembershipUpstream(InitTaskBaseResource):
    def get_task_count(self, **kwargs):
        
        merchant_key = kwargs.get('merchant_key')
        
        
        db_client = create_db_client(caller_info="InitCreateMerchantRegisteredCustomerUpstrea")
    
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            
        
            count = CustomerMembership.count_merchant_customer_membership(merchant_acct)
        
        return count
    
    def get_task_batch_size(self):
        return 50
    
    def get_task_url(self):
        return '/maint/upstream/customer-membership-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
    
    def get_data_payload(self):
        merchant_key=request.get_json().get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }
    
class ExecuteCreateCustomerMembershipUpstream(TaskBaseResource):
    def execute_task(self, offset, limit, **kwargs):
        merchant_key    = kwargs.get('merchant_key')
        start_cursor    = kwargs.get('start_cursor')
        task_index      = int(kwargs.get('task_index'))
        next_cursor     = None
        
        logger.debug('execute_task debug: merchant_key=%s task_index=%d, offset=%d, limit=%d', merchant_key, task_index, offset, limit)
        
        db_client = create_db_client(caller_info="ExecuteCreateMerchantRegisteredCustomer")
    
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            
            if merchant_acct:
                
                (result, next_cursor) = CustomerMembership.list_merchant_customer_membership(merchant_acct, limit=50, start_cursor=start_cursor, return_with_cursor=True) 
                                                                                            
                logger.debug('=================>>>>>> ExecuteCreateMerchantRegisteredCustomerUpstream debug: result count=%s, next_cursor=%s', len(result), next_cursor)
                if result:
                    for customer_membership in result:
                        customer = customer_membership.customer
                        logger.debug('going to create upstream for customer name=%s', customer.name)
                        
                        create_customer_membership_upstream_for_merchant(customer)
                    
                    
                
        return next_cursor
        
    def get_task_queue(self):
        return 'upstream-maint'   
    
    def get_task_url(self):
        return '/maint/upstream/customer-membership-upstream'
    
    def get_data_payload(self):
        merchant_key=request.get_json().get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }         
    
class TriggerCreateCustomerRewardUpstream(TriggerTaskBaseResource):
    
    def get_task_url(self):
        return '/maint/upstream/init-merchant-customer-reward-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
        
    def get_data_payload(self):
        merchant_key=request.args.get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }    
        
class InitCreateCustomerRewardUpstream(InitTaskBaseResource):
    def get_task_count(self, **kwargs):
        count = 0
        merchant_key = kwargs.get('merchant_key')
        
        
        db_client = create_db_client(caller_info="InitCreateCustomerRewardUpstream")
    
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            
        
            count = CustomerTransaction.count_merchant_transaction(merchant_acct)
        
        return count
    
    def get_task_batch_size(self):
        return 50
    
    def get_task_url(self):
        return '/maint/upstream/merchant-customer-reward-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
    
    def get_data_payload(self):
        merchant_key=request.get_json().get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }
    
class ExecuteCreateCustomerRewardUpstream(TaskBaseResource):
    def execute_task(self, offset, limit, **kwargs):
        merchant_key    = kwargs.get('merchant_key')
        start_cursor    = kwargs.get('start_cursor')
        task_index      = int(kwargs.get('task_index'))
        next_cursor     = None
        
        logger.debug('execute_task debug: merchant_key=%s task_index=%d, offset=%d, limit=%d', merchant_key, task_index, offset, limit)
        
        db_client = create_db_client(caller_info="ExecuteCreateCustomerRewardUpstream")
    
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            
            if merchant_acct:
                
                (result, next_cursor) = CustomerTransaction.list_merchant_transaction(merchant_acct, start_cursor, limit=50, return_with_cursor=True) 
                                                                                            
                logger.debug('=================>>>>>> ExecuteCreateCustomerRewardUpstream debug: result count=%s, next_cursor=%s', len(result), next_cursor)
                if result:
                    for transaction_details in result:
                        create_transction_reward_upstream(transaction_details)    
                        #create_merchant_customer_transaction_upstream_for_merchant(transaction_details, streamed_datetime=transaction_details.transact_datetime)
                        
                    
                    
                
        return next_cursor
        
    def get_task_queue(self):
        return 'upstream-maint'   
    
    def get_task_url(self):
        return '/maint/upstream/merchant-customer-reward-upstream'
    
    def get_data_payload(self):
        merchant_key=request.get_json().get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }
        
class TriggerCreateMerchantSalesUpstream(TriggerTaskBaseResource):
    
    def get_task_url(self):
        return '/maint/upstream/init-merchant-sales-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
        
    def get_data_payload(self):
        merchant_key=request.args.get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }    
        
class InitCreateMerchantSalesUpstream(InitTaskBaseResource):
    def get_task_count(self, **kwargs):
        count = 0
        merchant_key = kwargs.get('merchant_key')
        
        
        db_client = create_db_client(caller_info="InitCreateMerchantSalesUpstream")
    
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            
        
            count = CustomerTransaction.count_merchant_transaction(merchant_acct)
        
        return count
    
    def get_task_batch_size(self):
        return 50
    
    def get_task_url(self):
        return '/maint/upstream/merchant-sales-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
    
    def get_data_payload(self):
        merchant_key=request.get_json().get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }
    
class ExecuteCreateMerchantSalesUpstream(TaskBaseResource):
    def execute_task(self, offset, limit, **kwargs):
        merchant_key    = kwargs.get('merchant_key')
        start_cursor    = kwargs.get('start_cursor')
        task_index      = int(kwargs.get('task_index'))
        next_cursor     = None
        
        logger.debug('execute_task debug: merchant_key=%s task_index=%d, offset=%d, limit=%d', merchant_key, task_index, offset, limit)
        
        db_client = create_db_client(caller_info="ExecuteCreateMerchantSalesUpstream")
    
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            
            if merchant_acct:
                
                (result, next_cursor) = CustomerTransaction.list_merchant_transaction(merchant_acct, start_cursor, limit=50, return_with_cursor=True) 
                                                                                            
                logger.debug('=================>>>>>> ExecuteCreateMerchantSalesUpstream debug: result count=%s, next_cursor=%s', len(result), next_cursor)
                if result:
                    for transaction_details in result:
                        create_merchant_customer_transaction_upstream_for_merchant(transaction_details, streamed_datetime=transaction_details.transact_datetime)
                        
                    
                    
                
        return next_cursor
        
    def get_task_queue(self):
        return 'upstream-maint'   
    
    def get_task_url(self):
        return '/maint/upstream/merchant-sales-upstream'
    
    def get_data_payload(self):
        merchant_key=request.get_json().get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }        
    
class TriggerCreateCustomerRedemptionUpstream(TriggerTaskBaseResource):
    
    def get_task_url(self):
        return '/maint/upstream/init-merchant-customer-redemption-upstream'
    
    def get_task_queue(self):
        return 'test'
        
    def get_data_payload(self):
        merchant_key=request.args.get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }    
        
class InitCreateCustomerRedemptionUpstream(InitTaskBaseResource):
    def get_task_count(self, **kwargs):
        count = 0
        merchant_key = kwargs.get('merchant_key')
        
        logger.debug('InitCreateCustomerRedemptionUpstream debug: merchant_key=%s', merchant_key)
        
        db_client = create_db_client(caller_info="InitCreateCustomerRedemptionUpstream")
    
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            
        
            count = CustomerRedemption.count_merchant_redemption(merchant_acct)
        
        logger.debug('InitCreateCustomerRedemptionUpstream debug: count=%d', count)
        
        return count
    
    def get_task_batch_size(self):
        return 50
    
    def get_task_url(self):
        return '/maint/upstream/merchant-customer-redemption-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
    
    def get_data_payload(self):
        merchant_key=request.get_json().get('merchant_key')
        
        logger.debug('InitCreateCustomerRedemptionUpstream debug: get_data_payload merchant_key=%s', merchant_key)
        
        return {
                'merchant_key': merchant_key,
            }
    
class ExecuteCreateCustomerRedemptionUpstream(TaskBaseResource):
    def execute_task(self, offset, limit, **kwargs):
        merchant_key    = kwargs.get('merchant_key')
        start_cursor    = kwargs.get('start_cursor')
        task_index      = int(kwargs.get('task_index'))
        next_cursor     = None
        
        logger.debug('ExecuteCreateCustomerRedemptionUpstream debug: merchant_key=%s task_index=%d, offset=%d, limit=%d', merchant_key, task_index, offset, limit)
        
        db_client = create_db_client(caller_info="ExecuteCreateCustomerRedemptionUpstream")
    
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(merchant_key)
            
            if merchant_acct:
                
                (result, next_cursor) = CustomerRedemption.list_merchant_transaction(merchant_acct, start_cursor, limit=50, return_with_cursor=True) 
                                                                                            
                logger.debug('=================>>>>>> ExecuteCreateCustomerRedemptionUpstream debug: result count=%s, next_cursor=%s', len(result), next_cursor)
                if result:
                    for redemption_details in result:
                        
                        create_redemption_upstream(redemption_details)    
                        
                    
                    
                
        return next_cursor
        
    def get_task_queue(self):
        return 'upstream-maint'   
    
    def get_task_url(self):
        return '/maint/upstream/merchant-customer-redemption-upstream'    
    
    def get_data_payload(self):
        merchant_key=request.get_json().get('merchant_key')
        return {
                'merchant_key': merchant_key,
            }
               
    
upstream_maintenance_setup_bp_api.add_resource(ModuleIndexResource,   '/index')

upstream_maintenance_setup_bp_api.add_resource(TriggerCreateMerchantRegisteredCustomerUpstream,   '/trigger-merchant-registered-customer-upstream')
upstream_maintenance_setup_bp_api.add_resource(InitCreateMerchantRegisteredCustomerUpstream,   '/init-merchant-registered-customer-upstream')
upstream_maintenance_setup_bp_api.add_resource(ExecuteCreateMerchantRegisteredCustomerUpstream,   '/merchant-registered-customer-upstream')

upstream_maintenance_setup_bp_api.add_resource(TriggerCreateCustomerMembershipUpstream,   '/trigger-customer-membership-upstream')
upstream_maintenance_setup_bp_api.add_resource(InitCreateCustomerMembershipUpstream,   '/init-customer-membership-upstream')
upstream_maintenance_setup_bp_api.add_resource(ExecuteCreateCustomerMembershipUpstream,   '/customer-membership-upstream')
          
upstream_maintenance_setup_bp_api.add_resource(TriggerCreateMerchantSalesUpstream,   '/trigger-merchant-sales-upstream')
upstream_maintenance_setup_bp_api.add_resource(InitCreateMerchantSalesUpstream,   '/init-merchant-sales-upstream')
upstream_maintenance_setup_bp_api.add_resource(ExecuteCreateMerchantSalesUpstream,   '/merchant-sales-upstream')

upstream_maintenance_setup_bp_api.add_resource(TriggerCreateCustomerRewardUpstream,   '/trigger-merchant-customer-reward-upstream')
upstream_maintenance_setup_bp_api.add_resource(InitCreateCustomerRewardUpstream,   '/init-merchant-customer-reward-upstream')
upstream_maintenance_setup_bp_api.add_resource(ExecuteCreateCustomerRewardUpstream,   '/merchant-customer-reward-upstream')

upstream_maintenance_setup_bp_api.add_resource(TriggerCreateCustomerRedemptionUpstream,   '/trigger-merchant-customer-redemption-upstream')
upstream_maintenance_setup_bp_api.add_resource(InitCreateCustomerRedemptionUpstream,   '/init-merchant-customer-redemption-upstream')
upstream_maintenance_setup_bp_api.add_resource(ExecuteCreateCustomerRedemptionUpstream,   '/merchant-customer-redemption-upstream')

