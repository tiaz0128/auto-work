import smtplib
import pytest
import os
from dotenv import load_dotenv

from app.smtp.email import NaverEmail


class TestSendMail:
    @pytest.fixture(autouse=True)
    def setup(self):
        load_dotenv()

        self.id = os.getenv("NAVER_ID")
        self.pw = os.getenv("NAVER_PW")

        self.server = smtplib.SMTP_SSL("smtp.naver.com", 465)

    def test_send_mail(self):
        self.naver_mail = NaverEmail(self.server, self.id, self.pw)

        mail_boxes = self.naver_mail.write_email()

        self.naver_mail.login_server()

        for mail_box in mail_boxes:
            self.naver_mail.send_email(mail_box)
