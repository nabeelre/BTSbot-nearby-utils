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

prod_UVOT_id = 1191
lab_UVOT_id = 1193
prod_UVOT = Filter(prod_UVOT_id, "anupg3", "UVOT")
latest_UVOT = Filter(lab_UVOT_id, "gfunuh", "UVOT")


def __main__():
    # Create directory for output
    run_t_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(f"logs/{run_t_stamp}/")
    curr_filter = prod_UVOT

    # Create TestCases
    TC_z001 = [
        TestCase(
            2460456.0, 2460460.0, neg_ids=[], pos_ids=["ZTF24aaozxhx"],
            notes="Recover 2024jlf", name="SN2024jlf"
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
        ),
        TestCase(
            60633.0, 60636.0, neg_ids=[], pos_ids=["ZTF24abtczty"],
            notes="ZTF24abtczty, low BTSbot score", name="ZTF24abtczty"
        ),
        TestCase(
            60591.0, 60593.0, neg_ids=[], pos_ids=["ZTF24ablleoq"],
            notes="ZTF24ablleoq", name="ZTF24ablleoq"
        ),
        TestCase(
            60438.0, 60442.0, neg_ids=[], pos_ids=["ZTF24aamtvxb"],
            notes="ZTF24aamtvxb", name="ZTF24aamtvxb"
        )
    ]

    TC_z0015 = [
        TestCase(
            60658.0, 60662.0, neg_ids=[], pos_ids=["ZTF24abyatjx"],
            notes="ZTF24abyatjx, short separation between two dets",
            name="ZTF24abyatjx"
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
        ),
        TestCase(
            60558.0, 60561.0, neg_ids=["ZTF24abgfibg"], pos_ids=[],
            notes="ZTF24abgfibg, distant host and poor early coverage", name="bad_host2"
        ),
        TestCase(
            60715.0, 60720.0, neg_ids=["ZTF25aafknns"], pos_ids=[],
            notes="ZTF25aafknns, atop distant galaxy but matched to nearby galaxy",
            name="bad_host3"
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
        ),
        TestCase(
            60670.0, 60680.0, neg_ids=["ZTF24acaccrk"], pos_ids=[],
            notes="ZTF24acaccrk, no lims and also no early ZTF coverage",
            name="no_lims2"
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
            notes="ZTF25aaastwn, medium drb", name="bogus3"
        ),
        TestCase(
            60678.0, 60681.0, neg_ids=["ZTF24aahcirg", "ZTF24aahcirc", "ZTF20abcyldz"],
            pos_ids=[], notes="ZTF24aahcirg, deep drilling bogus", name="bogus4"
        )
    ]

    # No non-detections within 3.5 days of first alert
    TC_loose_lims = [
        TestCase(
            60704.0, 60708.0, neg_ids=["ZTF25aadhlrs"], pos_ids=[],
            notes="ZTF25aadhlrs, 7 days between first alert and last non-det",
            name="loose_lims2"
        ),
        TestCase(
            60690.0, 60695.0, neg_ids=["ZTF25aaccmjq"], pos_ids=[],
            notes="ZTF25aaccmjq, 3.9 days between first alert and last non-det",
            name="ZTF25aaccmjq"
        ),
        TestCase(
            60380.0, 60390.0, neg_ids=["ZTF24aahgqwk"], pos_ids=[],
            notes="ZTF24aahgqwk, 8 days between first alert and last non-det",
            name="ZTF24aahgqwk"
        ),
        TestCase(
            60712.0, 60718.0, neg_ids=["ZTF25aafiibc"], pos_ids=[],
            notes="ZTF25aafiibc, ~4 days between first alert and last non-det",
            name="ZTF25aafiibc"
        )
    ]

    # ZTF25aadlqhw two dets with very little separation, poor coverage
    # ZTF25aabmhly one det, good coverage
    # ZTF24abyaspl one det on first night
    # ZTF25aaaqfrf TODO - how to avoid deep drilling
    # ZTF25aaduxhj NED dist incorrectly 10 Mpc
    # ZTF24abltbed no early ZTF coverage
    # Has limit immediately before first alert
    # TODO consider adding minimum separation between last non-det and first alert
    # TestCase(
    #     60704.0, 60708.0, neg_ids=[], pos_ids=["ZTF25aadlcbi"],
    #     notes="ZTF25aadlcbi, 8 days between first alert and last non-det",
    #     name="loose_lims1"
    # ),

    # Evaluate all TestCases
    TCs = TC_z001 + TC_z0015 + TC_bad_hist + TC_bad_assosciation + TC_no_lims + \
        TC_bogus + TC_loose_lims

    TC_24B = TestCase(
        60523.0, 60706.0, neg_ids=[], pos_ids=[
            'ZTF20aacedmi', 'ZTF20abidglx', 'ZTF24aadnhsl', 'ZTF24aaejecr',
            'ZTF24aaejvcx', 'ZTF24aaemydm', 'ZTF24aaerzgo', 'ZTF24aagpsfh',
            'ZTF24aahgaov', 'ZTF24aahgqwk', 'ZTF24aahgtjt', 'ZTF24aahiabd',
            'ZTF24aahnklb', 'ZTF24aahszxf', 'ZTF24aajqamj', 'ZTF24aamlalc',
            'ZTF24aamtvxb', 'ZTF24aankvcy', 'ZTF24aaozxhx', 'ZTF24aaqaroi',
            'ZTF24aaqkvyl', 'ZTF24aaqtode', 'ZTF24aarygdq', 'ZTF24aatbpbr',
            'ZTF24aatytqv', 'ZTF24aaupozr', 'ZTF24aauyikt', 'ZTF24aawrofs'
        ], notes="2024B", name="2024B"
    )

    TCs = [TC_24B]

    print(f"Evaluating {len(TCs)} TestCases")
    statuses = []
    for TC in TCs:
        failed = TC.evaluate_test(
            Kowalski=k, run_name=run_t_stamp,
            filt=curr_filter
        )
        statuses += [not failed]

    if not all(statuses):
        print("SOME TESTS FAILED")
        for TC, passed in zip(TCs, statuses):
            if not passed:
                print(f"  {TC.name}: {TC.notes}")


if __name__ == "__main__":
    __main__()
