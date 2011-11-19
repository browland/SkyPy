## SkyPy - A simple Skype Bot.
## ---------------------------
##
## Requires a Skype Client to be running locally.
##
## Once the Skype Client is up, run this script as a separate process
## (e.g. on the command line).
##
## This script will then wait for events from the Skype client and respond to them.
## The responses from the bot will appear to originate from the user
## logged in to the local Skype client.
##
## Initial support provided for a '!time' command.  E.g.:
##
## [12:55:56] Ben Rowland: !time
## [12:55:56] Ben Rowland: SkyPy says: Sat, 19 Nov 2011 12:55:56 +0000
##

## Required for the bot to function
import Skype4Py

## Just for our '!time' command
from time import gmtime, strftime

## Name of this bot
botName = 'SkyPy'

## White-List of Chat Topics this bot will respond to.
## If this list is populated with at least one string, then this bot will only
## respond to messages in chats with a matching topic.
chatTopicWhiteList = []

## White-List of Handles who should see messages from this bot.
## If this list is populated with at least one string, then this bot will only
## respond to messages in chats where *all* users are in this white-list.
userWhiteList = []

## Whether the bot should dump messages it will respond to (for debugging).
dumpMessages = True

def handleInternal(msgBody, chat):
    """
    Internal Handler for incoming msgs.
    Currently only a '!time' function is provided, but this
    method could dispatch to external modules for many more commands.
    """
    if msgBody == '!time':
        print 'OK, handling command ...'
        resp = botName + ' says: ' + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    else:
        print 'Unknown Command [%s]' % msgBody
        return

    ## Send the response to Skype
    chat.SendMessage(resp)

def parseAndDumpMsg(msg):
    """
    Logs the message to the console if dumpMessages is True.
    Extracts the body text from the message, and returns it.
    """
    body = msg.Body
    
    if dumpMessages:
        chatTopic = msg.Chat.Topic
        fromHandle = msg.FromHandle
        print 'responding to a message from ', fromHandle, 'in chat with topic: ', chatTopic, ' ... '
        print '-------------------------'
        print body
        print '-------------------------'
    return body

def shouldRespond(msg):
    """
    Returns True if the bot should respond to msg.
    """
    
    ## Ignore msgs from this bot to avoid recursion ...
    if botName + ' says:' in msg.Body:
        return False

    ## Filter so we only respond to white-listed chat Topics ...
    if chatTopicWhiteList:
        if msg.Chat.Topic not in chatTopicWhiteList:
            return False

    ## Ensure all users in the chat are in the white-list
    if userWhiteList:
        members = msg.Chat.Members
        for member in members:
            if not member.Handle in userWhiteList:
                return False

    ## Filter out msgs that are not addressed to this bot
    if msg.Body[0] != '!':
        return False

    ## This is a message the bot should try to respond to
    return True

## *** Handler for incoming msgs ***
## This function will be passed to the Skype4Py API
## to receive callbacks upon message receipt.
def message(msg, status):
    if not shouldRespond(msg):
        return

    ## OK, we have a message this bot should deal with
    body = parseAndDumpMsg(msg)
    handleInternal(body, msg.Chat)

# Create an instance of the Skype class.
skype = Skype4Py.Skype()

# Connect the Skype object to the Skype client.
skype.Attach()

# Inform user we're up and running
print 'Bot connected to Skype account', skype.CurrentUser.Handle

# Listen for events
skype.OnMessageStatus = message
print 'Listening for events ...'

## Stay alive
while True: pass