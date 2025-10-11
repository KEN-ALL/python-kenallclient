import argparse
import os
import sys
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from pprint import pprint
from typing import Dict, Type

from .client import KenAllClient


class Command(metaclass=ABCMeta):
    @abstractmethod
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        pass

    @abstractmethod
    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pass


commands: Dict[str, Command] = {}


def command(name: str) -> Callable[[Type[Command]], Type[Command]]:
    def _(typ: Type[Command]) -> Type[Command]:
        commands[name] = typ()
        return typ

    return _


@command("get")
class GetCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("postalcode")

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(client.get(args.postalcode, api_version=args.api_version))


@command("search")
class SearchCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--query", "-q")
        parser.add_argument("--text", "-t")
        parser.add_argument("--offset", type=int)
        parser.add_argument("--limit", type=int)
        parser.add_argument("--facet")

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(
            client.search(
                q=args.query,
                t=args.text,
                offset=args.offset,
                limit=args.limit,
                facet=args.facet,
            )
        )


@command("get-houjin")
class GetHoujinCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("houjinbangou")

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(client.get_houjin(args.houjinbangou, api_version=args.api_version))


@command("search-houjin")
class SearchHoujinCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("query")
        parser.add_argument("--offset", type=int)
        parser.add_argument("--limit", type=int)
        parser.add_argument("--mode")
        parser.add_argument("--facet-area")
        parser.add_argument("--facet-kind")
        parser.add_argument("--facet-process")
        parser.add_argument("--facet-close-cause")

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(
            client.search_houjin(
                q=args.query,
                offset=args.offset,
                limit=args.limit,
                mode=args.mode,
                facet_area=args.facet_area,
                facet_kind=args.facet_kind,
                facet_process=args.facet_process,
                facet_close_cause=args.facet_close_cause,
                api_version=args.api_version,
            )
        )


@command("search-holiday")
class SearchHolidayCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--year", type=int)
        parser.add_argument("--from", dest="from_")
        parser.add_argument("--to", dest="to")

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(
            client.search_holiday(
                year=args.year,
                from_=args.from_,
                to=args.to,
                api_version=args.api_version,
            )
        )


@command("get-banks")
class GetBanksCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        pass

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(client.get_banks(api_version=args.api_version))


@command("get-bank")
class GetBankCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("bank_code")

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(client.get_bank(args.bank_code, api_version=args.api_version))


@command("get-bank-branches")
class GetBankBranchesCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("bank_code")

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(client.get_bank_branches(args.bank_code, api_version=args.api_version))


@command("get-bank-branch")
class GetBankBranchCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("bank_code")
        parser.add_argument("bank_branch")

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(
            client.get_bank_branch(
                bank_code=args.bank_code,
                branch_code=args.bank_branch,
                api_version=args.api_version,
            )
        )


@command("get-school")
class GetSchoolCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("school_code")

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(client.get_school(args.school_code, api_version=args.api_version))


@command("search-school")
class SearchSchoolCommand(Command):
    def add_subparser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("query")
        parser.add_argument("--offset", type=int)
        parser.add_argument("--limit", type=int)
        parser.add_argument("--facet-area")
        parser.add_argument("--facet-prefecture")
        parser.add_argument("--facet-type")
        parser.add_argument("--facet-establishment-type")
        parser.add_argument("--facet-branch")

    def execute(self, client: KenAllClient, args: argparse.Namespace) -> None:
        pprint(
            client.search_school(
                q=args.query,
                offset=args.offset,
                limit=args.limit,
                facet_area=args.facet_area,
                facet_prefecture=args.facet_prefecture,
                facet_type=args.facet_type,
                facet_establishment_type=args.facet_establishment_type,
                facet_branch=args.facet_branch,
                api_version=args.api_version,
            )
        )


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apikey", default=os.environ.get("KENALL_API_KEY"))
    parser.add_argument("--apiurl", default=os.environ.get("KENALL_API_URL"))
    parser.add_argument(
        "--api-version",
        choices=["2022-09-01", "2022-11-01", "2023-09-01", "2024-01-01", "2025-01-01"],
        help="API version to use",
    )
    subparsers = parser.add_subparsers(dest="command")
    for name, command in commands.items():
        subparser = subparsers.add_parser(name)
        command.add_subparser(subparser)

    return parser


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    if args.apikey is None:
        args.apikey = os.environ.get("KENALL_API_KEY")
    if args.apikey is None:
        sys.stderr.write(
            "API key is not provided through the command line argument "
            "or KENALL_API_KEY environment variable\n"
        )
        sys.exit(255)
    if args.command is None:
        parser.print_help()
        sys.exit(255)
    client = KenAllClient(api_key=args.apikey, api_url=args.apiurl)
    commands[args.command].execute(client, args)


main()
