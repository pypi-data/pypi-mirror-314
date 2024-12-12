import sys
from argparse import ArgumentParser
from gluepy import VERSION
from gluepy.exceptions import CommandError


REGISTRY = {}


class Command(object):
    """Define a command that will be exposed to the CLI"""

    label = None
    parser_class = ArgumentParser
    autoload = True

    def __init_subclass__(cls, **kwargs):
        """Register the class in a REGISTRY to be used from cli"""
        super().__init_subclass__(**kwargs)
        if not cls.autoload:
            return

        name = cls.label or cls.__name__.lower()
        REGISTRY[name] = cls

    def handle(self, *args, **kwargs):
        """Hook to add logic to your command"""
        raise NotImplementedError("Command has not been implemented yet.")

    def add_arguments(self, parser):
        """Hook to add additional arguments to the parser"""
        pass

    def stdout(self, message):
        print(message)

    def stderr(self, message):
        print(message)

    def run(self):
        parser = self.parser_class()
        self.add_arguments(parser)
        kwargs = vars(parser.parse_args(args=None if sys.argv[1:] else ["--help"]))
        self.handle(**kwargs)


class DefaultCommand(Command):
    """Default command used when no command is provided.

    e.g. `.run.py --version` will use this command.

    """

    autoload = False

    def add_arguments(self, parser):
        parser.add_argument(
            "--list", "-l", help="List all available commands", action="store_true"
        )
        parser.add_argument(
            "--version", help="Print version of Gluepy", action="store_true"
        )

    def handle(self, **options):
        if not options:
            self.parser_class().print_help()
        elif options.get("version"):
            self.stdout("Gluepy version: %s" % VERSION)
        elif options.get("list"):
            self.stdout(
                "Available commands: \n%s" % "\n".join([cmd for cmd in REGISTRY.keys()])
            )


def call_command():
    """Main method that parse which command to call and calls it"""
    if len(sys.argv) <= 1 or sys.argv[1].startswith("-"):
        DefaultCommand().run()
        return

    cmd_label = sys.argv.pop(1)

    try:
        cmd = REGISTRY[cmd_label]()
    except KeyError:
        raise CommandError(f"The command '{cmd_label}' is not defined.")

    cmd.run()
