# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class KhachHangTiemNang(models.Model):
    _name = 'khach_hang_tiem_nang'
    # Kế thừa để có phần thảo luận (Chatter) và lịch hẹn (Activities)
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Khách hàng tiềm năng'

    # --- THÔNG TIN CƠ BẢN ---
    ma_lead = fields.Char(string="Mã lead", readonly=True, default=lambda self: _('Mới'))
    name = fields.Char(string="Tên lead", required=True, tracking=True)
    dien_thoai = fields.Char(string="Điện thoại", tracking=True)
    email = fields.Char(string="Email", tracking=True)
    ngay_sinh = fields.Date(string="Ngày sinh")
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ')
    ], string="Giới tính", default='nam', tracking=True)
    ngay_nhan_lead = fields.Datetime(string="Ngày nhận lead", default=fields.Datetime.now)
    
    # --- CÁC TRƯỜNG NGHIỆP VỤ CRM ---
    # Thầy giữ nguyên bộ giai đoạn em đã chọn để khớp với thanh statusbar trên giao diện
    giai_doan = fields.Selection([
        ('1', 'Tiếp cận'),
        ('1.5', 'Đã kết nối'),
        ('2', 'Đàm phán'),
        ('3', 'Ký hợp đồng'),
        ('4', 'Thất bại'),
    ], string='Giai đoạn', required=True, default='1', tracking=True)
    
    do_uu_tien = fields.Selection([
        ('0', 'Thấp'),
        ('1', 'Trung bình'),
        ('2', 'Cao'),
        ('3', 'Rất cao'),
    ], string='Độ ưu tiên', default='1')
    doanh_thu_tiem_nang = fields.Float(string='Doanh thu dự kiến', tracking=True)

    # --- LIÊN KẾT MODULE NHÂN SỰ ---
    # Thầy đã mở lại trường này vì module nhan_su của em đã ổn định
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên phụ trách", tracking=True)

    # --- XỬ LÝ TỰ ĐỘNG ---

    # 1. Hàm tự sinh mã Lead
    @api.model
    def create(self, vals):
        if vals.get('ma_lead', _('Mới')) == _('Mới'):
            # Lấy mã từ Sequence đã định nghĩa trong data/sequence.xml
            vals['ma_lead'] = self.env['ir.sequence'].next_by_code('khach_hang_tiem_nang.code') or _('Mới')
        return super(KhachHangTiemNang, self).create(vals)

    # 2. Nút bấm chuyển giai đoạn sang Ký hợp đồng
    def action_confirm_contract(self):
        for rec in self:
            rec.write({'giai_doan': '3'})
            rec.message_post(body=_("Hệ thống: Đã chốt hợp đồng. Khách hàng đã được thêm vào danh sách chính thức."))
        return True

    # 3. Tự động tạo Khách hàng chính thức khi giai đoạn chuyển thành '3' (Ký hợp đồng)
    def write(self, vals):
        res = super(KhachHangTiemNang, self).write(vals)
        # Nếu giai đoạn được chuyển thành '3' (Ký hợp đồng)
        if 'giai_doan' in vals and vals.get('giai_doan') == '3':
            for rec in self:
                # Kiểm tra trùng lặp qua Điện thoại hoặc Email
                domain = []
                if rec.dien_thoai:
                    domain.append(('phone', '=', rec.dien_thoai))
                if rec.email:
                    if domain: domain.insert(0, '|')
                    domain.append(('email', '=', rec.email))

                existing_customer = False
                if domain:
                    existing_customer = self.env['khach_hang'].search(domain, limit=1)
                
                # Nếu chưa tồn tại, tự động tạo mới bên bảng khach_hang
                if not existing_customer:
                    self.env['khach_hang'].create({
                        'name': rec.name,
                        'phone': rec.dien_thoai,
                        'email': rec.email,
                        'nhan_vien_id': rec.nhan_vien_id.id, # Thầy thêm dòng này để đồng bộ nhân viên phụ trách sang bảng chính thức
                        'address': 'Chuyển từ Lead: ' + (rec.ma_lead or ''),
                    })
        return res
# # -*- coding: utf-8 -*-
# from odoo import fields, models, api, _

# class KhachHangTiemNang(models.Model):
#     _name = 'khach_hang_tiem_nang'
#     # Kế thừa để có phần thảo luận (Chatter) và lịch hẹn (Activities)
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = 'Khách hàng tiềm năng'

#     # --- THÔNG TIN CƠ BẢN ---
#     ma_lead = fields.Char(string="Mã lead", readonly=True, default=lambda self: _('Mới'))
#     name = fields.Char(string="Tên lead", required=True, tracking=True)
#     dien_thoai = fields.Char(string="Điện thoại", tracking=True)
#     email = fields.Char(string="Email", tracking=True)
#     ngay_sinh = fields.Date(string="Ngày sinh")
#     gioi_tinh = fields.Selection([
#         ('nam', 'Nam'),
#         ('nu', 'Nữ')
#     ], string="Giới tính", default='nam', tracking=True)
#     ngay_nhan_lead = fields.Datetime(string="Ngày nhận lead", default=fields.Datetime.now)
    
#     # --- CÁC TRƯỜNG NGHIỆP VỤ CRM ---
#     giai_doan = fields.Selection([
#         ('1', 'Tiếp cận'),
#         ('1.5', 'Đã kết nối'),
#         ('2', 'Đàm phán'),
#         ('3', 'Ký hợp đồng'),
#         ('4', 'Thất bại'),
#     ], string='Giai đoạn', required=True, default='1', tracking=True)
#     do_uu_tien = fields.Selection([
#         ('0', 'Thấp'),
#         ('1', 'Trung bình'),
#         ('2', 'Cao'),
#         ('3', 'Rất cao'),
#     ], string='Độ ưu tiên', default='1')
#     doanh_thu_tiem_nang = fields.Float(string='Doanh thu dự kiến', tracking=True)

#     # --- TẠM ĐÓNG LIÊN KẾT NGOẠI ĐỂ TRÁNH LỖI SẬP REGISTRY ---
#     # Khi nào em cài module Nhan Su và Van Ban thì mình sẽ mở ra sau
#     nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên phụ trách", tracking=True)
#     # ho_so_ids = fields.One2many('ho_so', 'khach_hang_id', string='Tài liệu')

#     # --- XỬ LÝ TỰ ĐỘNG ---

#     # 1. Hàm tự sinh mã Lead
#     @api.model
#     def create(self, vals):
#         if vals.get('ma_lead', _('Mới')) == _('Mới'):
#             vals['ma_lead'] = self.env['ir.sequence'].next_by_code('khach_hang_tiem_nang.code') or _('Mới')
#         return super(KhachHangTiemNang, self).create(vals)

#     # 2. Nút bấm chuyển giai đoạn sang Ký hợp đồng
#     def action_confirm_contract(self):
#         for rec in self:
#             rec.write({'giai_doan': '3'})
#             rec.message_post(body=_("Hệ thống: Đã chốt hợp đồng. Khách hàng đã được thêm vào danh sách chính thức."))
#         return True

#     # 3. Tự động tạo Khách hàng chính thức khi giai đoạn chuyển thành '3' (Ký hợp đồng)
#     def write(self, vals):
#         res = super(KhachHangTiemNang, self).write(vals)
#         if 'giai_doan' in vals and vals.get('giai_doan') == '3':
#             for rec in self:
#                 # Tìm xem khách hàng đã tồn tại chưa dựa trên Email hoặc Số điện thoại
#                 domain = []
#                 if rec.dien_thoai:
#                     domain.append(('phone', '=', rec.dien_thoai))
#                 if rec.email:
#                     if domain: domain.insert(0, '|')
#                     domain.append(('email', '=', rec.email))

#                 existing_customer = False
#                 if domain:
#                     existing_customer = self.env['khach_hang'].search(domain, limit=1)
                
#                 # Nếu chưa có thì tự động tạo mới bên bảng khach_hang
#                 if not existing_customer:
#                     self.env['khach_hang'].create({
#                         'name': rec.name,
#                         'phone': rec.dien_thoai,
#                         'email': rec.email,
#                         'address': 'Chưa xác định', # Em có thể bổ sung trường address vào Lead nếu muốn
#                     })
#         return res