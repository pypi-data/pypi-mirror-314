# @omlish-manifest
_CLI_MODULE = {'$omdev.cli.types.CliModule': {
    'cmd_name': 'bootstrap',
    'mod_name': __name__,
}}


if __name__ == '__main__':
    from .main import _main

    _main()
