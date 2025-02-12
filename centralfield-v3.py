import csv
import json
import re

KEY_CAT_CPU = "cpu"
KEY_CAT_MB = "motherboard"
KEY_CAT_RAM = "ram"
KEY_CAT_GPU = "gpu"
KEY_CAT_SSD = "ssd"
KEY_CAT_POWER = "power"
KEY_CAT_CASE = "case"
KEY_CAT_HEAT = "heat"
KEY_CAT_MS = "microsoft"

class MachineSetup:
    
    def __init__(self, json_data):
        self.raw_data = json_data
        attributes_map = {
            "url": "url",
            "title": "pc_title",
            "id": "id",
            "price": "price",
            "list_raw_parts": "pc_parts",
        }
        dict_part_category = {
            KEY_CAT_CPU: r"【(.*CPU.*?)】",
            KEY_CAT_MB: r"【(.*主機板.*?)】",
            KEY_CAT_RAM: r"【(.*(?i:RAM).*?)】",
            KEY_CAT_GPU: r"【(.*顯示卡.*?)】",
            KEY_CAT_SSD: r"【(.*(?i:SSD).*?)】",
            KEY_CAT_POWER: r"【.*火牛.*】",
            KEY_CAT_CASE: r"【.*機箱.*】",
            KEY_CAT_HEAT: r"【(.*散熱.*?)】",
            KEY_CAT_MS: r"【(.*(?i:microsoft).*?)】",
        }

        for attribute_name, json_key in attributes_map.items():
            value = json_data.get(json_key)
            if value is None:
                print(f"Machine Setup Warning: Field named '{json_key}' not found")
            setattr(self, attribute_name, value)
        self.unknown_parts = []
        if isinstance(self.list_raw_parts, list):
            for raw_part in self.list_raw_parts:
                for part_name, pattern in dict_part_category.items():
                    str_rmv_header = re.sub(pattern, "", raw_part, flags=re.IGNORECASE)
                    if str_rmv_header == raw_part:
                        # print("no match")
                        self.unknown_parts.append(raw_part)
                        continue
                    # print("matched")
                    self.handle_part_data(part_name, str_rmv_header)
    def handle_part_data(self, part_name, part_data_full):
        part_data_full = part_data_full.strip()
        qty = int(re.match(r".*x(\d+)$", part_data_full).group(1))
        print(part_data_full, qty-1)
        setattr(self, part_name, {})
        pass
    def to_dict(self):
        return {
            "url": self.url,
            "id": self.id,
            "title": self.title,
            "price": self.price,
        }




class PartType:
    def __init__(self, part_type, pattern):
        self.type = part_type
        self.pattern = pattern
        self.qty = -1
        self.brand = ""
        self.raw_data = ""
        self.product_name = ""
        self.product_label = ""
        self.extra_info = []

    def to_dict(self):
        return {
            "brand": self.brand,
            "product_label": self.product_label,
            "product_name": self.product_name,
            "extra_info": self.extra_info,
            "raw_data": self.raw_data,
            "qty": self.qty,
        }

    def process_raw_data(self, str_raw_data):

        pass


dir_target = "."

json_files = [
    f"{dir_target}/centralfield-v1.1.json",
    f"{dir_target}/centralfield-v1.2.json",
]
json1 = json.load(open(json_files[0], "r", encoding="utf-8"))
json2 = json.load(open(json_files[1], "r", encoding="utf-8"))

json_data = json1 + json2


list_setup = []

for idx, data in enumerate(json_data):
    list_setup.append(MachineSetup(data))
    if idx == 1:
        break


def mapping(obj):
    return obj.to_dict()


list_setup = list(map(mapping, list_setup))


json.dump(
    list_setup,
    open(f"{dir_target}/centralfield-v3.0.json", "w", encoding="utf8"),
    ensure_ascii=False,
    indent=4,
)
