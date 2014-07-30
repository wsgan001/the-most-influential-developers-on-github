# -*- coding: utf-8 -*-


def loads_invalid_obj_list(s):
    from json import JSONDecoder

    decoder = JSONDecoder()
    s_len = len(s)
    objs = []
    end = 0

    while end != s_len:
        obj, end = decoder.raw_decode(s, idx=end)
        objs.append(obj)

    return objs


def grab():
    from gzip import GzipFile
    from urlgrabber import urlopen
    from datetime import datetime, timedelta

    from_time = datetime(2011, 2, 12, 0)
    # from_time = datetime(2011, 3, 15, 21)
    to_time = datetime(2014, 7, 29, 0)
    time_strs = [(from_time + timedelta(hours=x)).strftime(
        '%Y-%m-%d-%-H') for x in range(0, int(
            (to_time - from_time).total_seconds() / 3600))]

    for time_str in time_strs:
        url = 'http://data.githubarchive.org/%s.json.gz' % time_str

        with GzipFile(fileobj=urlopen(url)) as gz_file:
            events = loads_invalid_obj_list(''.join(
                map(lambda x: unicode(x, 'ISO-8859-1'), map(
                    lambda x: x.strip(), list(gz_file)))))

            well_defined_events = filter(
                lambda x: x['type'] == 'WatchEvent'
                and x['actor'].get('login', False), events)

            watch_events = map(
                lambda x: (
                    x['actor']['login'], x['repo']['name'], x['created_at']),
                well_defined_events)

            print watch_events, time_str
            # print (map(lambda x: x[1].get('login', False), watch_events))


grab()
