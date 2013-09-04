from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer)
ctlp = AppContext(title="ControlP")
grammar = Grammar("ctlp", context=ctlp)

rules = MappingRule(
    name = "ControlP",
    mapping = {
      "split": Key("c-s"),
      "vertical": Key("c-v"),
      "refresh": Key("f5"),
    },

    extras = [
        Dictation("text", format=False),
        Integer("n", 1, 20000),
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


