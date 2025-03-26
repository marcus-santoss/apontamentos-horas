import argparse

from core.providers.clockfy import ClockifyAnnotation
from core.providers.jira import JiraAnnotation

providers = {"jira": JiraAnnotation, "clockify": ClockifyAnnotation}


def parse_args():
    parser = argparse.ArgumentParser(description="Opções do Sistema")

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

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    provider = providers[args.provider]
    provider().fill_annotations(debug=args.debug, black_list=args.blacklist)
