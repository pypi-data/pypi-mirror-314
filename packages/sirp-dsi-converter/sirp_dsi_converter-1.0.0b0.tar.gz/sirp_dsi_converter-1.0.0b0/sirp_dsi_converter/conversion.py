import argparse

import rdflib

from .transformation import compoundUnitValidation


def dsi_to_sirp(dsi_string: str):
    # instantiate new class for this string
    info = compoundUnitValidation(dsi_string)

    # run validation and conversion
    info.validation()

    # prepare output
    if info.output_sirp_correspondance:
        graph = info.__g__
    else:
        graph = rdflib.Graph()

    return graph


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="convert_d2s",
        description="Convert D-SI unit string to corresponding SI Reference Point Representation in Turtle",
    )

    parser.add_argument(
        "dsi_string",
        default="",
        help="unit to convert from DSI to SIRP-TTL",
    )

    # parse CLI arguments
    args = parser.parse_args()

    g = dsi_to_sirp(args.dsi_string)
    ttl = g.serialize(format="ttl")
    print(ttl)
