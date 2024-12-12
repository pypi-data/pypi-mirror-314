"""
Land Cover

This model calculates historic land use change over a twenty-year period, extending the
functionality of the Blonk model.
"""
import math
from collections import defaultdict
from hestia_earth.schema import SiteSiteType, TermTermType
from hestia_earth.utils.lookup import (
    download_lookup, get_table_value, column_name,
    extract_grouped_data_closest_date, _is_missing_value, extract_grouped_data
)
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import safe_parse_float, to_precision, non_empty_value

from hestia_earth.models.log import logRequirements, log_as_table, logShouldRun
from hestia_earth.models.utils.management import _new_management
from hestia_earth.models.utils.term import get_lookup_value
from . import MODEL

REQUIREMENTS = {
    "Site": {
        "siteType": [
            "forest",
            "cropland",
            "permanent pasture",
            "other natural vegetation"
        ],
        "country": "",
        "management": [
            {
                "@type": "Management",
                "value": "",
                "term.termType": "landCover",
                "endDate": ""
            }
        ]
    }
}
RETURNS = {
    "Management": [{
        "@type": "Management",
        "term.termType": "landCover",
        "term.@id": [
            "Forest", "Annual cropland", "Permanent cropland", "Permanent pasture", "Other natural vegetation"
        ],
        "value": "",
        "endDate": "",
        "startDate": ""
    }]
}
LOOKUPS = {
    "region-crop-cropGroupingFaostatProduction-areaHarvestedUpTo20YearExpansion": "All crops",
    "region-crop-cropGroupingFaostatProduction-areaHarvested": "All crops",
    "region-faostatArea-UpTo20YearExpansion": "All land uses",
    "region-faostatArea": [
        "Arable land",
        "Cropland",
        "Forest land",
        "Land area",
        "Other land",
        "Permanent crops",
        "Permanent meadows and pastures"
    ],
    "crop": ["cropGroupingFaostatArea", "IPCC_LAND_USE_CATEGORY"],
    "landCover": ["cropGroupingFaostatProduction", "FAOSTAT_LAND_AREA_CATEGORY"]
}
MODEL_KEY = 'landCover'

LAND_AREA = LOOKUPS["region-faostatArea"][3]
TOTAL_CROPLAND = "Cropland"
ANNUAL_CROPLAND = "Arable land"
FOREST_LAND = "Forest land"
OTHER_LAND = "Other land"
PERMANENT_CROPLAND = "Permanent crops"
PERMANENT_PASTURE = "Permanent meadows and pastures"
TOTAL_AGRICULTURAL_CHANGE = "Total agricultural change"
ALL_LAND_USE_TERMS = [
    FOREST_LAND,
    TOTAL_CROPLAND,
    ANNUAL_CROPLAND,
    PERMANENT_CROPLAND,
    PERMANENT_PASTURE,
    OTHER_LAND
]
# Mapping from Land use terms to Management node terms.
# land use term: (@id, name)
LAND_USE_TERMS_FOR_TRANSFORMATION = {
    FOREST_LAND: ("forest", "Forest"),
    ANNUAL_CROPLAND: ("annualCropland", "Annual cropland"),
    PERMANENT_CROPLAND: ("permanentCropland", "Permanent cropland"),
    PERMANENT_PASTURE: ("permanentPasture", "Permanent pasture"),
    OTHER_LAND: ("otherLand", OTHER_LAND)  # Not used yet
}
SITE_TYPES = {
    SiteSiteType.CROPLAND.value,
    SiteSiteType.FOREST.value,
    SiteSiteType.OTHER_NATURAL_VEGETATION.value,
    SiteSiteType.PERMANENT_PASTURE.value
}
DEFAULT_WINDOW_IN_YEARS = 20
IPCC_LAND_USE_CATEGORY_ANNUAL = "Annual crops"
IPCC_LAND_USE_CATEGORY_PERENNIAL = "Perennial crops"
OUTPUT_SIGNIFICANT_DIGITS = 3


def _management(term_id: str, value: float, start_date: str, end_date: str):
    node = _new_management(term_id, MODEL)
    node['value'] = value
    node['startDate'] = start_date
    node['endDate'] = end_date
    return node


def _is_missing_or_none(value) -> bool:
    return value is None or _is_missing_value(value)


def _safe_divide(numerator, denominator, default=0) -> float:
    return default if not denominator else numerator / denominator


def site_area_sum_to_100(dict_of_percentages: dict):
    return False if dict_of_percentages == {} else \
        (math.isclose(sum(dict_of_percentages.values()), 1.0, rel_tol=0.01) or
         math.isclose(sum(dict_of_percentages.values()), 0.0, rel_tol=0.01))


def _lookup_land_use_type(nodes: list) -> str:
    """Look up the land use type from a management node."""
    return "" if nodes == [] else get_lookup_value(
        lookup_term=nodes[0].get("term", {}),
        column=LOOKUPS.get("landCover")[1],
        model=MODEL,
        term=nodes[0].get("term", {})
    )


def _crop_ipcc_land_use_category(
    crop_term_id: str,
    lookup_term_type: str = TermTermType.LANDCOVER.value
) -> str:
    """
    Looks up the crop in the lookup.
    Returns the IPCC_LAND_USE_CATEGORY.
    """
    return get_lookup_value(
        lookup_term={"@id": crop_term_id, "type": "Term", "termType": lookup_term_type},
        column=LOOKUPS.get("crop")[1],
        model=MODEL,
        term={"@id": crop_term_id, "type": "Term", "termType": lookup_term_type}
    )


def get_changes(country_id: str, end_year: int) -> dict:
    """
    For each entry in ALL_LAND_USE_TERMS, creates a key: value in output dictionary, also TOTAL
    """
    lookup = download_lookup("region-faostatArea-UpTo20YearExpansion.csv")
    changes_dict = {
        land_use_term: safe_parse_float(
            extract_grouped_data(
                get_table_value(lookup, 'termid', country_id, column_name(land_use_term)),
                str(end_year))
        )
        for land_use_term in ALL_LAND_USE_TERMS + [LAND_AREA]
    }
    changes_dict[TOTAL_AGRICULTURAL_CHANGE] = (float(changes_dict.get(TOTAL_CROPLAND, 0))
                                               + float(changes_dict.get(PERMANENT_PASTURE, 0)))

    return changes_dict


def _get_ratio_start_and_end_values(
    expansion: float,
    fao_name: str,
    country_id: str,
    end_year: int
) -> float:
    # expansion over twenty years / current area
    lookup = download_lookup('region-faostatArea.csv')
    table_value = get_table_value(lookup, 'termid', country_id, column_name(fao_name))
    end_value = safe_parse_float(value=extract_grouped_data_closest_date(table_value, end_year), default=None)
    return max(0.0, _safe_divide(numerator=expansion, denominator=end_value))


def _estimate_maximum_forest_change(
    forest_change: float, total_cropland_change: float, pasture_change: float, total_agricultural_change: float
):
    """
    (L): Estimate maximum forest loss
    Gives a negative number representing forest loss. Does not currently handle forest gain.
    """
    positive_change = pasture_change > 0 and total_cropland_change > 0
    return _negative_agricultural_land_change(
        forest_change=forest_change,
        pasture_change=pasture_change,
        total_cropland_change=total_cropland_change
    ) if not positive_change else (
        total_agricultural_change
        if -min(forest_change, 0) > total_agricultural_change else
        min(forest_change, 0)
    )


def _negative_agricultural_land_change(forest_change, pasture_change, total_cropland_change):
    return pasture_change if 0 < pasture_change < -min(forest_change, 0) \
        else min(forest_change, 0) if pasture_change > 0 \
        else -total_cropland_change if 0 < total_cropland_change < -min(forest_change, 0) \
        else min(forest_change, 0) if 0 < total_cropland_change \
        else 0


def _allocate_forest_loss(forest_loss: float, changes: dict):
    """Allocate forest loss between agricultural categories for the specific country"""
    return {
        TOTAL_CROPLAND: forest_loss * _safe_divide(
            numerator=max(changes[TOTAL_CROPLAND], 0),
            denominator=max(changes[TOTAL_CROPLAND], 0) + max(changes[PERMANENT_PASTURE], 0)
        ),
        PERMANENT_PASTURE: forest_loss * _safe_divide(
            numerator=max(changes[PERMANENT_PASTURE], 0),
            denominator=max(changes[TOTAL_CROPLAND], 0) + max(changes[PERMANENT_PASTURE], 0)
        )
    }


def _additional_allocation(changes, max_forest_loss_to_cropland, max_forest_loss_to_permanent_pasture):
    """Determine how much area still needs to be assigned"""
    return {
        TOTAL_CROPLAND: max(changes[TOTAL_CROPLAND], 0) + max_forest_loss_to_cropland,
        PERMANENT_PASTURE: max(changes[PERMANENT_PASTURE], 0) + max_forest_loss_to_permanent_pasture
    }


def _allocate_cropland_loss_to_pasture(changes: dict, land_required_for_permanent_pasture: float):
    """Allocate changes between Permanent pasture and cropland"""
    return (
        max(-land_required_for_permanent_pasture, changes[TOTAL_CROPLAND])
        if changes[TOTAL_CROPLAND] < 0 else 0
    )


def _allocate_pasture_loss_to_cropland(changes: dict, land_required_for_cropland: float):
    """Allocate changes between Permanent pasture and cropland"""
    return (
        max(-land_required_for_cropland, changes[PERMANENT_PASTURE])
        if changes[PERMANENT_PASTURE] < 0 else 0
    )


def _allocate_other_land(
        changes: dict, max_forest_loss_to: dict, pasture_loss_to_cropland: float, cropland_loss_to_pasture: float
) -> dict:
    """Allocate changes between Other land and cropland"""
    other_land_loss_to_cropland = (
        -(max(changes[TOTAL_CROPLAND], 0) + max_forest_loss_to[TOTAL_CROPLAND]
          + pasture_loss_to_cropland)
    )
    other_land_loss_to_pasture = (
        -(max(changes[PERMANENT_PASTURE], 0) + max_forest_loss_to[PERMANENT_PASTURE]
          + cropland_loss_to_pasture)
    )
    return {
        TOTAL_CROPLAND: other_land_loss_to_cropland,
        PERMANENT_PASTURE: other_land_loss_to_pasture,
        TOTAL_AGRICULTURAL_CHANGE: other_land_loss_to_cropland + other_land_loss_to_pasture
    }


def _allocate_annual_permanent_cropland_losses(changes: dict) -> tuple:
    """
    (Z, AA): Allocate changes between Annual cropland and Permanent cropland
    Returns: annual_cropland_loss_to_permanent_cropland, permanent_cropland_loss_to_annual_cropland
    """
    return (
        -min(-changes[ANNUAL_CROPLAND], changes[PERMANENT_CROPLAND])
        if (changes[ANNUAL_CROPLAND] < 0 and changes[PERMANENT_CROPLAND] > 0) else 0,
        -min(changes[ANNUAL_CROPLAND], -changes[PERMANENT_CROPLAND])
        if (changes[ANNUAL_CROPLAND] > 0 and changes[PERMANENT_CROPLAND] < 0) else 0
    )


def _estimate_conversions_to_annual_cropland(
    changes: dict,
    pasture_loss_to_crops: float,
    forest_loss_to_cropland: float,
    other_land_loss_to_annual_cropland: float,
    permanent_to_annual_cropland: float
) -> dict:
    """(AC-AG): Estimate percentage of land sources when converted to: Annual cropland"""
    # -> percent_annual_cropland_was[]
    def conversion_to_annual_cropland(factor: float):
        return factor * _safe_divide(
            numerator=_safe_divide(
                numerator=max(changes[ANNUAL_CROPLAND], 0),
                denominator=max(changes[ANNUAL_CROPLAND], 0) + max(changes[PERMANENT_CROPLAND], 0)),
            denominator=-changes[ANNUAL_CROPLAND]
        )

    percentages = {
        FOREST_LAND: conversion_to_annual_cropland(forest_loss_to_cropland),
        OTHER_LAND: conversion_to_annual_cropland(other_land_loss_to_annual_cropland),
        PERMANENT_PASTURE: conversion_to_annual_cropland(pasture_loss_to_crops),
        PERMANENT_CROPLAND: _safe_divide(numerator=permanent_to_annual_cropland, denominator=-changes[ANNUAL_CROPLAND])
    }
    return percentages


def _estimate_conversions_to_permanent_cropland(
    changes: dict,
    annual_loss_to_permanent_cropland: float,
    pasture_loss_to_cropland: float,
    forest_loss_to_cropland: float,
    other_land_loss_to_annual_cropland: float
) -> dict:
    """Estimate percentage of land sources when converted to: Annual cropland"""
    def conversion_to_permanent_cropland(factor: float):
        return _safe_divide(
            numerator=_safe_divide(
                numerator=factor * max(changes[PERMANENT_CROPLAND], 0),
                denominator=max(changes[ANNUAL_CROPLAND], 0) + max(changes[PERMANENT_CROPLAND], 0)),
            denominator=-changes[PERMANENT_CROPLAND]
        )

    percentages = {
        FOREST_LAND: conversion_to_permanent_cropland(forest_loss_to_cropland),
        OTHER_LAND: conversion_to_permanent_cropland(other_land_loss_to_annual_cropland),
        PERMANENT_PASTURE: conversion_to_permanent_cropland(pasture_loss_to_cropland),
        ANNUAL_CROPLAND: conversion_to_permanent_cropland(annual_loss_to_permanent_cropland)
    }
    return percentages


def _estimate_conversions_to_pasture(
    changes: dict,
    forest_loss_to_pasture: float,
    total_cropland_loss_to_pasture: float,
    other_land_loss_to_pasture: float
) -> dict:
    """Estimate percentage of land sources when converted to: Permanent pasture"""
    percentages = {
        FOREST_LAND: _safe_divide(
            numerator=forest_loss_to_pasture,
            denominator=-changes[PERMANENT_PASTURE],
        ),
        OTHER_LAND: _safe_divide(
            numerator=other_land_loss_to_pasture,
            denominator=-changes[PERMANENT_PASTURE]
        ),
        # AT
        ANNUAL_CROPLAND: _safe_divide(
            numerator=total_cropland_loss_to_pasture * _safe_divide(
                numerator=min(changes[ANNUAL_CROPLAND], 0),
                denominator=(min(changes[ANNUAL_CROPLAND], 0) + min(changes[PERMANENT_CROPLAND], 0))
            ),
            denominator=-changes[PERMANENT_PASTURE]
        ),
        PERMANENT_CROPLAND: _safe_divide(
            numerator=total_cropland_loss_to_pasture * _safe_divide(
                numerator=min(changes[PERMANENT_CROPLAND], 0),
                denominator=(min(changes[ANNUAL_CROPLAND], 0) + min(changes[PERMANENT_CROPLAND], 0))
            ),
            denominator=-changes[PERMANENT_PASTURE]
        )
    }
    return percentages


def _get_shares_of_expansion(
    land_use_type: str,
    percent_annual_cropland_was: dict,
    percent_permanent_cropland_was: dict,
    percent_pasture_was: dict
) -> dict:
    expansion_for_type = {
        ANNUAL_CROPLAND: percent_annual_cropland_was,
        PERMANENT_CROPLAND: percent_permanent_cropland_was,
        PERMANENT_PASTURE: percent_pasture_was
    }
    return {
        k: expansion_for_type[land_use_type].get(k, 0)
        for k in LAND_USE_TERMS_FOR_TRANSFORMATION.keys()
    }


def _get_faostat_name(term: dict) -> str:
    """For landCover terms, find the cropGroupingFaostatArea name for the landCover id."""
    return get_lookup_value(term, "cropGroupingFaostatArea")


def _get_complete_faostat_to_crop_mapping() -> dict:
    """Returns mapping in the format: {faostat_name: IPPC_LAND_USE_CATEGORY, ...}"""
    lookup = download_lookup("crop.csv")
    mappings = defaultdict(list)
    for crop_term_id in [row[0] for row in lookup]:
        key = column_name(
            get_table_value(lookup, 'termid', crop_term_id, column_name("cropGroupingFaostatArea"))
        )
        if key:
            mappings[key].append(_crop_ipcc_land_use_category(crop_term_id=crop_term_id, lookup_term_type="crop"))
    return {
        fao_name: max(set(crop_terms), key=crop_terms.count)
        for fao_name, crop_terms in mappings.items()
    }


def _get_harvested_area(country_id: str, year: int, faostat_name: str) -> float:
    """
    Returns a dictionary of harvested areas for the country & year, indexed by landCover term (crop)
    """
    lookup = download_lookup("region-crop-cropGroupingFaostatProduction-areaHarvested.csv")
    return safe_parse_float(
        value=extract_grouped_data_closest_date(
            data=get_table_value(lookup, "termid", country_id, column_name(faostat_name)),
            year=year
        ),
        default=None
    )


def _run_make_management_nodes(existing_nodes: list, percentage_transformed_from: dict, start_year: int) -> list:
    """Creates a list of new management nodes, excluding any dates matching existing ones."""
    existing_nodes_set = {
        (node.get("term", {}).get("@id", ""), node.get("startDate"), node.get("endDate"))
        for node in existing_nodes
    }
    values = [
        {
            "land_management_key": (
                LAND_USE_TERMS_FOR_TRANSFORMATION[land_type], f"{start_year}-01-01", f"{start_year}-12-31"
            ),
            "land_type": land_type,
            "percentage": 0.0 if ratio == -0.0 else to_precision(
                number=ratio * 100,
                digits=OUTPUT_SIGNIFICANT_DIGITS
            )
        }
        for land_type, ratio in percentage_transformed_from.items()
    ]
    values = [v for v in values if v.get("land_management_key") not in existing_nodes_set]

    return [
        _management(
            term_id=LAND_USE_TERMS_FOR_TRANSFORMATION[value.get("land_type")][0],
            value=value.get("percentage"),
            start_date=value.get("land_management_key")[1],
            end_date=value.get("land_management_key")[2]
        )
        for value in values
    ]


def get_ratio_of_expanded_area(country_id: str, fao_name: str, end_year: int) -> float:
    lookup = download_lookup("region-crop-cropGroupingFaostatProduction-areaHarvestedUpTo20YearExpansion.csv")
    table_value = get_table_value(lookup, 'termid', country_id, column_name(fao_name))
    expansion = safe_parse_float(value=extract_grouped_data(table_value, str(end_year)), default=None)
    end_value = _get_harvested_area(
        country_id=country_id,
        year=end_year,
        faostat_name=fao_name
    )
    return 0.0 if any([expansion is None, end_value is None]) else max(
        0.0, _safe_divide(numerator=expansion, denominator=(end_value - expansion))
    )


def _get_sum_for_land_category(
    values: dict,
    year: int,
    ipcc_land_use_category,
    fao_stat_to_ipcc_type: dict,
    include_negatives: bool = True
) -> float:
    return sum(
        [
            safe_parse_float(value=extract_grouped_data(table_value, str(year)), default=None)
            for fao_name, table_value in values.items()
            if not _is_missing_or_none(extract_grouped_data(table_value, str(year))) and
            fao_stat_to_ipcc_type[fao_name] == ipcc_land_use_category and
            (include_negatives or
             safe_parse_float(value=extract_grouped_data(table_value, str(year)), default=None) > 0.0)
        ]
    )


def _get_sums_of_crop_expansion(country_id: str, year: int, include_negatives: bool = True) -> tuple[float, float]:
    """
    Sum net expansion for all annual and permanent crops, returned as two values.
    Returns a tuple of (expansion of annual crops, expansion of permanent crops)
    """
    lookup = download_lookup("region-crop-cropGroupingFaostatProduction-areaHarvestedUpTo20YearExpansion.csv")
    values = {name: get_table_value(lookup, 'termid', country_id, column_name(name))
              for name in list(lookup.dtype.names) if name != "termid"}

    fao_stat_to_ipcc_type = _get_complete_faostat_to_crop_mapping()

    annual_sum_of_expansion = _get_sum_for_land_category(
        values=values,
        year=year,
        ipcc_land_use_category=IPCC_LAND_USE_CATEGORY_ANNUAL,
        fao_stat_to_ipcc_type=fao_stat_to_ipcc_type,
        include_negatives=include_negatives
    )
    permanent_sum_of_expansion = _get_sum_for_land_category(
        values=values,
        year=year,
        ipcc_land_use_category=IPCC_LAND_USE_CATEGORY_PERENNIAL,
        fao_stat_to_ipcc_type=fao_stat_to_ipcc_type,
        include_negatives=include_negatives
    )

    return annual_sum_of_expansion, permanent_sum_of_expansion


def _get_net_expansion_cultivated_vs_harvested(annual_crops_net_expansion, changes, land_use_type,
                                               permanent_crops_net_expansion):
    if land_use_type == ANNUAL_CROPLAND:
        net_expansion_cultivated_vs_harvested = _safe_divide(numerator=max(0, changes[ANNUAL_CROPLAND]),
                                                             denominator=(annual_crops_net_expansion / 1000))
    elif land_use_type == PERMANENT_CROPLAND:
        net_expansion_cultivated_vs_harvested = _safe_divide(numerator=max(0, changes[PERMANENT_CROPLAND]),
                                                             denominator=(permanent_crops_net_expansion / 1000))
    else:
        net_expansion_cultivated_vs_harvested = 1
    return net_expansion_cultivated_vs_harvested


def _should_run_historical_land_use_change(site: dict, land_use_type: str) -> tuple[bool, dict]:
    management_nodes = filter_list_term_type(site.get("management", []), TermTermType.LANDCOVER)
    # Assume a single management node for single-cropping.
    return _should_run_historical_land_use_change_single_crop(
        site=site,
        term=management_nodes[0].get("term", {}),
        country_id=site.get("country", {}).get("@id"),
        end_year=int(management_nodes[0].get("endDate")[:4]),
        land_use_type=land_use_type
    )


def _should_run_historical_land_use_change_single_crop(
    site: dict,
    term: dict,
    country_id: str,
    end_year: int,
    land_use_type: str
) -> tuple[bool, dict]:
    """Calculate land use change percentages for a single management node/crop."""
    # (C-H).
    changes = get_changes(country_id=country_id, end_year=end_year)

    # (L). Estimate maximum forest loss
    forest_loss = _estimate_maximum_forest_change(
        forest_change=changes[FOREST_LAND],
        total_cropland_change=changes[TOTAL_CROPLAND],
        pasture_change=changes[PERMANENT_PASTURE],
        total_agricultural_change=changes[TOTAL_AGRICULTURAL_CHANGE]
    )

    # (M, N). Allocate forest loss between agricultural categories for the specific country
    forest_loss_to = _allocate_forest_loss(forest_loss=forest_loss, changes=changes)

    # (P, Q): Determine how much area still needs to be assigned
    land_required_for = _additional_allocation(
        changes=changes,
        max_forest_loss_to_cropland=forest_loss_to[TOTAL_CROPLAND],
        max_forest_loss_to_permanent_pasture=forest_loss_to[PERMANENT_PASTURE]
    )

    # (R): Allocate changes between Permanent pasture and cropland
    cropland_loss_to_pasture = _allocate_cropland_loss_to_pasture(
        changes=changes,
        land_required_for_permanent_pasture=land_required_for[PERMANENT_PASTURE]
    )
    # (S)
    pasture_loss_to_cropland = _allocate_pasture_loss_to_cropland(
        changes=changes,
        land_required_for_cropland=land_required_for[TOTAL_CROPLAND]
    )

    # (V): Allocate changes between Other land and cropland
    other_land_loss_to = _allocate_other_land(
        changes=changes,
        max_forest_loss_to=forest_loss_to,
        pasture_loss_to_cropland=pasture_loss_to_cropland,
        cropland_loss_to_pasture=cropland_loss_to_pasture
    )

    # (Z, AA): Allocate changes between Annual cropland and Permanent cropland
    annual_cropland_loss_to_permanent_cropland, permanent_cropland_loss_to_annual_cropland = (
        _allocate_annual_permanent_cropland_losses(changes)
    )

    # (AC-AG): Estimate percentage of land sources when converted to: Annual cropland
    # Note: All percentages are expressed as decimal fractions. 50% = 0.5
    percent_annual_cropland_was = _estimate_conversions_to_annual_cropland(
        changes=changes,
        pasture_loss_to_crops=pasture_loss_to_cropland,
        forest_loss_to_cropland=forest_loss_to[TOTAL_CROPLAND],
        other_land_loss_to_annual_cropland=other_land_loss_to[TOTAL_CROPLAND],
        permanent_to_annual_cropland=permanent_cropland_loss_to_annual_cropland,
    )

    # (AJ-AM): Estimate percentage of land sources when converted to: Permanent cropland
    percent_permanent_cropland_was = _estimate_conversions_to_permanent_cropland(
        changes=changes,
        annual_loss_to_permanent_cropland=annual_cropland_loss_to_permanent_cropland,
        pasture_loss_to_cropland=pasture_loss_to_cropland,
        forest_loss_to_cropland=forest_loss_to[TOTAL_CROPLAND],
        other_land_loss_to_annual_cropland=other_land_loss_to[TOTAL_CROPLAND]
    )

    # Estimate percentage of land sources when converted to: Permanent pasture
    percent_pasture_was = _estimate_conversions_to_pasture(
        changes=changes,
        forest_loss_to_pasture=forest_loss_to[PERMANENT_PASTURE],
        total_cropland_loss_to_pasture=cropland_loss_to_pasture,
        other_land_loss_to_pasture=other_land_loss_to[PERMANENT_PASTURE]
    )

    # BA to BD
    shares_of_expansion = _get_shares_of_expansion(
        land_use_type=land_use_type,
        percent_annual_cropland_was=percent_annual_cropland_was,
        percent_permanent_cropland_was=percent_permanent_cropland_was,
        percent_pasture_was=percent_pasture_was
    )

    # Cell E8
    expansion_factor = _get_ratio_start_and_end_values(
        expansion=changes[PERMANENT_PASTURE],
        fao_name=PERMANENT_PASTURE,
        country_id=country_id,
        end_year=end_year
    ) if land_use_type == PERMANENT_PASTURE else get_ratio_of_expanded_area(
        country_id=country_id,
        fao_name=_get_faostat_name(term),
        end_year=end_year
    )

    # E9
    annual_crops_net_expansion, permanent_crops_net_expansion = _get_sums_of_crop_expansion(
        country_id=country_id,
        year=end_year,
        include_negatives=True
    )
    annual_crops_gross_expansion, permanent_crops_gross_expansion = _get_sums_of_crop_expansion(
        country_id=country_id,
        year=end_year,
        include_negatives=False
    )
    e9_net_expansion = _safe_divide(
        numerator=permanent_crops_net_expansion,
        denominator=permanent_crops_gross_expansion
    ) if land_use_type == PERMANENT_CROPLAND else (
        _safe_divide(
            numerator=annual_crops_net_expansion,
            denominator=annual_crops_gross_expansion
        ) if land_use_type == ANNUAL_CROPLAND else 1
    )

    # E10: Compare changes to annual/perennial cropland from net expansion.
    net_expansion_cultivated_vs_harvested = _get_net_expansion_cultivated_vs_harvested(
        annual_crops_net_expansion=annual_crops_net_expansion,
        changes=changes,
        land_use_type=land_use_type,
        permanent_crops_net_expansion=permanent_crops_net_expansion
    )

    site_area = {
        land_type: (
            shares_of_expansion[land_type] * expansion_factor * e9_net_expansion * net_expansion_cultivated_vs_harvested
        )
        for land_type in LAND_USE_TERMS_FOR_TRANSFORMATION.keys()
        if land_type != land_use_type
    }
    site_area[land_use_type] = 1 - sum(site_area.values())

    sum_of_site_areas_is_100 = site_area_sum_to_100(site_area)
    logRequirements(
        log_node=site,
        model=MODEL,
        term=term.get("@id"),
        model_key=MODEL_KEY,
        land_use_type=land_use_type,
        country_id=country_id,
        site_area=log_as_table(site_area),
        sum_of_site_areas_is_100=sum_of_site_areas_is_100
    )

    should_run = all(
        [
            site.get("siteType"),
            country_id,
            non_empty_value(term),
            site.get("siteType") in SITE_TYPES,
            sum_of_site_areas_is_100
        ]
    )
    logShouldRun(site, MODEL, term=term.get("@id"), should_run=should_run, key=MODEL_KEY)

    return should_run, site_area


def _should_run(site: dict) -> tuple[bool, dict]:
    management_nodes = filter_list_term_type(site.get("management", []), TermTermType.LANDCOVER)
    land_use_type = _lookup_land_use_type(nodes=management_nodes)
    should_run_result, site_area = (
        (False, {}) if land_use_type not in {ANNUAL_CROPLAND, PERMANENT_CROPLAND, PERMANENT_PASTURE}
        else _should_run_historical_land_use_change(
            site=site,
            land_use_type=land_use_type
        )
    )

    return should_run_result, site_area


def run(site: dict) -> list:
    should_run, site_area = _should_run(site)
    management_nodes = filter_list_term_type(site.get("management", []), TermTermType.LANDCOVER)
    return _run_make_management_nodes(
        existing_nodes=management_nodes,
        percentage_transformed_from=site_area,
        start_year=int(management_nodes[0].get("endDate")[:4]) - DEFAULT_WINDOW_IN_YEARS
    ) if should_run else []
