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

    # Create TestCases
    TC_sn2024jlf = TestCase(
        2460456.0, 2460460.0, neg_ids=[], pos_ids=["ZTF24aaozxhx"],
        notes="Recover 2024jlf / ZTF24aaozxhx", name="SN2024jlf"
    )

    TC_bad_hist = [
        TestCase(
            60656.0, 60660.0, neg_ids=["ZTF24abxxafd"], pos_ids=[],
            notes="ZTF24abxxafd", name="bad_hist1"
        ),
        TestCase(
            60651.0, 60655.0, neg_ids=["ZTF24abtiont"], pos_ids=[],
            notes="ZTF24abtiont", name="bad_hist2"
        )
    ]

    TC_bad_assosciation = [
        TestCase(
            60642.0, 60646.0, neg_ids=["ZTF24abuqraz"], pos_ids=[],
            notes="ZTF24abuqraz", name="bad_host1"
        )
    ]

    TC_no_lims = [
        TestCase(
            60631.0, 60635.0, neg_ids=["ZTF24abszdqt"], pos_ids=[],
            notes="ZTF24abszdqt", name="no_lims1"
        ),
        TestCase(
            60497.0, 60501.0, neg_ids=["ZTF24aaupozr"], pos_ids=[],
            notes="ZTF24aaupozr", name="no_lims2"
        )
    ]

    TC_bogus = [
        TestCase(
            60620.0, 60624.0, neg_ids=["ZTF24abrhrue"], pos_ids=[],
            notes="ZTF24abrhrue", name="bogus1"
        )
    ]

    # Evaluate all TestCases
    TCs = [TC_sn2024jlf] + TC_bad_hist + TC_bad_assosciation + TC_no_lims + TC_bogus
    print(f"Evaluating {len(TCs)} TestCases")
    statuses = []
    for TC in TCs:
        statuses += [TC.evaluate_test(
            Kowalski=k, run_name=run_t_stamp,
            filterid=curr_filterid, verbose=True
        )]

    if any(statuses):
        print("SOME TESTS FAILED")
        for TC, status in zip(TCs, statuses):
            if status:
                print(f"  {TC.name}: {TC.notes}")


if __name__ == "__main__":
    __main__()
