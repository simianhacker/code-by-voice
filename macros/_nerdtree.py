from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer, Mimic)
context = AppContext(title="nerdtree")
grammar = Grammar("nerdtree", context=context)
noSpaceNoCaps = Mimic("\\no-caps-on") + Mimic("\\no-space-on")
rules = MappingRule(
    name = "nerdtree",
    mapping = {
      "split": Key("i"),
      "vertical": Key("s"),
      "add [file]": Key("m, a") + noSpaceNoCaps,
      "move [file]": Key("m, m") + noSpaceNoCaps,
      "copy [file]": Key("m, c") + noSpaceNoCaps,
      "kill [file]": Key("m, d") + noSpaceNoCaps,
      "open <n>": Text(":%(n)d") + Key("enter") + Key("enter"),
      "open vertical <n>": Text(":%(n)d") + Key("enter, s"),
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


