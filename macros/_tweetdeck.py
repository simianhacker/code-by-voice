from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer)

context = AppContext(title="TweetDeck")
grammar = Grammar("tweetdeck", context=context)

rules = MappingRule(
    name = "tweetdeck",
    mapping = {
      "new Tweet": Key("n"), 
      "send": Key("c-enter"),
      "reply": Key("r"),
      "favorite": Key("f"),
      "retweet": Key("t"),
      },
    extras = [
        Dictation("text"),
        Integer("n", 0, 20000),
      ],
    defaults = {
      "n" : 1
      }
    )

grammar.add_rule(rules)

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None


