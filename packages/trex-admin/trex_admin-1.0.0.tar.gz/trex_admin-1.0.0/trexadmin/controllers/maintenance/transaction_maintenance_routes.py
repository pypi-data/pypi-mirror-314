'''
Created on 27 Mar 2023

@author: jacklok
'''
from flask import Blueprint, request, render_template, jsonify
import logging
from trexmodel.utils.model.model_util import create_db_client
from trexmodel.models.datastore.transaction_models import CustomerTransaction
from trexanalytics.helper.bigquery_upstream_helpers import list_transction_reward,\
    create_transction_reward_upstream
from flask.json import jsonify
from trexmodel.models.datastore.message_model_helper import create_transaction_message
from trexlib.libs.controllers.task_base_routes import TriggerTaskBaseResource,\
    InitTaskBaseResource, TaskBaseResource
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.merchant_models import MerchantAcct
from trexanalytics.bigquery_upstream_data_config import create_merchant_sales_transaction_upstream_for_merchant
from flask_restful import Api

transaction_maintenance_setup_bp = Blueprint('transaction_maintenance_setup_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/maint/transaction')


transaction_maintenance_setup_bp_api = Api(transaction_maintenance_setup_bp)

#logger = logging.getLogger('controller')
logger = logging.getLogger('debug')

@transaction_maintenance_setup_bp.route('/transaction-key/<transaction_key>/list-reward', methods=['get'])
def list_transaction_reward(transaction_key):
    db_client = create_db_client(caller_info="list_transaction_reward")
    rewards_list = []
    with db_client.context():
        customer_transaction = CustomerTransaction.fetch(transaction_key)
        logger.debug('customer_transaction=%s', customer_transaction)
        if customer_transaction:
            rewards_list = list_transction_reward(customer_transaction)
        
        
    return jsonify(rewards_list)

@transaction_maintenance_setup_bp.route('/transaction-id/<transaction_id>/list-reward', methods=['get'])
def list_transaction_reward_by_transaction_id(transaction_id):
    db_client = create_db_client(caller_info="list_transaction_reward_by_transaction_id")
    rewards_list = []
    with db_client.context():
        customer_transaction = CustomerTransaction.get_by_transaction_id(transaction_id)
        logger.debug('customer_transaction=%s', customer_transaction)
        if customer_transaction:
            _rewards_list = list_transction_reward(customer_transaction)
            if _rewards_list:
                for r in _rewards_list:
                    rewards_list.append(r.to_dict())
        
    return jsonify(rewards_list)

@transaction_maintenance_setup_bp.route('/transaction-id/<transaction_id>/create-reward-upstream', methods=['get'])
def create_tansaction_reward_upstream_by_transaction_id(transaction_id):
    db_client = create_db_client(caller_info="list_transaction_reward_by_transaction_id")
    rewards_list = []
    with db_client.context():
        customer_transaction = CustomerTransaction.get_by_transaction_id(transaction_id)
        logger.debug('customer_transaction=%s', customer_transaction)
        if customer_transaction:
            _rewards_list = list_transction_reward(customer_transaction)
            if _rewards_list:
                for r in _rewards_list:
                    rewards_list.append(r.to_dict())
            
            create_transction_reward_upstream(customer_transaction)
        
    return jsonify(rewards_list)

@transaction_maintenance_setup_bp.route('/transaction-id/<transaction_id>/create-transaction-message', methods=['get'])
def create_tansaction_message(transaction_id):
    db_client = create_db_client(caller_info="create_tansaction_message")
    rewards_list = []
    with db_client.context():
        customer_transaction = CustomerTransaction.get_by_transaction_id(transaction_id)
        logger.debug('customer_transaction=%s', customer_transaction)
        if customer_transaction:
            create_transaction_message(customer_transaction)
        
    return jsonify(rewards_list)

class TriggerCreateTransactionUpstream(TriggerTaskBaseResource):
    
    def get_task_url(self):
        return '/maint/transaction/init-create-transaction-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
        
    def get_data_payload(self):
        return {
                
            }    
    
class InitCreateTransactionUpstream(InitTaskBaseResource):
    def get_task_count(self, **kwargs):
        
        
        db_client = create_db_client(caller_info="InitCreateTransactionUpstream")
    
        with db_client.context():
            count = CustomerTransaction.count()

        return count
    
    def get_task_batch_size(self):
        return 50
    
    def get_task_url(self):
        return '/maint/transaction/create-transaction-upstream'
    
    def get_task_queue(self):
        return 'upstream-maint'
    
    
class ExecuteCreateTransactionUpstream(TaskBaseResource):
    def execute_task(self, offset, limit, **kwargs):
        merchant_key    = kwargs.get('merchant_key')
        start_cursor    = kwargs.get('start_cursor')
        task_index      = int(kwargs.get('task_index'))
        next_cursor     = None
        
        logger.debug('execute_task debug: task_index=%d, offset=%d, limit=%d', task_index, offset, limit)
        
        db_client = create_db_client(caller_info="ExecuteCreateTransactionUpstream")
        
        with db_client.context():
            if is_not_empty(merchant_key):
                merchant_acct = MerchantAcct.fetch(merchant_key)
                #(result, next_cursor) = Customer.list(limit=20, start_cursor=start_cursor, return_with_cursor=True)
                if merchant_acct:
                    (result, next_cursor) = CustomerTransaction.list_merchant_transaction(merchant_acct, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=True)
            else:
                (result, next_cursor) = CustomerTransaction.list(limit=20, start_cursor=start_cursor, return_with_cursor=True)
            
            logger.debug('=================>>>>>> ExecuteCreateTransactionUpstream debug: result count=%s, next_cursor=%s', len(result), next_cursor)
            if result:
                for transaction in result:
                    logger.debug('transaction key=%s', transaction.key_in_str)
                    create_merchant_sales_transaction_upstream_for_merchant(transaction)
            
        
        return next_cursor
        
    def get_task_queue(self):
        return 'upstream-maint'   
    
    def get_task_url(self):
        return '/maint/transaction/create-transaction-upstream' 


transaction_maintenance_setup_bp_api.add_resource(TriggerCreateTransactionUpstream,   '/trigger-create-transaction-upstream')
transaction_maintenance_setup_bp_api.add_resource(InitCreateTransactionUpstream,   '/init-create-transaction-upstream')
transaction_maintenance_setup_bp_api.add_resource(ExecuteCreateTransactionUpstream,   '/create-transaction-upstream')
    
