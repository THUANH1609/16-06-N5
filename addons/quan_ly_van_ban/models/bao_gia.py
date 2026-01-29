# -*- coding: utf-8 -*-
from odoo import fields, models, api

class BaoGia(models.Model):
    _name = "bao_gia"
    _description = "Báo giá khách hàng"
    _rec_name = 'so_bao_gia'

    so_bao_gia = fields.Char(string="Số báo giá", required=True, copy=False, readonly=True, 
                             default=lambda self: 'Mới')
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", ondelete='cascade')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Người lập báo giá")
    
    ngay_lap = fields.Date(string="Ngày lập", default=fields.Date.context_today)
    ngay_het_han = fields.Date(string="Ngày hết hạn")
    
    tong_tien = fields.Float(string="Tổng giá trị (VNĐ)", required=True)
    trang_thai = fields.Selection([
        ('du_thao', 'Dự thảo'),
        ('da_gui', 'Đã gửi khách'),
        ('chap_nhan', 'Khách đã chốt'),
        ('tu_choi', 'Bị từ chối')
    ], string="Trạng thái", default='du_thao')

    ghi_chu = fields.Text(string="Điều khoản thương mại")

    @api.model
    def create(self, vals):
        if vals.get('so_bao_gia', 'Mới') == 'Mới':
            # Em có thể tạo sequence để số báo giá tự nhảy (ví dụ: BG2026/0001)
            vals['so_bao_gia'] = self.env['ir.sequence'].next_by_code('bao_gia.code') or 'Mới'
        return super(BaoGia, self).create(vals)