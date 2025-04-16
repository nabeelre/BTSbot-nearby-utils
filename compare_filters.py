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

prod_SEDM_id = 1182
lab_SEDM_id = 1194
prod_SEDM = Filter(prod_SEDM_id, "zom8ye", "SEDM")
lab_SEDM = Filter(lab_SEDM_id, "e6921c", "SEDM")

prod_UVOT_id = 1191
lab_UVOT_id = 1193
prod_UVOT = Filter(prod_UVOT_id, "fomkqf", "UVOT")
lab_UVOT = Filter(lab_UVOT_id, "4sa56j", "UVOT")

prod_SOAR_id = 1209
lab_SOAR_id = 1195
prod_SOAR = Filter(prod_SOAR_id, "etrfnn", "SOAR")
lab_SOAR = Filter(lab_SOAR_id, "gjgihn", "SOAR")


def long_comp(filt_a, filt_b):
    # Create directory for output
    run_t_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(f"logs/cmp_{run_t_stamp}/")

    TC = TestCase(
        2460562.0, 2460727.0, neg_ids=[], pos_ids=[],
        notes="long_cmp", name="long_cmp"
    )
    TC.compare_filters(
        Kowalski=k, filt_a=filt_a, filt_b=filt_b,
        run_name=f"cmp_{run_t_stamp}"
    )


if __name__ == "__main__":
    long_comp(prod_SEDM, lab_SEDM)

    # long_comp(prod_UVOT, lab_UVOT)
