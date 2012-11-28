"""Bulk mailer.

This takes a message from message.txt and mails it to the e-mail
addresses listed, one per line, in members.txt.

Make sure you have a complete e-mail, including headers.  I'd suggest
adding (or using instead) the following headers for bulk traffic:

Return-Path: <example+bounces@example.com>
To: <example@example.com>
Organization: Example Co.
X-BeenThere: example@example.com
Precedence: list
Reply-To: example@example.com
List-Id: Full Name for the Example List
        <example.example.com>
List-Unsubscribe: <http://example.com/unsubscribe>,
        <mailto:example+unsubscribe@example.com>
List-Archive: <http://example.com/archive>
List-Help: <mailto:example+help@comoxvalleychamber.com>
List-Subscribe: <http://example.com/subscribe>,
        <mailto:example+subscribe@comoxvalleychamber.com>
Sender: example+bounces@example.com
Errors-To: example+bounces@example.com
Subject: [Example List] Original Subject
"""

import logging, turbomail

log = logging.getLogger('mlist')
logging.basicConfig(level=logging.INFO)

# Variables that can be adjusted.
batch_size = 10
members = open('members.txt')
members = [i.strip() for i in members if i.strip()]
content = open('message.txt').read()

# Uncomment this and define a list of addresses to perform a 'test run'.
#members = ['alice@gothcandy.com']

# Set this to the connection information for your mail server.
# If you have Postfix configured with a "re-queue" SMTP daemon (that doesn't run filters)
# I'd recommend using that.  E.g. SMTPD running on port 10025.
config = {
        'mail.on': True,
        'mail.manager': 'demand',
        'mail.transport': 'smtp',
        'mail.smtp.server': 'localhost:10025',
        'mail.smtp.username': '',
        'mail.smtp.password': ''
    }

turbomail.interface.start(config)


while True:
    log.info("Adding message to queue for %r", members[:min(len(members),batch_size)])
    
    message = turbomail.WrappedMessage(
            'enews-bounces@example.com', # Set this to the MAIL FROM of the list.  Usually there is a bounces-specific address.
            members[:min(len(members),batch_size)],
            message=content
        )
    
    message.send()
    
    del members[:min(len(members),batch_size)]
    
    if not members: break

log.info("Waiting for delivery to complete.")

turbomail.interface.stop(force=True)
