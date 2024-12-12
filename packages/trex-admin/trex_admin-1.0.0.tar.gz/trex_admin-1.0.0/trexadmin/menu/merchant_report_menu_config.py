'''
Created on 22 Dec 2020

@author: jacklok
'''

from flask_babel import gettext


merchant_customer_report_growth_menu_item = {
                                    'title'         : 'Customer Growth',
                                    'menu_item'     : 'merchant_report_customer_growth',
                                    'end_point'     : 'merchant_customer_growth_report_bp.merchant_customer_growth',
                                    'icon_class'    : 'fas fa-bar-chart',
                                    'permission'    : 'read_report',
                        
                        }



merchant_customer_report_sub_menu = {
                                    'title'         : gettext('Customer Report'),
                                    'menu_item'     : 'merchant_customer_report',
                                    'icon_class'    : 'fa fa-table',
                                    'permission'    : [
                                                        'read_report'
                                                        ],
                                    'childs'        : [
                                                        merchant_customer_report_growth_menu_item,
                                                        ]   
                        }


merchant_rewarding_daily_report_menu_item = {
                                    'title'         : gettext('Rewarding Daily Report'),
                                    'menu_item'     : 'merchant_reward_daily_report',
                                    'end_point'     : 'merchant_rewarding_report_bp.merchant_reward_daily_report',
                                    'icon_class'    : 'fas fa-table',
                                    'permission'    : 'read_report',
                        
                        }

merchant_rewarding_monthly_report_menu_item = {
                                    'title'         : gettext('Rewarding Monthly Report'),
                                    'menu_item'     : 'merchant_reward_monthly_report',
                                    'end_point'     : 'merchant_rewarding_report_bp.merchant_reward_monthly_report',
                                    'icon_class'    : 'fas fa-table',
                                    'permission'    : 'read_report',
                        
                        }

merchant_redemption_daily_report_menu_item = {
                                    'title'         : gettext('Redemption Daily Report'),
                                    'menu_item'     : 'merchant_redemption_daily_report',
                                    'end_point'     : 'merchant_redemption_report_bp.merchant_redemption_daily_report',
                                    'icon_class'    : 'fas fa-table',
                                    'permission'    : 'read_report',
                        
                        }

merchant_redemption_monthly_report_menu_item = {
                                    'title'         : gettext('Redemption Monthly Report'),
                                    'menu_item'     : 'merchant_redemption_monthly_report',
                                    'end_point'     : 'merchant_redemption_report_bp.merchant_redemption_monthly_report',
                                    'icon_class'    : 'fas fa-table',
                                    'permission'    : 'read_report',
                        
                        }

merchant_rewarding_report_sub_menu = {
                                    'title'         : gettext('Rewarding'),
                                    'menu_item'     : 'merchant_rewarding_report',
                                    'icon_class'    : 'fas fa-folder',
                                    'permission'    : [
                                                        'read_report',
                                                        ],
                                    'childs'        : [
                                                        merchant_rewarding_daily_report_menu_item,
                                                        merchant_rewarding_monthly_report_menu_item,
                                                        ]   
                        }

merchant_redemption_report_sub_menu = {
                                    'title'         : gettext('Redemption'),
                                    'menu_item'     : 'merchant_redemption_report',
                                    'icon_class'    : 'fas fa-folder',
                                    'permission'    : [
                                                        'read_report'
                                                        ],
                                    'childs'        : [
                                                        merchant_redemption_daily_report_menu_item,
                                                        merchant_redemption_monthly_report_menu_item,
                                                        ]   
                        }

merchant_top_spender_report_menu_item = {
                                    'title'         : gettext('Top Spender'),
                                    'menu_item'     : 'merchant_top_spender_report',
                                    'end_point'     : 'merchant_spender_performance_report_bp.merchant_top_spender_report',
                                    'icon_class'    : 'fas fa-table',
                                    'permission'    : 'read_report',
                        
                        }

merchant_non_active_customer_report_menu_item = {
                                    'title'         : gettext('Last Active Customer'),
                                    'menu_item'     : 'merchant_last_active_report',
                                    'end_point'     : 'merchant_spender_performance_report_bp.merchant_last_active_report',
                                    'icon_class'    : 'fas fa-table',
                                    'permission'    : 'read_report',
                        
                        }

merchant_voucher_daily_performance_report_menu_item = {
                                    'title'         : gettext('Daily'),
                                    'menu_item'     : 'merchant_voucher_daily_report',
                                    'end_point'     : 'merchant_voucher_performance_report_bp.merchant_voucher_daily_performance_report',
                                    'icon_class'    : 'fas fa-table',
                                    'permission'    : 'read_report',
                        
                        }

merchant_voucher_date_range_performance_report_menu_item = {
                                    'title'         : gettext('Date Range'),
                                    'menu_item'     : 'merchant_voucher_date_range_report',
                                    'end_point'     : 'merchant_voucher_performance_report_bp.merchant_voucher_by_date_range_performance_report',
                                    'icon_class'    : 'fas fa-table',
                                    'permission'    : 'read_report',
                        
                        }

merchant_voucher_monthly_performance_report_menu_item = {
                                    'title'         : gettext('Monthly'),
                                    'menu_item'     : 'merchant_voucher_monthly_report',
                                    'end_point'     : 'merchant_voucher_performance_report_bp.merchant_voucher_monthly_performance_report',
                                    'icon_class'    : 'fas fa-table',
                                    'permission'    : 'read_report',
                        
                        }

merchant_voucher_performance_report_sub_menu = {
                                    'title'         : gettext('Voucher'),
                                    'menu_item'     : 'merchant_voucher_performance_report',
                                    'icon_class'    : 'fas fa-folder',
                                    'permission'    : [
                                                        'read_report'
                                                        ],
                                    'childs'        : [
                                                        #merchant_voucher_daily_performance_report_menu_item,
                                                        #merchant_voucher_monthly_performance_report_menu_item,
                                                        merchant_voucher_date_range_performance_report_menu_item,
                                                        ]   
                        }

merchant_performance_report_sub_menu = {
                                    'title'         : gettext('Performance'),
                                    'menu_item'     : 'merchant_performance_report',
                                    'icon_class'    : 'fas fa-folder',
                                    'permission'    : [
                                                        'read_report'
                                                        ],
                                    'childs'        : [
                                                        merchant_top_spender_report_menu_item,
                                                        merchant_non_active_customer_report_menu_item,
                                                        merchant_voucher_performance_report_sub_menu,
                                                        ]   
                        }




menu_items = {
                                
                                'title'         : 'Report',
                                'menu_item'     : 'merchant_report',
                                'icon_class'    : 'fas fa-database',
                                'permission'    : ['read_report'],
                                'childs'        : [
                                    
                                                    #merchant_customer_report_sub_menu,
                                                    merchant_rewarding_report_sub_menu,
                                                    merchant_redemption_report_sub_menu,
                                                    merchant_performance_report_sub_menu,
                                                            
                                                ]
                }


