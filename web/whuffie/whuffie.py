import sys
from subprocess import Popen, PIPE
import simplejson as json
from digg import Digg

digg = Digg('http://www.gothcandy.com/whuffie')



# Iterate through all results for a given query; compound multiple actual queries into one result set.
def gather(kind, *args, **kw):
    kw['count'] = kw.get('count', 25)
    kw['offset'] = kw.get('offset', 0)
    
    while True:
        _ = kind(*args, **kw)
        for i in _: yield i
        
        if len(_) < kw['count']: return
        kw['offset'] += kw['count']


if __name__ == '__main__':
    score = 0
    user = sys.argv[1]
    
    print "---- Submissions"
    print "---- Every digg an article you submit gets, you get one point."
    
    for story in gather(digg.getUserSubmissions, user):
        score += story.diggs
        print ("%7d\t%7d\t%s\033[K\r" % (score, story.diggs, story.title)),
    
    print "\033[K%7d (Sub-Total)\n---- Comments" % (score, )
    print "---- Every comment you make has a score (positive-negative) and replies."
    print "---- Your score is adjusted by the value of each comment, with replies giving bonus points."
    print "---- Less two, as comments cost, so if no-one diggs your comment, you are out one whuffie."
    
    for comment in gather(digg.getUserComments, user, count=50):
        score += comment.up
        score -= comment.down
        score += comment.replies
        score -= 2
        print ("%7d\t%7d\t(+%du -%dd +%dr)\033[K\r" % (score, comment.up - comment.down + comment.replies - 2, comment.up, comment.down, comment.replies)),
    
    print "%7d (Sub-Total)\n---- Diggs" % (score, )
    print "---- By digging something yourself, you are giving away one of your whuffie."
    
    for story in gather(digg.getUserDiggs, user, count=50):
        score -= 1
        print ("%7d\t%7d\t%s\033[K\r" % (score, -1, story.date)),
    
    print "\033[K%7d (Total)" % (score, )
    
    sys.exit(0)