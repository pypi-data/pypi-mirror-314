from typing import Optional

from easytype.core import UserDefinedType

from dataset_sh import create
from dataset_sh.utils.files import checksum
from dataset_sh.utils.misc import get_tqdm
from dataset_sh.constants import DEFAULT_COLLECTION_NAME


def dump_single_collection(
        fn,
        data,
        name=DEFAULT_COLLECTION_NAME,
        type_annotation: Optional[UserDefinedType] = None,
        description: Optional[str] = None,
        silent=False
):
    """
    Args:
        fn:
        data:
        name:
        type_annotation:
        description:
        silent:
    Returns:
    """
    with create(fn) as out:
        if description:
            out.meta.description = description
        out.add_collection(name, data, type_annotation=type_annotation, tqdm=get_tqdm(silent=silent))
    return checksum(fn)


def dump_collections(
        fn,
        data_dict,
        type_dict=None,
        description: Optional[str] = None,
        report_item_progress=False,
        report_collection_progress=False
):
    """
    Args:
        fn:
        data_dict:
        type_dict:
        description:
        report_item_progress:
        report_collection_progress:

    Returns:

    """
    if type_dict is None:
        type_dict = {}
    inner_tqdm = get_tqdm(silent=not report_item_progress)
    with create(fn) as out:
        if description:
            out.meta.description = description
        for name, data in data_dict.items():
            if report_collection_progress:
                print(f'Importing collection {name}')
            if len(data) > 0:
                type_annotation = type_dict.get(name, None)
                out.add_collection(name, data, type_annotation=type_annotation, tqdm=inner_tqdm)
    return checksum(fn)
