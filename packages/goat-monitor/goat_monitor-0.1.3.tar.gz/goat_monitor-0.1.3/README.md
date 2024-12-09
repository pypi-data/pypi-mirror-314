# Goat Monitor

A command line tool for remotely monitoring command execution using Gotify.

Yes, I know Gotify doesn't have "goat" in its name but it sounds like it.

## Configuration

Configuration lives in a TOML file which should have (at a minimum) the following:

```toml
server = "https://gotify.example.com"
app_token = "app_token_from_gotify"
```

## Usage

```
goat_monitor --config ./config.toml --retries 3 -- <COMMAND TO MONITOR>
```

The command can be any shell command including arbitrarily many options / arguments.
Note that `--` is often necessary to prevent options within the monitored command from being parsed as options to goat_monitor.