import csv
import json
import re

DEBUGGING = True
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
        # self.raw_data = json_data
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
            # KEY_CAT_CASE: r"【.*機箱.*】",
            # KEY_CAT_HEAT: r"【(.*散熱.*?)】",
            # KEY_CAT_MS: r"【(.*(?i:microsoft).*?)】",
        }

        for attribute_name, json_key in attributes_map.items():
            value = json_data.get(json_key)
            if value is None:
                print(f"Machine Setup Warning: Field named '{json_key}' not found")
            setattr(self, attribute_name, value)
        self.unknown_parts = []
        if isinstance(self.list_raw_parts, list):
            for raw_part in self.list_raw_parts:
                found = False
                for part_name, pattern in dict_part_category.items():
                    str_rmv_header = re.sub(pattern, "", raw_part, flags=re.IGNORECASE)
                    if str_rmv_header == raw_part:
                        # print("no match")
                        continue
                    # print("matched")
                    found = True
                    self.handle_part_data(part_name, str_rmv_header)
                if not found:
                    self.unknown_parts.append(raw_part)
            del self.list_raw_parts

    def handle_part_data(self, part_name, part_data_full):
        str_data = part_data_full.strip()
        dict_part_data = {
            "brand": "NA",
            "fname": "NA",
            "lname": "NA",
            "extras": "NA",
            "qty": -1,
        }
        if DEBUGGING:
            dict_part_data["raw"] = str_data

        qty, str_data = self.extract_qty(str_data)
        dict_part_data["qty"] = qty

        if part_name == KEY_CAT_CPU:
            str_data = str_data.replace("(", "_").replace(")", "_")
            list_cpu_info = str_data.split("_")
            dict_part_data["extras"] = [info for info in list_cpu_info[1:] if info]
            matching = re.match(
                r"(?P<brand>(?i:intel|amd)\s(?P<name>.*)).*\s處理器\s(?P<thread>.*?)\s",
                list_cpu_info[0],
            )
            dict_part_data["brand"] = matching.group("brand")
            dict_part_data["fname"] = matching.group("name")
            dict_part_data["lname"] = matching.group("thread")
        elif part_name == KEY_CAT_GPU:
            pattern = r"(?P<manufacturer>\b.*)\sGeForce\s(?P<gpu>RTX\s4070(?:Ti| Ti)?(?:\sSUPER)?)"
            matching = re.match(pattern, str_data, flags=re.IGNORECASE)
            dict_part_data["brand"] = matching.group("manufacturer")
            dict_part_data["fname"] = matching.group("gpu")

        elif part_name == KEY_CAT_MB:
            pattern = (
                r"\b(?P<full_name>(?P<brand>.*)\b(?P<chip>[A-Z]\d{3}[\-A-Za-z]*)\b.*)\b.*\s主機板\s\((?P<info>.*)\)"
            )
            matching = re.match(pattern, str_data, flags=re.IGNORECASE)
            dict_part_data["brand"] = matching.group("brand")
            dict_part_data["fname"] = matching.group("chip")
            dict_part_data["lname"] = matching.group("full_name")
            dict_part_data["extras"] = [matching.group("info")]

        dict_part_data = {
            key: value for key, value in dict_part_data.items() if value != "NA"
        }
        setattr(self, part_name, dict_part_data)

    def extract_qty(self, str_data):
        pattern = r"\sx\d+$"
        match_qty = re.search(pattern, str_data)
        qty = -1
        if match_qty:
            try:
                str_qty = match_qty.group()
                qty = int(str_qty[-1])
                str_data = re.sub(pattern, "", str_data)
            except IndexError as e:
                print(f"group(...) Error: {e}")
            except ValueError as e:
                print(f"ParseInt Error: {e}")
        else:
            print("Qty No match")
        return (qty, str_data)

    def to_dict(self):
        return {
            "url": self.url,
            "id": self.id,
            "title": self.title,
            "price": self.price,
        }


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
    return obj.__dict__


list_setup = list(map(mapping, list_setup))


json.dump(
    list_setup,
    open(f"{dir_target}/centralfield-v3.0.json", "w", encoding="utf8"),
    ensure_ascii=False,
    indent=4,
)
