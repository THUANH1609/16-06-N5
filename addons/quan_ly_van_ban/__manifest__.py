# -*- coding: utf-8 -*-
{
    'name': "Quản lý khách hàng mới",
    'version': '1.0',

    'depends': ['base', 'mail'],
    # 'depends': ['base', 'nhan_su', 'khach_hang_clean'],
    # 'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/van_ban.xml',
        'views/van_ban_den.xml', # Phải nạp trước
        'views/van_ban_di.xml',  # Phải nạp trước
        # 'views/khach_hang_tn.xml',
        'views/menu.xml',
        # Em có thể tạo thêm file views/menu.xml sau hoặc dán chung vào khach_hang.xml
    ],
    'installable': True,
    'application': True,
}