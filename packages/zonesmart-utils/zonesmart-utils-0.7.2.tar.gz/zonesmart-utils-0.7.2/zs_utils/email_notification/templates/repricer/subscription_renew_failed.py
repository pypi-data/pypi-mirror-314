from zs_utils.email_notification.templates.repricer import base

icon = "payment_remind_icon.png"

title_ru = "Ошибка при продлении подписки"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                При продлении подписки произошла ошибка. В связи с этим синхронизация с маркетплейсами будет отключена.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{dashboard_url}" class="button" style="color: #ffffff">
                    Перейти в Zonesmart
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
