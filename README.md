# Alfred-cheat <img src="icon.png" width="100" align="right"/> ![GitHub All Releases](https://img.shields.io/github/downloads/wayneyaoo/alfred-cheat/total.svg)
**Start writing your very own cheat sheets in your way and make them searchable using Alfred!**

# Notice

- Thanks to [@giovannicoppola](https://github.com/giovannicoppola) for porting a [python3 version dependency](https://github.com/NorthIsUp/alfred-workflow-py3) so that this workflow works on macOS >= 12.3 now where default Python version is Python3. Starting from alfred-cheat 1.2.1, the workflow requires Python3 to run, and any version lower than 1.2.1 requires python2. So depending on you macOS version, you migth want to figure out whether you need to install an extra python.

- I'm fully switching to Linux DE for personal tasks and Windows for daily work hence won't be able to put a lot of effort on this workflow. It served me well for a long time. I'm still open to new Pull Request if you think new features should be added. But generally this workflow doesn't have a big scope and should always work.

# Demo

*Every sheet shown in the demo should be your knowledge base and is totally customizable.*

![...loading demo gif](assets/demo.gif)

# About & Acknowledgement

This project was initally inspired by [cheat](https://github.com/cheat/cheat). I attempted to wrap around it but failed because that project wasn't intended to be wrapped around. So this project ended up a separate one. These two projects serve similar purpose in different working environments. With the help of alfred, your efficiency in searching your cheat sheets will be significantly boosted. And the better news is, you're in complete control of your cheat sheets unlike [tldr](https://github.com/tldr-pages/tldr) (It's good though if you want it "just work").

I built this workflow because:

1. I want faster searching than the original [cheat](https://github.com/cheat/cheat) because that project is commandline based. Sometimes I want a very quick view and don't wanna popup a shell.

2. I want to build my own knowledge base instead of community-driven cheat sheets like [tldr](https://github.com/tldr-pages/tldr) does.

**Disclaimer**:

All codes in directory `workflow` are dependencies from [this project](https://github.com/deanishe/alfred-workflow). They're not my work and is the only "dependency" for this project. Since it's included in this repo, the workflow user doesn't have to concern about dependencies.

# Download via [release](https://github.com/wx-Yao/alfred-cheat/releases)

# How it works

1. You define a directory to store your cheat sheets, which are essentially text files. And name the file the command your wanna record. e.g, `nmap`, `top`, `tar` etc. (tips: you can start with the cheat sheets provided by [cheat](https://github.com/cheat/cheat))

2. You write your cheat sheet according to the [rules](#parsing-rule) (very intuitive and tolerant) bit by bit.

3. Tell the workflow where that directory is and start searching.

# Usage

First, you need to specify your sheet directory like this. Otherwise, it doesn't work. Both absolute or relative path will work.

![](assets/config.png)

Then, you're good to go.

- To list all your cheat: `cheat`

- To search and list the content of one of your cheat: `cheat <sheet name>`. Fuzzy search and autocomplete is supported.

- To search in a specific sheet indexed by some keyword: `cheat <sheet name> <keyword>`.

- To search across all your sheets for some keyword: `cheat --search <keyword>`

- When you find your desired record and you wanna paste it directly to the app you're using (e.g., Terminal or iTerm2), hit `Enter`. This behavior can be changed in the Alfred setting ([#3](https://github.com/wx-Yao/alfred-cheat/issues/2#issuecomment-509689404)).

- If you like to just copy, hit `cmd-c`.

# Parsing rule

It's not even a rule... You just need to remember two things when writing your cheat sheet:

1. Comment first, then the command.

2. Separate each `comment, command` pair with 2 newlines. (one newline visually)

That's it.

e.g. this cheat sheet is called `demosheet`. Its content is the following:

```
# This is a one line comment. 
command one goes here.

# This is a second comment for the second command
# Yes we can have multiple line comment.
# But remember only the last line will be considered "command".
command two goes here

#
command three: in rare cases you don't have any comment, keep an empty # above.

# Any failed parsing will be ignored, like this line because it isn't associated with a command

or this line because it's a single line.
```

The above sheet will be parsed like this:

![](assets/demosheet.png)

Kindly note that **hidden cheatsheets (starting with `.`) will be ignored and hidden directory will be ignored as well**. Hierachical structure is supported but that's only for your management purpose. This tool will only "flatten" every cheatsheets in the base directory. i.e., `cheat/mydir/yourdir/somecheat` will be equivalent to `cheat/somecheat` in its perspective. Also make sure you don't have duplicated cheatsheets in different directories otherwise only one of them will be dominant. Thanks for [@Blackvz](https://github.com/Blackvz) for the feature suggestion [#4](https://github.com/wx-Yao/alfred-cheat/issues/4).

# Compatibility

This workflow works out of the box (zero dependencies). It's tested on **macOS 10.14.5 Mojave** with **Alfred 4**. You need the [powerpack](https://www.alfredapp.com/shop/) to get it working. I believe it works with Alfred3 on any macOS after 10.10 Yosemite but that hasn't been tested. Report an issue if there's a problem.

# Contribution

Any idea of improvement will be welcomed. But I don't wanna add the feature of modifying cheat sheet right in Alfred because it isn't what it is supposed to do. Use vim or other editors you like.
