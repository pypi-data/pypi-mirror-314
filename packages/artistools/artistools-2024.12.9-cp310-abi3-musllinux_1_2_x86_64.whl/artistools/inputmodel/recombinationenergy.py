#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argparse
import string
import typing as t
from collections.abc import Sequence
from pathlib import Path

import argcomplete
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import artistools as at


def get_model_recombenergy(dfbinding, args: argparse.Namespace):
    args.inputfile = Path(
        "/Users/luke/Library/Mobile"
        " Documents/com~apple~CloudDocs/artis_runs/kilonova_SFHo_1d_0p05day_ufix_betaminusthermdelay_fixinitialye_verylate_redo"
    )

    print(f"Reading {args.inputfile}")
    dfmodel, t_model_init_days, _ = at.inputmodel.get_modeldata_tuple(args.inputfile, get_elemabundances=False)

    t_model_init_seconds = t_model_init_days * 24 * 60 * 60
    print(f"Model is defined at {t_model_init_days} days ({t_model_init_seconds:.4f} seconds)")

    msun_g = 1.989e33
    amu_g = 1.66054e-24  # 1 atomic mass unit in grams
    ev_erg = 1.60218e-12  # 1 eV in erg
    mass_msun_rho = dfmodel["mass_g"].sum() / msun_g

    mass_msun_accounted = 0.0
    model_el_binding_en_ev: dict[str, float] = {}
    model_tot_binding_en_ev = 0.0
    for column in dfmodel.columns:
        if column.startswith("X_"):
            species = column.replace("X_", "")
            speciesabund_g = np.dot(dfmodel[column], dfmodel["mass_g"])

            species_mass_msun = speciesabund_g / msun_g

            if species[-1].isdigit():  # isotopic species
                atomic_number = at.get_atomic_number(species)
                elsymb = at.get_elsymbol(atomic_number)
                massnumber = int(species.lstrip(string.ascii_letters))
                matchrows = dfbinding.query("Z == @atomic_number")

                binding_en_ev = 0.0 if matchrows.empty else matchrows.iloc[0]["TotBEn"]

                # print(species, atomic_number, massnumber, el_binding_en_ev)
                contrib_binding_en_ev = speciesabund_g / (massnumber * amu_g) * binding_en_ev

                model_el_binding_en_ev[elsymb] = model_el_binding_en_ev.get(elsymb, 0.0) + contrib_binding_en_ev
                mass_msun_accounted += species_mass_msun
                model_tot_binding_en_ev += contrib_binding_en_ev

            elif species.lower() != "fegroup":  # ignore special group abundance
                pass

    def sortkey(item):
        return at.get_atomic_number(item[0])

    for _elsymb, binding_en_ev in sorted(model_el_binding_en_ev.items(), key=sortkey):
        zstr = f"Z={atomic_number}"
        print(f"{zstr:>5} {binding_en_ev * ev_erg} erg")

    print(f"Total electron binding energy {model_tot_binding_en_ev * ev_erg:.3e} erg")
    print(f"Mass from density {mass_msun_rho:.3e}")
    print(f"Mass from sum of isotopes {mass_msun_accounted:.3e}")


def get_particle_elec_binding_energy_per_gram(traj_root, dictbinding, particleid, time_s):
    # find the closest timestep to the required time
    nts = at.inputmodel.rprocess_from_trajectory.get_closest_network_timestep(traj_root, particleid, time_s)
    memberfilename = f"./Run_rprocess/nz-plane{nts:05d}"

    dftrajnucabund, _ = at.inputmodel.rprocess_from_trajectory.get_trajectory_timestepfile_nuc_abund(
        traj_root=traj_root, particleid=particleid, memberfilename=memberfilename
    )

    dftrajnucabund["Z_be_tot_ev"] = [dictbinding.get(Z, 0.0) for Z in dftrajnucabund["Z"]]

    amu_g = 1.66054e-24  # 1 atomic mass unit in grams  # noqa: F841

    # frac_unaccounted = dftrajnucabund[dftrajnucabund['Z_be_tot_ev'] == 0].massfrac.sum()
    # print(f'frac_unaccounted {frac_unaccounted}')
    # if frac_unaccounted > .3:
    #     print(dftrajnucabund)
    # assert frac_unaccounted < 0.3

    dftrajnucabund = dftrajnucabund.eval("recombenergy_ev_per_gram = Z_be_tot_ev * massfrac / (Z + N) / @amu_g")

    # contrib_binding_en_ev = speciesabund_g / (massnumber * amu_g) * binding_en_ev

    # print(dftrajnucabund)

    return dftrajnucabund["recombenergy_ev_per_gram"].sum()


def get_particle_nucenergy_released(traj_root, particleid, tmin_s, time_s_end):  # noqa: ARG001
    from scipy import integrate

    memberfilename = "./Run_rprocess/energy_thermo.dat"
    erg_to_ev = 6.242e11
    with at.inputmodel.rprocess_from_trajectory.open_tar_file_or_extracted(
        traj_root=traj_root, particleid=particleid, memberfilename=memberfilename
    ) as fthermo:
        dfthermo = pd.read_csv(fthermo, sep=r"\s+", usecols=["#count", "time/s", "Qdot", "Ye"])
        dfthermo = dfthermo.rename(columns={"time/s": "time_s"})
        dfthermo = dfthermo.query("time_s >= @tmin_s")
        dfthermo = dfthermo.query("time_s <= @time_s_end")
        return integrate.trapezoid(y=dfthermo["Qdot"], x=dfthermo["time_s"]) * erg_to_ev
        # print(dfthermo)


def get_particles_recomb_nuc_energy(traj_root, dfbinding):
    # sourcery skip: use-contextlib-suppress
    dfsnapshot = at.inputmodel.modelfromhydro.read_ejectasnapshot(
        "/Users/luke/Library/Mobile Documents/com~apple~CloudDocs/Archive/Astronomy/Mergers/SFHo_snapshot"
    ).sort_values("ye")

    dictbinding = dict(dfbinding[["Z", "TotBEn"]].itertuples(index=False))

    tmin_s = 10
    time_s = 6 * 3600

    ye_list = []
    elecbinding_en_list = []
    nuclear_released_en_list = []
    for particleid, ye, _pmass in dfsnapshot[["id", "ye", "pmass"]].itertuples(index=False):
        try:
            elecbinding_en = get_particle_elec_binding_energy_per_gram(
                traj_root=traj_root, dictbinding=dictbinding, particleid=particleid, time_s=time_s
            )
            nuc_en_released = get_particle_nucenergy_released(
                traj_root=traj_root, particleid=particleid, tmin_s=tmin_s, time_s_end=time_s
            )
            ye_list.append(ye)
            elecbinding_en_list.append(elecbinding_en)
            nuclear_released_en_list.append(nuc_en_released)
            # print(particleid, ye, elecbinding_en)
        except FileNotFoundError:
            # print(f' WARNING particle {particleid} not found! ')
            pass

    dfrecomb = pd.DataFrame({
        "ye": ye_list,
        "recombenergy_ev_per_gram": elecbinding_en_list,
        "nuclear_released_ev_per_gram": nuclear_released_en_list,
    })

    print(dfrecomb)

    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        sharex=True,
        sharey=False,
        figsize=(6, 4),
        tight_layout={"pad": 0.4, "w_pad": 0.0, "h_pad": 0.0},
    )

    ax.plot(
        dfrecomb["ye"],
        dfrecomb["recombenergy_ev_per_gram"],
        label=f"electron binding for composition at {time_s:.1e} s [eV/g]",
        lw=0,
        marker=".",
    )
    ax.plot(
        dfrecomb["ye"],
        dfrecomb["nuclear_released_ev_per_gram"],
        label=f"nuclear release between {tmin_s:.1e} s and {time_s:.1e} s [eV/g]",
        lw=0,
        marker=".",
    )
    ax.legend(loc="best", handlelength=2, frameon=False, numpoints=1)
    ax.set_xlabel("Ye")
    ax.set_yscale("log")
    ax.set_ylim(bottom=1e24, top=1e33)

    fig.savefig("recomb.pdf", format="pdf")


def addargs(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-inputfile", "-i", default="model.txt", help="Path of input file or folder containing model.txt"
    )


def main(args: argparse.Namespace | None = None, argsraw: Sequence[str] | None = None, **kwargs: t.Any) -> None:
    if args is None:
        parser = argparse.ArgumentParser(
            formatter_class=at.CustomArgHelpFormatter,
            description="Get the recombination energy from fully ionised to fully neutral for an input model.",
        )

        addargs(parser)
        at.set_args_from_dict(parser, kwargs)
        argcomplete.autocomplete(parser)
        args = parser.parse_args([] if kwargs else argsraw)

    with Path(at.get_config()["path_datadir"], "ElBiEn_2007.txt").open(encoding="utf-8") as fbinding:
        for _ in range(11):
            header = fbinding.readline().lstrip(" #").split()
        # print(header)
        dfbinding = pd.read_csv(fbinding, sep=r"\s+", names=header)
        # print(dfbinding)

    traj_root = Path(
        Path.home() / "Google Drive/Shared Drives/GSI NSM/Mergers/SFHo_long/Trajectory_SFHo_long-radius-entropy"
    )
    get_model_recombenergy(dfbinding, args)
    get_particles_recomb_nuc_energy(traj_root, dfbinding)


if __name__ == "__main__":
    main()
