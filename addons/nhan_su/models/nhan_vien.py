# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Thông tin nhân viên'
    _rec_name = 'ho_va_ten'

    # Trường mã nhân viên: Mặc định là 'Mới' và để hệ thống tự cấp số
    ma_nhan_vien = fields.Char(string="Mã nhân viên", required=True, 
                               copy=False, default=lambda self: _('Mới'))
    
    ho_va_ten = fields.Char(string="Họ và tên", required=True)
    image = fields.Binary(string="Ảnh nhân viên")
    chuc_vu = fields.Char(string="Chức vụ/Vai trò") 
    so_dien_thoai = fields.Char(string="Số điện thoại")
    email = fields.Char(string="Email")
    ngay_sinh = fields.Date(string="Ngày sinh")
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ')
    ], string="Giới tính", default='nam')
    
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu làm việc", default=fields.Date.today())
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban")
    trang_thai = fields.Selection([
        ('dang_lam', 'Đang làm việc'),
        ('nghi_viec', 'Nghỉ việc')
    ], string="Trạng thái", default='dang_lam')
    
    diem_hieu_suat = fields.Float(string="Điểm hiệu suất")
    tai_khoan_id = fields.Many2one('res.users', string="Tài khoản hệ thống")
    van_ban_ids = fields.One2many('quan_ly_van_ban', 'nhan_vien_id', string="Văn bản liên quan")

    @api.model
    def create(self, vals):
        # Kiểm tra nếu mã là 'Mới' thì gọi máy phát số 'nhan_vien' đã tạo trong XML
        if vals.get('ma_nhan_vien', _('Mới')) == _('Mới'):
            vals['ma_nhan_vien'] = self.env['ir.sequence'].next_by_code('nhan_vien') or _('Mới')
        return super(NhanVien, self).create(vals)

class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Phòng ban'
    _rec_name = 'ten_phong_ban'

    # Tương tự cho phòng ban nếu em muốn tự động sinh mã PBxxxxx
    ma_phong_ban = fields.Char(string="Mã phòng ban", required=True, 
                               copy=False, default=lambda self: _('Mới'))
    ten_phong_ban = fields.Char(string="Tên phòng ban", required=True)
    truong_phong_id = fields.Many2one('nhan_vien', string="Trưởng phòng")
    mo_ta = fields.Text(string="Mô tả")

    @api.model
    def create(self, vals):
        if vals.get('ma_phong_ban', _('Mới')) == _('Mới'):
            vals['ma_phong_ban'] = self.env['ir.sequence'].next_by_code('phong_ban') or _('Mới')
        return super(PhongBan, self).create(vals)

# # -*- coding: utf-8 -*-
# from odoo import models, fields, api

# class NhanVien(models.Model):
#     _name = 'nhan_vien'
#     _description = 'Quản lý thông tin nhân viên'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _rec_name = 'ho_va_ten'
#     _order = 'ma_nhan_vien asc'

#     # --- THÔNG TIN CƠ BẢN ---
#     anh_dai_dien = fields.Binary(string='Ảnh đại diện', attachment=True)
#     ma_nhan_vien = fields.Char(string="Mã nhân viên", required=True, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('nhan_vien') or 'NV-New')
#     ho_va_ten = fields.Char(string="Họ và tên", required=True, tracking=True)
#     phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban", tracking=True)
#     chuc_vu = fields.Char(string="Chức vụ", tracking=True)
#     email = fields.Char(string="Email", tracking=True)
#     so_dien_thoai = fields.Char(string="Số điện thoại", tracking=True)
#     trang_thai = fields.Selection([
#         ('dang_lam', 'Đang làm'), 
#         ('nghi_viec', 'Nghỉ việc')
#     ], string="Trạng thái", default='dang_lam', tracking=True, required=True)
#     tai_khoan_id = fields.Many2one('res.users', string="Tài khoản hệ thống", tracking=True)

#     # --- LIÊN KẾT DỮ LIỆU ---
#     # PHẢI MỞ DÒNG NÀY THÌ HÀM COMPUTE MỚI CHẠY ĐƯỢC
#     ho_so_ids = fields.One2many('ho_so', 'nhan_vien_id', string="Danh sách Hồ sơ đã lập")

#     # --- PHẦN TÍNH TOÁN DASHBOARD ---
#     diem_hieu_suat = fields.Float(
#         string="Hiệu suất (%)", 
#         compute='_compute_diem_hieu_suat',
#         store=True # Lưu vào database để API React lấy dữ liệu
#     )

#     @api.depends('ho_so_ids')
#     def _compute_diem_hieu_suat(self):
#         for record in self:
#             # Kiểm tra an toàn để không bị lỗi KeyError hay AttributeError
#             so_luong_ho_so = len(record.ho_so_ids) if record.ho_so_ids else 0
#             # Công thức tính hiệu suất: Mỗi hồ sơ hoàn thành được 20%
#             record.diem_hieu_suat = min(so_luong_ho_so * 20, 100)
    
#     # --- CÁC HÀM XỬ LÝ TRẠNG THÁI ---
#     def action_set_nghi_viec(self):
#         for record in self:
#             record.trang_thai = 'nghi_viec'

#     def action_set_dang_lam(self):
#         for record in self:
#             record.trang_thai = 'dang_lam'

#     _sql_constraints = [
#         ('ma_nhan_vien_unique', 'unique(ma_nhan_vien)', 'Mã nhân viên này đã tồn tại!'),
#         ('email_unique', 'unique(email)', 'Email này đã được sử dụng!')
#     ]