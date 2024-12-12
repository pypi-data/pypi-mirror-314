from enum import Enum


class HybridSolverOptSenses(Enum):
    """An enumeration class representing the optimization senses for the hybrid solver.

    Attributes:
    ----------
        MAXIMIZE: Holds a string representing maximization.
        MINIMIZE: Holds a string representing minimization.

    """

    MAXIMIZE = "MAXIMIZE"
    MINIMIZE = "MINIMIZE"


class HybridSolverProblemType(str, Enum):
    MIP = "MIP"
    QUBO = "QUBO"


class VarType(Enum):
    """An enumeration class representing the types of variables.

    Attributes:
    ----------
    CONTINUOUS : str
        Represents a continuous variable.
    INTEGER : str
        Represents an integer variable.
    BINARY : str
        Represents a binary variable.
    """

    CONTINUOUS = "C"
    INTEGER = "I"
    BINARY = "B"


class HybridSolverStatus(str, Enum):
    OPTIMAL = "Optimal"
    OBJECTIVE_LIMIT_REACHED = "Objective limit reached"
    FEASIBLE = "Feasible"
    INFEASIBLE = "Infeasible"
    UNBOUNDED = "Unbounded"
    INFEASIBLE_OR_UNBOUNDED = "Infeasible or unbounded"
    UNSUITABLE = "Unsuitable"
    TIMELIMIT = "Time limit"
    ABORTED = "Aborted"  # This means that the user aborted the run
    NUMERICAL_ERROR = "Numerical Error"
    READERROR = "Read error"
    TERMINATED = "Terminated"
    FAILED = "Failed"
    COMPLETE = "Complete"
    UNKNOWN = "Unknown"
