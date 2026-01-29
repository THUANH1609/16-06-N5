# -*- coding: utf-8 -*-
from odoo import fields, models, api

class LichSuTuongTac(models.Model):
    _name = "lich_su_tuong_tac"
    _description = "Lịch sử tương tác khách hàng"
    _order = "ngay_tuong_tac desc" # Hiện cái mới nhất lên đầu

    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", ondelete='cascade')
    ngay_tuong_tac = fields.Datetime(string="Thời gian", default=fields.Datetime.now)
    loai_hinh = fields.Selection([
        ('goi_dien', 'Gọi điện'),
        ('email', 'Gửi Email'),
        ('gap_mat', 'Gặp trực tiếp'),
        ('zalo', 'Nhắn tin Zalo/Facebook'),
        ('khac', 'Khác')
    ], string="Hình thức", default='goi_dien')
    
    nhan_vien_id = fields.Many2one('nhan_vien', string="Người thực hiện")
    noi_dung = fields.Text(string="Nội dung chi tiết", required=True)
    ket_qua = fields.Selection([
        ('tot', 'Tốt/Quan tâm'),
        ('trung_binh', 'Đang cân nhắc'),
        ('kem', 'Không quan tâm/Bận')
    ], string="Kết quả")