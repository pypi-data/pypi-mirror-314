import random
from functools import wraps
from typing import Callable

import numpy as np

from .utils import (
    match_lists,
    to_abs,
    DOUBLE_THR,
)

from .. import (
    Confpool,
    base,
    H2KC,
    KC2H,
    Molecule,
)

MolProxy = base.MolProxy

PYXYZ_TESTS = {}


def test(raw_f: Callable) -> Callable:

    @wraps(raw_f)
    def f():
        try:
            raw_f()
            success = True
            message = ''
        except Exception as e:
            success = False
            message = repr(e)
        return (success, message)

    PYXYZ_TESTS[f.__name__] = f
    return f


@test
def load_hydrogen():
    p = Confpool()
    p.include_from_file(to_abs("hydrogen_atom.xyz"))
    assert p.size == len(p) == 1, "Incorrect number of conformers"
    assert p.natoms == 1, "Incorrect number of conformers"
    assert p.atom_symbols == ['H'], "Incorrect number of conformers"
    m = p[0]
    assert match_lists(
        m.xyz.tolist(),
        [[0.0, 0.0, 0.0]]), (f"{m.xyz.tolist()} vs. {[0.0,0.0,0.0]}")
    assert m.idx == 0
    assert m.natoms == 1
    assert m.descr == "Energy = -1488.228"

    p.generate_connectivity(0, mult=1.3)
    p.generate_isomorphisms()
    p.rmsd_filter(0.2)


@test
def empty_filter():
    p = Confpool()
    p.include_from_file(to_abs("aminoacid_single.xyz"))
    p.filter(lambda m: m.l(1, 19) < 2.0)
    assert p.size == 0, "Incorrect number of conformers"


def _load_ensemble():
    p = Confpool()
    p.include_from_file(to_abs("aminoacid_ensemble.xyz"))
    p["Energy"] = lambda m: float(m.descr.strip())
    p.descr = lambda m: "Conf #{}; Energy = {:9f} a.u.".format(
        m.idx + 1, m["Energy"])
    return p


@test
def description_edit():
    p = _load_ensemble()
    p.float_from_descr("Energy_check", 1)
    assert match_lists(
        p["Energy"],
        p["Energy_check"]), f'{p["Energy"]} vs.\n {p["Energy_check"]}'


@test
def filtering():
    p = _load_ensemble()
    p.upper_cutoff("Energy", 5.0 * KC2H)
    assert all(m["Energy"] < 5.0 * KC2H for m in p)
    p.filter(lambda m: m.l(1, 19) < 2.0)
    assert all(m.l(1, 19) < 2.0 for m in p)


@test
def sorting():
    p = _load_ensemble()
    p.sort("Energy")
    energies = p['Energy']
    assert all(i < j
               for i, j in zip(energies, energies[1:])), "Basic sort failed"
    p.sort("Energy", ascending=False)
    energies = p['Energy']
    assert all(
        i > j
        for i, j in zip(energies, energies[1:])), "Descending sort failed"


@test
def attrs():
    p = _load_ensemble()
    xyz = p[0].xyz
    assert all(m.idx == i for i, m in enumerate(p)), "'idx' attr failed"
    assert xyz.shape[1] == 3
    natoms_ref = xyz.shape[0]
    assert p.natoms == natoms_ref, (
        f"Confpool natoms fail: {p.natoms} (ref={natoms_ref})")
    assert p[0].natoms == natoms_ref, (
        f"MolProxy natoms fail: {p[0].natoms} (ref={natoms_ref})")
    assert all(m.descr.startswith(f"Conf #{i+1}")
               for i, m in enumerate(p)), ("'descr' attr failed")


@test
def rmsd():
    p = Confpool()
    p.include_from_file(to_abs("crest_conformersA.xyz"))
    p.include_from_file(to_abs("crest_conformersB.xyz"))
    assert len(p) == 365
    p.generate_connectivity(0,
                            mult=1.3,
                            sdf_name=to_abs('test_topology.sdf'),
                            ignore_elements=['HCarbon'],
                            add_bonds=[[13, 23]])
    p.generate_isomorphisms()
    rmsd_matrix: np.ndarray = p.get_rmsd_matrix()
    assert rmsd_matrix.shape[0] == rmsd_matrix.shape[
        1], "RMSD matrix shape fail"
    assert all((rmsd_matrix[i, i] <= DOUBLE_THR and rmsd_matrix[i, i] >= 0.0)
               for i in range(rmsd_matrix.shape[0])), (
                   "RMSD matrix nonzero diagonal fail")
    assert all(
        abs(rmsd_matrix[i, j] - rmsd_matrix[j, i]) <= DOUBLE_THR
        for i in range(rmsd_matrix.shape[0])
        for j in range(i)), ("RMSD matrix symmetry fail")

    i, j = random.randint(0, rmsd_matrix.shape[0] - 1), random.randint(
        0, rmsd_matrix.shape[0] - 1)
    manual_rmsd = p[i].rmsd(p[j])[0]
    assert abs(manual_rmsd - rmsd_matrix[i, j]) < DOUBLE_THR, (
        f"Manual {manual_rmsd} vs. matrix {rmsd_matrix[i, j]} RMSD for i={i}, j={j}"
    )
    p.rmsd_filter(0.3, rmsd_matrix=rmsd_matrix)

    pp = Confpool()
    pp.include_from_file(to_abs("crest_conformersA.xyz"))
    pp.include_from_file(to_abs("crest_conformersB.xyz"))
    pp.generate_connectivity(0,
                             mult=1.3,
                             ignore_elements=['HCarbon'],
                             add_bonds=[[13, 23]])
    pp.generate_isomorphisms()
    pp.rmsd_filter(0.3)
    assert len(p) == len(pp), (
        f"Filtering cross check failed: {len(p)} vs. {len(pp)}")


@test
def rmsd_pair_iter():
    p = _load_ensemble()
    p.generate_connectivity(0, mult=1.3, ignore_elements=['HCarbon'])
    p.generate_isomorphisms()
    rmsd_matrix = p.get_rmsd_matrix()

    min_rmsd = 0.2
    max_rmsd = 0.25
    check_entry_count = sum(
        1 for i in range(len(p)) for j in range(i)
        if rmsd_matrix[i, j] >= min_rmsd and rmsd_matrix[i, j] <= max_rmsd)

    entry_count = sum(1
                      for _ in p.rmsd_fromto(min_rmsd, max_rmsd, rmsd_matrix))

    ascending_rmsd = [
        rmsd for _, __, rmsd in p.rmsd_fromto(min_rmsd, max_rmsd, rmsd_matrix)
    ]
    descending_rmsd = [
        rmsd for _, __, rmsd in p.rmsd_fromto(max_rmsd, min_rmsd, rmsd_matrix)
    ]

    assert ascending_rmsd == sorted(ascending_rmsd)
    assert descending_rmsd == sorted(ascending_rmsd, key=lambda x: -x)

    assert entry_count == check_entry_count, f"actual {entry_count} vs. check {check_entry_count}"


@test
def molgraph():

    def check(p):
        confA = Molecule(p[0])
        confB = Molecule(p[1])
        assert (confA.G.number_of_edges()
                != 0) and (confA.G.number_of_nodes()
                           != 0), ("Num nodes or Num edges == 0")
        a_data = (confA.G.number_of_edges(), confA.G.number_of_nodes())
        b_data = (confB.G.number_of_edges(), confB.G.number_of_nodes())
        assert a_data == b_data, f"Compare fail: {a_data} vs. {b_data}"
        gsum = confA + confB
        sum_data = (gsum.G.number_of_edges(), gsum.G.number_of_nodes())
        assert sum_data == (a_data[0] * 2, a_data[1] *
                            2), (f"Sum fail. {sum_data} vs. {a_data}")
        gsum.save_sdf(to_abs('test_sum.sdf'))

    p = _load_ensemble()
    p.generate_connectivity(0, mult=1.3)
    check(p)
    p = _load_ensemble()
    p.generate_connectivity(0, mult=1.3, ignore_elements=['HCarbon'])
    check(p)


@test
def geom_analysis():
    p = Confpool()
    p.include_from_file(to_abs("geom_analysis.xyz"))
    m = p[0]
    assert match_lists([m.l(1, 2), m.l(2, 3), m.l(3, 4)],
                       [0.96, 1.67, 2.0]), "Length check failed"
    assert match_lists([m.v(1, 2, 3), m.v(2, 3, 4)],
                       [120.0, 140.0]), "Vangle check failed"
    assert abs(m.z(1, 2, 3, 4) + 50.0) < DOUBLE_THR, (
        f"Dihedral check failed: {m.z(1, 2, 3, 4)} vs. -50.0")

    init_coords = [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0], [10.0, 20.0, 10.0],
                   [-1.0, -1.0, -1.0]]
    p.include_from_xyz(np.matrix(init_coords), "Test descr")
    m = p[2]
    xyz = m.xyz
    assert match_lists(xyz.tolist(), init_coords)
    xyz[0] = [-5.0, -5.0, -5.0]
    p.include_from_xyz(xyz, "Test descr2")
    assert abs(p[3].l(1, 2) - 12.206555615733702) < DOUBLE_THR
    p.generate_connectivity(0,
                            mult=1.3,
                            sdf_name=to_abs('geom_topology.sdf'),
                            ignore_elements=['HCarbon'])
    p.generate_isomorphisms()
    p.rmsd_filter(0.3)
    assert p.size == 3
