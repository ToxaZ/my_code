__author__ = 'ToxaZ'
# Simple script to get the number of listens or purchases for sequence of ids from Hive

import pyhs2

def id_split(id):
    """Splitting sequence of id's to the Hive condition"""
    sid = id.split()
    kid = ""

    # creating condition
    try:
        for each in sid[0:-1]:
            kid += 'src_id = %d or ' % (int(each))
        kid = '%ssrc_id = %s' % (kid, sid[-1])
        return kid
    except:
        return "Please provide space delimited sequence"

def listen(id):
    """Returning the number of playevents longer than 30 sec with ok flag for certain ids"""

    #splitting ids
    cid = id_split(id)

    # uncomment the line below to print created Hive query
    # print ('select count(1), src_id from playevent where %s and play_duration > 30 and ok_flag group by src_id;' % (cid))

    # connecting to Hive, sending query, returning results of query
    conn = pyhs2.connect(host='nif-nif.zvq.me', port=10000, authMechanism="NOSASL", user='hive', password='test',
                         database='default')
    cur = conn.cursor()
    cur.execute(
        'select count(1), src_id from playevent where %s and play_duration > 30 and ok_flag group by src_id' % (cid))
    results = cur.fetch()
    cur.close()
    conn.close()
    return results

def purchase(id, purchase_type):
    """Returning the number of purchases for certain ids. Type of purchase (release or track) is needed"""

    # testing if purchase type is correct
    if purchase_type == 'release':
        ctype = 'release_id'
    elif purchase_type == 'track':
        ctype = 'track_id'
    else:
        raise AttributeError("provide valid purchase_type: 'release' or 'track'")

    #splitting ids
    cid = id_split(id)

    # uncomment the line below to print created Hive query
    # print ('select count(transaction_id), %s from purchase where %s group by %s;' % (ctype, cid, ctype))

    # connecting to Hive, sending query, returning results of query
    conn = pyhs2.connect(host='nif-nif.zvq.me', port=10000, authMechanism="NOSASL", user='hive', password='test',
                         database='default')
    cur = conn.cursor()
    cur.execute('select count(transaction_id), %s from purchase where %s group by %s' % (ctype, cid, ctype))
    results = cur.fetch()
    cur.close()
    conn.close()
    return results