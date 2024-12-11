import time

import pytest

from crow_client.clients.rest_client import RestClient


@pytest.mark.flaky(reruns=3)
def test_paperqa_job():
    client = RestClient()
    job_data = {
        "name": "crow-job-paperqa-server-dev",
        "query": "How does the density of the 111 plan compare to the 100 plance in an FCC structure?",
    }
    client.create_job(job_data)

    while (job_status := client.get_job()["data"]["status"]) == "in progress":
        time.sleep(5)

    assert job_status == "success"
