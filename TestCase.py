from tqdm import tqdm
from Filter import Filter
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

    def write_output(self, annotations, objids, filt, run_name, failed):
        """
        Write the provided annotations and objectIds to separate files in the
        logs directory.
        """

        # Write annotations to disk
        with open(f'logs/{run_name}/{self.name}_annotations.json', 'w') as f:
            json.dump(annotations, f, indent=2)

        # Write list of ZTFIDs to disk
        with open(f'logs/{run_name}/{self.name}_objids.txt', 'w') as f:
            f.write(f"#TestCase: {self.name}\n")
            f.write(f"#{self.notes}\n")
            f.write(f"#{self.jd_min} - {self.jd_max} on filter {filt.stream_id}")
            f.write(f" ({filt.ver_hash})\n")
            f.write(f"#pos:{self.pos_ids}\n")
            f.write(f"#neg:{self.neg_ids}\n")
            f.write(f"#test passed:{not failed}\n")

            f.write("ZTFID\n")
            for objid in objids:
                f.write(f"{objid}\n")

    def simulate_alert_stream(self, Kowalski, filt: Filter,
                              apply_autosave_filter: bool = True):
        """
        Using this TestCase's JD range, simulate the ZTF alert stream running
        through the provided filter and log the results. Optionally apply an
        autosave filter to the output before logging.

        Returns
        -------
        objids_passed : list
            List of ZTFIDs that passed the filter
        annotations : list
            List of annotations for each object that passed through the filter
        """
        # Split JD range into 1-day slices
        jd_slices = [self.jd_min]
        while jd_slices[-1] < self.jd_max - 1:
            jd_slices.append(jd_slices[-1] + 1)

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
                "max_time_ms": 300000,
                # "filter_version": filt.ver_hash
            }

            response = Kowalski.api('POST', f'api/filters/{filt.stream_id}/test', data=data)

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
                        # TODO update autosave filter
                        objids_passed += [item['objectId']]
                else:
                    objids_passed += [item['objectId']]

        # Take only unique object IDs
        objids_passed = list(set(objids_passed))

        return objids_passed, annotations

    def evaluate_test(self, Kowalski, run_name: str, filt: Filter,
                      apply_autosave_filter: bool = True):
        """
        Call Kowalski API endpoint to run alerts through a filter and evaluate
        whether the test case is passed. Optianally apply additional autosave
        filtering before analyzing the output.

        Returns
        -------
        failed : bool
            True if the test case failed, False if it passed
        """

        objids_passed, annotations = self.simulate_alert_stream(
            Kowalski, filt, apply_autosave_filter
        )

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
        print(f"TestCase {self.name} {'Failed' if failed else 'Passed'}")
        print()

        self.write_output(annotations, objids_passed, filt, run_name, failed)

        return failed

    def compare_filters(self, Kowalski, filt_a: Filter, filt_b: Filter,
                        apply_autosave_filter: bool = True):

        objids_passed_a, annotations_a = self.simulate_alert_stream(
            Kowalski, filt_a, apply_autosave_filter
        )

        objids_passed_b, annotations_b = self.simulate_alert_stream(
            Kowalski, filt_b, apply_autosave_filter
        )

        passed_both = set(objids_passed_a) & set(objids_passed_b)
        passed_only_a = set(objids_passed_a) - set(objids_passed_b)
        passed_only_b = set(objids_passed_b) - set(objids_passed_a)

        print("ObjectIds that passed both filter A and B:")
        for objid in passed_both:
            print(objid)
        print()

        print("ObjectIds that passed only filter A:")
        for objid in passed_only_a:
            print(objid)
        print()

        print("ObjectIds that passed only filter B:")
        for objid in passed_only_b:
            print(objid)
        print()

        # FPs_a = [objid for objid in objids_passed_a if objid in self.neg_ids]
        # FPs_b = [objid for objid in objids_passed_b if objid in self.neg_ids]

        # FNs_a = [objid for objid in objids_passed_a if objid in self.pos_ids]
        # FNs_b = [objid for objid in objids_passed_b if objid in self.pos_ids]

        # print(f"False Positives for filter A: {FPs_a}")
        # print(f"False Positives for filter B: {FPs_b}")
