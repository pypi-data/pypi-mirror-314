from dataclasses import dataclass


@dataclass
class PolicyCondition:
    start_time: int | None = None
    end_time: int | None = None
    ip_addresses: str | None = None

    def from_dict(self, condition_data: dict):
        self.start_time = condition_data['start_time'] if 'start_time' in condition_data else None
        self.end_time = condition_data['end_time']
        self.ip_addresses = condition_data['ip_addresses'] if 'ip_addresses' in condition_data else None

    def to_dict(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "ip_addresses": self.ip_addresses
        }


@dataclass
class Policy:
    resources: str | None = None
    condition: PolicyCondition | None = None

    def from_dict(self, policy_data: dict):
        self.resources = policy_data['resources']
        self.condition = PolicyCondition()
        self.condition.from_dict(policy_data['condition'])

    def to_dict(self):
        return {
            'resources': self.resources,
            'condition': self.condition.to_dict()
        }
