from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer, Mimic)
javascript = AppContext(title="javascript")
grammar = Grammar("javascript", context=(javascript))

noSpaceNoCaps = Mimic("\\no-caps-on") + Mimic("\\no-space-on")

rules = MappingRule(
    name = "javascript",
    mapping = {
    "smear"                : Text("err"),
    "function"             : Text("fn") + Key("tab") + noSpaceNoCaps,
    "very equal"           : Text("var_equal") + Key("tab") + noSpaceNoCaps,
    "very"                 : Text("var") + Key("tab") + noSpaceNoCaps,
    "require J query"      : Text("req_jquery") + Key("tab"),
    "require"              : Text("req") + Key("tab") + noSpaceNoCaps,
    "load"                 : Text("load") + Key("tab") + noSpaceNoCaps,
    "model"                : Text("model") + Key("tab") + noSpaceNoCaps,
    "define"               : Text("def") + Key("tab") + noSpaceNoCaps,
    "single if"            : Text("single_if") + Key("tab") + noSpaceNoCaps,
    "if"                   : Text("if") + Key("tab") + noSpaceNoCaps,
    "undies"               : Text("undermethod") + Key("tab") + noSpaceNoCaps,
    "require undies"       : Text("require_underscore") + Key("tab"),
    "require lodash"       : Text("require_lodash") + Key("tab"),
    "chain undies"         : Text("chain_undies") + Key("tab") + noSpaceNoCaps,
    "for each"             : Text(".forEach()") + Key("escape, i") + noSpaceNoCaps,
    "express method"       : Text("express_method") + Key("tab") + noSpaceNoCaps,
    "happy"                : Text("app"),
    "return call back air" : Text("return_callback_error") + Key("tab"),
    "callback function"    : Text("callback_function") + Key("tab") + noSpaceNoCaps,
    "log"                  : Text("cl") + Key("tab") + noSpaceNoCaps,
    "comment <text>"       : Text("// %(text)s"),
    "type of"              : Text("typeof") + Key('tab') + noSpaceNoCaps,
    "homey"                : Text("home"),
    "module exports"              : Text("module.exports"),
    "regex"                       : Text("//") + Key("escape, i") + noSpaceNoCaps,
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

