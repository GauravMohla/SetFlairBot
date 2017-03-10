#!/usr/bin/python
import praw
import pdb
import re
import os
import datetime
import time


# Reddit instance
reddit = praw.Reddit('bot1')

while True:
    systime = time.mktime(datetime.datetime.today().timetuple())
    #print (systime)
    yesterday = time.mktime((datetime.datetime.today() - datetime.timedelta(1)).timetuple())
    #print (yesterday)
    
    flag = True
    
    # Get the subreddit
    subreddit = reddit.subreddit('stubred')
    for submission in subreddit.submissions(int(yesterday), int(systime)):
        print("The title of submission is: ", submission.title," and the author is: ", submission.author)
        if submission.link_flair_text in ['Waiting on OP']:
            print("The flair is already set")
            continue
        chois = submission.comments
        if not chois:
            print("No comments")
            continue
        for comment_id in chois:
            if len(chois) == 1:
                if comment_id.author == "AutoModerator":
                    print("Only AutoModerator has replied")
                    flag = False
                    continue
            #print("Hi There ", comment_id.author)
            if comment_id.author == submission.author:
                print("Author has replied")
                flag = False
                continue
            for second_level_comment in comment_id.replies:
                if not second_level_comment:
                    print("No replies")
                    continue
                if second_level_comment.author == submission.author:
                    print("OP posted a reply to comment")
                    flag = False
                    continue
                #print(second_level_comment.body, " ", second_level_comment.author)
                
        if flag:
            # Change the flair
            choices = submission.flair.choices()
            template_id = next(x for x in choices
            if x['flair_text_editable'])['flair_template_id']
            print("Setting flair")
            submission.flair.select(template_id, 'Waiting on OP')
    #Sleep for 15 minutes
    time.sleep(15*60)