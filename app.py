import argparse
import re
from datetime import datetime

from core.exceptions import DependencyParamError, PatternNotMatchError
from core.providers.clockfy import ClockifyAnnotation
from core.providers.jira import JiraAnnotation

providers = {"jira": JiraAnnotation, "clockify": ClockifyAnnotation}


def parse_args():
    parser = argparse.ArgumentParser(description="Opções do Sistema")

    parser.add_argument('--start-date', type=str, help="Data de início", required=False)
    parser.add_argument('--end-date', type=str, help="Data de término", required=False)

    parser.add_argument(
        "--provider",
        type=str,
        required=True,
        choices=["jira", "clockify"],
        help="Provedor de dados para preenchimento das anotações. Escolha entre 'jira' ou 'clockify'.",
    )

    parser.add_argument("--debug", action="store_true", help="Ativa o modo debug.")

    parser.add_argument(
        "--blacklist",
        type=str,
        nargs="+",
        default=[],
        help="Lista de datas de feriados no formato YYYY-MM-DD.",
    )

    return validate_dates(parser.parse_args())


def validate_dates(args):
    if args.start_date and not args.end_date:
        raise DependencyParamError(provided="--start-date", missing="--end-date")

    if args.end_date and not args.start_date:
        raise DependencyParamError(provided="--end-date", missing="--start-date")

    for val in (args.start_date, args.end_date):
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", val):
            raise PatternNotMatchError(value=val)

    start = datetime.strptime(args.start_date, "%Y-%m-%d")
    end = datetime.strptime(args.end_date, "%Y-%m-%d")
    if start > end:
        raise Exception("A --start-date não pode ser maior do que --end-data")

    args.start_date = start
    args.end_date = end
    return args

if __name__ == "__main__":
    args = parse_args()
    provider = providers[args.provider]
    provider().fill_annotations(args)
