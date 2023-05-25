
import os
env_ug4_root = os.environ['UG4_ROOT']
import sys
sys.path.append(env_ug4_root+'/lib/')
sys.path.append(env_ug4_root+'/bin/plugins/ug4py')
print(sys.path)

import ug4py as ug4
import pylimex as limex
import pyconvectiondiffusion as cd
# import pysuperlu as slu

def CreateDomain(gridName, numRefs, requiredSubsets):
    # Choosing a domain object
    # (either 1d, 2d or 3d suffix)
    dom = ug4.Domain2d()

    # Loading the given grid into the domain
    print("Loading Domain {gridName}...")
    ug4.LoadDomain(dom, gridName)
    print("Domain loaded.")
    
    
    # Optional: Refining the grid
    if numRefs > 0:
        print("Refining ...")
        refiner = ug4.GlobalDomainRefiner(dom)
        for i in range(numRefs):
            ug4.TerminateAbortedRun()
            refiner.refine()
            print("Refining step {i} ...")

        print("Refining done")

    # checking if geometry has the needed subsets of the probelm
    sh = dom.subset_handler()
    for e in requiredSubsets:
        if sh.get_subset_index(e) == -1:
            print(f"Domain does not contain subset {e}.")
            sys.exit(1)
    
    return dom

def CreateApproximationSpace(dom, approxSpaceDesc):
    approxSpace = ug4.ApproximationSpace2d(dom)
    approxSpace.add_fct(approxSpaceDesc["fct"], approxSpaceDesc["type"], approxSpaceDesc["order"])
    approxSpace.init_levels()
    approxSpace.init_top_surface()
    print("Approximation space:")
    approxSpace.print_statistic()
    return approxSpace

def CreateDiffusionElemDisc(fname, subdom, mass_scale, diffusion, reaction):
    elemDisc = cd.ConvectionDiffusionFV12d(fname, subdom)
    elemDisc.set_mass_scale(mass_scale)
    elemDisc.set_diffusion(diffusion)
    elemDisc.set_reaction(reaction)
    return elemDisc
