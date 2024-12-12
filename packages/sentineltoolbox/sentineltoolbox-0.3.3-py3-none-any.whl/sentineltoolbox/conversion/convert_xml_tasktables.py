# type: ignore
import copy
import importlib.resources
import json
import sys
import xml.etree.ElementTree as ET

from sentineltoolbox.resources.data import DATAFILE_METADATA

global_param = [
    "processor_name",
    # 'version',
    # 'min_disk_space',
    # 'max_time'
]


def convert_tt(tasktable: str, version: str = "", baseline_collection: str = "") -> str:
    # namespaces = {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}
    tree = ET.parse(tasktable)
    root = tree.getroot()

    new_tt = {}
    new_tt["version"] = version
    new_tt["baseline_collection"] = baseline_collection

    # Global parameters
    for child in root:
        tag = child.tag.lower()
        if tag in global_param:
            new_tt[child.tag.lower()] = child.text

    duplicate_adf = None
    for t in root.find("List_of_Pools/Pool/List_of_Tasks/Task"):
        if t.tag != "List_of_Inputs":
            continue
        new_tt["list_of_inputs"] = []
        for input in t.findall("Input"):
            in_item = {}
            for child in input:
                if child.tag == "List_of_Alternatives":
                    in_item["Alternatives"] = []
                    for adf in child.findall("Alternative"):
                        attrs = {}
                        for attr in adf:
                            if attr.tag == "File_Type":
                                adf_type = attr.text
                                adf_type = DATAFILE_METADATA.to_dpr_ptype(adf_type)
                                if isinstance(adf_type, list):
                                    duplicate_adf = adf_type
                                    attrs["File_Type"] = adf_type[0]
                                else:
                                    attrs["File_Type"] = adf_type
                            attrs[attr.tag] = attr.text

                        in_item["Alternatives"].append(attrs)
                else:
                    in_item[child.tag] = child.text

            if in_item not in new_tt["list_of_inputs"] and in_item["Alternatives"]:
                new_tt["list_of_inputs"].append(in_item)
            # Add new entry when legacy ADF is split into several new ADFs
            # only when no alternatives
            if duplicate_adf:
                if len(in_item["Alternatives"]) > 1:
                    print(
                        "Error: entry is to be duplicated because of multple new adfs ",
                        duplicate_adf,
                    )
                    sys.exit()
                for d in duplicate_adf[1:]:
                    in_item_dup = copy.deepcopy(in_item)
                    in_item_dup["Alternatives"][0]["File_Type"] = d
                    new_tt["list_of_inputs"].append(in_item_dup)

                duplicate_adf = None

    json_str = json.dumps(new_tt, indent=4)

    return json_str


if __name__ == "__main__":
    # Sentinel 3 TaskTables
    tt_conf = importlib.resources.files("sentinelutils") / "resources/tasktables"

    ipfs = {
        # "OL1": ("06.17", "OL__L1_.003.03.01"),
        # "OL1_RAC": ("06.15", "OL__L1_.003.03.01"),
        # "OL1_SPC": ("06.12", "OL__L1_.003.03.01"),
        # "OL2_FR": ("06.18", "OL__L2L.002.11.02"),
        # "SL1": ("06.21", "SL__L1_.004.06.00"),
        # "SL2": ("06.22", "SL__LST.004.07.02"),
        # "SL2_FRP": ("01.09", "FRP_NTC.004.08.02"),
        # "SY2": ("06.26", "SYN_L2_.002.18.01"),
        # "SY2_AOD": ("01.09", "AOD_NTC.002.08.01"),
        # "SY2_VGS": ("06.13", "SYN_L2V.002.09.01"),
        "L0_DO_DOP": ("06.15", ""),
        "L0_DO_NAV": ("06.15", ""),
        "L0_GN_GNS": ("06.15", ""),
        "L0_MW_MWR": ("06.15", ""),
        "L0_OL_CR_": ("06.15", ""),
        "L0_OL_EFR": ("06.15", ""),
        "L0_SL_SLT": ("06.15", ""),
        "L0_SR_CAL": ("06.15", ""),
        "L0_SR_SRA": ("06.15", ""),
        "L0_TM_HKM": ("06.15", ""),
        "L0_TM_HKM2": ("06.15", ""),
        "L0_TM_NAT": ("06.15", ""),
    }
    for ipf, version in ipfs.items():
        print(f"* Convert {ipf} TaskTable")
        json_str = convert_tt(
            str(tt_conf / "xml" / f"TaskTable_S3A_{ipf}.xml"),
            version=version[0],
            baseline_collection=version[1],
        )
        new_tt_file = tt_conf / "json" / f"TaskTable_{ipf}.json"
        with open(str(new_tt_file), mode="w") as f:
            f.write(json_str)
