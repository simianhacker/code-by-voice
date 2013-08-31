from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text)

putty_context = AppContext(executable="putty")
grammar = Grammar("putty", context=putty_context)

putty_rules = MappingRule(
    name = "putty",
    mapping = {
      "mux north": Key('c-b, k'),
      "mux south": Key('c-b, j'),
      "mux west": Key('c-b, h'),
      "mux east": Key('c-b, l'),
      },
    extras = [
        Dictation("text")
      ]
    )

grammar.add_rule(putty_rules)

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
