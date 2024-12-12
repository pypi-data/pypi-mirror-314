'''
Created on 8 Jan 2021

@author: jacklok
'''

from trexadmin.menu import merchant_report_menu_config, merchant_crm_menu_config, testing_menu_config,\
    merchant_program_menu_config
from trexadmin.menu import merchant_setting_menu_config
from trexadmin.menu import merchant_product_mgmt_menu_config
from trexadmin.menu import merchant_pos_menu_config
from trexadmin.menu import merchant_marketing_menu_config
from flask_babel import gettext
from trexconf import conf


guide_menu_item = {
                        'title'         : gettext('Guide'),
                        'menu_item'     : 'merchant_guide',
                        'end_point'     : 'merchant_bp.guide_page',
                        'icon_class'    : 'fas fa-info',
                        'permission'    : '',
                        
                }


dashboard_menu_item = {
                        'title'         : gettext('Dashboard'),
                        'menu_item'     : 'merchant_dashboard',
                        'end_point'     : 'merchant_bp.dashboard_page',
                        'icon_class'    : 'fas fa-tachometer-alt',
                        'permission'    : '',
                        'active'        : True,
                        'reload_window' : True,
                }

setup_guide_menu_item = {
                        'title'         : gettext('Setup Guide'),
                        'menu_item'     : 'merchant_tour',
                        'end_point'     : 'merchant_tour_bp.tour_page',
                        'icon_class'    : 'fas fa-book',
                        'permission'    : '',
                        
                        
                }

guide_menu_item = {
                        'title'         : gettext('Guide'),
                        'menu_item'     : 'merchant_guide',
                        'end_point'     : 'merchant_tour_bp.tour_page',
                        'icon_class'    : 'fas fa-book',
                        'permission'    : '',
                        'childs'        :[
                                            setup_guide_menu_item
                                            ]
                        
                }

menu_items  = [
                        guide_menu_item,
                        dashboard_menu_item,
                        merchant_setting_menu_config.menu_items,
                        merchant_product_mgmt_menu_config.product_submenu_items,
                        merchant_program_menu_config.menu_items,
                        merchant_crm_menu_config.menu_items,
                        merchant_marketing_menu_config.menu_items,
                        merchant_pos_menu_config.menu_items,
                        merchant_report_menu_config.menu_items, 
                        
                        ]  

if conf.IS_LOCAL:
    menu_items.append(testing_menu_config.menu_items)
