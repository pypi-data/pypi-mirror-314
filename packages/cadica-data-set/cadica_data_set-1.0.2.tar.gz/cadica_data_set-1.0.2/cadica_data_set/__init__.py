import sys

if not '-m' in sys.argv:
    from .cadica_data_set import CadicaDataSet
    from .cadica_data_set import CadicaDataSetSamplingPolicy