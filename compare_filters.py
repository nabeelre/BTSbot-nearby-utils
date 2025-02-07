from TestCase import TestCase
from penquins import Kowalski
from Filter import Filter
import datetime
import json
import os

with open('/Users/nabeelr/credentials.json', 'r') as f:
    creds = json.load(f)
token = creds['tmp_kowalski_token']

k = Kowalski(
    protocol="https",
    host="kowalski.caltech.edu",
    port=443,
    token=token,
    timeout=305,
)
assert k.ping()

prod_SEDM_id = 1174
test_SEDM_id = 1194

prod_UVOT_id = 1191
lab_UVOT_id = 1193


def test_SEDM_filter():
    prod_SEDM = Filter(test_SEDM_id, "d4e8w3", "SEDM")
    latest_SEDM = Filter(test_SEDM_id, "e6921c", "SEDM")

    TC = TestCase(
        2460456.0, 2460460.0, neg_ids=[], pos_ids=["ZTF24aaozxhx"],
        notes="Recover 2024jlf", name="SN2024jlf"
    )
    TC.compare_filters(Kowalski=k, filt_a=prod_SEDM, filt_b=latest_SEDM)


def test_UVOT_filter():
    prod_UVOT = Filter(prod_UVOT_id, "fomkqf", "UVOT")
    latest_UVOT = Filter(lab_UVOT_id, "9x5366", "UVOT")

    # Create directory for output
    run_t_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(f"logs/cmp_{run_t_stamp}/")

    TC = TestCase(
        2460456.0, 2460460.0, neg_ids=[], pos_ids=["ZTF24aaozxhx"],
        notes="UVOT filter comparison, around 24jlf", name="UVOT_cmp_24jlf"
    )
    TC.compare_filters(
        Kowalski=k, filt_a=prod_UVOT, filt_b=latest_UVOT,
        run_name=f"cmp_{run_t_stamp}"
    )


def __main__():
    test_UVOT_filter()


if __name__ == "__main__":
    __main__()
