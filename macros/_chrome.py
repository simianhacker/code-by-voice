from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer, Mimic)

context = AppContext(executable="chrome")
grammar = Grammar("chrome", context=context)
noSpaceNoCaps = Mimic("\\no-caps-on") + Mimic("\\no-space-on")

rules = MappingRule(
    name = "chrome",
    mapping = {
      "edit": Key("w-a"),
      "reload" : Key("f5"),
      "open": Key("escape, o"),
      "jump": Key("escape, f"),
      "new tab": Key("escape, t"),
      "search tabs": Key("escape, T"),
      "find": Key("escape, slash"),
      "console": Key("cs-j"),
      "close tab": Key("c-w"),
      "escape": Key('escape'),
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

