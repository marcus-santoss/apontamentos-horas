import random
import time
from datetime import datetime

import requests

from core.annotations import Annotation


class JiraAnnotation(Annotation):
    def __init__(self):
        super().__init__("jira")

    def time_entries(self):
        times = {}
        data, first, last = self.get_entries()
        for d in data["results"]:
            dt = d["startDate"]
            if dt not in times:
                times[dt] = d["timeSpentSeconds"]
            else:
                times[dt] += d["timeSpentSeconds"]

        return times, first, last

    def registry_entry(
        self,
        description,
        init_hour: str,
        end_hour: str,
        current_date: str,
        debug: bool = False,
    ):
        to_datetime = lambda x: datetime.strptime(x, "%H:%M")
        spent = to_datetime(end_hour) - to_datetime(init_hour)
        body = {
            "authorAccountId": self.provider.account_id,
            "description": description,
            "issueId": self.provider.issue_id,
            "startDate": current_date,
            "startTime": f"{init_hour}:{random.randint(10, 59)}",
            "timeSpentSeconds": spent.total_seconds(),
        }
        if debug:
            self.dumps(body)
            return

        resp = requests.post(
            self.provider.base_url, headers=self.provider.auth, json=body
        )
        if resp.status_code < 300:
            print("OK")
        else:
            self.report_error(description, resp)

        time.sleep(1)
