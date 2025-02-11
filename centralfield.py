import csv
import json
import re


class PartType:
    def __init__(self, part_type, pattern):
        self.type = part_type
        self.pattern = pattern
        self.qty = -1
        self.brand = ""
        self.name = ""
        self.extra = []
        self.full_name = ""


dict_patterns = {
    "cpu": r"【(.*CPU.*?)】",
    "motherboard": r"【(.*主機板.*?)】",
    "ram": r"【(.*(?i:RAM).*?)】",
    "gpu": r"【(.*顯示卡.*?)】",
    "heat": r"【(.*散熱.*?)】",
    "ssd": r"【(.*(?i:SSD).*?)】",
    "power": r"【.*火牛.*】",
    "case": r"【.*機箱.*】",
    "microsoft": r"【(.*(?i:microsoft).*?)】",
}

json_files = ["PC-specs/centralfield-v1.1.json", "PC-specs/centralfield-v1.2.json"]
json1 = json.load(open(json_files[0], "r", encoding="utf-8"))
json2 = json.load(open(json_files[1], "r", encoding="utf-8"))

json_data = json1 + json2
for idx, data in enumerate(json_data):
    list_parts = data["pc_parts"]
    for str_part in list_parts:
        for part_name, pattern in dict_patterns.items():
            regex_result = re.sub(pattern, "", str_part, flags=re.IGNORECASE)
            if regex_result == str_part:
                # print("no match")
                continue
            # print("matched")
            if (
                part_name not in json_data[idx]
            ):  # or not isinstance(json_data[idx][part_name], str):
                json_data[idx][part_name] = ""
            else:
                json_data[idx][part_name] += " ; "
            json_data[idx][part_name] += regex_result
json.dump(
    json_data,
    open("PC-specs/centralfield-v2.0.json", "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=4,
)
pattern_qty_at_end = r"\sx\d$"
for idx in range(0, len(json_data)):
    del json_data[idx]["pc_parts"]
    del json_data[idx]["url"]
    for part_name in json_data[idx]:
        # remove qty at the end of the string
        if not isinstance(json_data[idx][part_name], str):
            continue
        str_modified = re.sub(
            pattern_qty_at_end, "", json_data[idx][part_name], flags=re.IGNORECASE
        )
        if part_name == "cpu":
            str_modified = str_modified.split("處理器")[0]
        # if part_name == "motherboard":
        #     matches = re.match(r"([A-Z]\d{3}.*)(\s)",str_modified)
        #     str_modified = str_modified.split("處理器")[0]
        # 
        json_data[idx][part_name] = str_modified
json.dump(
    json_data,
    open("PC-specs/centralfield-v2.1.json", "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=4,
)


# now we will open a file for writing
data_file = open("PC-specs/centralfield-v2.1.csv", "w",encoding='utf-8')

# create the csv writer object
csv_writer = csv.writer(data_file)

# Counter variable used for writing
# headers to the CSV file
count = 0

for data in json_data:
    if count == 0:

        # Writing headers of CSV file
        header = data.keys()
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow(data.values())

data_file.close()
