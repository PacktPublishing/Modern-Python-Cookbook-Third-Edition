#!/usr/bin/env python
# coding: utf-8

# Python Cookbook, 3rd Ed.
#
# Chapter 14, Application Integration: Combination
# Markov Summary
#

# In[1]:


from collections import Counter
import csv
from pathlib import Path


def main() -> None:
    # In[2]:

    outcome_counts = Counter()
    lengths = {
        "Fail": Counter(),
        "Success": Counter(),
    }

    # In[3]:

    for source in Path("data/ch14").glob("*.csv"):
        with source.open() as source_file:
            line_iter = iter(source_file)
            # Skip past the header
            for line in line_iter:
                if "-----" in line:
                    break
                # print(line.rstrip())
            reader = csv.DictReader(line_iter)
            for sample in reader:
                outcome_counts[sample["outcome"]] += 1
                lengths[sample["outcome"]][int(sample["length"])] += 1

    # In[4]:

    print(dict(outcome_counts))
    for k, v in lengths.items():
        print((k, dict(v)))

    # In[5]:

    def tabulate(label: str, value: str, mapping: dict[str, int]) -> None:
        hline2 = f"+{'='*10}+{'='*10}+"
        hline1 = f"+{'-'*10}+{'-'*10}+"

        print(hline2)
        print(f"| {label:^8s} | {value:^8s} |")
        for k, v in sorted(mapping.items()):
            print(hline1)
            print(f"| {str(k):<8s} | {v:>8d} |")
        print(hline2)

    # In[6]:

    tabulate("Outcome", "Count", outcome_counts)

    # In[7]:

    print("## Fail Chains")
    tabulate("len", "Count", lengths["Fail"])
    print()
    print("## Success Chains")
    tabulate("len", "Count", lengths["Success"])
    print()


if __name__ == "__main__":
    main()
