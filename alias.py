__module_name__ = "alias"
__module_version__ = "1.0"
__module_description__ = "Allows user to set aliases for any string."

import hexchat, collections, os

alias_list_help = "/alias_list - Shows list of available aliases.";
alias_add_help = "/alias_add <alias> <definition> - Adds a new alias to the list.";
alias_overwrite_help = "/alias_overwrite <alias> <definition> - Replaces an existing alias. If the alias doesn't already exist, it is added.";
alias_remove_help = "/alias_remove <alias> - Removes an alias from the list.";
alias_reload_help = "/alias_reload - Reloads list of aliases from file.";

alias_help = (
"""/alias <alias> - Say the definition of an existing alias.
%s
%s
%s
%s
%s""" % (alias_list_help, alias_add_help, alias_overwrite_help, alias_remove_help, alias_reload_help));

aliases = collections.OrderedDict();

def initialise(word = None, word_eol = None, userdata = None):
    global aliases;
    aliases = collections.OrderedDict();
    if not os.path.isfile("aliases.csv"):
        with open("aliases.csv", "w", encoding = "utf-8") as file:
            pass;
    with open("aliases.csv", "r", encoding="utf-8") as file:
        i = 0;
        for line in file:
            if line:
                i += 1;
                data = line.split(",");
                aliases[data[0]] = data[1].rstrip();
    print("Loaded %d alias%s." % (i, "" if i == 1 else "es"));
                
def updateFile():
    global aliases;
    with open("aliases.csv", "w", encoding = "utf-8") as file:
        pass;
    with open("aliases.csv", "a", encoding = "utf-8") as file:
        for alias, definition in aliases.items():
            file.write(u"%s,%s\n" % (alias, definition));

def listAliases(word, word_eol, userdata, returnList = False):
    global aliases;
    for alias, definition in aliases.items():
        print("%s ==> %s" % (alias, definition));
    return hexchat.EAT_HEXCHAT;
    for line in output:
        hexchat.command("SAY %s" % line)

def addAlias(word, word_eol, userdata, overwrite = False):
    global aliases;
    alias = word[1];
    if alias in aliases and not overwrite:
        print("\"%s\" is already defined as \"%s\"" % (alias, aliases[alias]));
        print("Use /alias_overwrite to overwrite an existing alias.");
        return hexchat.EAT_HEXCHAT;
        
    definition = word_eol[2];
    aliases[alias] = definition;
    updateFile();
    
    print("Added: %s ==> %s" % (alias, definition));
    
    if not overwrite:
        return hexchat.EAT_HEXCHAT;
        
def removeAlias(word, word_eol, userdata):
    global aliases;
    alias = word[1];
    if alias not in aliases:
        print("Alias not found!");
        return hexchat.EAT_HEXCHAT;
    definition = aliases[alias];
    aliases.move_to_end(alias);
    aliases.popitem();
    updateFile();
    print("\"%s ==> %s\" removed." % (alias, definition));
    return hexchat.EAT_HEXCHAT;
    
def overwriteAlias(word, word_eol, userdata):
    addAlias(word, word_eol, userdata, True);
    return hexchat.EAT_HEXCHAT;
    
def alias(word, word_eol, userdata):
    global aliases;
    alias = word[1];
    if alias not in aliases:
        print("Alias not found!");
        return hexchat.EAT_HEXCHAT;
    hexchat.command("SAY %s" % aliases[alias]);
    return hexchat.EAT_HEXCHAT;
    
initialise();

hexchat.hook_command("alias_list", listAliases, help = alias_list_help);
hexchat.hook_command("alias_add", addAlias, help = alias_add_help);
hexchat.hook_command("alias_overwrite", overwriteAlias, help = alias_overwrite_help);
hexchat.hook_command("alias_remove", removeAlias, help = alias_remove_help);
hexchat.hook_command("alias_reload", initialise, help = alias_reload_help);
hexchat.hook_command("alias", alias, help = alias_help);
