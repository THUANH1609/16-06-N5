# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class BaoGia(models.Model):
    _name = "bao_gia"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Báo giá khách hàng"
    _rec_name = 'so_bao_gia'

    so_bao_gia = fields.Char(
        string="Số báo giá",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: 'Mới'
    )
    khach_hang_id = fields.Many2one(
        'khach_hang',
        string="Khách hàng",
        ondelete='cascade'
    )
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Người lập báo giá"
    )

    ngay_lap = fields.Date(
        string="Ngày lập",
        default=fields.Date.today
    )
    ngay_het_han = fields.Date(string="Ngày hết hạn")

    tong_tien = fields.Float(
        string="Tổng giá trị (VNĐ)",
        required=True
    )

    trang_thai = fields.Selection([
        ('du_thao', 'Dự thảo'),
        ('da_gui', 'Đã gửi khách'),
        ('chap_nhan', 'Chấp nhận'),
        ('tu_choi', 'Từ chối'),
    ], string='Trạng thái', default='du_thao', tracking=True)

    ghi_chu = fields.Text(string="Điều khoản thương mại")

    @api.model
    def create(self, vals):
        if vals.get('so_bao_gia', 'Mới') == 'Mới':
            vals['so_bao_gia'] = self.env['ir.sequence'].next_by_code('bao_gia.code') or 'Mới'
        return super(BaoGia, self).create(vals)

    def action_gui_mail_bao_gia(self):
        self.ensure_one()

        if not self.khach_hang_id.email:
            raise UserError("Khách hàng chưa có địa chỉ Email!")

        subject = f"THÔNG TIN BÁO GIÁ: {self.so_bao_gia}"

        body_html = f"""
            <div style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; line-height: 1.6;">
                <p>Chào chị <b>{self.khach_hang_id.name}</b>,</p>

                <p>Công ty <b>AAHK</b> xin gửi tới anh/chị thông tin chi tiết báo giá dịch vụ:</p>

                <div style="background: #fff5f5; padding: 20px;
                            border-left: 5px solid #e74c3c;
                            margin: 15px 0; border-radius: 4px;">
                    <h3 style="margin-top: 0; color: #e74c3c;">
                        CHI TIẾT BÁO GIÁ
                    </h3>
                    <ul style="list-style: none; padding: 0;">
                        <li><b>Mã báo giá:</b> {self.so_bao_gia}</li>
                        <li>
                            <b>Tổng giá trị:</b>
                            <span style="font-size: 18px; color: #e74c3c; font-weight: bold;">
                                {self.tong_tien:,.0f} VNĐ
                            </span>
                        </li>
                        <li><b>Ngày lập:</b>
                            {self.ngay_lap.strftime('%d/%m/%Y') if self.ngay_lap else ''}
                        </li>
                    </ul>
                </div>

                <p>
                    Báo giá có hiệu lực trong vòng <b>15 ngày</b>.
                    Chị vui lòng kiểm tra và phản hồi sớm giúp công ty.
                </p>

                <p>Trân trọng,</p>

                <p>
                    <b>
                        {self.nhan_vien_id.ho_va_ten if self.nhan_vien_id else 'CÔNG TY AAHK'}
                    </b><br/>
                    Phòng Kinh doanh
                </p>
            </div>
        """

        # 🔥 CHỖ QUAN TRỌNG NHẤT – FIX NGƯỜI GỬI
        mail_values = {
            'subject': subject,
            'body_html': body_html,
            'email_to': self.khach_hang_id.email,

            # 👇 TÊN HIỂN THỊ + EMAIL GỬI
            'email_from': 'AAHK CSKH <khanhhuyen8324@gmail.com>',
            'reply_to': 'AAHK CSKH <khanhhuyen8324@gmail.com>',
        }

        mail = self.env['mail.mail'].sudo().create(mail_values)
        mail.send()

        self.trang_thai = 'da_gui'
        self.message_post(
            body=f"Hệ thống AAHK CSKH đã gửi báo giá cho khách hàng {self.khach_hang_id.name}"
        )

        return True

# # -*- coding: utf-8 -*-
# from odoo import fields, models, api, _
# from odoo.exceptions import UserError

# class BaoGia(models.Model):
#     _name = "bao_gia"
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = "Báo giá khách hàng"
#     _rec_name = 'so_bao_gia'

#     so_bao_gia = fields.Char(string="Số báo giá", required=True, copy=False, readonly=True, 
#                              default=lambda self: 'Mới')
#     khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", ondelete='cascade')
#     nhan_vien_id = fields.Many2one('nhan_vien', string="Người lập báo giá")
    
#     ngay_lap = fields.Date(string="Ngày lập", default=fields.Date.today)
#     ngay_het_han = fields.Date(string="Ngày hết hạn")
    
#     tong_tien = fields.Float(string="Tổng giá trị (VNĐ)", required=True)
    
#     trang_thai = fields.Selection([
#         ('du_thao', 'Dự thảo'),
#         ('da_gui', 'Đã gửi khách'),
#         ('chap_nhan', 'Chấp nhận'),
#         ('tu_choi', 'Từ chối'),
#     ], string='Trạng thái', default='du_thao', tracking=True)

#     ghi_chu = fields.Text(string="Điều khoản thương mại")

#     @api.model
#     def create(self, vals):
#         if vals.get('so_bao_gia', 'Mới') == 'Mới':
#             vals['so_bao_gia'] = self.env['ir.sequence'].next_by_code('bao_gia.code') or 'Mới'
#         return super(BaoGia, self).create(vals)

#     def action_gui_mail_bao_gia(self):
#         self.ensure_one()
#         if not self.khach_hang_id.email:
#             from odoo.exceptions import UserError
#             raise UserError("Khách hàng chưa có địa chỉ Email!")

#         # THIẾT KẾ GIAO DIỆN CHUYÊN NGHIỆP ĐỒNG BỘ VỚI HỢP ĐỒNG
#         subject = f"THÔNG TIN BÁO GIÁ: {self.so_bao_gia}"
#         body_html = f"""
#             <div style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; line-height: 1.6;">
#                 <p>Chào chị <b>{self.khach_hang_id.name}</b>,</p>
#                 <p>Công ty AAHK xin gửi tới chị thông tin chi tiết báo giá dịch vụ:</p>
                
#                 <div style="background: #fff5f5; padding: 20px; border-left: 5px solid #e74c3c; margin: 15px 0; border-radius: 4px;">
#                     <h3 style="margin-top: 0; color: #e74c3c;">CHI TIẾT BÁO GIÁ</h3>
#                     <ul style="list-style: none; padding: 0;">
#                         <li style="margin-bottom: 8px;"><b>Mã báo giá:</b> {self.so_bao_gia}</li>
#                         <li style="margin-bottom: 8px;"><b>Tổng giá trị:</b> <span style="font-size: 18px; color: #e74c3c; font-weight: bold;">{self.tong_tien:,.0f} VNĐ</span></li>
#                         <li style="margin-bottom: 8px;"><b>Ngày lập:</b> {self.ngay_lap.strftime('%d/%m/%Y') if self.ngay_lap else ''}</li>
#                     </ul>
#                 </div>
                
#                 <p>Báo giá này có hiệu lực trong vòng 15 ngày. Chị vui lòng kiểm tra và phản hồi sớm.</p>
                
#                <p>Trân trọng,</p>
#                 <p><b>{self.nhan_vien_id.ho_va_ten or 'Ban Quản trị Gemini'}</b></p>
#                 </div>
#             </div>
#         """

#         mail_values = {
#             'subject': subject,
#             'body_html': body_html,
#             'email_to': self.khach_hang_id.email,
#             'email_from': self.env.user.email,
#         }
        
#         # TẠO VÀ GỬI MAIL (ĐÃ SỬA LỖI Ở ĐÂY)
#         mail = self.env['mail.mail'].sudo().create(mail_values)
#         # Bỏ force_send vì nó gây lỗi TypeError
#         mail.send() 
        
#         # Cập nhật trạng thái
#         self.trang_thai = 'da_gui'
#         self.message_post(body=f"Hệ thống Admin đã gửi báo giá chuyên nghiệp cho {self.khach_hang_id.name}")
#         return True
