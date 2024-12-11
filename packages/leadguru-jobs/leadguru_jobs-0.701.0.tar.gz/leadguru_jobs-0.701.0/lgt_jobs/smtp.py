from abc import ABC
from pydantic import BaseModel
import logging as log
from lgt_jobs.basejobs import BaseBackgroundJobData, BaseBackgroundJob
from lgt_jobs.env import smtp_login, smtp_password
from lgt_jobs.lgt_data.enums import ImageName

"""
Send email
"""


class SendMailJobData(BaseBackgroundJobData, BaseModel):
    html: str
    subject: str
    recipient: str
    sender: str = "noreply@leadguru.io"
    images: list[ImageName] = []


class SendMailJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return SendMailJobData

    def exec(self, data: SendMailJobData):
        from redmail import gmail
        gmail.username = smtp_login
        gmail.password = smtp_password
        body_image = {}
        for image in data.images:
            body_image[f'IMAGE_{ImageName(image.value).name}'] = f'lgt_jobs/assets/images/{image.value}'

        gmail.send(
            sender=f"Leadguru <{data.sender}>",
            receivers=[data.recipient],
            subject=data.subject,
            html=data.html,
            body_images=body_image
        )
        log.info('email message has been sent')
