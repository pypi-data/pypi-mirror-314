from tables import (
    IsDescription,
    BoolCol,
    StringCol,
    UInt16Col,
    UInt8Col,
    Float16Col,
)

eUMI_DELIM = "|"
UMI_DELIM = "|"


class Schema(IsDescription):
    pass


class MoleculeSchema(Schema):
    position = UInt16Col()
    barcode = StringCol(50)
    variant = StringCol(20)
    group_id = StringCol(100)
    call = StringCol(1)
    ref = StringCol(1)
    consensus_group_size = UInt8Col()
    supporting_counts = UInt8Col()
    fraction_supporting_call = Float16Col()
    fraction_supporting_ref = Float16Col()

    single_group_size = UInt8Col()
    single_supporting_counts = UInt8Col()
    single_fraction_supporting_call = Float16Col()
    single_fraction_supporting_ref = Float16Col()

    double_group_size = UInt8Col()
    double_supporting_counts = UInt8Col()
    double_fraction_supporting_call = Float16Col()
    double_fraction_supporting_ref = Float16Col()

    fwd_count = UInt8Col()
    rev_count = UInt8Col()


class ConsensusGroupSchema(Schema):
    group_id = StringCol(100)
    # group_type = EnumCol(Enum({"UMI": "UMI", "eUMI": "eUMI"}), "eUMI", base="string")
    # pytables has a bug with enumcols so just using string and will manually enforce
    group_type = StringCol(20)
    has_alt = BoolCol()
    encoding_vector = StringCol(2000)


class BarcodeSchema(Schema):
    barcode = StringCol(50)
    average_total_depth = Float16Col()
    average_high_quality_depth = Float16Col()


class MetadataSchema(Schema):
    genome_path = StringCol(100)
    genome_length = UInt16Col()
    sample_id = StringCol(1000)
