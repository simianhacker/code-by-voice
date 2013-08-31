from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer)

vi = AppContext(title="vi")
gvim = AppContext(title="GVIM")
grammar = Grammar("vim", context=(vi | gvim))

rules = MappingRule(
    name = "vim",
    mapping = {
    "north [by] [<n>]"     : Key("escape, %(n)d, c-k"),
    "south [by] [<n>]"     : Key("escape, %(n)d, c-j"),
    "east [by] [<n>]"      : Key("escape, %(n)d, c-l"),
    "west [by] [<n>]"      : Key("escape, %(n)d, c-h"),
    "balance"              : Key("escape, c-w, equal"),
    "insert"               : Key("escape, i"),
    "flow"                 : Key("equals"),
    "after"                : Key("escape, a"),
    "big after"            : Key("escape, A"),
    "big insert"           : Key("escape, I"),
    "oh"                   : Key("escape, o"),
    "big oh"               : Key("escape, O"),
    "escape"               : Key("escape"),
    "cancel"               : Key("escape"),
    "sip [<text>]"         : Key("slash") + Text("%(text)s"),
    "sup [<text>]"         : Key("question") + Text("%(text)s"),
    "inside quote"         : Key("slash") + Text("'.\{-}'") + Key("enter, l"),
    "inside double quote"  : Key("slash") + Text("\".\{-}\"") + Key("enter, l"),
    "transpose"            : Key("x, p"),

    # editin
    "diz"                  : Key("c, i, squote"),
    "dib"                  : Key("c, i, dquote"),
    "dip"                  : Key("c, i, lparen"),
    "dice"                 : Key("c, i, lbrace"),
    "dick"                 : Key("c, i, lbracket"),

    "Dwight"               : Key("c, w"),

    "semi"                 : Key("escape, A") + Text(";"),
    "commie"               : Key("escape, A, comma"),
    "corn hole"            : Key("escape, A, colon, space"),
    "align equals"         : Key("colon") + Text("Align="),
    "align colon"          : Key("colon") + Text("Align") + Key('colon'),
      
    # movements
    "bark [<n>]"           : Text("%(n)d") + Key("b"),
    "woof [<n>]"           : Text("%(n)d") + Key("w"),
    "eck [<n>]"            : Text("%(n)d") + Key("e"),
    "beck [<n>]"           : Text("%(n)d") + Key("g, e"),
    "race"                 : Key("question") + Text("\s\S") + Key("enter"),
    "ace"                  : Key("slash") + Text("\s\S") + Key("enter"),
    "hop"                  : Key("space, e"),
    "trip"                 : Key("space, g, e"),
    "jump"                 : Key("space, w"),
    "crouch"               : Key("space, b"),
    "to end"               : Key("dollar"),
    "to start"             : Key("caret"),
      
    "viz"                  : Key("v, i, squote"),
    "vib"                  : Key("v, i, dquote"),
    "vip"                  : Key("v, i, lparen"),
    "vice"                 : Key("v, i, lbrace"),
    "vick"                 : Key("v, i, lbracket"),

    "next [by] [<n>]"      : Text("%(n)d") + Key("n"),
    "visual"               : Key("escape, v"),
    "big visual"           : Key("escape, V"),
    "call visual"          : Key("escape, c-v"),
    "yank"                 : Key("y"),
    "big yank"             : Key("Y"),
    "put"                  : Key("p"),
    "big put"              : Key("P"),
    "that's all"           : Key("escape, g, g, V, G"),

    "save"                 : Key("escape, colon, w, enter"),
    "close"                : Key("escape, colon, q, enter"),
    "command [<text>]"       : Key("escape, colon") + Text("%(text)s"),
    "scratch"              : Key("escape, u"),
    "oops"                 : Key("escape, u"),
    "redo"                 : Key("escape, c-r"),
    "Spock"                : Key("space"),
    "plus"                 : Text(" + "),
    "equal"                : Text(" = "),
    "Ash"                  : Text("-"),
    "kill [<n>]"           : Text("%(n)d") + Key("x"),
    "kill line"            : Key("d,d"),
    "delete line"          : Key("d,d"),
    "line <n>"             : Key("escape, colon") + Text("%(n)d") + Key("enter"),
    "nerd"                 : Key("escape, c-t"),
    "small braces"         : Text("{}") + Key("escape, i"),
    "braces"               : Text("{  }") + Key("escape, h, i"),
    "small brackets"       : Text("[]") + Key("escape, i"),
    "brackets"             : Text("[  ]") + Key("escape, h, i"),
    "parens"               : Text("()") + Key("escape, i"),
    "angles"               : Text("<>") + Key("escape, i"),
    "doubles"              : Text("\"\"") + Key("escape, i"),
    "singles"              : Text("''") + Key("escape, i"),
    "module exports"       : Text("module.exports"),
    "regex"                : Text("//") + Key("escape, i"),
    "smear"                : Text("err"),


    "jog"                  : Key("c-j"),
    "function"             : Text("fn") + Key("tab"),
    "very"                 : Text("var") + Key("tab"),
    "require"              : Text("req") + Key("tab"),
    "model"                : Text("model") + Key("tab"),
    "define"               : Text("def") + Key("tab"),
    "single if"            : Text("single_if") + Key("tab"),
    "if"                   : Text("if") + Key("tab"),
    "undies"               : Text("undermethod") + Key("tab"),
    "chain undies"         : Text("chain_undies") + Key("tab"),
    "for each"             : Text(".forEach()") + Key("escape, i"),
    "express method"       : Text("express_method") + Key("tab"),
    "happy"                : Text("app"),
    "return call back air" : Text("return_callback_error") + Key("tab"),
    "callback function"    : Text("callback_function") + Key("tab"),
    "inc."                 : Key("c-a"),
    "deinc"                : Key("c-x"),
    "log"                  : Text("cl") + Key("tab"),
    
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
