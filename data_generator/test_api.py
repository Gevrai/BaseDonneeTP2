import eventful

api = eventful.API('NGGMrssxfJT52ZSP')

# If you need to log in:
# api.login('username', 'password')

events = api.call('events/search', l='Canada')
for event in events['category']:
    print "id: %s       name: %s" % (event['id'], event['name'])
