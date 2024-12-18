from TestCase import TestCase
from penquins import Kowalski
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

lab_40Mpc_filterid = 1191
lab_60Mpc_filterid = 1194
lab_80Mpc_filterid = 1195


def __main__():
    # Create directory for output
    run_t_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(f"logs/{run_t_stamp}/")
    curr_filterid = 1182

    # Create and evaluate TestCases
    TC_sn2024jlf = TestCase(
        2460456.0, 2460460.0, neg_ids=[], pos_ids=["ZTF24aaozxhx"],
        notes="Recover 2024jlf / ZTF24aaozxhx", name="SN2024jlf"
    )

    TC_bad_hist = [
        TestCase(
            60656.0, 60660.0, neg_ids=["ZTF24abxxafd"], pos_ids=[],
            notes="bad_hist1: ZTF24abxxafd", name="bad_hist1"
        ),
        TestCase(
            60651.0, 60655.0, neg_ids=["ZTF24abtiont"], pos_ids=[],
            notes="bad_hist1: ZTF24abtiont", name="bad_hist2"
        )
    ]

    TCs = [TC_sn2024jlf] + TC_bad_hist
    statuses = []
    for TC in TCs:
        statuses += [TC.evaluate_test(
            Kowalski=k, run_name=run_t_stamp,
            filterid=curr_filterid, verbose=True
        )]

    if any(statuses):
        print("SOME TESTS FAILED:")
        for TC, status in zip(TCs, statuses):
            if status:
                print(f"name:{TC.name}, desc:{TC.notes}")


if __name__ == "__main__":
    __main__()
