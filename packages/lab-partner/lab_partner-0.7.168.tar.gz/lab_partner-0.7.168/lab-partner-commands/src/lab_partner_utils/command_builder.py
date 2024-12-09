import typing as t
import inspect
import importlib

import click
from click import Context, Command, Option, Argument
import docstring_parser


class CommandBuilder(click.MultiCommand):

    def __init__(self, fn_list: t.List[t.Callable], name: t.Optional[str] = None, invoke_without_command: bool = False,
                 no_args_is_help: t.Optional[bool] = None, subcommand_metavar: t.Optional[str] = None,
                 chain: bool = False, result_callback: t.Optional[t.Callable[..., t.Any]] = None,
                 **attrs: t.Any) -> None:
        super().__init__(name, invoke_without_command, no_args_is_help, subcommand_metavar, chain, result_callback, **attrs)
        self.fn_map = {fn.__name__: inspect.getmodule(fn).__name__ for fn in fn_list}

    def list_commands(self, ctx: Context) -> t.List[str]:
        command_names = list(self.fn_map.keys())
        command_names.sort()
        return command_names

    def get_command(self, ctx: Context, cmd_name: str) -> t.Optional[Command]:
        module = importlib.import_module(self.fn_map[cmd_name])
        fn = getattr(module, cmd_name)

        docstring = docstring_parser.parse(inspect.getdoc(fn))
        help = f'''
        {docstring.short_description}
        
        {docstring.long_description}
        '''
        short_help = docstring.short_description
        fn_sig = inspect.signature(fn)

        options = []
        for i, param in enumerate(fn_sig.parameters.values()):
            arg_type = click.types.convert_type(param.annotation)
            arg_name = param.name.replace('_', '-')
            print(f'param.annotation: {param.annotation}')
            arg_description = docstring.params[i].description




