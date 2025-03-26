import time
from datetime import datetime
from typing import Literal

import requests

from core.annotations import Annotation


class ClockifyAnnotation(Annotation):
    def __init__(self):
        super().__init__("clockify")

    @staticmethod
    def adjust_tz(date: str):
        dt = date.split(":")
        dt1 = int(dt[0]) + 3
        return f"{dt1}:{dt[1]}"

    def time_entries(self) -> tuple:
        times = {}
        to_datetime = lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")

        url = "{url}/api/v1/workspaces/{workspace}/user/{user}/time-entries".format(
            url=self.provider.base_url,
            workspace=self.provider.workspace_id,
            user=self.provider.user_id,
        )
        data, first, last = self.get_entries(url)

        for d in data:
            dt = d["timeInterval"]["start"].split("T")[0]
            spent = to_datetime(d["timeInterval"]["end"]) - to_datetime(
                d["timeInterval"]["start"]
            )
            if dt not in times:
                times[dt] = spent.total_seconds()
            else:
                times[dt] += spent.total_seconds()

        return times, first, last

    def registry_entry(
        self,
        description,
        init_hour: str,
        end_hour: str,
        current_date: str = None,
        entry_type: Literal["task", "meet"] = "task",
        debug: bool = False,
    ):
        body = {
            "billable": True,
            "description": description,
            "start": f"{current_date}T{self.adjust_tz(init_hour)}:00Z",
            "end": f"{current_date}T{self.adjust_tz(end_hour)}:00Z",
            "projectId": self.provider.project_id,
            "taskId": self.provider.entry_type_map[entry_type],
            "type": "REGULAR",
        }
        if debug:
            self.dumps(body)
            return

        url: str = "{url}/api/v1/workspaces/{workspace}/time-entries".format(
            url=self.provider.base_url, workspace=self.provider.workspace_id
        )
        resp: requests.Response = requests.post(
            url, headers=self.provider.auth, json=body
        )
        if resp.status_code < 300:
            print("OK")
        else:
            self.report_error(description, resp)

        time.sleep(1)
