from dataclasses import dataclass


@dataclass
class Header:
    api_key: str
    api_secret: str
    created_by: str
    reason: str = None
    comment: str = None

    def dict(self):
        return {
            "X-Killbill-ApiKey": self.api_key,
            "X-Killbill-ApiSecret": self.api_secret,
            "X-Killbill-CreatedBy": self.created_by,
            "X-Killbill-Reason": self.reason,
            "X-Killbill-Comment": self.comment,
        }
