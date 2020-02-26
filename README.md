# `shell_pipe`

[Pelican](https://blog.getpelican.com/) plugin for piping shell output (`stdout`) into site content (articles and pages), unlocking the versatility and flexibility of the shell for automated content generation and updates.

## warning

`shell_pipe` relies on `shell=True` flag within Python's [`subprocess`] library, and this comes with [risks](https://docs.python.org/2/library/subprocess.html#frequently-used-arguments).

Make sure you control the source of commands to avoid shell injection and arbitrary command execution. 

## usage

Add `shell_pipe` to `PLUGINS` list:

```python
PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = [
    # ...
    "shell_pipe",
    # ...
]
```

Then, specify shell commands in-line in post & article sources:

```markdown
Title: My Post

...

<!-- SHELL_BEGIN -->my-shell-command<!-- SHELL_END --> 
```

## example

See this [example](https://coyote.life/skoolie-budget.html).
 
A budget-balance report was produced by [`hledger`](https://hledger.org/), a command-line plaintext accounting program and written to the article's content.
 
In the post's source markdown:

```markdown
<pre><!-- SHELL_BEGIN -->hledger bal -f ./.ledger/bus | head -n -2 | sed -z 's/\n/<br>/g'<!-- SHELL_END --></pre>
```

The post is updated to reflect the latest ledger each time the site is built: the `hledger` command is executed with the latest input file `./ledger/bus`.










