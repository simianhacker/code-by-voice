from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer)

grammar = Grammar("global phonetics")
rules = MappingRule(
    name = "global phonetics",
    mapping = {
			"Alpha"    : Key("a"),
			"bravo"    : Key("b"),
			"Charlie"  : Key("c"),
			"Callie"   : Key("c"),
			"Delta"    : Key("d"),
			"echo"     : Key("e"),
			"foxtrot"  : Key("f"),
			"foxy"     : Key("f"),
			"golf"     : Key("g"),
			"gamma"    : Key("g"),
			"Juliet"   : Key("j"),
			"hotel"    : Key("h"),
			"India"    : Key("i"),
			"kilo"     : Key("k"),
			"Lima"     : Key("l"),
			"Mike"     : Key("m"),
			"November" : Key("n"),
			"Oscar"    : Key("o"),
			"Papa"     : Key("p"),
			"Queen"    : Key("q"),
			"Rico"     : Key("r"),
			"soy"      : Key("s"),
			"tango"    : Key("t"),
			"toy"      : Key("t"),
			"uniform"  : Key("u"),
			"Victor"   : Key("v"),
			"Van"      : Key("v"),
			"whiskey"  : Key("w"),
			"x-ray"    : Key("x"),
			"yellow"   : Key("y"),
			"Zulu"     : Key("z"),
			"zebra"    : Key("z"),
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

