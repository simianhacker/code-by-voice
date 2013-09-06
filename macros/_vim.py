from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Key, Text, Integer, Mimic, Playback)
vi = AppContext(title="vi")
gvim = AppContext(title="GVIM")
grammar = Grammar("vim", context=(vi | gvim))

rules = MappingRule(
    name = "vim",
    mapping = {
      "north [by] [<n>]"            : Key("escape, c-k:%(n)d"),
      "south [by] [<n>]"            : Key("escape, c-j:%(n)d"),
      "east [by] [<n>]"             : Key("escape, c-l:%(n)d"),
      "west [by] [<n>]"             : Key("escape, c-h:%(n)d"),

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
      "bo"                          : Key("escape, O"),
      "escape"                      : Key("escape"),
      "cancel"                      : Key("escape"),
      "find [<text>]"               : Key("slash") + Text("%(text)s"),
      "sip [<text>]"                : Key("slash") + Text("%(text)s"),
      "sup [<text>]"                : Key("question") + Text("%(text)s"),
      "reverse inside singles"      : Key("question, squote, dot, backslash, lbrace, hyphen, rbrace, squote, enter, l"),
      "reverse inside doubles"      : Key("question, dquote, dot, backslash, lbrace, hyphen, rbrace, dquote, enter, l"),
      "inside singles"              : Key("slash, squote, dot, backslash, lbrace, hyphen, rbrace, squote, enter, l"),
      "inside doubles"              : Key("slash, dquote, dot, backslash, lbrace, hyphen, rbrace, dquote, enter, l"),
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
      "bark [<n>]"                  : Key("b:%(n)d"),
      "woof [<n>]"                  : Key("w:%(n)d"),
      "eck [<n>]"                   : Key("e:%(n)d"),
      "beck [<n>]"                  : Text("%(n)d") + Key("g, e"),
      "kill space"                  : Key("escape, m, z, question, backslash, s, enter, x, backtick, z, i"),
    "kill slash"                  : Key("escape, m, z, question, backslash, slash, enter, x, backtick, z, a"),
    "race"                        : Key("question, backslash, s, backslash, S, enter"),
    "ace"                         : Key("slash, backslash, s, backslash, S, enter"),
    "ot"                          : Key("escape, question, backslash, lparen, dquote, backslash, bar, squote, backslash, bar, rparen, backslash, bar, rbrace, backslash, bar, rbracket, backslash, rparen, enter, a"),
    "oink"                          : Key("escape, slash, backslash, lparen, dquote, backslash, bar, squote, backslash, bar, rparen, backslash, bar, rbrace, backslash, bar, rbracket, backslash, rparen, enter, a"),
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

    "next [by] [<n>]"             : Key("n:%(n)d"),
    "visual"                      : Key("escape, v"),
    "big visual"                  : Key("escape, V"),
    "call visual"                 : Key("escape, c-v"),
    "yank"                        : Key("y"),
    "big yank"                    : Key("Y"),
    "put"                         : Key("p"),
    "big put"                     : Key("P"),
    "duplicate line"                     : Key("Y, P"),
    "that's all"                  : Key("escape, g, g, V, G"),
    "comment out": Key("backslash, backslash"),

    "save"                        : Key("escape, colon, w, enter"),
    "close"                       : Key("escape, colon, q, enter"),
    "close all"                       : Key("escape, colon, q, a, l, l, enter"),
    "hard close"                  : Key("escape, colon, q, exclamation, enter"),
    "command [<text>]"            : Key("escape, colon") + Text("%(text)s"),
    "scratch"                     : Key("escape, u"),
    "oops"                        : Key("escape, u"),
    "redo"                        : Key("escape, c-r"),
    "spa"                         : Key("space"),
    "plus"                 : Key("space, plus, space"),
    "minus"                : Key("space, minus, space"),
    "equal"                : Key("space, equal, space"),
    "Ash"                         : Key("hyphen"),
    "kill [<n>]"                  : Key("x:%(n)d"),
    "kill line"                   : Key("d,d"),
    "delete line"                 : Key("d,d"),
    "line <n>"                    : Key("escape, colon") + Text("%(n)d") + Key("enter"),
    "nerd"                        : Key("escape, c-t"),
    "small braces"                : Key("lbrace, rbrace, escape, i"),
    "braces"                      : Key("lbrace, space, space, rbrace, escape, h, i"),
    "small brackets"              : Key("lbracket, rbracket, escape, i"),
    "brackets"                    : Key("lbracket, space, space, rbracket, h, i"),
    "parens"                      : Key("lparen, rparen, escape, i"),
    "angles"                      : Key("langle, rangle, escape, i"),
    "doubles"                     : Key("dquote, dquote, escape, i"),
    "singles"                     : Key("squote, squote, escape, i"),
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
