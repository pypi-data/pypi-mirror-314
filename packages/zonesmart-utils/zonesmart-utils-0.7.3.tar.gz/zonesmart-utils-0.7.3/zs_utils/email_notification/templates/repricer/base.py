logo = "logo-1.png"

base_template = """
<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <style type="text/css">
            @font-face {{{{
                font-family: Trebuchet;
                font-style: normal;
                font-weight: 400;
                src: url('fonts/TrebuchetMS.woff') format('woff');
            }}}}
            .button {{{{
                text-decoration: none;
                background-color: #43D6C1;
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                padding: 8px 30px;
                border-radius: 50px;
            }}}}
        </style>
    </head>
    <body>
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;word-break:normal;word-wrap:normal;">
            <tbody>
                <tr>
                    <td align="center">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;word-break:normal;word-wrap:normal; font-family: 'Trebuchet', sans-serif;max-width:600px;width:100%">
                            <tbody>
                            <tr>
                                <td align="center" style="word-break:normal;word-wrap:normal">
                                    <table bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0" width="100%" style="box-sizing:border-box;max-width:420px;width:100%">
                                        <tbody>
                                        <tr>
                                            <td style="padding: 20px 0">
                                                <img src="{static_url}{logo}" alt="logo">
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" style="padding: 20px 0 0 0">
                                                <img src="{static_url}{email_icon}" alt="icon_email">
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" style="padding: 10px 0 30px 0">
                                                <h1 style="color: #37373C;font-family: 'Trebuchet', sans-serif;font-weight: bold;font-size: 24px;line-height: 140%; letter-spacing: 1.3px; margin-bottom: 0">
                                                    {title}
                                                </h1>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td style="font-size: 13px">
                                    {body}
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <hr color="#EAE7FF">
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="word-break:normal;word-wrap:normal">
                                    <table bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0" width="100%" style="box-sizing:border-box;width:100%; font-size: 13px; color: #888888; padding: 0 20px">
                                        <tbody>
                                        <tr>
                                            <td style="padding: 40px 0" align="left">
                                                <table>
                                                    <tbody>
                                                        {cheers}
                                                    </tbody>
                                                </table>
                                            </td>
                                            <td style="padding: 40px 0" align="right">
                                                <a href="https://t.me/zonesmart_ecom" style="text-decoration: none; margin: 0 2px">
                                                    <img src="{static_url}sn_icons/tg_icon.png" alt="telegram">
                                                </a>
                                                <a href="https://www.linkedin.com/company/zonesmart/" style="text-decoration: none; margin: 0 2px">
                                                    <img src="{static_url}sn_icons/linkedin-icon.png" alt="linkedin">
                                                </a>
                                                <a href="https://www.youtube.com/channel/UCYV_W03i-Ygoh_6-ENW-33Q" style="text-decoration: none; margin: 0 2px">
                                                    <img src="{static_url}sn_icons/youtube-icon.png" alt="youtube">
                                                </a>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2" style="padding: 20px 0 15px" align="left">
                                                <hr color="#EAE7FF">
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2" align="center" style="padding: 20px 0 50px; font-size: 10px; line-height: 132%">
                                                <div style="max-width: 300px; width: 100%">
                                                    {footer}
                                                </div>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
    </body>
</html>
"""

cheers_team_email_ru = """
    <tr>
        <td>
            Спасибо за чтение,
        </td>
    </tr>
    <tr>
        <td style="color: #3BD0BC;">
            Команда Zonesmart
        </td>
    </tr>
"""
