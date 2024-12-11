from enum import Enum


class FilterSet(str, Enum):
    mtscATAC = "mtscATAC"
    REDEEM = "REDEEM"
    MAESTER = "MAESTER"
    DLP = "DLP"
    SMART_SEQ = "SMART_SEQ"
    CUSTOM = "CUSTOM"


known_filters = [
    "mean_coverage",
    "min_strand_correlation",
    "n_cells_over_5",
    "min_vmr",
    "min_consensus_group_size",
    "molecular_position_bias_threshold",
    "homoplasmic_threshold",
]

mtscATAC_filters = {
    "mean_coverage": 10,
    "min_strand_correlation": 0.65,
    "n_cells_over_5": 3,
    "min_vmr": 0.01,
    "min_consensus_group_size": 1,
    "molecular_position_bias_threshold": 0.35,
    "homoplasmic_threshold": 0.95,
}

REDEEM_filters = {
    "mean_coverage": 10,
    "min_strand_correlation": 0.65,
    "n_cells_over_5": 3,
    "min_vmr": 0.01,
    "min_consensus_group_size": 2,
    "molecular_position_bias_threshold": 0.35,
    "homoplasmic_threshold": 0.95,
}

DLP_filters = {
    "mean_coverage": 1,
    "min_strand_correlation": 0.65,
    "n_cells_over_5": 3,
    "min_vmr": 0.01,
    "min_consensus_group_size": 1,
    "molecular_position_bias_threshold": 0.35,
    "homoplasmic_threshold": 0.95,
}

SMART_SEQ_filters = {
    "mean_coverage": 50,
    "min_strand_correlation": 0.65,
    "n_cells_over_5": 3,
    "min_vmr": 0.01,
    "min_consensus_group_size": 1,
    "molecular_position_bias_threshold": 0.35,
    "homoplasmic_threshold": 0.95,
}

MAESTER_filters = {
    "mean_coverage": 50,
    "min_strand_correlation": 0,
    "n_cells_over_5": 5,
    "min_vmr": 0.01,
    "min_consensus_group_size": 1,
    "molecular_position_bias_threshold": 1,
    "homoplasmic_threshold": 0.95,
}


FILTER_MAP = {
    "mtscATAC": mtscATAC_filters,
    "REDEEM": REDEEM_filters,
    "DLP": DLP_filters,
    "SMART_SEQ": SMART_SEQ_filters,
    "MAESTER": MAESTER_filters,
}
