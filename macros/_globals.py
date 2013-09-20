from dragonfly import (Grammar, FocusWindow, MappingRule, Key, Config, Section, Item, Playback, Mimic)

rules = MappingRule(
	name = "general",
	mapping = { 
		"slap": Key("enter"),
		"Max when": Key("w-up"),
		"left when": Key("w-left"),
		"right when": Key("w-right"),
		"min win": Key("w-down"),
    "switch apps": Key("alt:down, tab"),
		"switch app": Key("a-tab"),
    "termi": Key("w-b/10, s-tab/10, enter"),
    "foxy": Key("w-b/10, s-tab/10, right:1/10, enter"),
    "foxy reload": Key("w-b/10, s-tab/10, right:1/10, enter/10, f5"),
    "Jimmy": Key("w-b/10, s-tab/10, right:2/10, enter"), 
    "Heidi": Key("w-b/10, s-tab/10, right:3/10, enter"),
    "Tweedy": Key("w-b/10, s-tab/10, right:4/10, enter"),
    "spotty": Key("w-b/10, s-tab/10, right:5/10, enter"),
    "smelly": Key("w-b/10, s-tab/10, right:6/10, enter"),
    "code mode": Mimic("\\no-caps-on") + Mimic("\\no-space-on"),
	}
)

grammar = Grammar("general")
grammar.add_rule(rules)
grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
