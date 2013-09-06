# This macro will copy your password from "Password Safe", provided that the application
# is in the 8th position on your taskbar
from dragonfly import (Grammar, MappingRule, Key, Config, Section, Item, Text, Dictation)
from dragonfly.windows.clipboard import Clipboard

class PasswordRule(MappingRule):
  name = "mypassword"

  mapping = { 
      "<text> password": Text('%(text)s'),
      }

  extras = [
      Dictation("text", format=False),
      ]

  def _process_recognition(self, value, extras): 
    getPassword = Key("w-b/10, s-tab/10, right:8/10, enter, c-f/10") + value + Key('enter/10, escape/10, c-c/10, a-tab/10')
    getPassword.execute()
    clipboard = Clipboard()
    clipboard.copy_from_system()
    password = clipboard.get_text()
    action = Text(password)
    action.execute()

grammar = Grammar("mypassword")
grammar.add_rule(PasswordRule())
grammar.load() 
def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None

