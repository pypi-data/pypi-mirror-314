import traceback
import termcolor
import inspect
import json
import os
from networkdisk.mock import nxmockClass
import networkdisk as nd
from .nx_scrap import get_nx_tests


def run(
    verbose=False, stop_after_errors=False, class_filter=None, importants_only=None
):
    path = f"{list(nd.__path__)[0]}/tests/test_infos.json"
    if os.path.isfile(path):
        importants_only = True if importants_only is None else importants_only
        with open(path) as f:
            infos = json.load(f)
    else:
        importants_only = False if importants_only is None else importants_only
        infos = {}
    print("Scrapping tests")
    testsClasses = get_nx_tests()
    testsClasses = {
        e.__name__ + "_" + e.__module__.replace(".", "_"): e for e in testsClasses
    }
    classCount = len(testsClasses)
    print(f"pytest TestClass founds {classCount}")
    tot_count = 0
    tot_success = 0
    last_class = None.__class__
    for i, (name, class_to_mock) in enumerate(testsClasses.items()):
        if importants_only and name not in infos.get("importants", []):
            continue
        sname, context = name.split("_", maxsplit=1)
        repr_class = f"[{i}/{classCount}] {sname} ({context})"
        if infos.get("blacklist", {}).get(name, False) is True:
            termcolor.cprint(
                "=" * 80 + f"\n\t{repr_class}, Blacklisted... \n" + "=" * 80, "yellow"
            )
            continue
        if class_filter:
            if not class_filter in name:
                continue
        context = context.replace("_", ".")
        print()
        termcolor.cprint("=" * 80 + f"\n\t {repr_class}\n" + "=" * 80)
        print()
        count = 0
        success = 0
        C = nxmockClass(class_to_mock)()
        try:
            for setup in filter(lambda e: e.lower().startswith("setup"), dir(C)):
                getattr(C, setup)()
        except:
            termcolor.cprint(f"Class setup failed on {setup} attr", color="red")
            stop_after_errors += -1
            if not stop_after_errors:
                return class_to_mock
            if verbose:
                print("\n" + traceback.format_exc())

            continue
        for att in dir(C):
            if not att.startswith("test"):
                continue
            if att in infos.get("blacklist", {}).get(name, []) or att in infos.get(
                "blacklist", {}
            ).get("functions", []):
                termcolor.cprint(f" {att} is blacklisted, skipping...", color="yellow")
                continue
            print(f" handling {att} ...", end="")
            Obj = getattr(C, att)
            count += 1
            Pass = True
            msg = ""
            info = infos.get(name, {}).get(att, False)
            if info:
                success += 1
                color = "yellow"
                msg = info
            else:
                try:
                    Obj()
                    success += 1
                except:
                    Pass = False
                    if verbose:
                        error = traceback.format_exc().strip().split("\n")
                        msg = "\n\t|\t" + "\n\t|\t".join(error)
            color = "red" if not Pass else "green"
            termcolor.cprint(f" done ({'ok' if Pass else 'Not ok'})", color=color)
            if msg:
                print(msg)
                print()
        print()
        tot_count += count
        tot_success += success
        print(f"Result {success}/{count}. Globally {tot_success}/{tot_count}")
        print("=" * 80)
        print()
        if stop_after_errors and (stop_after_errors + tot_success - tot_count < 0):
            return class_to_mock
        last_class = class_to_mock
    return last_class
