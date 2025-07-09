# coding=utf-8

__author__ = 'a_baradulkin'
import json


def aveg(koefs):
    res = 1
    for k in koefs:
        res -= 1. / k
    return res


result_events = {}


def add_result(site, site_events):
    global result_events
    i = 0
    for name, values in site_events.items():
        i += 1
        is_match = False
        sim_limit = 0.75
        match_key = ""
        for key in result_events:
            if (site not in result_events[key].keys()) and (similar(name, key) > sim_limit):
                is_match = True
                match_key = key
                sim_limit = similar(name, key)
        if is_match:
            result_events[match_key].update({site: values, "sim": sim_limit})
        else:
            result_events[name] = {site: values, "sim": sim_limit}

def add_result2(site, site_events):
    global result_events
    for name, values in site_events.items():
        sim_limit = 0.85
        is_match = False
        for key in result_events:
            if (site not in result_events[key].keys()) and (similar(name, key) >= result_events[key]['sim']):
                result_events[key].update({site: values, "sim": similar(name, key)})
                is_match = True
        if not is_match:
            result_events[name] = {site: values, "sim": sim_limit}


def similar(a, b):
    from difflib import SequenceMatcher

    return SequenceMatcher(None, a, b).ratio()


if __name__ == '__main__':
    from pprint import pprint

    for site in ['1xbet', 'favbet', 'parimatch']:
        site_events = json.load(open("{}.txt".format(site)))
        print "{} site events = {}".format(site, len(site_events))
        add_result(site, site_events)
        print "Total events = {}".format(len(result_events))

    for event, values in result_events.iteritems():
        total = [1, 1, 1]
        for i in range(3):
            for site, koefs in values.iteritems():
                if site != 'sim':
                    total[i] = max(total[i], koefs[i])
        if aveg(total) > 0:
            print "Name", event
            print "Value", aveg(total)
            print "Best:", total
            for name, koefs in values.iteritems():
                print name, koefs
            print
            print