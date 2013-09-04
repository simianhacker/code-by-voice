from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer)
vi = AppContext(title="vi")
gvim = AppContext(title="GVIM")
grammar = Grammar("vim", context=(vi | gvim))

rules = MappingRule(
    name = "vim",
    mapping = {
    "north [by] [<n>]"            : Key("escape, %(n)d, c-k"),
    "south [by] [<n>]"            : Key("escape, %(n)d, c-j"),
    "east [by] [<n>]"             : Key("escape, %(n)d, c-l"),
    "west [by] [<n>]"             : Key("escape, %(n)d, c-h"),

    "drop [by] [<n>]"             : Text("%(n)d") + Key("j"),
    "rise [by] [<n>]"             : Text("%(n)d") + Key("k"),

    "balance"                     : Key("escape, c-w, equal"),
    "insert"                      : Key("escape, i"),
    "reflow"                      : Key("equals"),
    "flow"                        : Key("equals"),
    "after"                       : Key("escape, a"),
    "big after"                   : Key("escape, A"),
    "big insert"                  : Key("escape, I"),
    "oh"                          : Key("escape, o"),
    "big oh"                      : Key("escape, O"),
    "escape"                      : Key("escape"),
    "cancel"                      : Key("escape"),
    "find [<text>]"               : Key("slash") + Text("%(text)s"),
    "sip [<text>]"                : Key("slash") + Text("%(text)s"),
    "sup [<text>]"                : Key("question") + Text("%(text)s"),
    "reverse inside singles"        : Key("question") + Text("'.\{-}'") + Key("enter, l"),
    "reverse inside doubles" : Key("question") + Text("\".\{-}\"") + Key("enter, l"),
    "inside singles"                : Key("slash") + Text("'.\{-}'") + Key("enter, l"),
    "inside doubles"         : Key("slash") + Text("\".\{-}\"") + Key("enter, l"),
    "transpose"                   : Key("x, p"),
    "file"                        : Key("c-f"),

    # editin
    "diz"                         : Key("c, i, squote"),
    "dib"                         : Key("c, i, dquote"),
    "dip"                         : Key("c, i, lparen"),
    "dice"                        : Key("c, i, lbrace"),
    "dick"                        : Key("c, i, lbracket"),

    "Dwight"                      : Key("c, w"),

    "semi"                        : Key("escape, A") + Text(";"),
    "commie"                      : Key("escape, A, comma"),
    "corn hole"                   : Key("escape, A, colon, space"),
    "align equals"                : Key("colon") + Text("Align="),
    "align colon"                 : Key("colon") + Text("Align") + Key('colon'),
      
    # movements
    "bark [<n>]"                  : Text("%(n)d") + Key("b"),
    "woof [<n>]"                  : Text("%(n)d") + Key("w"),
    "eck [<n>]"                   : Text("%(n)d") + Key("e"),
    "beck [<n>]"                  : Text("%(n)d") + Key("g, e"),
    "kill space"                  : Key("escape, m, z") + Text("?\s") + Key("enter, x, backtick, z, i"),
    "kill slash"                  : Key("escape, m, z") + Text("?\\") + Key("enter, x, backtick, z, a"),
    "race"                        : Key("question") + Text("\s\S") + Key("enter"),
    "ace"                         : Key("slash") + Text("\s\S") + Key("enter"),
    "ot"                          : Key("escape, slash") + Text("\(\"\|'\|)\|}\|]\)") + Key("enter, a"),
    "hop"                         : Key("space, e"),
    "trip"                        : Key("space, g, e"),
    "jump"                        : Key("space, w"),
    "squat"                      : Key("space, b"),
    "to end"                      : Key("dollar"),
    "to start"                    : Key("caret"),
    "to top"                      : Key("g,g"),
    "to bottom"                   : Key("G"),
      
    "viz"                         : Key("v, i, squote"),
    "vib"                         : Key("v, i, dquote"),
    "vip"                         : Key("v, i, lparen"),
    "vice"                        : Key("v, i, lbrace"),
    "vick"                        : Key("v, i, lbracket"),

    "next [by] [<n>]"             : Text("%(n)d") + Key("n"),
    "visual"                      : Key("escape, v"),
    "big visual"                  : Key("escape, V"),
    "call visual"                 : Key("escape, c-v"),
    "yank"                        : Key("y"),
    "big yank"                    : Key("Y"),
    "put"                         : Key("p"),
    "big put"                     : Key("P"),
    "duplicate line"                     : Key("Y, P"),
    "that's all"                  : Key("escape, g, g, V, G"),

    "save"                        : Key("escape, colon, w, enter"),
    "close"                       : Key("escape, colon, q, enter"),
    "hard close"                  : Key("escape, colon, q, exclamation, enter"),
    "command [<text>]"            : Key("escape, colon") + Text("%(text)s"),
    "scratch"                     : Key("escape, u"),
    "oops"                        : Key("escape, u"),
    "redo"                        : Key("escape, c-r"),
    "spa"                         : Key("space"),
    "plus"                        : Text(" + "),
    "minus"                       : Text(" - "),
    "equal"                       : Text(" = "),
    "Ash"                         : Text("-"),
    "kill [<n>]"                  : Text("%(n)d") + Key("x"),
    "kill line"                   : Key("d,d"),
    "delete line"                 : Key("d,d"),
    "line <n>"                    : Key("escape, colon") + Text("%(n)d") + Key("enter"),
    "nerd"                        : Key("escape, c-t"),
    "small braces"                : Text("{}") + Key("escape, i"),
    "braces"                      : Text("{  }") + Key("escape, h, i"),
    "small brackets"              : Text("[]") + Key("escape, i"),
    "brackets"                    : Text("[  ]") + Key("escape, h, i"),
    "parens"                      : Text("()") + Key("escape, i"),
    "angles"                      : Text("<>") + Key("escape, i"),
    "doubles"                     : Text("\"\"") + Key("escape, i"),
    "singles"                     : Text("''") + Key("escape, i"),
    "module exports"              : Text("module.exports"),
    "regex"                       : Text("//") + Key("escape, i"),
    "inc."                        : Key("c-a"),
    "deinc"                       : Key("c-x"),
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
