from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer)

putty_context = AppContext(executable="putty")
bash_context = AppContext(title="bash")
grammar = Grammar("bash", context=(putty_context | bash_context))

rules = MappingRule(
    name = "bash",
    mapping = {
      "term <n>": Key('c-b') + Text("%(n)d"),
      "term create": Key('c-b, c'),
      "term north": Key('c-b, k'),
      "term south": Key('c-b, j'),
      "term west": Key('c-b, h'),
      "term east": Key('c-b, l'),
      "term vertical": Key('c-b, v'),
      "term split": Key('c-b, s'),
      "term detach": Key('c-b, d'),
      "term down [<n>]": Key('c-b, colon') + Text("resize-pane -D %(n)d") + Key('enter'),
      "term up [<n>]": Key('c-b, colon') + Text("resize-pane -U %(n)d") + Key('enter'),
      "term left [<n>]": Key('c-b, colon') + Text("resize-pane -L %(n)d") + Key('enter'),
      "term right [<n>]": Key('c-b, colon') + Text("resize-pane -R %(n)d") + Key('enter'),
      "change directory": Text("cd "),
      "cancel": Key("c-c"),
      "exit": Key("c-d"),
      "up directory": Text("cd ..") + Key('enter'),
      "change directory to <text>": Text("cd %(text)s"),
      "list files": Text("ls -l") + Key("enter"),
      "go home": Text("cd ~") + Key("enter"),
      "attach": Text("tmux attach") + Key("enter"),
      "them": Text("vi") + Key("enter"),
      "tmux": Text("tmux") + Key("enter"),
      },
    extras = [
        Dictation("text"),
        Integer("n", 0, 20000),
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
