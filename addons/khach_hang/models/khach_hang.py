# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class KhachHang(models.Model):
    _name = 'khach_hang'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Khách Hàng'
    _rec_name = 'name'

    # --- GIỮ NGUYÊN BẢN GỐC ---
    ma_khach_hang = fields.Char(string="Mã khách hàng", required=True, 
                                copy=False, default=lambda self: _('Mới'))
    name = fields.Char(string='Tên khách hàng', required=True, tracking=True)
    loai_khach = fields.Selection([
        ('tiem_nang', 'Từ Lead'),
        ('truc_tiep', 'Tạo trực tiếp')
    ], string="Loại khách hàng", default='truc_tiep')

    lich_su_ids = fields.One2many('lich_su_tuong_tac', 'khach_hang_id', string="Lịch sử tương tác")
    description = fields.Html(string="Ghi chú")
    bao_gia_ids = fields.One2many('bao_gia', 'khach_hang_id', string="Danh sách báo giá")
    tai_lieu_ids = fields.One2many('tai_lieu_phap_ly', 'khach_hang_id', string="Hồ sơ pháp lý")
    
    # 1. TÍCH HỢP LƯU TRỮ HỢP ĐỒNG (Thêm trường liên kết)
    hop_dong_ids = fields.One2many('hop_dong', 'khach_hang_id', string="Hợp đồng đã ký")

    # 2. TÍCH HỢP VĂN BẢN ĐẾN (Sửa domain để hiện cả 'hoan_tat')
    van_ban_ids = fields.One2many(
        'quan_ly_van_ban', 
        'khach_hang_id', 
        string="Văn bản liên quan",
        domain=[('trang_thai', 'in', ['da_ky', 'hoan_tat'])] 
    )

    giai_doan = fields.Selection([
        ('tiep_can', 'Tiếp cận'),
        ('ket_noi', 'Đã kết nối'),
        ('dam_phan', 'Đàm phán'),
        ('ky_hop_dong', 'Ký hợp đồng'),
        ('thanh_cong', 'Thành công'),
        ('that_bai', 'Thất bại'),
    ], string='Giai đoạn', default='tiep_can', tracking=True)

    doanh_thu_tiem_nang = fields.Float(string='Doanh thu dự kiến', tracking=True)
    ngay_nhan_lead = fields.Datetime(string="Ngày nhận lead", default=fields.Datetime.now, tracking=True)
    gender = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ'), ('khac', 'Khác')], string='Giới tính', default='nam', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Số điện thoại', tracking=True)
    address = fields.Char(string='Địa chỉ', tracking=True)
    birthday = fields.Date(string='Ngày sinh/Ngày thành lập')
    image = fields.Binary(string="Ảnh/Logo")
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên phụ trách', tracking=True)
    
    @api.model
    def create(self, vals):
        if vals.get('ma_khach_hang', _('Mới')) == _('Mới'):
            vals['ma_khach_hang'] = self.env['ir.sequence'].next_by_code('khach_hang.code') or _('Mới')
        return super(KhachHang, self).create(vals)

    # 3. TÍCH HỢP TẠO HỢP ĐỒNG KHI BẤM NÚT (Sửa hàm này)
    def action_set_contract(self):
        for rec in self:
            rec.giai_doan = 'ky_hop_dong'
            # Tự động tạo bản ghi bên bảng Hợp đồng
            self.env['hop_dong'].create({
                'ten': f"Hợp đồng kinh tế: {rec.name}",
                'khach_hang_id': rec.id,
                'gia_tri_hop_dong': rec.doanh_thu_tiem_nang,
                'ngay_bat_dau': fields.Date.today(),
                'trang_thai': 'dang_thuc_hien',
            })

    def action_set_done(self):
        self.giai_doan = 'thanh_cong'

    def action_set_fail(self):
        self.giai_doan = 'that_bai'
# # -*- coding: utf-8 -*-
# from odoo import fields, models, api, _

# class KhachHang(models.Model):
#     _name = 'khach_hang'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = 'Khách Hàng'
#     _rec_name = 'name'

#     # 1. Sửa lại mã khách hàng: Bỏ readonly ở đây để tránh lỗi khi Save trực tiếp
#     ma_khach_hang = fields.Char(string="Mã khách hàng", required=True, 
#                                 copy=False, default=lambda self: _('Mới'))
    
#     name = fields.Char(string='Tên khách hàng', required=True, tracking=True)
    
#     # Thêm trường để biết khách từ đâu tới (Option để em dễ demo)
#     loai_khach = fields.Selection([
#         ('tiem_nang', 'Từ Lead'),
#         ('truc_tiep', 'Tạo trực tiếp')
#     ], string="Loại khách hàng", default='truc_tiep')

#     # Các trường One2many giữ nguyên của em...
#     lich_su_ids = fields.One2many('lich_su_tuong_tac', 'khach_hang_id', string="Lịch sử tương tác")
#     description = fields.Html(string="Ghi chú")
#     bao_gia_ids = fields.One2many('bao_gia', 'khach_hang_id', string="Danh sách báo giá")
#     tai_lieu_ids = fields.One2many('tai_lieu_phap_ly', 'khach_hang_id', string="Hồ sơ pháp lý")
    
#     van_ban_ids = fields.One2many(
#         'quan_ly_van_ban', 
#         'khach_hang_id', 
#         string="Văn bản liên quan",
#         domain=[('trang_thai', '=', 'da_ky')]
#     )

#     giai_doan = fields.Selection([
#         ('tiep_can', 'Tiếp cận'),
#         ('ket_noi', 'Đã kết nối'),
#         ('dam_phan', 'Đàm phán'),
#         ('ky_hop_dong', 'Ký hợp đồng'),
#         ('thanh_cong', 'Thành công'),
#         ('that_bai', 'Thất bại'),
#     ], string='Giai đoạn', default='tiep_can', tracking=True)

#     # Các trường thông tin khác giữ nguyên...
#     doanh_thu_tiem_nang = fields.Float(string='Doanh thu dự kiến', tracking=True)
#     ngay_nhan_lead = fields.Datetime(string="Ngày nhận lead", default=fields.Datetime.now, tracking=True)
#     gender = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ'), ('khac', 'Khác')], string='Giới tính', default='nam', tracking=True)
#     email = fields.Char(string='Email', tracking=True)
#     phone = fields.Char(string='Số điện thoại', tracking=True)
#     address = fields.Char(string='Địa chỉ', tracking=True)
#     birthday = fields.Date(string='Ngày sinh/Ngày thành lập')
#     image = fields.Binary(string="Ảnh/Logo")
#     nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên phụ trách', tracking=True)
    
#     @api.model
#     def create(self, vals):
#         # Kiểm tra nếu đang tạo mới mà chưa có mã
#         if vals.get('ma_khach_hang', _('Mới')) == _('Mới'):
#             vals['ma_khach_hang'] = self.env['ir.sequence'].next_by_code('khach_hang.code') or _('Mới')
        
#         # LOGIC CHO KỊCH BẢN CỦA EM:
#         # Nếu nhân viên tạo trực tiếp, ta có thể tự động đẩy sang giai đoạn 'thành công' hoặc 'ký hợp đồng' luôn
#         # nếu họ điền đủ thông tin hợp đồng.
#         return super(KhachHang, self).create(vals)

#     def action_set_contract(self):
#         self.giai_doan = 'ky_hop_dong'

#     def action_set_done(self):
#         self.giai_doan = 'thanh_cong'

#     def action_set_fail(self):
#         self.giai_doan = 'that_bai'
