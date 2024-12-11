# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module holding the HTS runtime related json encoder-decoder classes."""
from typing import Any, Dict
import copy
from json import JSONEncoder, JSONDecoder

from ..data_models.content_hash_vocabulary import ContentHashVocabulary
from ..data_models.node_columns_info import NodeColumnsInfo
from ..data_models.status_record import StatusRecord
from ..data_models.raw_data_info import RawDataInfo
from ..data_models.inference_configs import InferenceConfigs
from ..data_models.evaluation_configs import EvaluationConfigs


class HTSEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        json_dict = copy.deepcopy(o.__dict__)
        if isinstance(o, StatusRecord):
            json_dict["__type__"] = StatusRecord.__name__
        return json_dict


class HTSDecoder(JSONDecoder):
    def __init__(self, object_hook=None):
        if object_hook is None:
            super(HTSDecoder, self).__init__(object_hook=self.hts_object_hook)
        else:
            super(HTSDecoder, self).__init__(object_hook=object_hook)

    def hts_object_hook(self, dct: Dict[str, Any]) -> Any:
        if dct.get("__type__") == StatusRecord.__name__:
            return StatusRecord(*[dct.get(arg) for arg in StatusRecord.get_args_list()])  # type: ignore
        return dct


class HTSRuntimeEncoder(HTSEncoder):
    def default(self, o: Any) -> Any:
        json_dict = copy.deepcopy(o.__dict__)
        if isinstance(o, ContentHashVocabulary):
            json_dict["__type__"] = ContentHashVocabulary.__name__
            return json_dict
        elif isinstance(o, NodeColumnsInfo):
            json_dict["__type__"] = NodeColumnsInfo.__name__
            return json_dict
        elif isinstance(o, RawDataInfo):
            json_dict["__type__"] = RawDataInfo.__name__
            return json_dict
        elif isinstance(o, InferenceConfigs):
            json_dict["__type__"] = InferenceConfigs.__name__
            return json_dict
        elif isinstance(o, EvaluationConfigs):
            json_dict["__type__"] = EvaluationConfigs.__name__
            return json_dict
        else:
            return super(HTSRuntimeEncoder, self).default(o)


class HTSRuntimeDecoder(HTSDecoder):
    def __init__(self):
        super(HTSRuntimeDecoder, self).__init__(object_hook=self.hts_runtime_object_hook)

    def hts_runtime_object_hook(self, dct: Dict[str, Any]) -> Any:
        if dct.get("__type__") == ContentHashVocabulary.__name__:
            return ContentHashVocabulary(
                *[dct.get(arg) for arg in ContentHashVocabulary.get_args_list()])  # type: ignore
        elif dct.get("__type__") == NodeColumnsInfo.__name__:
            return NodeColumnsInfo(
                *[dct.get(arg) for arg in NodeColumnsInfo.get_args_list()])  # type: ignore
        elif dct.get("__type__") == RawDataInfo.__name__:
            return RawDataInfo(
                *[dct.get(arg) for arg in RawDataInfo.get_args_list()])  # type: ignore
        elif dct.get("__type__") == InferenceConfigs.__name__:
            return InferenceConfigs(
                *[dct.get(arg) for arg in InferenceConfigs.get_args_list()])  # type: ignore
        elif dct.get("__type__") == EvaluationConfigs.__name__:
            return EvaluationConfigs(
                *[dct.get(arg) for arg in EvaluationConfigs.get_args_list()])
        return super(HTSRuntimeDecoder, self).hts_object_hook(dct)
