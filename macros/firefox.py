from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text)

firefox_context = AppContext(executable="firefox")
grammar = Grammar("firefox", context=firefox_context)

firefox_rules = MappingRule(
    name = "firefox",
    mapping = {
        "jump": Key("f12"),
        "edit": Key("cs-f4"),
      },
    extras = [
        Dictation("text")
      ]
    )

grammar.add_rule(firefox_rules)

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
