"""
发送邮件
"""
# https://stackoverflow.com/questions/882712/sending-html-email-using-python
# pylint: disable=E0611
# pylint: disable=R0911
# pylint: disable=R0912
# pylint: disable=R0913
# pylint: disable=R0914
# pylint: disable=R0915
# pylint: disable=R1710
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
from typing import Optional, TypedDict, cast

from loguru import logger

from . import utils


class TypedSMTP(TypedDict):
    """smtp type"""
    server: str
    port: int
    tls: bool

class TypedSender(TypedDict):
    """sender type"""
    name: str
    address: str
    password: str

class TypedBody(TypedDict, total=False):
    """body type"""
    content: str
    type: Optional[str]

def format_parse(s):
    _name, _addr = parseaddr(s)
    return formataddr((Header(_name, "utf-8").encode(), _addr))

def sendemail(
    smtp: TypedSMTP,
    sender: TypedSender,
    recipients: str | list,
    subject: str,
    body: TypedBody,
    images: None | list = None
) -> bool:
    """
    smtp SMTP信息

        server  SMTP地址
        port    SMTP端口
        tls     是否使用TLS

    sender 发件人信息

        name     发件人名称
        address  发件人邮箱地址
        password 发件人邮箱密码(SMTP)

    recipients  收件人(或列表)

    subject     邮件主题

    body        邮件主体

        content 内容
        type    类型 (默认 plain, 或者 file, 或者 html)

    images 图片列表(可选)

        cid  图片CID
        path 图片路径
    """

    # 参数判断
    # match True:
    #     case True if utils.vTrue(smtp, dict) == False:
    #         logger.error('ERROR!! {} is not dictionary or none'.format('smtp'))
    #         return False
    #     case True if utils.vTrue(sender, dict) == False:
    #         logger.error('ERROR!! {} is not dictionary or none'.format('sender'))
    #         return False
    #     case True if (utils.vTrue(recipients, str) == False) and (utils.vTrue(recipients, list) == False):
    #         logger.error('ERROR!! {} is not list or none'.format('recipients'))
    #         return False
    #     case True if utils.vTrue(subject, str) == False:
    #         logger.error('ERROR!! {} is not string or none'.format('subject'))
    #         return False
    #     case True if utils.vTrue(html_file, str) == False:
    #         logger.error('ERROR!! {} is not string or none'.format('html_file'))
    #         return False

    logger.success("sendemail start")

    try:

        # 邮件主体

        if utils.v_true(body, dict) is False:
            logger.error("body error")
            return False

        message: MIMEMultipart = MIMEMultipart()

        body_content = cast(str, body.get("content"))

        if utils.v_true(body_content, str) is False:
            logger.error(f"body content error: {body_content}")
            return False

        body_type = cast(str, body.get("type"))

        # 从文本文件读取内容
        if body_type == "file":
            with open(body_content, "r", encoding="utf-8") as file:
                message.attach(MIMEText(file.read(), "plain", "utf-8"))

        # 从HTML文件读取内容
        elif body_type == "html":
            message = MIMEMultipart("related")
            with open(body_content, "r", encoding="utf-8") as file:
                message.attach(MIMEText(file.read(), "html", "utf-8"))

        # 纯文本内容
        else:
            message.attach(MIMEText(body_content, "plain", "utf-8"))

        # ------------------------------------------------------------------------------------------

        # SMTP

        if utils.v_true(smtp, dict) is False:
            logger.error("smtp error")
            return False

        smtp_host = cast(str, smtp.get("server"))
        smtp_port = cast(int, smtp.get("port"))
        smtp_tls = cast(bool, smtp.get("tls"))

        if utils.v_true(smtp_host, str) is False:
            logger.error(f"smtp host error: {smtp_host}")
            return False

        if utils.v_true(smtp_port, int) is False:
            logger.error(f"smtp port error: {smtp_port}")
            return False

        smtp_tls = utils.v_true(smtp_tls, bool)

        # ------------------------------------------------------------------------------------------

        # 发件人信息

        if utils.v_true(sender, dict) is False:
            logger.error("sender error")
            return False

        sender_name = cast(str, sender.get("name"))
        sender_address = cast(str, sender.get("address"))
        sender_password = cast(str, sender.get("password"))

        if utils.v_true(sender_name, str) is False:
            logger.error(f"sender name error: {sender_name}")
            return False

        if utils.v_true(sender_address, str) is False:
            logger.error(f"sender address error: {sender_address}")
            return False

        if utils.v_true(sender_password, str) is False:
            logger.error(f"sender password error: {sender_password}")
            return False

        message["From"] = formataddr((sender_name, sender_address))

        # ------------------------------------------------------------------------------------------

        # 收件人(或列表)

        if utils.v_true(recipients, str):
            message["To"] = format_parse(recipients)
        elif utils.v_true(recipients, list):
            message["To"] = ", ".join(list(map(format_parse, recipients)))
        else:
            logger.error("recipients error")
            return False

        # ------------------------------------------------------------------------------------------

        # 邮件主题

        if utils.v_true(subject, str) is False:
            logger.error("subject error")
            return False

        message["Subject"] = subject

        # ------------------------------------------------------------------------------------------

        if images is not None and utils.v_true(images, list):

            for image in images:

                try:

                    if utils.check_file_type(image.get("path", ""), "file"):

                        # 添加图片
                        # with open(image_path, "rb") as image_file:
                        #     mime_image = MIMEImage(image_file.read())
                        #     # Define the image's ID as referenced above
                        #     mime_image.add_header("Content-ID", "<CID>")
                        #     message.attach(mime_image)

                        with open(image["path"], "rb") as _image_file:
                            mime_image = MIMEImage(_image_file.read())
                            mime_image.add_header("Content-ID", f"<{image['cid']}>")
                            message.attach(mime_image)

                except Exception as e:
                    logger.exception(e)
                    return False

        # ------------------------------------------------------------------------------------------

        # 发送邮件

        # SMTP.sendmail(from_addr, to_addrs, msg, mail_options=(), rcpt_options=())
        #
        #     to_addrs = sender_to + sender_cc
        #     https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.sendmail
        #     https://gist.github.com/AO8/c5a6f747eeeca02351152ae8dc79b537

        # if smtp.get('ssl', False) is True:

        #     with smtplib.SMTP_SSL(smtp_host, smtp_port) as _smtp:
        #         _smtp.login(sender_address, sender_password)
        #         _smtp.sendmail(sender_address, recipients, _message.as_string())

        # else:

        with smtplib.SMTP(smtp_host, smtp_port) as smtp_server:
            if smtp_tls is True:
                smtp_server.starttls()
            smtp_server.login(sender_address, sender_password)
            smtp_server.sendmail(sender_address, recipients, message.as_string())

            logger.success("sendemail success")

            return True

    except Exception as e:

        # 忽略腾讯邮箱返回的异常
        if e.args == (-1, b'\x00\x00\x00'):
            # pass
            return True

        logger.error('sendemail error')
        logger.exception(e)
        return False
