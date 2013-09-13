from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer, Mimic)

context = AppContext(title = "less")
grammar = Grammar("less", context=context)
noSpaceNoCaps = Mimic("\\no-caps-on") + Mimic("\\no-space-on")

rules = MappingRule(
    name = "less",
    mapping = {
      "heading [<n>]": Text("h%(n)d "),
      "paragraph": Text("p "),
      "unordered list": Text("ul "),
      "list item": Text("li "),
      "image": Text("img "),
      "<n> (pixel|pixels)": Text("%(n)dpx"),
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


