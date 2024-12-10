from typing import Optional

from pypxml import PageXML, PageType


def regularize(pxml: PageXML, rules: dict[tuple[PageType, Optional[str]], tuple[PageType, Optional[str]]]) -> PageXML:
    """
    Merge PageXML Regions by a set of rules.
    :param pxml: The PageXML object to edit.
    :param rules: A set of rules to merge. Format: `(PageType, type attribute): (PageType, type attribute)`,
        where the left (key) side is merged into the right (value) side.
    :return: The regularized PageXML object.
    """
    for region in pxml.regions:
        reg_tup = (region.type, region.get_attribute('type'))
        print(reg_tup)
        if reg_tup in rules.keys():
            up_tup = rules[(region.type, region['type'])]
            region.type = up_tup[0]
            region.set_attribute('type', up_tup[1])
    return pxml
