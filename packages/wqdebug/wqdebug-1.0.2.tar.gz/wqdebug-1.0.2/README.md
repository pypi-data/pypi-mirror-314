# wqdebug

## Install
pip install wqdebug

## Usage
```cmd
# cmd or powershell or bash
wqdebug
```

### GDB
```
(gdb) wq
"wq" must be followed by the name of a subcommand.
List of wq subcommands:

wq dfs -- print dfs.
wq find -- find ram.
wq heap5 -- freertos heap5.
wq ipc -- IPC
wq kv -- print Key Value cache list.
wq log -- print log buffer.
wq pm -- print power manage device list.
wq queue -- wq os shim queue.
wq queue_app -- print app queue.
wq queue_as -- print audio service queue.
wq queue_share -- print share task queue.
wq rpc -- RPC
wq section -- print section.
wq stack -- dispaly stack info. usage: wq stack [full]
wq task -- print all tasks
wq timer -- print all timer
wq tlsf -- wq tlsf.
wq trace -- freertos trace
wq usage -- print usage
wq wdt -- WDT

Type "help wq" followed by wq subcommand name for full documentation.
Type "apropos word" to search for commands related to "word".
Type "apropos -v word" for full documentation of commands related to "word".
Command name abbreviations are allowed if unambiguous.
```

## Develop
pip install -e .

