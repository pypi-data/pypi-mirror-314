from zs_utils.email_notification.templates.landing import base

icon = "icon_email.png"

subject_ru = "Новая заявка zonesmart.ru"

title_ru = "Поступила новая заявка с {url}"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 14px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td>
                Время: {created_at} UTC
            </td>
        </tr>
        <tr>
            <td>
                Имя: {name}
            </td>
        </tr>
        <tr>
            <td>
                Телефон: {phone}
            </td>
        </tr>
        <tr>
            <td>
                Статус: Передано в Kokoc CRM
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
