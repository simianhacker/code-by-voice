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
    "termi": Key("w-1"),
    "foxy": Key("w-2"),
    "foxy reload": Key("w-2/10, f5"),
    "Jimmy": Key("w-3"), 
    "Heidi": Key("w-4"),
    "chrome": Key("w-5"),
    "chrome reload": Key("w-5/10, f5"),
    "smelly": Key("w-6"),
    "bashing": Key("w-7"),
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
