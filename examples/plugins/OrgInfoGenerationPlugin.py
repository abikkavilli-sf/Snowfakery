import random
import string
import hashlib
import os
from snowfakery.plugins import SnowfakeryPlugin
from faker import Faker

fake = Faker()

class OrgInfoGenerationPlugin(SnowfakeryPlugin):

    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.instances = self._load_instances()
        self.generated_org_ids = set()

    def _load_instances(self):
        filename = os.path.join(os.path.dirname(__file__), "instances.txt")
        with open(filename, "r") as f:
            instances = [line.strip() for line in f.readlines() if line.strip()]
        return instances

    class Functions:
        def __init__(self, plugin_instance):
            self.plugin_instance = plugin_instance

        def generate_org_id(self, context=None):
            max_attempts = 100
            base62 = string.digits + string.ascii_uppercase + string.ascii_lowercase
            for _ in range(max_attempts):
                org_suffix = ''.join(random.choices(base62, k=12))
                org_id = f"OOD{org_suffix}"
                if org_id not in self.plugin_instance.generated_org_ids:
                    self.plugin_instance.generated_org_ids.add(org_id)
                    return org_id

        def get_instance_for_org(self, org_id: str, context=None):
            h = hashlib.sha256(org_id.encode("utf-8")).hexdigest()
            instance_index = int(h[:8], 16) % len(self.plugin_instance.instances)
            return self.plugin_instance.instances[instance_index]

        def generate_org_name(self):
            return fake.company()

        def generate_org_version(self, context=None):
            latest_major_version = 258
            major = latest_major_version if random.random() < 0.9 else random.choice(range(230, latest_major_version, 2))
            minor = random.randint(0, 9)
            return f"{major}.{minor}"

        def generate_org_status(self):
            return random.choice(["Active", "Free", "Trial", "Demo"])

        def generate_org_type(self):
            return random.choice(["Production", "Sandbox"])

    def custom_functions(self):
        return self.Functions(self)