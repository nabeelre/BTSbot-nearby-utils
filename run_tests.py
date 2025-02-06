from TestCase import TestCase
from Filter import Filter
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

streamid_40Mpc = 1191
streamid_60Mpc = 1194
streamid_80Mpc = 1195

latest_SEDM = Filter(streamid_60Mpc, "zl40lh", "SEDM")

# TODO write function for running and comparing output of two filters


def __main__():
    # Create directory for output
    run_t_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(f"logs/{run_t_stamp}/")
    curr_filter = latest_SEDM

    # Create TestCases
    TC_z001 = [
        TestCase(
            2460456.0, 2460460.0, neg_ids=[], pos_ids=["ZTF24aaozxhx"],
            notes="Recover 2024jlf", name="SN 2024jlf"
        ),
        TestCase(
            60690.0, 60695.0, neg_ids=[], pos_ids=["ZTF25aacerkv"],
            notes="Recover ZTF25aacerkv", name="ZTF25aacerkv"
        ),
        TestCase(
            60688.0, 60693.0, neg_ids=[], pos_ids=["ZTF25aabylkr"],
            notes="Recover ZTF25aabylkr, although has slightly spotty coverage",
            name="ZTF25aabylkr"
        ),
        TestCase(
            60688.0, 60695.0, neg_ids=[], pos_ids=["ZTF25aabxywm"],
            notes="ZTF25aabxywm", name="ZTF25aabxywm"
        )
    ]

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

    # No non-detections prior to first alert
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
        ),
        TestCase(
            60675.0, 60690.0, neg_ids=["ZTF22aacffrr"], pos_ids=[],
            notes="ZTF22aacffrr, one alert with high drb, medium bts", name="bogus2"
        ),
        TestCase(
            60676.0, 60682.0, neg_ids=["ZTF25aaastwn"], pos_ids=[],
            notes="ZTF25aaastwn, medium drb", name="bogus2"
        )
    ]

    # Only non-detections (2.5-10 days since first alert), trigger SEDM but not others
    TC_loose_lims = [
        # Has limit immediately before first alert
        # TODO consider adding minimum separation between last non-det and first alert
        # TestCase(
        #     60704.0, 60708.0, neg_ids=[], pos_ids=["ZTF25aadlcbi"],
        #     notes="ZTF25aadlcbi, 8 days between first alert and last non-det",
        #     name="loose_lims1"
        # ),
        TestCase(
            60704.0, 60708.0, neg_ids=[], pos_ids=["ZTF25aadhlrs"],
            notes="ZTF25aadhlrs, 7 days between first alert and last non-det",
            name="loose_lims2"
        ),
        TestCase(
            60690.0, 60695.0, neg_ids=[], pos_ids=["ZTF25aaccmjq"],
            notes="ZTF25aaccmjq, >3 days between first alert and last non-det",
            name="ZTF25aaccmjq"
        )
    ]

    # ZTF25aadlqhw one det, poor coverage
    # ZTF25aabmhly one det, good coverage
    # ZTF25aaaqfrf TODO - how to avoid deep drilling

    # Evaluate all TestCases
    TCs = TC_z001 + TC_bad_hist + TC_bad_assosciation + TC_no_lims + TC_bogus + TC_loose_lims

    print(f"Evaluating {len(TCs)} TestCases")
    statuses = []
    for TC in TCs:
        failed = TC.evaluate_test(
            Kowalski=k, run_name=run_t_stamp,
            filt=curr_filter, verbose=True
        )
        statuses += [not failed]

    if not all(statuses):
        print("SOME TESTS FAILED")
        for TC, status in zip(TCs, statuses):
            if status:
                print(f"  {TC.name}: {TC.notes}")


if __name__ == "__main__":
    __main__()
