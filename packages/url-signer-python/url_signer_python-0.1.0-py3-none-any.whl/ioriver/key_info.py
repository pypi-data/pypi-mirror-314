from dataclasses import dataclass


@dataclass
class KeyInfo:
    cloudfront_key_id: str | None = None
    fastly_key_id: str | None = None
    akamai_key_id: str | None = None

    def from_dict(self, key_data: dict):
        self.cloudfront_key_id = key_data['cloudfront_key_id'] if 'cloudfront_key_id' in key_data else None
        self.fastly_key_id = key_data['fastly_key_id'] if 'fastly_key_id' in key_data else None
        self.akamai_key_id = key_data['akamai_key_id'] if 'akamai_key_id' in key_data else None
