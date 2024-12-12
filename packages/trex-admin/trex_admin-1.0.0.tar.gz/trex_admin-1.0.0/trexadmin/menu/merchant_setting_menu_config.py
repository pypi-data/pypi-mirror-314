'''
Created on 17 Dec 2020

@author: jacklok
'''
from flask_babel import gettext
from trexadmin.menu import merchant_staff_mgmt_menu_config

merchant_manage_account_sub_menu = {
                        'title'         : gettext('Details'),
                        'menu_item'     : 'manage_merchant_account',
                        'end_point'     : 'merchant_manage_account_bp.merchant_account_details',
                        'icon_class'    : 'fas fa-gear',
                        'permission'    : 'manage_merchant_account',
                        
                        }

merchant_upload_logo_sub_menu = {
                        'title'         : gettext('Logo'),
                        'menu_item'     : 'manage_merchant_logo',
                        'end_point'     : 'merchant_manage_account_bp.upload_logo',
                        'icon_class'    : 'fas fa-gear',
                        'permission'    : 'manage_merchant_account',
                        
                        }

merchant_manage_outlet_sub_menu = {
                        'title'         : gettext('Outlet'),
                        'menu_item'     : 'manage_outlet',
                        'end_point'     : 'merchant_manage_outlet_bp.manage_outlet',
                        'icon_class'    : 'fas fa-gear',
                        'permission'    : 'manage_merchant_outlet',
                        
                        }

manage_banner_sub_menu = {
                        'title'         : gettext('Upload Banner'),
                        'menu_item'     : 'upload_banner',
                        'end_point'     : 'merchant_manage_banner_bp.manage_banner_index',
                        'icon_class'    : 'fas fa-gear',
                        'permission'    : 'upload_banner',
                        
                        }


merchant_integration_sub_menu = {
                        'title'         : gettext('Integration'),
                        'menu_item'     : 'manage_integration',
                        'end_point'     : 'merchant_manage_integration_bp.manage_integration_index',
                        'icon_class'    : 'fas fa-gear',
                        'permission'    : 'manage_merchant_integration',
                        
                        }



menu_items = {
                                'title'         : 'Account',
                                'menu_item'     : 'merchant_settings',
                                'icon_class'    : 'fas fa-building',
                                'permission'    : ['manage_merchant_account'],
                                'childs'        : [
                                    
                                                    merchant_manage_account_sub_menu,
                                                    merchant_upload_logo_sub_menu,
                                                    manage_banner_sub_menu,
                                                    merchant_staff_mgmt_menu_config.menu_items,
                                                    merchant_manage_outlet_sub_menu,
                                                    merchant_integration_sub_menu,
                                                            
                                                ]
                }

