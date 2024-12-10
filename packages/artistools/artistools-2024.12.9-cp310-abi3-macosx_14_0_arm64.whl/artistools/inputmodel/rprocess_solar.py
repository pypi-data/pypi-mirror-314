#!/usr/bin/env python3
import argparse
import math
from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

import artistools as at


def addargs(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-outputpath", "-o", default=".", help="Path for output files")


def main(args: argparse.Namespace | None = None, argsraw: Sequence[str] | None = None, **kwargs) -> None:
    """Create solar r-process pattern in ARTIS format."""
    if args is None:
        parser = argparse.ArgumentParser(formatter_class=at.CustomArgHelpFormatter, description=__doc__)

        addargs(parser)
        at.set_args_from_dict(parser, kwargs)
        args = parser.parse_args([] if kwargs else argsraw)

    dfsolarabund = pd.read_csv(
        at.get_config()["path_datadir"] / "solar_r_abundance_pattern.txt", sep=r"\s+", comment="#"
    )

    dfsolarabund["radioactive"] = True

    # print(dfsolarabund)

    dfbetaminus = pd.read_csv(
        at.get_config()["path_datadir"] / "betaminusdecays.txt",
        sep=r"\s+",
        comment="#",
        names=["A", "Z", "Q[MeV]", "Egamma[MeV]", "Eelec[MeV]", "Eneutrino[MeV]", "tau[s]"],
    )

    def undecayed_z(row):
        dfmasschain = dfbetaminus.query("A == @row.A", inplace=False)
        return int(row.Z) if dfmasschain.empty else int(dfmasschain.Z.min())

    dfsolarabund_undecayed = dfsolarabund.copy()
    dfsolarabund_undecayed["Z"] = dfsolarabund_undecayed.apply(undecayed_z, axis=1)

    # Andreas uses 90% Fe and the rest solar
    dfsolarabund_undecayed = pd.concat(
        [
            dfsolarabund_undecayed,
            pd.DataFrame([
                {"Z": 26, "A": 56, "numberfrac": 0.005, "radioactive": False},
                {"Z": 27, "A": 59, "numberfrac": 0.005, "radioactive": False},
                {"Z": 28, "A": 58, "numberfrac": 0.005, "radioactive": False},
            ]),
        ],
        ignore_index=True,
    )

    normfactor = (  # noqa: F841
        dfsolarabund_undecayed.numberfrac.sum()
    )  # convert number fractions in solar to fractions of r-process
    dfsolarabund_undecayed = dfsolarabund_undecayed.eval("numberfrac = numberfrac / @normfactor").eval(
        "massfrac = numberfrac * A"
    )
    massfracnormfactor = dfsolarabund_undecayed.massfrac.sum()  # noqa: F841
    dfsolarabund_undecayed = dfsolarabund_undecayed.eval("massfrac = massfrac / @massfracnormfactor")

    # print(dfsolarabund_undecayed)

    t_model_init_days = 0.000231481
    t_model_init_seconds = t_model_init_days * 24 * 60 * 60  # noqa: F841

    wollager_profilename = "wollager_ejectaprofile_10bins.txt"
    if Path(wollager_profilename).exists():
        with Path(wollager_profilename).open("rt", encoding="utf-8") as f:
            t_model_init_days_in = float(f.readline().strip().removesuffix(" day"))
        dfdensities = pd.read_csv(
            wollager_profilename, sep=r"\s+", skiprows=1, names=["cellid", "vel_r_max_kmps", "rho"]
        )
        dfdensities["mgi"] = dfdensities["cellid"].astype(int)
        dfdensities["vel_r_min_kmps"] = np.concatenate(([0.0], dfdensities["vel_r_max_kmps"].to_numpy()[:-1]))

        t_model_init_seconds_in = t_model_init_days_in * 24 * 60 * 60  # noqa: F841
        dfdensities = dfdensities.eval(
            "mass_g = rho * 4. / 3. * @math.pi * (vel_r_max_kmps ** 3 - vel_r_min_kmps ** 3)"
            "* (1e5 * @t_model_init_seconds_in) ** 3"
        )

        # now replace the density at the input time with the density at required time

        dfdensities = dfdensities.eval(
            "rho = mass_g / ("
            "4. / 3. * @math.pi * (vel_r_max_kmps ** 3 - vel_r_min_kmps ** 3)"
            " * (1e5 * @t_model_init_seconds) ** 3)"
        )
    else:
        dfdensities = pd.DataFrame([{"rho": 10**-3, "vel_r_max_kmps": 6.0e4, "mgi": 0}])

    dfdensities["inputcellid"] = dfdensities["mgi"] + 1
    # print(dfdensities)
    cellcount = len(dfdensities)

    dictelemabund = {}
    for atomic_number in range(1, dfsolarabund_undecayed.Z.max() + 1):
        dictelemabund[f"X_{at.get_elsymbol(atomic_number)}"] = dfsolarabund_undecayed.query(
            "Z == @atomic_number", inplace=False
        ).massfrac.sum()

    dfelabundances = pl.DataFrame([{"inputcellid": mgi + 1} | dictelemabund for mgi in range(cellcount)])
    # print(dfelabundances)
    at.inputmodel.save_initelemabundances(dfelabundances=dfelabundances, outpath=Path(args.outputpath))

    # write model.txt

    rowdict = {
        "X_Fegroup": 1.0,
        "X_Ni56": 0.0,
        "X_Co56": 0.0,
        "X_Fe52": 0.0,
        "X_Cr48": 0.0,
        "X_Ni57": 0.0,
        "X_Co57": 0.0,
    }

    for _, row in dfsolarabund_undecayed.query("radioactive == True").iterrows():
        rowdict[f"X_{at.get_elsymbol(int(row.Z))}{int(row.A)}"] = row.massfrac

    modeldata = [
        (
            {
                "inputcellid": densityrow["inputcellid"],
                "vel_r_max_kmps": densityrow["vel_r_max_kmps"],
                "logrho": math.log10(densityrow["rho"]),
            }
            | rowdict
        )
        for mgi, densityrow in dfdensities.iterrows()
    ]

    dfmodel = pd.DataFrame(modeldata)
    # print(dfmodel)
    at.inputmodel.save_modeldata(dfmodel=dfmodel, t_model_init_days=t_model_init_days, outpath=args.outputpath)


if __name__ == "__main__":
    main()
