import argparse

from tafel.core.reader import Reader


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True)
    parser.add_argument(
        "-p", "--ph", type=float, default=13, help="pH of the electrolyte (default: 13)"
    )
    parser.add_argument(
        "-r",
        "--reference-potential",
        type=float,
        default=0.210,
        help="""Reference potential in V vs RHE (default: 0.210 V)
    Common choices:
        Standard hydrogen electrode (SHE): 0.0 V
        Saturated calomel electrode: 0.241 V
        Ag/AgCl/saturated KCl: 0.197 V
        Ag/AgCl/3.5 mol/kg KCl: 0.205 V
        Ag/AgCl/3.0 mol/kg KCl: 0.210 V
        Ag/AgCl/1.0 mol/kg KCl: 0.235 V
        Ag/AgCl/0.6 mol/kg KCl: 0.250 V
        Ag/AgCl (seawater): 0.266 V""",
    )
    parser.add_argument(
        "-e", "--electrolyte-resistance (default: 0.05)", type=float, default=0.05
    )

    args = parser.parse_args()

    reader = Reader(
        ph=args.ph,
        reference_potential=args.reference_potential,
        electrolyte_resistance=args.electrolyte_resistance,
    )
    reader.read_mpt(args.file)


if __name__ == "__main__":
    main()
