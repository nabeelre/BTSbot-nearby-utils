from tqdm import tqdm
import json


class TestCase:
    """
    A class to represent a BTSbot-nearby test case.
    Test cases involve assuring a particular source is properly recovered or
    rejected by BTSbot-nearby filtering by running the ZTF alert stream through
    an alert filter

    TestCase objects contain a JD range to select which alerts are run through
    the filter, a list of ZTFIDs of positive and negative examples, and notes
    describing the test case.
    """

    def __init__(self, jd_min: float, jd_max: float,
                 neg_ids: list, pos_ids: list,
                 notes: str, name: str):
        if jd_min >= jd_max:
            raise ValueError("jd_min must be less than jd_max")

        # Automatically convert to JDs if given as MJD
        if jd_min < 2400000:
            jd_min += 2400000.5
        if jd_max < 2400000:
            jd_max += 2400000.5

        self.jd_min = jd_min  # starting JD
        self.jd_max = jd_max  # ending JD
        self.neg_ids = neg_ids  # list of ZTFIDs that should not be in the output
        self.pos_ids = pos_ids  # list of ZTFIDs that should be in the output
        self.notes = notes  # description of what is being tested
        self.name = name  # single word name for the test case

    def write_output(self, annotations, objids, filterid, run_name, status):
        # Write annotations to disk
        with open(f'logs/{run_name}/{self.name}_annotations.json', 'w') as f:
            json.dump(annotations, f, indent=2)

        # Write list of ZTFIDs to disk
        with open(f'logs/{run_name}/{self.name}_objids.txt', 'w') as f:
            f.write(f"#TestCase: {self.name}\n")
            f.write(f"#{self.notes}\n")
            f.write(f"#{self.jd_min} - {self.jd_max} on filter {filterid}\n")
            f.write(f"#pos:{self.pos_ids}\n")
            f.write(f"#neg:{self.neg_ids}\n")
            f.write(f"#test passed:{status}\n")

            f.write("ZTFID\n")
            for objid in objids:
                f.write(f"{objid}\n")

    def evaluate_test(self, Kowalski, run_name: str, filterid: int,
                      apply_autosave_filter: bool = True,
                      verbose: bool = False):
        """
        Call Kowalski API endpoint to run alerts through a filter and evaluate
        whether the test case is passed. Optianally apply additional autosave
        filtering before analyzing the output.
        """

        # Split JD range into 1-day slices
        jd_slices = [self.jd_min]
        while jd_slices[-1] < self.jd_max - 1:
            jd_slices.append(jd_slices[-1] + 1)

        if verbose:
            num_days = (self.jd_max - self.jd_min)
            num_months = ((self.jd_max - self.jd_min) / 30.5)
            print(f"TestCase {self.name} from {self.jd_min} to {self.jd_max} " +
                  f"({num_days:.0f} day / {num_months:.1f} month)")

        objids_passed = []
        annotations = []

        for jd in tqdm(jd_slices, unit='day',
                       desc=f'Running {self.name}'):
            data = {
                "start_date": jd,
                "end_date": jd + 1,
                "max_time_ms": 300000
            }
            response = Kowalski.api('POST', f'api/filters/{filterid}/test', data=data)

            if response["status"] != "success":
                print(f"Failed to test filter from {jd} to {jd + 1}: {response['message']}")
                continue

            results = response["data"]
            annotations += results

            if not all('objectId' in item for item in results):
                raise Exception('Not all items have an objectId field')

            # for each ZTF object in the results...
            for item in results:
                if apply_autosave_filter:
                    if (item['annotations']['bts'] >= 0.5) &\
                       (item['annotations']['sgscore1'] >= 0.0) &\
                       (item['annotations']['sgscore2'] >= 0.0):
                        objids_passed += [item['objectId']]
                else:
                    objids_passed += [item['objectId']]

        # Take only unique object IDs
        objids_passed = list(set(objids_passed))

        # Check if all positive examples are in the output
        failed = False
        for pos_id in self.pos_ids:
            if pos_id not in objids_passed:
                print(f"FAILED: {pos_id} NOT IN OUTPUT")
                failed = True

        # Check if all negative examples are not in the output
        for neg_id in self.neg_ids:
            if neg_id in objids_passed:
                print(f"FAILED: {neg_id} IN OUTPUT")
                failed = True
        print()

        self.write_output(annotations, objids_passed, filterid, run_name, failed)

        return failed
