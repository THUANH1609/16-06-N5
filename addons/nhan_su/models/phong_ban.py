# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Quản lý thông tin phòng ban'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Thêm chatter
    _rec_name = 'ten_phong_ban'
    _order = 'ma_phong_ban asc'

    # 1. Thông tin chính
    ma_phong_ban = fields.Char(
        string="Mã phòng ban", 
        required=True, 
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('phong_ban') or 'PB-New'
    )
    ten_phong_ban = fields.Char(
        string="Tên phòng ban", 
        required=True,
        tracking=True  # Theo dõi thay đổi trong chatter
    )
    mo_ta = fields.Text(
        string="Mô tả",
        tracking=True
    )

    # 2. Chức năng: Xem danh sách nhân viên thuộc phòng này
    nhan_vien_ids = fields.One2many(
        comodel_name='nhan_vien', 
        inverse_name='phong_ban_id', 
        string="Danh sách nhân viên"
    )

    # 3. Trường computed: Đếm số lượng nhân viên
    so_luong_nhan_vien = fields.Integer(
        string='Số lượng nhân viên',
        compute='_compute_so_luong_nhan_vien',
        store=True,
        help="Tổng số nhân viên trong phòng ban"
    )

    # Ràng buộc: Mã phòng ban không được trùng
    _sql_constraints = [  # Sửa lỗi chính tả: _sql_constrains -> _sql_constraints
        ('ma_phong_ban_unique', 'unique(ma_phong_ban)', 'Mã phòng ban đã tồn tại!')
    ]

    @api.depends('nhan_vien_ids')
    def _compute_so_luong_nhan_vien(self):
        """Tính số lượng nhân viên trong phòng ban"""
        for record in self:
            record.so_luong_nhan_vien = len(record.nhan_vien_ids)

    def action_view_employees(self):
        """Mở danh sách nhân viên của phòng ban (dùng cho button box)"""
        self.ensure_one()
        return {
            'name': f'Nhân viên - {self.ten_phong_ban}',
            'type': 'ir.actions.act_window',
            'res_model': 'nhan_vien',
            'view_mode': 'tree,form',
            'domain': [('phong_ban_id', '=', self.id)],
            'context': {
                'default_phong_ban_id': self.id,
                'search_default_active': 1  # Mặc định hiển thị nhân viên đang làm
            }
        }
# # -*- coding: utf-8 -*-
# from odoo import models, fields, api

# class PhongBan(models.Model):
#     _name = 'phong_ban'
#     _description = 'Quản lý thông tin phòng ban'
#     _rec_name = 'ten_phong_ban'  # Để khi chọn bên Nhân viên sẽ hiện Tên thay vì ID
#     _order = 'ma_phong_ban asc'

#     # 1. Thông tin chính
#     ma_phong_ban = fields.Char(string="Mã phòng ban", required=True)
#     ten_phong_ban = fields.Char(string="Tên phòng ban", required=True)
#     mo_ta = fields.Text(string="Mô tả")

#     # 2. Chức năng: Xem danh sách nhân viên thuộc phòng này
#     # Field này kết nối ngược lại với 'phong_ban_id' bên model 'nhan_vien'
#     nhan_vien_ids = fields.One2many(
#         comodel_name='nhan_vien', 
#         inverse_name='phong_ban_id', 
#         string="Danh sách nhân viên"
#     )

#     # Ràng buộc: Mã phòng ban không được trùng
#     _sql_constrains = [
#         ('ma_phong_ban_unique', 'unique(ma_phong_ban)', 'Mã phòng ban đã tồn tại!')
#     ]