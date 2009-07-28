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
