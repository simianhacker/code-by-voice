from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer)

context = AppContext(title = "jade")
grammar = Grammar("jade", context=context)

rules = MappingRule(
    name = "jade",
    mapping = {
      "heading [<n>]": Text("h%(n)d "),
      "span [<n>]": Text(".span%(n)d"),
      "paragraph": Text("p "),
      "link": Text("link") + Key("tab"),
      "attribute": Text("attribute") + Key("tab"),
      "Eckelberry": Text("echo_var") + Key("tab"),
      "row fluid": Text(".row-fluid "),
      "row": Text(".row"),
      "container": Text(".container"),
      "unordered list": Text("ul"),
      "list item": Text("li"),
      "image": Text("image") + Key("tab"),
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

