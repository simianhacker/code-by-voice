from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer)
javascript = AppContext(title="javascript")
grammar = Grammar("javascript", context=(javascript))

rules = MappingRule(
    name = "javascript",
    mapping = {
    "smear"                : Text("err"),
    "jog"                  : Key("c-j"),
    "function"             : Text("fn") + Key("tab"),
    "very equal"           : Text("var_equal") + Key("tab"),
    "very"                 : Text("var") + Key("tab"),
    "require J query"      : Text("req_jquery") + Key("tab"),
    "require"              : Text("req") + Key("tab"),
    "load"                 : Text("load") + Key("tab"),
    "model"                : Text("model") + Key("tab"),
    "define"               : Text("def") + Key("tab"),
    "single if"            : Text("single_if") + Key("tab"),
    "if"                   : Text("if") + Key("tab"),
    "undies"               : Text("undermethod") + Key("tab"),
    "require undies"       : Text("require_underscore") + Key("tab"),
    "require lodash"       : Text("require_lodash") + Key("tab"),
    "chain undies"         : Text("chain_undies") + Key("tab"),
    "for each"             : Text(".forEach()") + Key("escape, i"),
    "express method"       : Text("express_method") + Key("tab"),
    "happy"                : Text("app"),
    "return call back air" : Text("return_callback_error") + Key("tab"),
    "callback function"    : Text("callback_function") + Key("tab"),
    "log"                  : Text("cl") + Key("tab"),
    "comment"          : Key("slash, slash"),
    "comment <text>"       : Text("// %(text)s"),
    "triple equals"        : Text(" === "),
    "triple not equals"    : Text(" !== "),
    "type of"              : Text("typeof") + Key('tab'),
    "homey"                : Text("home"),
    "module exports"              : Text("module.exports"),
    "regex"                       : Text("//") + Key("escape, i"),
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

