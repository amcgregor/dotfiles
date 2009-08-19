#  PyDigg
#
#  Python toolkit for the Digg.com API
#  http://neothoughts.com/pydigg
#
#  Author: Derek van Vliet <derek@neothoughts.com>
#  Copyright: Copyright (c) 2007 Derek van Vliet
#  License: MIT <http://www.opensource.org/licenses/mit-license.php>
#
#  Documentation: http://neothoughts.com/pydigg
#  Digg API Documentation: http://apidoc.digg.com
#
#  TODO: Fix some weirdness introduced by new Digg features, like
#        currently unsupported Dialogg comments.

from urllib import urlencode, urlopen
from xml.dom import minidom

class Bag: pass

class Digg(object):
    def __init__(self, appkey):
        self.__appkey = str(appkey)
        
    appkey = property(lambda self: self.__appkey)    
    
    def getErrors(self):
        data = self._get('/errors')
        errors = Digg.Errors(data.errors.timestamp)
        for error in data.errors.error:
            errors.append(Digg.Error(error.code, error.message))
        return errors
    
    def getError(self,
                 code):
        data = self._get('/error/' + str(code))
        return Digg.Error(data.errors.error.code, data.errors.error.message)

    def getDiggs(self,
                 min_date='',
                 max_date='',
                 sort='date-desc',
                 count='25',
                 offset='0'):
        data = self._get('/stories/diggs',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))
        return self._parseDiggs(data)
    
    def getContainerDiggs(self,
                          container_name,
                          min_date='',
                          max_date='',
                          sort='date-desc',
                          count='25',
                          offset='0'):
        data = self._get('/stories/container/' + container_name + '/diggs',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))
        return self._parseDiggs(data)
    
    def getPopularDiggs(self,
                        min_date='',
                        max_date='',
                        sort='date-desc',
                        count='25',
                        offset='0'):
        data = self._get('/stories/popular/diggs',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))
        return self._parseDiggs(data)

    def getUpcomingDiggs(self,
                         min_date='',
                         max_date='',
                         sort='date-desc',
                         count='25',
                         offset='0'):
        data = self._get('/stories/upcoming/diggs',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))
        return self._parseDiggs(data)
    
    def getStoryDiggs(self,
                      story_id,
                      min_date='',
                      max_date='',
                      sort='date-desc',
                      count='25',
                      offset='0'):
        data = self._get('/story/' + str(story_id) + '/diggs',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))
        return self._parseDiggs(data)

    def getStoriesDiggs(self,
                        story_ids,
                        min_date='',
                        max_date='',
                        sort='date-desc',
                        count='25',
                        offset='0'):
        data = self._get('/stories/' + str(story_ids) + '/diggs',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))
        return self._parseDiggs(data)
   
    def getUserDiggs(self,
                     user_name,
                     min_date='',
                     max_date='',
                     sort='date-desc',
                     count='25',
                     offset='0'):
        data = self._get('/user/' + user_name + '/diggs',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))
        return self._parseDiggs(data)
    
    def getUsersDiggs(self,
                      user_names,
                      min_date='',
                      max_date='',
                      sort='date-desc',
                      count='25',
                      offset='0'):
        data = self._get('/users/' + user_names + '/diggs',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))
        return self._parseDiggs(data)
    
    def getStoryUserDigg(self,
                         story_id,
                         user_name,
                         min_date='',
                         max_date='',
                         sort='date-desc',
                         count='25',
                         offset='0'):
        data = self._get('/story/' + str(story_id) + '/user/' + user_name + '/digg',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))
        return self._parseDiggs(data)

    def getComments(self,
                    min_date='',
                    max_date='',
                    sort='date-desc',
                    count='25',
                    offset='0'):
        data = self._get('/stories/comments',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))        
        return self._parseComments(data)

    def getPopularComments(self,
                           min_date='',
                           max_date='',
                           sort='date-desc',
                           count='25',
                           offset='0'):
        data = self._get('/stories/popular/comments',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))        
        return self._parseComments(data)

    def getUpcomingComments(self,
                            min_date='',
                            max_date='',
                            sort='date-desc',
                            count='25',
                            offset='0'):
        data = self._get('/stories/upcoming/comments',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))        
        return self._parseComments(data)
    
    def getStoryComment(self,
                        story_id,
                        comment_id,
                        min_date='',
                        max_date='',
                        sort='date-desc',
                        count='25',
                        offset='0'):
        data = self._get('/story/' + str(story_id) + '/comment/' + str(comment_id),min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))        
        return self._parseComments(data)
    
    def getStoryComments(self,
                         story_id,
                         min_date='',
                         max_date='',
                         sort='date-desc',
                         count='25',
                         offset='0'):
        data = self._get('/story/' + str(story_id) + '/comments',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))        
        return self._parseComments(data)

    def getStoriesComments(self,
                           story_ids,
                           min_date='',
                           max_date='',
                           sort='date-desc',
                           count='25',
                           offset='0'):
        data = self._get('/stories/' + story_ids + '/comments',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))        
        return self._parseComments(data)
    
    def getUserComments(self,
                        user_name,
                        min_date='',
                        max_date='',
                        sort='date-desc',
                        count='25',
                        offset='0'):
        data = self._get('/user/' + user_name + '/comments',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))        
        return self._parseComments(data)
    
    def getUsersComments(self,
                         user_names,
                         min_date='',
                         max_date='',
                         sort='date-desc',
                         count='25',
                         offset='0'):
        data = self._get('/users/' + user_names + '/comments',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))        
        return self._parseComments(data)
    
    def getCommentReplies(self,
                          story_id,
                          comment_id,
                          min_date='',
                          max_date='',
                          sort='date-desc',
                          count='25',
                          offset='0'):
        data = self._get('/story/' + str(story_id) + '/comment/' + str(comment_id) + '/replies',min_date=str(min_date),max_date=str(max_date),sort=sort,count=str(count),offset=str(offset))        
        return self._parseComments(data)

    def getStories(self,
                   min_submit_date='',
                   max_submit_date='',
                   min_promote_date='',
                   max_promote_date='',
                   sort='submit_date-desc',
                   count='10',
                   offset='0',
                   domain='',
                   link=''):
        data = self._get('/stories',min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getPopularStories(self,
                          min_submit_date='',
                          max_submit_date='',
                          min_promote_date='',
                          max_promote_date='',
                          sort='promote_date-desc',
                          count='10',
                          offset='0',
                          domain='',
                          link=''):
        data = self._get('/stories/popular',min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getUpcomingStories(self,
                           min_submit_date='',
                           max_submit_date='',
                           min_promote_date='',
                           max_promote_date='',
                           sort='submit_date-desc',
                           count='10',
                           offset='0',
                           domain='',
                           link=''):
        data = self._get('/stories/upcoming',min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getContainerStories(self,
                            container_name,
                            min_submit_date='',
                            max_submit_date='',
                            min_promote_date='',
                            max_promote_date='',
                            sort='submit_date-desc',
                            count='10',
                            offset='0',
                            domain='',
                            link=''):
        data = self._get('/stories/container/' + container_name,min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getContainerPopularStories(self,
                                   container_name,
                                   min_submit_date='',
                                   max_submit_date='',
                                   min_promote_date='',
                                   max_promote_date='',
                                   sort='promote_date-desc',
                                   count='10',
                                   offset='0',
                                   domain='',
                                   link=''):
        data = self._get('/stories/container/' + container_name + '/popular',min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getContainerUpcomingStories(self,
                                    container_name,
                                    min_submit_date='',
                                    max_submit_date='',
                                    min_promote_date='',
                                    max_promote_date='',
                                    sort='submit_date-desc',
                                    count='10',
                                    offset='0',
                                    domain='',
                                    link=''):
        data = self._get('/stories/container/' + container_name + '/upcoming',min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getTopicStories(self,
                        topic_name,
                        min_submit_date='',
                        max_submit_date='',
                        min_promote_date='',
                        max_promote_date='',
                        sort='submit_date-desc',
                        count='10',
                        offset='0',
                        domain='',
                        link=''):
        data = self._get('/stories/topic/' + topic_name,min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getTopicPopularStories(self,
                               topic_name,
                               min_submit_date='',
                               max_submit_date='',
                               min_promote_date='',
                               max_promote_date='',
                               sort='promote_date-desc',
                               count='10',
                               offset='0',
                               domain='',
                               link=''):
        data = self._get('/stories/topic/' + topic_name + '/popular',min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getTopicUpcomingStories(self,
                                topic_name,
                                min_submit_date='',
                                max_submit_date='',
                                min_promote_date='',
                                max_promote_date='',
                                sort='submit_date-desc',
                                count='10',
                                offset='0',
                                domain='',
                                link=''):
        data = self._get('/stories/topic/' + topic_name + '/upcoming',min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getStoryByID(self,
                     story_id,
                     min_submit_date='',
                     max_submit_date='',
                     min_promote_date='',
                     max_promote_date='',
                     sort='submit_date-desc',
                     count='10',
                     offset='0',
                     domain='',
                     link=''):
        data = self._get('/story/' + str(story_id),min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)
    
    def getStoryByCleanTitle(self,
                             clean_title,
                             min_submit_date='',
                             max_submit_date='',
                             min_promote_date='',
                             max_promote_date='',
                             sort='submit_date-desc',
                             count='10',
                             offset='0',
                             domain='',
                             link=''):
        data = self._get('/story/' + clean_title,min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getStoriesByID(self,
                       story_ids,
                       min_submit_date='',
                       max_submit_date='',
                       min_promote_date='',
                       max_promote_date='',
                       sort='submit_date-desc',
                       count='10',
                       offset='0',
                       domain='',
                       link=''):
        data = self._get('/stories/' + story_ids,min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getUserSubmissions(self,
                           user_name,
                           min_submit_date='',
                           max_submit_date='',
                           min_promote_date='',
                           max_promote_date='',
                           sort='submit_date-desc',
                           count='10',
                           offset='0',
                           domain='',
                           link=''):
        data = self._get('/user/' + user_name + '/submissions',min_submit_date=str(min_submit_date),max_submit_date=str(max_submit_date),min_promote_date=str(min_promote_date),max_promote_date=str(max_promote_date),sort=sort,count=str(count),offset=str(offset),domain=domain,link=link)
        return self._parseStories(data)

    def getTopics(self):
        data = self._get('/topics')
        return self._parseTopics(data)

    def getTopic(self,
                 short_name):
        data = self._get('/topic/' + short_name)
        return self._parseTopics(data)

    def getUsers(self,
                 sort='username-desc',
                 count='10',
                 offset='0'):
        data = self._get('/users',sort=sort,count=str(count),offset=str(offset))
        return self._parseUsers(data)

    def getUser(self,
                user_name,
                sort='username-desc',
                count='10',
                offset='0'):
        data = self._get('/user/' + user_name,sort=sort,count=str(count),offset=str(offset))
        return self._parseUsers(data)

    def getUserFriends(self,
                       user_name,
                       sort='username-desc',
                       count='10',
                       offset='0'):
        data = self._get('/user/' + user_name + '/friends',sort=sort,count=str(count),offset=str(offset))
        return self._parseUsers(data)

    def getUserFriend(self,
                      user_name,
                      friend_user_name,
                      sort='username-desc',
                      count='10',
                      offset='0'):
        data = self._get('/user/' + user_name + '/friend/' + friend_user_name,sort=sort,count=str(count),offset=str(offset))
        return self._parseUsers(data)

    def getUserFans(self,
                    user_name,
                    sort='username-desc',
                    count='10',
                    offset='0'):
        data = self._get('/user/' + user_name + '/fans',sort=sort,count=str(count),offset=str(offset))
        return self._parseUsers(data)

    def getUserFan(self,
                   user_name,
                   fan_user_name,
                   sort='username-desc',
                   count='10',
                   offset='0'):
        data = self._get('/user/' + user_name + '/fan/' + fan_user_name,sort=sort,count=str(count),offset=str(offset))
        return self._parseUsers(data)
    
    class Error(Exception):
        def __init__(self,
                     code,
                     message):

            self.__code = code
            self.__message = message
        
        def __str__(self):
            return "Error(%s, %s)" % (self.__code, self.__message)
        
        code = property(lambda self: self.__code)
        message = property(lambda self: self.__message)

    class Errors(list):
        def __init__(self,
                     timestamp):
            
            self.__timestamp = timestamp

        timestamp = property(lambda self: self.__timestamp)

    class Digg(object):
        def __init__(self,
                     app,
                     date,
                     story,
                     id,
                     user,
                     status):
            
            self.__app = app
            self.__date = date
            self.__story = story
            self.__id = id
            self.__user = user
            self.__status = status

        date = property(lambda self: self.__date)
        story = property(lambda self: self.__story)
        id = property(lambda self: self.__id)
        user = property(lambda self: self.__user)
        status = property(lambda self: self.__status)

        def getStory(self):
            return self.__app.getStoryByID(self.story)

        def getUser(self):
            return self.__app.getUser(self.user)

    class Comment(object):
        def __init__(self,
                     app,
                     date,
                     story,
                     id,
                     up,
                     down,
                     replies,
                     user,
                     content):
            
            self.__app = app
            self.__date = date
            self.__story = story
            self.__id = id
            self.__up = int(up)
            self.__down = int(down)
            self.__replies = int(replies)
            self.__user = user
            self.__content = content

        date = property(lambda self: self.__date)
        story = property(lambda self: self.__story)
        id = property(lambda self: self.__id)
        up = property(lambda self: self.__up)
        down = property(lambda self: self.__down)
        replies = property(lambda self: self.__replies)
        user = property(lambda self: self.__user)
        content = property(lambda self: self.__content)

        def getReplies(self,
                       min_date='',
                       max_date='',
                       sort='date-desc',
                       count='25',
                       offset='0'):
            return self.__app.getCommentReplies(self.story, self.id, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))

        def getStory(self):
            return self.__app.getStoryByID(self.story)

        def getUser(self):
            return self.__app.getUser(self.user)

    class Events(list):
        def __init__(self,
                     app,
                     timestamp,
                     min_date,
                     max_date,
                     total,
                     offset,
                     count):
            
            self.__app = app
            self.__timestamp = timestamp
            self.__min_date = min_date
            self.__max_date = max_date
            self.__total = total
            self.__offset = offset
            self.__count = count

        timestamp = property(lambda self: self.__timestamp)
        min_date = property(lambda self: self.__min_date)
        max_date = property(lambda self: self.__max_date)
        total = property(lambda self: self.__total)
        offset = property(lambda self: self.__offset)
        count = property(lambda self: self.__count)

        def getStories(self,
                       min_submit_date='',
                       max_submit_date='',
                       min_promote_date='',
                       max_promote_date='',
                       sort='submit_date-desc',
                       count='10',
                       offset='0',
                       domain='',
                       link=''):
            ids = ','.join([event.story for event in self])
            return self.__app.getStoriesByID(ids, min_submit_date=min_submit_date, max_submit_date=max_submit_date, min_promote_date=min_promote_date, max_promote_date=max_promote_date, sort=sort, count=str(count), offset=str(offset), domain=domain, link=link)

    class Story(object):
        def __init__(self,
                     app,
                     id,
                     link,
                     submit_date,
                     diggs,
                     comments,
                     href,
                     status,
                     title,
                     description,
                     user_name,
                     user_icon,
                     user_registered,
                     user_profileviews,
                     topic_name,
                     topic_short_name,
                     container_name,
                     container_short_name):
            
            self.__app = app
            self.__id = id
            self.__link = link
            self.__submit_date = submit_date
            self.__diggs = int(diggs)
            self.__comments = int(comments)
            self.__href = href
            self.__status = status
            self.__title = title
            self.__description = description
            self.__user_name = user_name
            self.__user_icon = user_icon
            self.__user_registered = user_registered
            self.__user_profileviews = user_profileviews
            self.__topic_name = topic_name
            self.__topic_short_name = topic_short_name
            self.__container_name = container_name
            self.__container_short_name = container_short_name

        id = property(lambda self: self.__id)
        link = property(lambda self: self.__link)
        submit_date = property(lambda self: self.__submit_date)
        diggs = property(lambda self: self.__diggs)
        comments = property(lambda self: self.__comments)
        href = property(lambda self: self.__href)
        status = property(lambda self: self.__status)
        title = property(lambda self: self.__title)
        description = property(lambda self: self.__description)
        user_name = property(lambda self: self.__user_name)
        user_icon = property(lambda self: self.__user_icon)
        user_registered = property(lambda self: self.__user_registered)
        user_profileviews = property(lambda self: self.__user_profileviews)
        topic_name = property(lambda self: self.__topic_name)
        topic_short_name = property(lambda self: self.__topic_short_name)
        container_name = property(lambda self: self.__container_name)
        container_short_name = property(lambda self: self.__container_short_name)

        def getDiggs(self,
                     min_date='',
                     max_date='',
                     sort='date-desc',
                     count='25',
                     offset='0'):
            return self.__app.getStoryDiggs(self.id, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))

        def getUserDigg(self,
                        user_name,
                        min_date='',
                        max_date='',
                        sort='date-desc',
                        count='25',
                        offset='0'):
            return self.__app.getStoryUserDigg(self.id, user_name, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))

        def getComment(self,
                       comment_id,
                       min_date='',
                       max_date='',
                       sort='date-desc',
                       count='25',
                       offset='0'):
            return self.__app.getStoryComment(self.id, comment_id, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))

        def getComments(self,
                        min_date='',
                        max_date='',
                        sort='date-desc',
                        count='25',
                        offset='0'):
            return self.__app.getStoryComments(self.id, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))

        def getSubmitter(self):
            return Digg.User(self.__app, self.user_name, self.user_icon, self.user_registered, self.user_profileviews)

        def getTopic(self):
            return Digg.Topic(self.__app, self.topic_name, self.topic_short_name, self.container_name, self.container_short_name)
        
    class Stories(list):
        def __init__(self,
                     app,
                     timestamp,
                     min_date,
                     max_date,
                     total,
                     offset,
                     count):
            
            self.__app = app
            self.__timestamp = timestamp
            self.__min_date = min_date
            self.__max_date = max_date
            self.__total = total
            self.__offset = offset
            self.__count = count
            
        timestamp = property(lambda self: self.__timestamp)
        min_date = property(lambda self: self.__min_date)
        max_date = property(lambda self: self.__max_date)
        total = property(lambda self: self.__total)
        offset = property(lambda self: self.__offset)
        count = property(lambda self: self.__count)

        def getDiggs(self,
                     min_date='',
                     max_date='',
                     sort='date-desc',
                     count='25',
                     offset='0'):
            ids = ','.join([story.id for story in self])
            return self.__app.getStoriesDiggs(ids, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))

        def getComments(self,
                        min_date='',
                        max_date='',
                        sort='date-desc',
                        count='25',
                        offset='0'):
            ids = ','.join([story.id for story in self])
            return self.__app.getStoriesComments(ids, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))

        def getSubmitters(self):
            users = Digg.Users(self.__app, self.timestamp, 0, 0, len(self))
            for story in self:
                users.append(Digg.User(self.__app, story.user_name, story.user_icon, story.user_registered, story.user_profileviews))
            return users

        def getTopics(self):
            topics = Digg.Topics(self.timestamp)
            for story in self:
                topics.append(Digg.Topic(self.__app, story.topic_name, story.topic_short_name, story.container_name, story.container_short_name))
            return topics

    class Topic(object):
        def __init__(self,
                     app,
                     name,
                     short_name,
                     container_name,
                     container_short_name):
            
            self.__app = app
            self.__name = name
            self.__short_name = short_name
            self.__container_name = container_name
            self.__container_short_name = container_short_name

        name = property(lambda self: self.__name)
        short_name = property(lambda self: self.__short_name)
        container_name = property(lambda self: self.__container_name)
        container_short_name = property(lambda self: self.__container_short_name)
        
        def getStories(self,
                       min_submit_date='',
                       max_submit_date='',
                       min_promote_date='',
                       max_promote_date='',
                       sort='submit_date-desc',
                       count='10',
                       offset='0',
                       domain='',
                       link=''):
            return self.__app.getTopicStories(self.short_name, min_submit_date=min_submit_date, max_submit_date=max_submit_date, min_promote_date=min_promote_date, max_promote_date=max_promote_date, sort=sort, count=str(count), offset=str(offset), domain=domain, link=link)
        
        def getPopularStories(self,
                              min_submit_date='',
                              max_submit_date='',
                              min_promote_date='',
                              max_promote_date='',
                              sort='promote_date-desc',
                              count='10',
                              offset='0',
                              domain='',
                              link=''):
            return self.__app.getTopicPopularStories(self.short_name, min_submit_date=min_submit_date, max_submit_date=max_submit_date, min_promote_date=min_promote_date, max_promote_date=max_promote_date, sort=sort, count=str(count), offset=str(offset), domain=domain, link=link)
        
        def getUpcomingStories(self,
                               min_submit_date='',
                               max_submit_date='',
                               min_promote_date='',
                               max_promote_date='',
                               sort='submit_date-desc',
                               count='10',
                               offset='0',
                               domain='',
                               link=''):
            return self.__app.getTopicUpcomingStories(self.short_name, min_submit_date=min_submit_date, max_submit_date=max_submit_date, min_promote_date=min_promote_date, max_promote_date=max_promote_date, sort=sort, count=str(count), offset=str(offset), domain=domain, link=link)

        def getContainerStories(self,
                                min_submit_date='',
                                max_submit_date='',
                                min_promote_date='',
                                max_promote_date='',
                                sort='submit_date-desc',
                                count='10',
                                offset='0',
                                domain='',
                                link=''):
            return self.__app.getContainerStories(self.container_short_name, min_submit_date=min_submit_date, max_submit_date=max_submit_date, min_promote_date=min_promote_date, max_promote_date=max_promote_date, sort=sort, count=str(count), offset=str(offset), domain=domain, link=link)
        
        def getContainerPopularStories(self,
                                       min_submit_date='',
                                       max_submit_date='',
                                       min_promote_date='',
                                       max_promote_date='',
                                       sort='promote_date-desc',
                                       count='10',
                                       offset='0',
                                       domain='',
                                       link=''):
            return self.__app.getContainerPopularStories(self.container_short_name, min_submit_date=min_submit_date, max_submit_date=max_submit_date, min_promote_date=min_promote_date, max_promote_date=max_promote_date, sort=sort, count=str(count), offset=str(offset), domain=domain, link=link)

        def getContainerUpcomingStories(self,
                                        min_submit_date='',
                                        max_submit_date='',
                                        min_promote_date='',
                                        max_promote_date='',
                                        sort='submit_date-desc',
                                        count='10',
                                        offset='0',
                                        domain='',
                                        link=''):
            return self.__app.getContainerUpcomingStories(self.container_short_name, min_submit_date=min_submit_date, max_submit_date=max_submit_date, min_promote_date=min_promote_date, max_promote_date=max_promote_date, sort=sort, count=str(count), offset=str(offset), domain=domain, link=link)
        
    class Topics(list):
        def __init__(self,
                     timestamp):
            
            self.__timestamp = timestamp

        timestamp = property(lambda self: self.__timestamp)

    class User(object):
        def __init__(self,
                     app,
                     name,
                     icon,
                     registered,
                     profileviews):
            
            self.__app = app
            self.__name = name
            self.__icon = icon
            self.__registered = registered
            self.__profileviews = profileviews

        name = property(lambda self: self.__name)
        icon = property(lambda self: self.__icon)
        registered = property(lambda self: self.__registered)
        profileviews = property(lambda self: self.__profileviews)

        def getDiggs(self,
                     min_date='',
                     max_date='',
                     sort='date-desc',
                     count='25',
                     offset='0'):
            return self.__app.getUserDiggs(self.name, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))

        def getStoryDigg(self,
                         story_id,
                         min_date='',
                         max_date='',
                         sort='date-desc',
                         count='25',
                         offset='0'):
            return self.__app.getStoryUserDigg(story_id, self.name, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))

        def getComments(self,
                        min_date='',
                        max_date='',
                        sort='date-desc',
                        count='25',
                        offset='0'):
            return self.__app.getUserComments(self.name, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))
        
        def getSubmissions(self,
                           min_submit_date='',
                           max_submit_date='',
                           min_promote_date='',
                           max_promote_date='',
                           sort='submit_date-desc',
                           count='10',
                           offset='0',
                           domain='',
                           link=''):
            return self.__app.getUserSubmissions(self.name, min_submit_date=min_submit_date, max_submit_date=max_submit_date, min_promote_date=min_promote_date, max_promote_date=max_promote_date, sort=sort, count=str(count), offset=str(offset), domain=domain, link=link)
        
        def getFriends(self,
                       sort='username-desc',
                       count='10',
                       offset='0'):
            return self.__app.getUserFriends(self.name, sort=sort, count=str(count), offset=str(offset))
        
        def getFriend(self,
                      friend_user_name,
                      sort='username-desc',
                      count='10',
                      offset='0'):
            return self.__app.getUserFriend(self.name, friend_user_name, sort=sort, count=str(count), offset=str(offset))
        
        def getFans(self,
                    sort='username-desc',
                    count='10',
                    offset='0'):
            return self.__app.getUserFans(self.name, sort=sort, count=str(count), offset=str(offset))
        
        def getFan(self,
                   fan_user_name,
                   sort='username-desc',
                   count='10',
                   offset='0'):
            return self.__app.getUserFan(self.name, fan_user_name, sort=sort, count=str(count), offset=str(offset))

    class Users(list):
        def __init__(self,
                     app,
                     timestamp,
                     total,
                     offset,
                     count):
            
            self.__app = app
            self.__timestamp = timestamp
            self.__total = total
            self.__offset = offset
            self.__count = count

        name = property(lambda self: self.__name)
        total = property(lambda self: self.__total)
        offset = property(lambda self: self.__offset)
        count = property(lambda self: self.__count)

        def getDiggs(self,
                     min_date='',
                     max_date='',
                     sort='date-desc',
                     count='25',
                     offset='0'):
            ids = ','.join([user.id for user in self])
            return self.__app.getUsersDiggs(ids, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))

        def getComments(self,
                        min_date='',
                        max_date='',
                        sort='date-desc',
                        count='25',
                        offset='0'):
            ids = ','.join([user.id for user in self])
            return self.__app.getUsersComments(ids, min_date=min_date, max_date=max_date, sort=sort, count=str(count), offset=str(offset))
        
    def _parseDiggs(self,
                    data):
        _min_date = None
        _max_date = None
        if hasattr(data.events, 'min_date'):
            _min_date = data.events.min_date
        if hasattr(data.events, 'max_date'):
            _max_date = data.events.max_date
        events = Digg.Events(self, data.events.timestamp, _min_date, _max_date, data.events.total, data.events.offset, data.events.count)
        if hasattr(data.events, 'digg'):
            if isinstance(data.events.digg, list):
                for digg in data.events.digg:
                    events.append(Digg.Digg(self, digg.date, digg.story, digg.id, digg.user, digg.status))
            else:
                digg = data.events.digg
                events.append(Digg.Digg(self,digg.date, digg.story, digg.id, digg.user, digg.status))
                
        return events
    
    def _parseComments(self,
                       data):
        _min_date = None
        _max_date = None
        if hasattr(data.events, 'min_date'):
            _min_date = data.events.min_date
        if hasattr(data.events, 'max_date'):
            _max_date = data.events.max_date
        events = Digg.Events(self, data.events.timestamp, _min_date, _max_date, data.events.total, data.events.offset, data.events.count)
        if hasattr(data.events, 'comment'):
            if isinstance(data.events.comment, list):
                for comment in data.events.comment:
                    if hasattr(comment, 'story'):
                        events.append(Digg.Comment(self, comment.date, comment.story, comment.id, comment.up, comment.down, comment.replies, comment.user, comment.text))
            else:
                if hasattr(comment, 'story'):
                    comment = data.events.comment
                    events.append(Digg.Comment(self, comment.date, comment.story, comment.id, comment.up, comment.down, comment.replies, comment.user, comment.text))
                
        return events
    
    def _parseStories(self,
                      data):
        _min_date = None
        _max_date = None
        
        if hasattr(data.stories, 'min_date'):
            _min_date = data.stories.min_date
        if hasattr(data.stories, 'max_date'):
            _max_date = data.stories.max_date
        stories = Digg.Stories(self, data.stories.timestamp, _min_date, _max_date, data.stories.total, data.stories.offset, data.stories.count)
        if hasattr(data.stories, 'story'):
            user_name = None
            user_icon = None
            user_registered = None
            user_profileviews = None
            topic_name = None
            topic_short_name = None
            container_name = None
            container_short_name = None
            if isinstance(data.stories.story, list):
                for story in data.stories.story:
                    if hasattr(story, 'user'):
                        user_name = story.user.name
                        user_icon = story.user.icon
                        user_registered = story.user.registered
                        user_profileviews = story.user.profileviews
                    if hasattr(story, 'topic'):
                        topic_name = story.topic.name
                        topic_short_name = story.topic.short_name
                    if hasattr(story, 'container'):
                        container_name = story.container.name
                        container_short_name = story.container.short_name
                    stories.append(Digg.Story(self, story.id, story.link, story.submit_date, story.diggs, story.comments, story.href, story.status, story.title.text, story.description.text, user_name, user_icon, user_registered, user_profileviews, topic_name, topic_short_name, container_name, container_short_name))
            else:
                story = data.stories.story
                if hasattr(story, 'user'):
                    user_name = story.user.name
                    user_icon = story.user.icon
                    user_registered = story.user.registered
                    user_profileviews = story.user.profileviews
                if hasattr(story, 'topic'):
                    topic_name = story.topic.name
                    topic_short_name = story.topic.short_name
                if hasattr(story, 'container'):
                    container_name = story.container.name
                    container_short_name = story.container.short_name
                stories.append(Digg.Story(self, story.id, story.link, story.submit_date, story.diggs, story.comments, story.href, story.status, story.title.text, story.description.text, user_name, user_icon, user_registered, user_profileviews, topic_name, topic_short_name, container_name, container_short_name))
                
        return stories
    
    def _parseTopics(self,
                     data):
        topics = Digg.Topics(data.topics.timestamp)
        if hasattr(data.topics, 'topic'):
            if isinstance(data.topics.topic, list):
                for topic in data.topics.topic:
                    topics.append(Digg.Topic(self, topic.name, topic.short_name, topic.container.name, topic.container.short_name))
            else:
                topic = data.topics.topic
                topics.append(Digg.Topic(self, topic.name, topic.short_name, topic.container.name, topic.container.short_name))
                
        return topics

    def _parseUsers(self,
                    data):
        users = Digg.Users(self, data.users.timestamp, data.users.total, data.users.offset, data.users.count)
        if hasattr(data.users, 'user'):
            if isinstance(data.users.user, list):
                for user in data.users.user:
                    _registered = None
                    _profileviews = None
                    if hasattr(user, 'registered'):
                        _registered = user.registered
                    if hasattr(user, 'profileviews'):
                        _profileviews = user.profileviews
                    users.append(Digg.User(self, user.name, user.icon, _registered, _profileviews))
            else:
                user = data.users.user
                _registered = None
                _profileviews = None
                if hasattr(user, 'registered'):
                    _registered = user.registered
                if hasattr(user, 'profileviews'):
                    _profileviews = user.profileviews
                users.append(Digg.User(self, user.name, user.icon, _registered, _profileviews))
                
        return users

    def _get(self,
             endpoint,
             **params):
        args = {}
        for (key, value) in params.items():
            if len(value) > 0:
                args[key] = value
                
        url = 'http://services.digg.com%s/?appkey=%s&%s' % (endpoint, self.appkey, urlencode(args))

        response = urlopen(url).read()
        response = unicode(response,errors='ignore')
        xml = minidom.parseString(response)
        data = self._unmarshal(xml)
        if hasattr(data, 'error'):
            raise Digg.Error(data.error.code, repr(response)) #, data.error.message)

        return data
    
    def _unmarshal(self,
                   element):
        bag = Bag()
        if isinstance(element, minidom.Element):
            for key in element.attributes.keys():
                setattr(bag, key, element.attributes[key].value)
                
        childElements = [e for e in element.childNodes \
                         if isinstance(e, minidom.Element)]
        if childElements:
            for child in childElements:
                key = child.tagName
                if hasattr(bag, key):
                    if type(getattr(bag, key)) <> type([]):
                        setattr(bag, key, [getattr(bag, key)])
                    setattr(bag, key, getattr(bag, key) + [self._unmarshal(child)])
                elif isinstance(child, minidom.Element) and \
                         (child.tagName == 'Details'):
                    setattr(bag,key,[self._unmarshal(child)])
                else:
                    setattr(bag, key, self._unmarshal(child))
        else:
            text = "".join([e.data for e in element.childNodes \
                            if isinstance(e, minidom.Text)])
            setattr(bag, 'text', text)
        return bag