import argparse
import csv
import json
import os
from collections import defaultdict
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Any

from babel.dates import format_date
import pandas as pd


class JSONDataConverter:
    def __init__(self, root_path: str) -> None:
        self.root_path = root_path

    @cached_property
    def elections_data(self) -> pd.DataFrame:
        return pd.read_csv(
            Path(__file__).parent.parent / "data/common/elections.csv",
            header=0,
            sep=";",
            dtype={
                "id": str,
                "label": str,
            },
        )

    def save_json(self, data: list | dict, file_path: str) -> None:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as jsonfile:
            json.dump(
                data,
                jsonfile,
                ensure_ascii=False,
                indent=None,
                separators=(",", ":"),
            )

    def read_csv(self, file_path, delimiter=";"):
        with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for row in reader:
                yield row

    def output_riks_data(self) -> None:
        data: Any = {}

        riks = pd.read_csv(
            Path(__file__).parent.parent / "data/common/riks.csv",
            header=0,
            sep=";",
            dtype={
                "rik_code": str,
            },
        )

        for _, rik in riks.iterrows():
            data[rik.rik_code] = {
                "id": rik.rik_code,
                "name": rik.rik_name,
            }

        data = list(data.values())
        data.sort(key=lambda x: x.get("id"), reverse=False)

        target_file_path = os.path.join(self.root_path, "common", "riks", "index.json")
        self.save_json(data, target_file_path)

    def output_municipalities_data(self) -> None:
        data: Any = {}

        municipalities = pd.read_csv(
            Path(__file__).parent.parent / "data/common/municipalities.csv",
            header=0,
            sep=";",
            dtype={
                "rik_code": str,
                "municipality_code": str,
            },
        )
        for _, mun in municipalities.iterrows():
            data[mun.municipality_code] = {
                "id": mun.municipality_code,
                "rid": mun.rik_code,
                "name": mun.municipality,
            }

        data = list(data.values())
        data.sort(key=lambda x: x.get("id"), reverse=False)

        target_file_path = os.path.join(
            self.root_path, "common", "municipalities", "index.json"
        )
        self.save_json(data, target_file_path)

    def output_elections_data(self) -> None:
        data: Any = {}

        for _, election in self.elections_data.iterrows():
            date_str = format_date(
                datetime.strptime(election["id"], "%Y%m%d"),
                format="d LLLL yyyy",
                locale="bg",
            )
            data[election["id"]] = {
                "id": election["id"],
                "code": election["label"],
                "name": f"Избори за Народно събрание - {date_str}",
            }

        data = list(data.values())
        data.sort(key=lambda x: x.get("id"), reverse=False)

        target_file_path = os.path.join(
            self.root_path, "common", "elections", "index.json"
        )
        self.save_json(data, target_file_path)

    def output_participants_data(self) -> None:
        participants: Any = {}
        for _, election in self.elections_data.iterrows():
            source_file_path = (
                Path(__file__).parent.parent
                / f"data/{election["id"]}/21_participants.csv"
            )
            for row in self.read_csv(source_file_path):
                pid = row.get("code", "")
                if pid not in participants:
                    participants[pid] = {
                        "id": pid,
                        "name": row.get("name", ""),
                        "elections": [],
                    }
                elections_data = {
                    "eid": election["id"],
                    "reg_name": row.get("registration_name", ""),
                    "reg_code": row.get("registration_code", ""),
                }
                reg_sub_code = row.get("registration_sub_code", "")
                if reg_sub_code != "0":
                    elections_data["reg_sub_code"] = reg_sub_code
                participants[pid]["elections"].append(elections_data)

        data = list(participants.values())
        data.sort(key=lambda x: x.get("id"), reverse=False)

        target_file_path = os.path.join(
            self.root_path, "common", "participants", "index.json"
        )
        self.save_json(data, target_file_path)

    def output_per_elections_data(self) -> None:
        def create_default_entry():  # -> dict[str, Any]:
            return {
                "id": "",
                "e": "",
                "prv": 0,
                "rv": 0,
                "olv": 0,
                "v": 0,
                "db": 0,
                "uupb": 0,
                "dpb": 0,
                "ub": 0,
                "upb": 0,
                "umb": 0,
                # "urn_machine_ballots_md": 0,
                "ipb": 0,
                "vv": 0,
                # "valid_votes_md": 0,
                "vvp": 0,
                # "valid_votes_for_parties_md": 0,
                "vvsn": 0,
                "vd": defaultdict(
                    lambda: {
                        "id": "",
                        "n": "",
                        "p": 0,
                        "m": 0,
                        "md": 0,
                        "t": 0,
                    }
                ),
            }

        for _, election in self.elections_data.iterrows():
            protocols_file = (
                Path(__file__).parent.parent / f"data/{election["id"]}/41_protocols.csv"
            )
            votes_file = (
                Path(__file__).parent.parent
                / f"data/{election["id"]}/51_votes_combined.csv"
            )
            output_dir = os.path.join(self.root_path, election["id"])

            sections: defaultdict = defaultdict(create_default_entry)
            municipalities: defaultdict = defaultdict(create_default_entry)
            riks: defaultdict = defaultdict(create_default_entry)
            total: defaultdict = defaultdict(create_default_entry)

            for row in self.read_csv(protocols_file):
                section_id = row["section_id"]
                municipality_code = section_id[:4]
                rik_code = section_id[:2]

                for key, data in [
                    ("total", total),
                    (section_id, sections),
                    (municipality_code, municipalities),
                    (rik_code, riks),
                ]:
                    data[key]["e"] = election["id"]
                    data[key]["id"] = key
                    data[key]["prv"] += int(row["pre_registered_voters"])
                    data[key]["rv"] += int(row["registered_voters"])
                    data[key]["olv"] += int(row["onsite_listed_voters"])
                    data[key]["v"] += int(row["voted_voters"])
                    data[key]["db"] += int(row["distributed_ballots"])
                    data[key]["uupb"] += int(row["unused_paper_ballots"])
                    data[key]["dpb"] += int(row["destroyed_paper_ballots"])
                    data[key]["upb"] += int(row["urn_paper_ballots"])
                    data[key]["umb"] += int(row["urn_machine_ballots"])
                    data[key]["ipb"] += int(row["invalid_paper_ballots"])
                    data[key]["vvp"] += int(row["valid_paper_votes_for_parties"]) + int(
                        row["valid_machine_votes_for_parties"]
                    )
                    data[key]["vvsn"] += int(row["support_noone_paper_ballots"]) + int(
                        row["support_noone_machine_ballots"]
                    )
                    data[key]["ub"] = data[key]["upb"] + data[key]["umb"]
                    data[key]["vv"] = data[key]["vvp"] + data[key]["vvsn"]

            for row in self.read_csv(votes_file):
                section_id = row["section_id"]
                municipality_code = row["municipality_code"]
                rik_code = row["rik_code"]
                pid = row["participant_code"]

                for key, data in [
                    (section_id, sections),
                    (municipality_code, municipalities),
                    (rik_code, riks),
                    ("total", total),
                ]:
                    data[key]["id"] = key
                    vote_entry = data[key]["vd"][pid]
                    vote_entry["id"] = pid
                    vote_entry["n"] = row["participant_name"]
                    vote_entry["p"] += int(row["paper_votes"])
                    vote_entry["m"] += int(row["machine_votes"])
                    vote_entry["md"] += int(row["machine_data_votes"])
                    vote_entry["t"] = vote_entry["p"] + vote_entry["m"]

            for category, data in {
                "total": total,
                "sections": sections,
                "municipalities": municipalities,
                "riks": riks,
            }.items():
                category_dir = f"{output_dir}/{category}"
                for key, value in data.items():
                    values = list(value["vd"].values())
                    values.sort(key=lambda x: x.get("id"), reverse=False)
                    value["vd"] = values
                    target_file_path = (
                        f"{category_dir}/{key}/index.json"
                        if key != category
                        else f"{category_dir}/index.json"
                    )
                    self.save_json(value, target_file_path)

    def output_combined_elections_data(self) -> None:
        def create_default_data_entry():
            return {
                "e": "",
                "v": 0,
            }

        def create_default_entry():  # -> dict[str, Any]:
            return {
                "id": "",
                "prv": defaultdict(create_default_data_entry),
                "rv": defaultdict(create_default_data_entry),
                "olv": defaultdict(create_default_data_entry),
                "v": defaultdict(create_default_data_entry),
                "db": defaultdict(create_default_data_entry),
                "uupb": defaultdict(create_default_data_entry),
                "dpb": defaultdict(create_default_data_entry),
                "ub": defaultdict(create_default_data_entry),
                "upb": defaultdict(create_default_data_entry),
                "umb": defaultdict(create_default_data_entry),
                "ipb": defaultdict(create_default_data_entry),
                "vv": defaultdict(create_default_data_entry),
                "vvp": defaultdict(create_default_data_entry),
                "vvsn": defaultdict(create_default_data_entry),
                "vd": defaultdict(
                    lambda: {
                        "id": "",
                        "n": "",
                        "p": defaultdict(create_default_data_entry),
                        "m": defaultdict(create_default_data_entry),
                        "md": defaultdict(create_default_data_entry),
                        "t": defaultdict(create_default_data_entry),
                    }
                ),
            }

        sections: defaultdict = defaultdict(create_default_entry)
        municipalities: defaultdict = defaultdict(create_default_entry)
        riks: defaultdict = defaultdict(create_default_entry)
        total: defaultdict = defaultdict(create_default_entry)

        for _, election in self.elections_data.iterrows():
            el = election["id"]
            protocols_file = (
                Path(__file__).parent.parent / f"data/{election["id"]}/41_protocols.csv"
            )
            votes_file = (
                Path(__file__).parent.parent
                / f"data/{election["id"]}/51_votes_combined.csv"
            )

            for row in self.read_csv(protocols_file):
                section_id = row["section_id"]
                municipality_code = section_id[:4]
                rik_code = section_id[:2]

                for key, data in [
                    ("total", total),
                    (section_id, sections),
                    (municipality_code, municipalities),
                    (rik_code, riks),
                ]:
                    data[key]["id"] = key
                    data[key]["prv"][el]["e"] = el
                    data[key]["prv"][el]["v"] += int(row["pre_registered_voters"])
                    data[key]["rv"][el]["e"] = el
                    data[key]["rv"][el]["v"] += int(row["registered_voters"])
                    data[key]["olv"][el]["e"] = el
                    data[key]["olv"][el]["v"] += int(row["onsite_listed_voters"])
                    data[key]["v"][el]["e"] = el
                    data[key]["v"][el]["v"] += int(row["voted_voters"])
                    data[key]["db"][el]["e"] = el
                    data[key]["db"][el]["v"] += int(row["distributed_ballots"])
                    data[key]["uupb"][el]["e"] = el
                    data[key]["uupb"][el]["v"] += int(row["unused_paper_ballots"])
                    data[key]["dpb"][el]["e"] = el
                    data[key]["dpb"][el]["v"] += int(row["destroyed_paper_ballots"])
                    data[key]["upb"][el]["e"] = el
                    data[key]["upb"][el]["v"] += int(row["urn_paper_ballots"])
                    data[key]["umb"][el]["e"] = el
                    data[key]["umb"][el]["v"] += int(row["urn_machine_ballots"])
                    data[key]["ipb"][el]["e"] = el
                    data[key]["ipb"][el]["v"] += int(row["invalid_paper_ballots"])
                    data[key]["vvp"][el]["e"] = el
                    data[key]["vvp"][el]["v"] += int(
                        row["valid_paper_votes_for_parties"]
                    ) + int(row["valid_machine_votes_for_parties"])
                    data[key]["vvsn"][el]["e"] = el
                    data[key]["vvsn"][el]["v"] += int(
                        row["support_noone_paper_ballots"]
                    ) + int(row["support_noone_machine_ballots"])

                    data[key]["ub"][el]["e"] = el
                    data[key]["ub"][el]["v"] = (
                        data[key]["upb"][el]["v"] + data[key]["umb"][el]["v"]
                    )
                    data[key]["vv"][el]["e"] = el
                    data[key]["vv"][el]["v"] = (
                        data[key]["vvp"][el]["v"] + data[key]["vvsn"][el]["v"]
                    )

            for row in self.read_csv(votes_file):
                section_id = row["section_id"]
                municipality_code = row["municipality_code"]
                rik_code = row["rik_code"]
                pid = row["participant_code"]

                for key, data in [
                    (section_id, sections),
                    (municipality_code, municipalities),
                    (rik_code, riks),
                    ("total", total),
                ]:
                    data[key]["id"] = key
                    vote_entry = data[key]["vd"][pid]
                    vote_entry["id"] = pid
                    vote_entry["n"] = row["participant_name"]
                    vote_entry["p"][el]["e"] = el
                    vote_entry["p"][el]["v"] += int(row["paper_votes"])
                    vote_entry["m"][el]["e"] = el
                    vote_entry["m"][el]["v"] += int(row["machine_votes"])
                    vote_entry["md"][el]["e"] = el
                    vote_entry["md"][el]["v"] += int(row["machine_data_votes"])
                    vote_entry["t"][el]["e"] = el
                    vote_entry["t"][el]["v"] = (
                        vote_entry["p"][el]["v"] + vote_entry["m"][el]["v"]
                    )

        target_file_path = os.path.join(
            self.root_path, "common", "participants", "index.json"
        )

        for category, data in {
            "sections": sections,
            "municipalities": municipalities,
            "riks": riks,
            "total": total,
        }.items():
            category_dir = f"{self.root_path}/combined/{category}"

            for key, value in data.items():
                for prop in [
                    "prv",
                    "rv",
                    "olv",
                    "v",
                    "db",
                    "uupb",
                    "dpb",
                    "ub",
                    "upb",
                    "umb",
                    "ipb",
                    "vv",
                    "vvp",
                    "vvsn",
                ]:
                    try:
                        values = list(value[prop].values())
                        values.sort(key=lambda x: x.get("e"), reverse=False)
                        value[prop] = values
                    except AttributeError as ex:
                        pass

                values = list(value["vd"].values())
                values.sort(key=lambda x: x.get("id"), reverse=False)
                value["vd"] = values
                for vd_value in value["vd"]:
                    for prop in ["p", "m", "md", "t"]:
                        vd_values = list(vd_value[prop].values())
                        vd_values.sort(key=lambda x: x.get("e"), reverse=False)
                        vd_value[prop] = vd_values

                target_file_path = (
                    f"{category_dir}/{key}/index.json"
                    if key != category
                    else f"{category_dir}/index.json"
                )
                self.save_json(value, target_file_path)

    def output_section_total_votes(self) -> None:
        source_file_path = (
            Path(__file__).parent.parent / f"data/processed/sections_total_votes.csv"
        )
        sections = []

        for row in self.read_csv(source_file_path):
            section_id = row["section_id"]
            # Extract dates and values from the CSV row
            data_entries = []
            for key, value in row.items():
                if key.startswith("E") and value:
                    date_str = datetime.strptime(key[1:], "%Y%m%d").strftime("%Y-%m-%d")
                    data_entries.append({"d": date_str, "v": int(value)})

            # Append section data
            sections.append(
                {
                    "id": section_id,
                    "data": data_entries,
                }
            )

        target_file_path = os.path.join(
            self.root_path, "custom", "sections_total_votes", "index.json"
        )
        self.save_json({"sections": sections}, target_file_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert election data to JSON format")
    parser.add_argument("root_path", help="Root path for output JSON files")
    args = parser.parse_args()

    converter = JSONDataConverter(args.root_path)
    converter.output_riks_data()
    converter.output_municipalities_data()
    converter.output_elections_data()
    converter.output_participants_data()
    converter.output_per_elections_data()
    converter.output_combined_elections_data()
    converter.output_section_total_votes()


if __name__ == "__main__":
    main()
