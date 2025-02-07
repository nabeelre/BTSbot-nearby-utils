from TestCase import TestCase
from Filter import Filter
from penquins import Kowalski
import json

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

prod_BTSbotnearby = 1174
streamid_60Mpc = 1194

prod_SEDM = Filter(prod_BTSbotnearby, "h2qjt2", "SEDM")
latest_SEDM = Filter(streamid_60Mpc, "zl40lh", "SEDM")


def __main__():
    TC = TestCase(
        2460456.0, 2460460.0, neg_ids=[], pos_ids=["ZTF24aaozxhx"],
        notes="Recover 2024jlf", name="SN2024jlf"
    )

    TC.compare_filters(Kowalski=k, filt_a=prod_SEDM, filt_b=latest_SEDM)


if __name__ == "__main__":
    __main__()
