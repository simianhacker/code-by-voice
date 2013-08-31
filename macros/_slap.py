from dragonfly import (Grammar, MappingRule, Key, Config, Section, Item)

rules = MappingRule(
	name = "slap",
	mapping = { 
		"slap": Key("enter"),
	}
)

grammar = Grammar("slap")
grammar.add_rule(rules)
grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None

