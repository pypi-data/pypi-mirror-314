from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from pulp.apis import LpSolver_CMD, PulpSolverError, constants

from quantagonia import HybridSolver
from quantagonia.parameters import HybridSolverParameters

if TYPE_CHECKING:
    from os import PathLike

    import pulp


class HybridSolver_CMD(LpSolver_CMD):  # noqa: N801 name is not CameCase due to convention of pulp
    """The HybridSolver command to be passed to the :code:`solve` method of PuLP.

    Args:
        api_key (str): A string containing the API key.
        params (HybridSolverParameters): (optional) The parameters for the solver.
        keepFiles (bool): (optional) If True, files are saved in the current directory and not deleted after solving.
        obfuscate (bool): (optional) If True, constraints and variable names are obfuscated.

    """

    name = "HybridSolver_CMD"

    def __init__(
        self,
        api_key: str,
        params: dict | None = None,
        # To replicate the signature of the parent class, this is camelcase
        keepFiles: bool = False,  # noqa: N803
        obfuscate: bool = True,
    ):
        self.hybrid_solver = HybridSolver(api_key)
        self.params = params
        if self.params is None:
            self.params = HybridSolverParameters()
        self.obfuscate = obfuscate
        LpSolver_CMD.__init__(
            self,
            mip=True,
            path="",
            keepFiles=keepFiles,
        )

    # overrides pulp method hence the camelCase
    def defaultPath(self) -> str:  # noqa: N802
        return self.executableExtension("qqvm")

    def available(self) -> str | PathLike[str] | None | bytes:
        """True if the solver is available."""
        return self.executable(self.path)

    # overrides pulp method hence the camelCase
    def actualSolve(self, lp: pulp.LpProblem) -> int:  # noqa: N802
        """Solve a well formulated lp problem."""
        var_lp = False  # When lp files are written, qqvm-bolt loses the ordering of variables. This results in wrong
        # reading of solutions as the assumed ordering is not present. In order to support varLP=True, one would have to
        # reimplement the readsol method.

        if var_lp:
            tmp_mps, tmp_sol, tmp_options, tmp_log = self.create_tmp_files(
                lp.name, "lp", "sol", "HybridSolver", "HybridSolver_log"
            )
        else:
            tmp_mps, tmp_sol, tmp_options, tmp_log = self.create_tmp_files(
                lp.name, "mps", "sol", "HybridSolver", "HybridSolver_log"
            )

        if not var_lp and lp.sense == constants.LpMaximize:
            # we swap the objectives
            # because it does not handle maximization.

            print("INFO: HybridSolver_CMD solving equivalent minimization form.")

            # don't print: 'Overwriting previously set objective' warning
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                lp += -lp.objective

        lp.checkDuplicateVars()
        lp.checkLengthVars(52)

        # flag for renaming in writeMPS() should be {0,1}
        rename = 1
        if not self.obfuscate:
            rename = 0

        rename_map = {}

        if var_lp:
            lp.writeLP(filename=tmp_mps)  # , mpsSense=constants.LpMinimize)
        else:
            ret_tpl = lp.writeMPS(filename=tmp_mps, rename=rename)  # , mpsSense=constants.LpMinimize)
            rename_map = ret_tpl[1]

        if lp.isMIP() and not self.mip:
            warnings.warn("HybridSolver_CMD cannot solve the relaxation of a problem", stacklevel=2)

        ########################################################################
        # actual solve operation (local or cloud)
        result, _ = self.hybrid_solver.solve(tmp_mps, self.params)
        ########################################################################

        if not var_lp and lp.sense == constants.LpMaximize:
            print("INFO: Transforming solution value back to original maximization form.")
            # don't print: 'Overwriting previously set objective' warning
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                lp += -lp.objective

        # parse solution
        content = result["solver_log"].splitlines()

        sol_status_key = "Solution Status"
        try:
            sol_status = (
                next(line for line in content if sol_status_key in line).strip().split(sol_status_key)[1].strip()
            )
        except Exception as err:
            error_message = "Pulp: Error while executing"
            raise PulpSolverError(error_message, self.path) from err

        has_sol_key = "Best Solution"
        has_sol = len([line for line in content if has_sol_key in line]) >= 1

        # map HybridSolver Status to pulp status
        if "optimal" in sol_status.lower():  # optimal
            status, status_sol = (
                constants.LpStatusOptimal,
                constants.LpSolutionOptimal,
            )
        elif sol_status.lower() == "time limit" and has_sol:  # feasible
            # Following the PuLP convention
            status, status_sol = (
                constants.LpStatusOptimal,
                constants.LpSolutionIntegerFeasible,
            )
        elif sol_status.lower() == "time limit" and not has_sol:  # feasible
            # Following the PuLP convention
            status, status_sol = (
                constants.LpStatusOptimal,
                constants.LpSolutionNoSolutionFound,
            )
        elif "infeasible" in sol_status.lower():  # infeasible
            status, status_sol = (
                constants.LpStatusInfeasible,
                constants.LpSolutionNoSolutionFound,
            )
        elif "unbounded" in sol_status.lower():  # unbounded
            status, status_sol = (
                constants.LpStatusUnbounded,
                constants.LpSolutionNoSolutionFound,
            )
        else:
            error_message = f"Uncatched solution status: {sol_status}"
            raise RuntimeError(error_message)

        self.delete_tmp_files(tmp_mps, tmp_sol, tmp_options, tmp_log)
        lp.assignStatus(status, status_sol)

        if not has_sol:
            return status

        # remap obfuscated variable names to original variable names
        for orig_name, obfuscated_name in rename_map.items():
            result["solution"][orig_name] = result["solution"].pop(obfuscated_name)

        if status == constants.LpStatusOptimal:
            lp.assignVarsVals(result["solution"])

        return status
