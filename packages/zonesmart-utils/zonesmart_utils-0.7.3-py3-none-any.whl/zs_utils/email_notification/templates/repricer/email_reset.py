from zs_utils.email_notification.templates.repricer import base

icon = "icon_email.png"

subject_ru = "Изменение email"

title_ru = "Подтвердите изменение email адреса"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                Здравствуйте, <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Для изменения адреса электронной почты вашего аккаунта <span style='color: #3BD0BC; font-weight: bold'>Zonesmart</span>, пожалуйста, введите данный код:
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                <span style='color: #3BD0BC; font-weight: bold; font-size: 16px'>{code}</span>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Если вы не просили нас изменить email адрес, то просто проигнорируйте\nэто письмо. Ваша учетная запись в безопасности.
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru

footer_ru = """
    Это письмо было отправлено, потому что вы изменили email на <a href='https://ar.zonesmart.com' style='color: #3BD0BC; text-decoration: none'>Zonesmart</a>
"""
