import openpyxl
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class NaverEmail:
    def __init__(self, server: smtplib.SMTP_SSL, mail: str, pw: str) -> None:
        self.server = server

        self.my_mail = mail
        self.pw = pw

    def login_server(self) -> None:
        self.server.login(self.my_mail, self.pw)

    def send_email(self, mail_box: MIMEMultipart) -> None:
        self.server.sendmail(self.my_mail, self.my_mail, mail_box.as_string())

    def write_email(self) -> list[MIMEMultipart]:
        book = openpyxl.load_workbook(".temp/mail.xlsx")
        sheet = book.active

        mail_boxes = []

        for row in sheet.iter_rows(min_row=2):
            date = row[0].value
            name = row[1].value
            your_email = row[2].value
            product = row[3].value
            title = f"주문 내역은 다음과 같습니다."
            content = (
                f"""안녕하세요. {name}님, 주문 내역은 다음과 같습니다.\n"""
                f"""구매일자 : {date}\n"""
                f"""성함 : {name}\n"""
                f"""주문제품 : {product}\n"""
            )

            mail_box = MIMEMultipart()
            mail_box["From"] = self.my_mail
            mail_box["To"] = your_email
            mail_box["Subject"] = title

            msg = MIMEText(content, _charset="euc-kr")
            mail_box.attach(msg)

            mail_boxes.append(mail_box)

        return mail_boxes
