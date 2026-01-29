# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError

class QuanLyVanBan(models.Model):
    _name = "quan_ly_van_ban"
    _description = "Quản lý văn bản văn phòng"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'so_hieu'

    so_hieu = fields.Char(string="Số hiệu văn bản", required=True, copy=False, 
                         readonly=True, default=lambda self: 'Mới', tracking=True)
    ten_van_ban = fields.Char(string="Trích yếu nội dung", required=True, tracking=True)
    
    luong_van_ban = fields.Selection([
        ('den', 'Văn bản đến'),
        ('di', 'Văn bản đi'),
        ('noi_bo', 'Văn bản nội bộ')
    ], string="Loại văn bản (Luồng)", default='den', required=True)

    hinh_thuc_van_ban = fields.Selection([
        ('cong_van', 'Công văn'),
        ('to_trinh', 'Tờ trình'),
        ('quyet_dinh', 'Quyết định'),
        ('thong_bao', 'Thông báo'),
        ('bao_cao', 'Báo cáo')
    ], string="Thể loại văn bản", default='cong_van', required=True)

    # --- SỬA TẠI ĐÂY: Thêm ondelete='restrict' để bảo vệ hồ sơ số hóa ---
    nhan_vien_id = fields.Many2one('nhan_vien', string="Người soạn thảo/Liên quan", ondelete='restrict')
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng liên quan", ondelete='restrict')

    ngay_ban_hanh = fields.Date(string="Ngày ban hành", tracking=True)
    ngay_hieu_luc = fields.Date(string="Ngày hiệu lực", tracking=True)
    
    file_van_ban = fields.Binary(string="Tệp đính kèm")
    file_name = fields.Char(string="Tên tệp")

    trang_thai = fields.Selection([
        ('du_thao', 'Dự thảo'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_ky', 'Đã ký/Ban hành'),
        ('tiep_nhan', 'Tiếp nhận'),
        ('dang_xu_ly', 'Đang xử lý'),
        ('hoan_tat', 'Hoàn tất'),
        ('huy', 'Đã hủy'),
    ], string='Trạng thái', default='du_thao', tracking=True)
    ghi_chu = fields.Html(string="Nội dung chi tiết")
    # ghi_chu = fields.Text(string="Ghi chú thêm")

    # --- CÁC HÀM XỬ LÝ CHO VĂN BẢN ĐI (WORKFLOW) ---
    
    def action_confirm(self):
        """Hàm Trình duyệt: Chuyển sang chờ duyệt và CẤP MÃ NGAY"""
        for rec in self:
            # Lấy mã số hiệu từ Sequence ngay tại bước này
            seq_code = self.env['ir.sequence'].next_by_code('van_ban.code') or 'Mới'
            rec.write({
                'trang_thai': 'cho_duyet',
                'so_hieu': seq_code  # Không để 'Đang chờ duyệt...' nữa mà gán mã thật luôn
            })

    def action_done(self):
        """Hàm Ký và Ban hành: Chỉ chuyển trạng thái (Mã đã có ở bước trước)"""
        for rec in self:
            # Không gọi Sequence ở đây nữa để tránh bị nhảy 2 số hiệu cho 1 văn bản
            rec.write({
                'trang_thai': 'da_ky',
                'ngay_ban_hanh': fields.Date.today()
            })
    
    # def action_confirm(self):
    #     """Hàm Trình duyệt (Cho văn bản Đi)"""
    #     for rec in self:
    #         rec.write({
    #             'trang_thai': 'cho_duyet',
    #             'so_hieu': 'Đang chờ duyệt...'
    #         })

    # def action_done(self):
    #     """Hàm Ký và Ban hành (Cho văn bản Đi)"""
    #     for rec in self:
    #         seq_code = self.env['ir.sequence'].next_by_code('van_ban.code') or 'Mới'
    #         rec.write({
    #             'so_hieu': seq_code, 
    #             'trang_thai': 'da_ky',
    #             'ngay_ban_hanh': fields.Date.today()
    #         })

    # --- CÁC HÀM XỬ LÝ CHO VĂN BẢN ĐẾN (NEW) ---

    def action_xu_ly(self):
        """Hàm chuyển sang Đang xử lý (Cho văn bản Đến)"""
        for rec in self:
            rec.write({'trang_thai': 'dang_xu_ly'})

    def action_hoan_tat(self):
        """Hàm chuyển sang Hoàn tất và Tự động gửi thông báo nội bộ"""
        for rec in self:
            rec.write({'trang_thai': 'hoan_tat'})
            
            # Nếu là Văn bản nội bộ, hệ thống tự động gửi thông báo cho nhân viên
            if rec.luong_van_ban == 'noi_bo':
                # Tìm tất cả người dùng trong hệ thống (trừ Admin đang thao tác)
                all_users = self.env['res.users'].search([('id', '!=', self.env.user.id)])
                partner_ids = all_users.mapped('partner_id').ids
                
                if partner_ids:
                    # Tạo nội dung thông báo chuyên nghiệp
                    subject = f"🔔 THÔNG BÁO MỚI: {rec.ten_van_ban}"
                    body = f"""
                        <div style="font-family: Arial, sans-serif;">
                            <p>Chào bạn,</p>
                            <p>Công ty vừa ban hành văn bản nội bộ mới với nội dung tóm tắt như sau:</p>
                            <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #00A09D;">
                                {rec.ghi_chu}
                            </div>
                            <p style="margin-top: 15px;">Vui lòng kiểm tra chi tiết trên hệ thống Quản lý văn bản.</p>
                            <p>Trân trọng!</p>
                        </div>
                    """
                    # Gửi thông báo vào hệ thống Chatter/Messaging
                    rec.message_post(
                        body=body,
                        subject=subject,
                        partner_ids=partner_ids,
                        message_type='comment',
                        subtype_xmlid='mail.mt_comment'
                    )

    # def action_hoan_tat(self):
    #     """Hàm chuyển sang Hoàn tất (Cho văn bản Đến)"""
    #     for rec in self:
    #         rec.write({'trang_thai': 'hoan_tat'})

    def action_cancel(self):
        """Hàm Hủy bỏ"""
        self.write({'trang_thai': 'huy', 'so_hieu': 'Đã hủy'})

    # --- LOGIC TỰ ĐỘNG ---

    @api.model

    @api.model
    def create(self, vals):
        seq_code = self.env['ir.sequence'].next_by_code('van_ban.code') or 'Mới'
        
        # Ép cả văn bản ĐẾN và NỘI BỘ vào Tiếp nhận
        if vals.get('luong_van_ban') in ['den', 'noi_bo']:
            vals['trang_thai'] = 'tiep_nhan'
            vals['so_hieu'] = seq_code
        elif vals.get('luong_van_ban') == 'di':
            vals['trang_thai'] = 'du_thao'
            vals['so_hieu'] = 'Dự thảo'
            
        return super(QuanLyVanBan, self).create(vals)
    # def create(self, vals):
    #     # Lấy mã số tiếp theo từ Sequence 'van_ban.code'
    #     seq_code = self.env['ir.sequence'].next_by_code('van_ban.code') or 'Mới'

    #     if vals.get('luong_van_ban') == 'den':
    #         vals['trang_thai'] = 'tiep_nhan'
    #         # Văn bản đến: Cấp số hiệu ngay khi tạo
    #         if not vals.get('so_hieu') or vals.get('so_hieu') == 'Mới':
    #             vals['so_hieu'] = seq_code

    #     elif vals.get('luong_van_ban') == 'noi_bo':
    #         vals['trang_thai'] = 'du_thao'
    #         # Văn bản nội bộ: Cấp số hiệu ngay khi tạo
    #         if not vals.get('so_hieu') or vals.get('so_hieu') == 'Mới':
    #             vals['so_hieu'] = seq_code

    #     elif vals.get('luong_van_ban') == 'di':
    #         vals['trang_thai'] = 'du_thao'
    #         # Văn bản đi: Giữ là 'Dự thảo', sẽ cấp số ở hàm action_done
    #         if not vals.get('so_hieu') or vals.get('so_hieu') == 'Mới':
    #             vals['so_hieu'] = 'Dự thảo'
        
    #     return super(QuanLyVanBan, self).create(vals)

    def write(self, vals):
        # Tự động xóa khách hàng nếu chuyển loại thành văn bản nội bộ
        if vals.get('luong_van_ban') == 'noi_bo' or (self.luong_van_ban == 'noi_bo' and not vals.get('luong_van_ban')):
            vals['khach_hang_id'] = False
        return super(QuanLyVanBan, self).write(vals)

    def unlink(self):
        # Chặn xóa hồ sơ quan trọng
        for rec in self:
            if rec.trang_thai in ['da_ky', 'hoan_tat']:
                raise UserError(_("Không thể xóa văn bản đã ban hành hoặc đã hoàn tất để bảo vệ hồ sơ số hóa!"))
        return super(QuanLyVanBan, self).unlink()
    # def unlink(self):
    #     # TẠM THỜI MỞ KHÓA ĐỂ DỌN RÁC: 
    #     # Thầy đã comment (vô hiệu hóa) lệnh raise UserError bên dưới
    #     for rec in self:
    #         if rec.trang_thai in ['da_ky', 'hoan_tat']:
    #             # raise UserError(_("Không thể xóa văn bản đã ban hành..."))
    #             pass 
    #     return super(QuanLyVanBan, self).unlink()
