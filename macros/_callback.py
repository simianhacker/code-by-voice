import natlink
import natlinkmain
import pprint
import redis

def myCallback(command, args):
  if command == "mic":
    try:
      print "setting natlink.mic to %s" % args
      r = redis.Redis()
      r.set('natlink.mic', args)
    except e:
      print e
      print "falied to connect to redis"
      
  apply(natlinkmain.changeCallback, [command, args])

natlink.setChangeCallback(myCallback)

def unload():
  print "unloading callback"
  natlink.setChangeCallback(natlinkmain.changeCallback)
