#!/usr/bin/env python3


import argparse
import math
import typing as t
from math import exp

from astropy import units as u

import artistools as at


def forward_doubledecay(
    iso1fract0: float | u.Quantity,
    iso2fract0: float | u.Quantity,
    iso3fract0: float | u.Quantity,
    tlate: float | u.Quantity,
    meanlife1_days: float | u.Quantity,
    meanlife2_days: float | u.Quantity,
) -> tuple[float | u.Quantity, float | u.Quantity, float | u.Quantity]:
    # get the abundances at a late time from the time zero abundances
    # e.g. Ni56 -> Co56 -> Fe56 decay
    # meanlife1 is the mean lifetime of the parent (e.g. Ni56) and meanlife2 is the mean life of the daughter nucleus (e.g. Co56)
    assert tlate > 0

    lamb1 = 1 / meanlife1_days
    lamb2 = 1 / meanlife2_days

    iso1fraclate = iso1fract0 * exp(-lamb1 * tlate)  # larger abundance before decays

    iso2fraclate = iso2fract0 * exp(-lamb2 * tlate) + iso1fract0 * lamb1 / (lamb1 - lamb2) * (
        exp(-lamb2 * tlate) - exp(-lamb1 * tlate)
    )

    iso3fromdecay = (
        (iso1fract0 + iso2fract0) * (lamb1 - lamb2)
        - iso2fract0 * lamb1 * exp(-lamb2 * tlate)
        + iso2fract0 * lamb2 * exp(-lamb2 * tlate)
        - iso1fract0 * lamb1 * exp(-lamb2 * tlate)
        + iso1fract0 * lamb2 * exp(-lamb1 * tlate)
    ) / (lamb1 - lamb2)

    iso3fraclate = iso3fract0 + iso3fromdecay

    return iso1fraclate, iso2fraclate, iso3fraclate


def addargs(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-modelpath", default=".", help="Path to ARTIS folder")

    parser.add_argument("-timedays", "-t", default=330, type=float, help="Time in days")


def main_analytical(args: argparse.Namespace | None = None, argsraw: list[str] | None = None, **kwargs: t.Any) -> None:
    """Use the model initial conditions to calculate the deposition rates."""
    if args is None:
        parser = argparse.ArgumentParser(formatter_class=at.CustomArgHelpFormatter, description=__doc__)
        addargs(parser)
        at.set_args_from_dict(parser, kwargs)
        args = parser.parse_args([] if kwargs else argsraw)
    dfmodel, modelmeta = at.inputmodel.get_modeldata(args.modelpath, derived_cols=["mass_g", "vel_r_min_kmps"])

    t_init = modelmeta["t_model_init_days"] * u.day

    meanlife_ni56 = 8.8 * u.day
    meanlife_co56 = 113.7 * u.day
    # define TCOBALT (113.7*DAY)     // cobalt-56
    # T48CR = 1.29602 * u.day
    # T48V = 23.0442 * u.day
    # define T52FE   (0.497429*DAY)
    # define T52MN   (0.0211395*DAY)

    t_now = args.timedays * u.day
    print(f"t_now = {t_now.to('d')}")
    print("The following assumes that all 56Ni has decayed to 56Co and all energy comes from emitted positrons")

    # adata = at.atomic.get_levels(args.modelpath, get_photoionisations=True)
    # timestep = at.get_timestep_of_timedays(args.modelpath, args.timedays)
    # dfnltepops = at.nltepops.read_files(
    #     args.modelpath, timestep=timestep).query('Z == 26')

    # phixs = adata.query('Z==26 & ion_stage==1', inplace=False).iloc[0].levels.iloc[0].phixstable[0][1] * 1e-18

    global_posdep = 0.0 * u.erg / u.s
    for i, row in dfmodel.iterrows():
        v_inner = row["vel_r_min_kmps"] * u.km / u.s
        v_outer = row["vel_r_max_kmps"] * u.km / u.s

        volume_init = ((4 * math.pi / 3) * ((v_outer * t_init) ** 3 - (v_inner * t_init) ** 3)).to("cm3")

        volume_now = ((4 * math.pi / 3) * ((v_outer * t_now) ** 3 - (v_inner * t_now) ** 3)).to("cm3")

        # volume_now2 = (volume_init * (t_now / t_init) ** 3).to('cm3')

        rho_init = (10 ** row["logrho"]) * u.g / u.cm**3
        mni56_init = row["X_Ni56"] * (volume_init * rho_init).to("solMass")
        mco56_init = row["X_Co56"] * (volume_init * rho_init).to("solMass")
        mfe56_init = 0
        # mco56_now = mco56_init * math.exp(- (t_now - t_init) / meanlife_co56)
        _mni56_now, mco56_now, _mfe56_now = forward_doubledecay(
            mni56_init, mco56_init, mfe56_init, t_now - t_init, meanlife_ni56, meanlife_co56
        )

        co56_positron_dep = (0.19 * 0.610 * u.MeV * (mco56_now / (55.9398393 * u.u)) / meanlife_co56).to("erg/s")
        v48_positron_dep = 0

        global_posdep += co56_positron_dep
        power_now = co56_positron_dep + v48_positron_dep

        epsilon = power_now / volume_now
        print(f"zone {i:3d}, velocity = [{v_inner:8.2f}, {v_outer:8.2f}], epsilon = {epsilon:.3e}")
        # print(f'  epsilon = {epsilon.to("eV/(cm3s)"):.2f}')

        # dfnltepops_cell = dfnltepops.query('modelgridindex == @i', inplace=False)
        # if not dfnltepops_cell.empty:
        #     nnlevel = dfnltepops_cell.query('level == 0', inplace=False).iloc[0]['n_NLTE']
        #     width = ((v_outer - v_inner) * t_now).to('cm').value
        #     tau = width * phixs * nnlevel
        #     print(f'width: {width:.3e} cm, phixs: {phixs:.3e} cm^2, nnlevel: {nnlevel:.3e} cm^-3, tau: {tau:.3e}')
    print(f"Global posdep: {global_posdep.to('solLum'):.3e}")


def main(args: argparse.Namespace | None = None, argsraw: list[str] | None = None, **kwargs: t.Any) -> None:
    """Plot deposition rate of a model at time t (days)."""
    main_analytical(args=args, argsraw=argsraw, **kwargs)
    if args is None:
        parser = argparse.ArgumentParser(formatter_class=at.CustomArgHelpFormatter, description=__doc__)
        addargs(parser)
        at.set_args_from_dict(parser, kwargs)
        args = parser.parse_args([] if kwargs else argsraw)

        # TODO: plot deposition.out file!


if __name__ == "__main__":
    main()
