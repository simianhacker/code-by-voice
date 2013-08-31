from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text)

putty_context = AppContext(executable="putty")
bash_context = AppContext(title="bash")
grammar = Grammar("bash", context=(putty_context | bash_context))

rules = MappingRule(
    name = "bash",
    mapping = {
      "change directory": Text("cd "),
      "cancel": Key("c-c"),
      "up directory": Text("cd ..") + Key('enter'),
      "change directory to <text>": Text("cd %(text)s"),
      "list files": Text("ll") + Key("enter"),
      "go home": Text("cd ~") + Key("enter"),
      "attach": Text("tmux attach") + Key("enter"),
      "tmux": Text("tmux") + Key("enter"),
      },
    extras = [
        Dictation("text")
      ]
    )

grammar.add_rule(rules)

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
