from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer)

context = AppContext(title="irssi")
grammar = Grammar("irssi", context=context)

rules = MappingRule(
    name = "irssi",
    mapping = {
			"next when": Key("c-n"),
			"when <n>": Text("/win %(n)d") + Key("enter"),
			"join": Text("/join "),
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

