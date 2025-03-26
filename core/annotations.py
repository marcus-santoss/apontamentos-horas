import abc
import json
import pandas as pd
import requests
from abc import ABC
from core.schedules import generate_schedule_with_descriptions
from core.utils import get_configs, get_provider
from datetime import datetime


class Annotation(ABC):
    def __init__(self, provider_name: str):
        self.provider_name: str = provider_name
        self.configs = get_configs()
        self.provider = get_provider(provider_name)
        self.annotations: list = []

    @staticmethod
    def get_dates():
        first_day = datetime.today().replace(day=1)
        last_day = datetime.today()
        return first_day, last_day

    @staticmethod
    def report_error(description, resp):
        print(f"Failed to register entry: {description}")
        print(resp.text)
        print(resp.reason)
        print(resp.status_code)

    @staticmethod
    def dumps(body: dict):
        print(json.dumps(body, indent=2, ensure_ascii=False, default=str))

    def get_entries(self, url=None):
        url = url or self.provider.base_url
        first, last = self.get_dates()
        params = {
            self.provider.params.start.key: first.strftime(self.provider.params.start.format),
            self.provider.params.end.key: last.strftime(self.provider.params.start.format),
            self.provider.params.limit.key: self.provider.params.limit.value
        }

        resp = requests.get(url, headers=self.provider.auth, params=params)
        if resp.ok:
            return resp.json(), first, last

        raise Exception(resp.reason)

    @abc.abstractmethod
    def time_entries(self) -> tuple:
        raise NotImplementedError()

    @abc.abstractmethod
    def registry_entry(
            self, description: str, init_hour: str, current_date: str, end_hour: str, debug: bool = False
    ) -> None:
        raise NotImplementedError()

    def report(self):
        total = 0
        print("=" * 100)
        print(self.provider_name.upper())
        print("=" * 100)
        for entry in self.annotations:
            spent_minutes = entry["spent"] / 60
            not_is_ok = spent_minutes < self.configs.minutes_per_day["min"]
            status = "Abaixo Min" if not_is_ok else "OK"
            msg = f"[{status}] {entry['date']}: {entry['spent'] / 3600:.2f}h"
            total += spent_minutes
            print(msg)
        print("-" * 100)
        print("Tempo total: ", round(total / 60, 2))

    def fill_annotations(self, debug=False, black_list=None):
        entries, first, last = self.time_entries()

        for d in pd.date_range(first, last):
            if d.weekday() > 4:
                continue

            target_date = d.strftime("%Y-%m-%d")
            if target_date in black_list:
                print(f"O dia {target_date} foi pulado pois está na black list")
                continue

            action = "Registrando"
            if target_date in entries:
                spent = entries[target_date]
                self.annotations.append({"date": target_date, "spent": spent})
                if spent >= self.configs.minutes_per_day["min"]:
                    continue

                action = "Ajustando"

            print("-" * 100)
            print(f"{action} apontamentos para o dia: ", target_date)
            print("-" * 100)
            for entry in generate_schedule_with_descriptions(self.provider.common_tasks):
                print("Task: ", entry["description"], ": ", end="")
                self.registry_entry(
                    description=entry["description"],
                    init_hour=entry["start"],
                    current_date=target_date,
                    end_hour=entry["end"],
                    debug=debug
                )

        self.report()
