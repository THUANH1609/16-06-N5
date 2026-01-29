# -*- coding: utf-8 -*-
from odoo import fields, models, api

class TaiLieuPhapLy(models.Model):
    _name = "tai_lieu_phap_ly"
    _description = "Tài liệu pháp lý khách hàng"

    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", ondelete='cascade')
    
    ten_tai_lieu = fields.Char(string="Tên tài liệu", required=True, placeholder="VD: Giấy phép kinh doanh, CCCD...")
    loai_tai_lieu = fields.Selection([
        ('gpkd', 'Giấy phép kinh doanh'),
        ('cccd', 'CCCD/CMND'),
        ('mst', 'Giấy chứng nhận MST'),
        ('khac', 'Tài liệu khác')
    ], string="Loại tài liệu", default='gpkd')

    file_dinh_kem = fields.Binary(string="Bản quét (PDF/Ảnh)", required=True)
    file_name = fields.Char(string="Tên tệp")
    
    ngay_cap = fields.Date(string="Ngày cấp")
    ngay_het_han = fields.Date(string="Ngày hết hạn")
    ghi_chu = fields.Text(string="Ghi chú")