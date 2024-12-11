Examples
================================================================================

### 01_type_hint.py

```console
$ python3 01_type_hint.py config.toml --epochs 10 --model cnn --lr 0.01
YadOptArgs(config_path=config.toml, epochs=10, model=cnn, lr=0.01, help=False)
```

### 02_decorator.py

```console
$ python3 02_decorator.py config.toml --epochs 10 --model cnn --lr 0.01
YadOptArgs(config_path=config.toml, epochs=10, model=cnn, lr=0.01, help=False)
```

### 03_sub_command.py

```console
$ python3 03_subcommand.py foo --foo_opt 10
YadOptArgs(foo_opt=0, bar_opt=0, help=False, foo=True)
```

