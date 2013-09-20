#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for **Firefox**
============================================================================

This module offers direct control of the `Firefox 
<http://www.mozilla.com/en-US/firefox/>`_ web browser.  It 
requires the `mouseless-browsing 
<https://addons.mozilla.org/en-US/firefox/addon/879>`_ 
(mlb) add-on for reliable access to hyperlinks.

This module includes direct searching using Firefox's 
search bar and Firefox's keyword searching.  It also 
allows single-utterance submitting of text into form text 
fields.

Installation
----------------------------------------------------------------------------

If you are using DNS and Natlink, simply place this file in you Natlink 
macros directory.  It will then be automatically loaded by Natlink when 
you next toggle your microphone or restart Natlink.

Customization
----------------------------------------------------------------------------

Users should customize this module by editing its 
configuration file.  In this file they should edit the 
``search.searchbar`` and ``search.keywords`` settings to 
match their own personal search preferences.  These 
variables map *what you say* to which *search engines* to 
use.

"""

try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r76")
except ImportError:
    pass

from dragonfly import *


#---------------------------------------------------------------------------
# Set up this module's configuration.

config                 = Config("Firefox control")
config.search          = Section("Search-related section")
config.search.keywords = Item(
                              default={
                                       "wikipedia": "wikipedia",
                                      },
                              doc="Mapping of spoken-forms to Firefox search-keywords.",
                             )
config.search.searchbar = Item(
                              default=[
                                       "google",
                                       "yahoo",
                                       "amazon",
                                       "answers",
                                       "creative commons",
                                       "eBay",
                                       "wikipedia",
                                      ],
                              doc="Spoken-forms of search engines in the Firefox search-bar; they must be given in the same order here as they are available in Firefox.",
                             )

config.lang                        = Section("Language section")
config.lang.new_win                = Item("new (window | win)")
config.lang.new_tab                = Item("new (tab | sub)")
config.lang.close_tab              = Item("close (tab | sub)")
config.lang.close_tab_n            = Item("close (tab | sub) <n>")
config.lang.close_n_tabs           = Item("close <n> (tabs | subs)")
config.lang.address_bar            = Item("address [bar]")
config.lang.copy_address           = Item("copy address")
config.lang.paste_address          = Item("paste address")
config.lang.search_bar             = Item("search bar")
config.lang.go_home                = Item("go home")
config.lang.stop_loading           = Item("stop loading")
config.lang.toggle_tags            = Item("toggle tags")
config.lang.fresh_tags             = Item("fresh tags")
config.lang.caret_browsing         = Item("(caret | carrot) browsing")
config.lang.bookmark_page          = Item("bookmark [this] page")
config.lang.save_page_as           = Item("save [page | file] as")
config.lang.print_page             = Item("print [page | file]")
config.lang.show_tab_n             = Item("show tab <n>")
config.lang.back                   = Item("back [<n>]")
config.lang.forward                = Item("forward [<n>]")
config.lang.next_tab               = Item("next tab [<n>]")
config.lang.prev_tab               = Item("(previous | preev) tab [<n>]")
config.lang.normal_size            = Item("normal text size")
config.lang.smaller_size           = Item("smaller text size [<n>]")
config.lang.bigger_size            = Item("bigger text size [<n>]")
config.lang.find                   = Item("find")
config.lang.find_text              = Item("find <text>")
config.lang.find_next              = Item("find next [<n>]")

config.lang.submit                 = Item("submit")
config.lang.submit_text            = Item("submit <text>")
config.lang.submit_clipboard       = Item("submit (clipboard | clip board)")
config.lang.link_open              = Item("[link] <link> [open]")
config.lang.link_save              = Item("save [link] <link> [as]")
config.lang.link_save_now          = Item("save [link] <link> now now")
config.lang.link_select            = Item("[link] <link> select")
config.lang.link_menu              = Item("[link] <link> (menu | pop up)")
config.lang.link_force             = Item("[link] <link> force")
config.lang.link_window            = Item("[link] <link> [in [new]] window")
config.lang.link_tab               = Item("[link] <link> [in [new]] tab")
config.lang.link_copy              = Item("[link] <link> copy")
config.lang.link_copy_into_tab     = Item("[link] <link> copy into tab")
config.lang.link_list              = Item("[link] <link> list")
config.lang.link_submit            = Item("[link] <link> submit")
config.lang.link_submit_text       = Item("[link] <link> submit <text>")
config.lang.link_submit_clipboard  = Item("[link] <link> submit (clipboard | clip board)")
config.lang.link_dictation_box      = Item("edit [link] <link>")
config.lang.link_assign_keyword    = Item("assign [a] keyword to [link] <link>")
config.lang.tabify_links           = Item("tab if I <links>")
config.lang.tabify_links_sep       = Item("comma")

config.lang.search_text            = Item("[power] search [for] <text>")
config.lang.search_keyword_text    = Item("[power] search <keyword> [for] <text>")
config.lang.search_searchbar_text  = Item("[power] search <searchbar> [for] <text>")
config.lang.search_clipboard       = Item("[power] search [for] (clipboard | clip board)")
config.lang.search_keyword_clipboard = Item("[power] search <keyword> [for] clipboard")
config.lang.search_searchbar_clipboard = Item("[power] search <searchbar> [for] clipboard")

#config.generate_config_file()
config.load()


#---------------------------------------------------------------------------
# Check and prepare search-related config values.

keywords = config.search.keywords
searchbar = dict([(n,i) for i,n in enumerate(config.search.searchbar)])


#---------------------------------------------------------------------------
# Create the rule to match mouseless-browsing link numbers.

class LinkRule(Rule):

    def __init__(self):
        element = Number(zero=True)
        Rule.__init__(self, "link_rule", element, exported=False)

    def value(self, node):
        # Format and return keystrokes to select the link.
        digits = str(node.children[0].value())
        link_keys = "f6,s-f6," + ",".join(["numpad"+i for i in digits])
        self._log.debug("Link keys: %r" % link_keys)
        return link_keys

link = RuleRef(name="link", rule=LinkRule())


#---------------------------------------------------------------------------
# Create the main command rule.

class CommandRule(MappingRule):

    mapping = {
        config.lang.new_win:            Key("c-n"),
        config.lang.new_tab:            Key("c-t"),
        config.lang.close_tab:          Key("c-w"),
        config.lang.close_tab_n:        Key("0, %(n)d, enter/20, c-w"),
        config.lang.close_n_tabs:       Key("c-w/20:%(n)d"),
        config.lang.address_bar:        Key("a-d"),
        config.lang.copy_address:       Key("a-d, c-c"),
        config.lang.paste_address:      Key("a-d, c-v, enter"),
        config.lang.search_bar:         Key("c-k"),
        config.lang.go_home:            Key("a-home"),
        config.lang.stop_loading:       Key("escape"),
        config.lang.toggle_tags:        Key("f12"),
        config.lang.fresh_tags:         Key("f12, f12"),
        config.lang.caret_browsing:     Key("f7"),
        config.lang.bookmark_page:      Key("c-d"),
        config.lang.save_page_as:       Key("c-s"),
        config.lang.print_page:         Key("c-p"),

        config.lang.show_tab_n:         Key("0, %(n)d, enter"),
        config.lang.back:               Key("a-left/15:%(n)d"),
        config.lang.forward:            Key("a-right/15:%(n)d"),
        config.lang.next_tab:           Key("c-tab:%(n)d"),
        config.lang.prev_tab:           Key("cs-tab:%(n)d"),

        config.lang.normal_size:        Key("a-v/20, z/20, r"),
        config.lang.smaller_size:       Key("c-minus:%(n)d"),
        config.lang.bigger_size:        Key("cs-equals:%(n)d"),

        config.lang.submit:             Key("enter"),
        config.lang.submit_text:        Text("%(text)s") + Key("enter"),
        config.lang.submit_clipboard:   Key("c-v, enter"),

        config.lang.find:               Key("c-f"),
        config.lang.find_text:          Key("c-f") + Text("%(text)s"),
        config.lang.find_next:          Key("f3/10:%(n)d"),

        config.lang.link_open:          Key("%(link)s, enter"),
        config.lang.link_save:          Key("%(link)s, shift/10, apps/20, k"),
        config.lang.link_save_now:      Key("%(link)s, shift/10, apps/20, k")
                                         + WaitWindow(title="Enter name of file")
                                         + Pause("20") + Key("enter"),
        config.lang.link_select:        Key("%(link)s, shift"),
        config.lang.link_menu:          Key("%(link)s, shift/10, apps"),
        config.lang.link_force:         Key("%(link)s, shift/10, enter"),
        config.lang.link_window:        Key("%(link)s, shift/10, apps/20, w"),
        config.lang.link_tab:           Key("%(link)s, shift/10, apps/20, t"),
        config.lang.link_copy:          Key("%(link)s, shift/10, apps/20, a"),
        config.lang.link_copy_into_tab: Key("%(link)s, shift/10, apps/20, a/10, c-t/20, c-v, enter"),
        config.lang.link_list:          Key("%(link)s, enter, a-down"),
        config.lang.link_submit:        Key("%(link)s, enter/30, enter"),
        config.lang.link_submit_text:   Key("%(link)s, enter/30")
                                         + Text("%(text)s") + Key("enter"),
        config.lang.link_submit_clipboard: Key("%(link)s, enter/30, c-v, enter"),
        config.lang.link_dictation_box: Key("%(link)s, enter/30, cs-d"),
        config.lang.link_assign_keyword: Key("%(link)s, enter/10, apps/20, k"),

        config.lang.search_text:        Key("c-k")
                                         + Text("%(text)s") + Key("enter"),
        config.lang.search_searchbar_text: Key("c-k, c-up:20, c-down:%(searchbar)d")
                                         + Text("%(text)s") + Key("enter"),
        config.lang.search_keyword_text: Key("a-d")
                                         + Text("%(keyword)s %(text)s")
                                         + Key("enter"),
        config.lang.search_clipboard:   Key("c-k, c-v, enter"),
        config.lang.search_searchbar_clipboard: Key("c-k, c-up:20, c-down:%(searchbar)d, c-v, enter"),
        config.lang.search_keyword_clipboard: Key("a-d") + Text("%(keyword)s")
                                         + Key("c-v, enter"),
        }
    extras = [
        link,
        IntegerRef("n", 1, 20),
        Dictation("text"),
        Choice("keyword", keywords),
        Choice("searchbar", searchbar),
        ]
    defaults = {
        "n": 1,
        }


#---------------------------------------------------------------------------
# Create the command rule for sliding.

slide_directions = {
                    "up":    (0,-1),
                    "down":  (0,+1),
                   }
slide_speeds     = {
                    "1":     10,
                    "2":     20,
                    "3":     30,
                    "4":     40,
                   }
slide_default_speed = 15
slide_start_spec = "(-15,0.6)"

slide_grammar = None

def start_sliding(direction, speed):
    offset_x = direction[0] * speed
    offset_y = direction[1] * speed
    offset_spec = "<%d,%d>" % (offset_x, offset_y)
    action = Key("escape")
    action.execute()
    action = Mouse("%s/25, middle/25, %s" % (slide_start_spec, offset_spec))
    action.execute()

    global slide_grammar
    if not slide_grammar:
        slide_grammar = Grammar("Firefox slide grammar")
        slide_grammar.add_rule(SlideControlRule())
        slide_grammar.load()
        slide_grammar.set_exclusive(True)

def stop_sliding():
    action = Key("escape")
    action.execute()

    global slide_grammar
    if slide_grammar:
        slide_grammar.set_exclusive(False)
        slide_grammar.unload()
        slide_grammar = None

class SlideStartRule(MappingRule):

    mapping  = {
                "slide <direction> [<speed>]":  Function(start_sliding),
               }
    extras   = [
                Choice("direction", slide_directions),
                Choice("speed", slide_speeds),
               ]
    defaults = {
                "speed": slide_default_speed,
               }


class SlideControlRule(MappingRule):

    mapping  = {
                "[slide] <direction> [<speed>]":  Function(start_sliding),
                "[slide] stop":                   Function(stop_sliding),
               }
    extras   = [
                Choice("direction", slide_directions),
                Choice("speed", slide_speeds),
               ]
    defaults = {
                "speed": slide_default_speed,
               }


#---------------------------------------------------------------------------
# Create the main command rule.

class TabifyRule(CompoundRule):

    spec = config.lang.tabify_links
    sep_element = Compound(config.lang.tabify_links_sep)
    repeat_element = Sequence([sep_element, link])
    repetitions = Repetition(child=repeat_element, min=0, max=8)
    extras = [Sequence(name="links", children=(link, repetitions))]

    def _process_recognition(self, node, extras):
        link_nodes = node.get_children_by_name("link")
        for n in link_nodes:
            action = Key(n.value()) + Key("shift/10, apps/20, t/20")
            action.execute()


#---------------------------------------------------------------------------
# Create and load this module's grammar.

context = AppContext(executable="firefox")
grammar = Grammar("firefox_general", context=context)
grammar.add_rule(CommandRule())
grammar.add_rule(SlideStartRule())
grammar.add_rule(TabifyRule())
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
