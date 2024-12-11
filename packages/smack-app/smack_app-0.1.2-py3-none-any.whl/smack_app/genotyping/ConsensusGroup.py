from collections import namedtuple


DNA_LETTERS = ["A", "C", "G", "T", "N"]
DNA_BASES = ["A", "C", "G", "T"]


ReadPair = namedtuple("ReadPair", "read_name fwd_read rev_read")
ConsensusCallResult = namedtuple(
    "ConsensusCallResult", "encoding_vector rows quality_coverage_count"
)

DNA_LETTERS = ["A", "C", "G", "T", "N"]
DNA_BASES = ["A", "C", "G", "T"]


class ConsensusGroup:

    def __init__(self) -> None:
        self.readpairs = []
        self.key = None
        self.group_type = None

    def add_readpair(self, read: ReadPair) -> None:
        self.readpairs.append(read)
