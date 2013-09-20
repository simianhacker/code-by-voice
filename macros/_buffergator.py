from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer, Mimic)
context = AppContext(title="buffergator")
grammar = Grammar("buffergator", context=context)
noSpaceNoCaps = Mimic("\\no-caps-on") + Mimic("\\no-space-on")
rules = MappingRule(
    name = "buffergator",
    mapping = {
      "split": Key("c-s"),
      "vertical": Key("c-v"),
      },

    extras = [
        Dictation("text", format=False),
        Integer("n", 1, 20000),
      ],

    defaults = {
      "text": '',
      "n" : 1
      }
    )
 
grammar.add_rule(rules)
grammar.load()
def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None


