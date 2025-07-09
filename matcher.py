# coding=utf-8

__author__ = 'a_baradulkin'
import json

if __name__ == '__main__':
    result2 = json.load(open("фавбет.txt"))
    result1 = json.load(open("1xbet.txt"))

    print len(result1), len(result2)
    count = 0
    for key, value1 in result1.items():
        value2 = result2.get(key)
        if value2:
            res = []
            for a, b in zip(value1, value2):
                res.append(max(a, b))
            res = ' '.join(res)
            print "Key: {}\n\t{}".format(key, res)
            count += 1
            #print key
    print count
