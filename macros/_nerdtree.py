from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer)
context = AppContext(title="nerdtree")
grammar = Grammar("nerdtree", context=context)
rules = MappingRule(
    name = "nerdtree",
    mapping = {
      "split": Key("s"),
      "add [file]": Key("m, a"),
      "move [file]": Key("m, m"),
      "copy [file]": Key("m, c"),
      "kill [file]": Key("m, d"),
      "change root": Key("C"),
      "level up": Key("u"),
      "go to parent": Key("P"),
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


