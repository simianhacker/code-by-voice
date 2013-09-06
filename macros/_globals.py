from dragonfly import (Grammar, FocusWindow, MappingRule, Key, Config, Section, Item, Playback)

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
    "termi": FocusWindow(executable="putty"),
    "foxy": FocusWindow(executable="firefox"),
    "Jimmy": FocusWindow(executable = "gvim"),
    "Heidi": FocusWindow(executable = "heidisql"),
	}
)

grammar = Grammar("general")
grammar.add_rule(rules)
grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
