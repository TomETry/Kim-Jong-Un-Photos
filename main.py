#main.py
#/usr/bin/env python3
'''Often, the best way to annoy your friends is to send them pictures of Kim Jong-Un looking at things

This module helps you do just that'''


import pickle
import emailer
import kim_photo
import argparse
import re
import os
import sys

PATH = os.getcwd()
EMAIL_CHECK_REGEX = re.compile(".+@.+\..+")


class CheckEmail(argparse.Action):
    '''A subclass of Action to check whether an arg is a valid e-mail address'''
    def __call__(self, parser, namespace, values, option_string=None):
        if EMAIL_CHECK_REGEX.match(values):
            setattr(namespace, self.dest, values)
        else:
            raise ValueError("{} does not appear to be a valid e-mail address, which is required for {}".format(values,
                                                                                       self.dest))


def check_new(tar_photo, recipient_email):
    '''Return True if photo has not been sent to recipient_email'''
    if not isinstance(tar_photo, kim_photo.KimPhoto):
        raise TypeError("{} not a KimPhoto".format(photo.__str__))
    if EMAIL_CHECK_REGEX.match(recipient_email) is None:
        raise ValueError("{} must be a valid e-mail address".format(recipient_email))
    if not os.path.isfile(PATH+"/hist.log"):
        return True
    with open(PATH+"/hist.log", "rb") as f:
        log = pickle.load(f)
        if log[recipient_email] == tar_photo.src:
                print("[+]\t{} has already seen the most recent Kim photo".format(recipient_email))
                quit()
        else:
            return True
         
        
            
    
    
parser = argparse.ArgumentParser(usage='A program to annoy someone by sending them pictures of Kim Jong-Un looking at things.')
parser.add_argument('recipient',
                    help = 'Name of the person to whom the email is sent')
parser.add_argument('recipient e-mail',
                    help = 'E-mail address of the person to whom the email is sent',
                    action = CheckEmail)
parser.add_argument('sender',
                    help = 'Name of the sender of the e-mail')
parser.add_argument('sender e-mail',
                    help = 'E-mail address of the sender of the e-mail',
                    action = CheckEmail)
parser.add_argument('sender mail server',
                    help = 'Sender\'s mail server')
parser.add_argument('sender mail server password',
                    help = 'Sender\'s mail server password')

args = parser.parse_args()

new_photo = kim_photo.KimPhoto(kim_photo.get_newest_photo())
check_new(new_photo, args.__getattribute__("recipient e-mail"))

message = emailer.KimMail(new_photo, 
                          args.__getattribute__("recipient"),
                          args.__getattribute__("recipient e-mail"),
                          args.__getattribute__("sender"),
                          args.__getattribute__("sender e-mail"),
                          args.__getattribute__("sender mail server"),
                          args.__getattribute__("sender mail server password"))


message.send()

