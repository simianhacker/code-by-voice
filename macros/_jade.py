from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer, Mimic)

context = AppContext(title = "jade")
grammar = Grammar("jade", context=context)
noSpaceNoCaps = Mimic("\\no-caps-on") + Mimic("\\no-space-on")

rules = MappingRule(
    name = "jade",
    mapping = {
      "heading [<n>]": Text("h%(n)d "),
      "span [<n>]": Text(".span%(n)d"),
      "paragraph": Text("p ") + noSpaceNoCaps,
      "link": Text("link") + Key("tab") + noSpaceNoCaps,
      "attribute": Text("attribute") + Key("tab") + noSpaceNoCaps,
      "Eckelberry": Text("echo_var") + Key("tab") + noSpaceNoCaps,
      "row fluid": Text(".row-fluid ") + noSpaceNoCaps,
      "row": Text(".row") + noSpaceNoCaps,
      "container": Text(".container") + noSpaceNoCaps,
      "unordered list": Text("ul") + noSpaceNoCaps,
      "list item": Text("li") + noSpaceNoCaps,
      "image": Text("image") + Key("tab") + noSpaceNoCaps,
      "equal": Text("=") + noSpaceNoCaps,
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

