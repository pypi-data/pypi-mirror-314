"""
Characterises [soilQualityIndexLandTransformation](https://hestia.earth/term/soilQualityIndexLandTransformation)
based on an updated [LANCA model (De Laurentiis et al. 2019)](
http://publications.jrc.ec.europa.eu/repository/handle/JRC113865) and on the LANCA (Regionalised) Characterisation
Factors version 2.5 (Horn and Meier, 2018).
"""
from typing import List, Tuple, Optional

from hestia_earth.schema import TermTermType
from hestia_earth.utils.lookup import download_lookup
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logRequirements, logShouldRun, log_as_table
from . import MODEL
from .utils import get_coefficient_factor
from ..utils.impact_assessment import get_country_id
from ..utils.indicator import _new_indicator
from ..utils.landCover import get_pef_grouping
from ..utils.lookup import fallback_country, _node_value
from ..utils.term import get_land_cover_terms

REQUIREMENTS = {
    "ImpactAssessment": {
        "emissionsResourceUse": [
            {
                "@type": "Indicator",
                "term.units": "m2 / year",
                "term.termType": "resourceUse",
                "term.name": "Land transformation from",
                "value": "> 0",
                "landCover": {"@type": "Term", "term.termType": "landCover"}
            }
        ],
        "optional": {"country": {"@type": "Term", "termType": "region"}}
    }
}

# Note: CFs in `region-pefTermGrouping-landTransformation-from.csv` appear to be the opposite values as those in
# `region-pefTermGrouping-landTransformation-to.csv` but can be different in some cases.
LOOKUPS = {
    "region-pefTermGrouping-landTransformation-from": "using country and `pefTermGrouping` from `landCover`",
    "region-pefTermGrouping-landTransformation-to": "using country and `pefTermGrouping` from `landCover`",
    "landCover": "pefTermGrouping"
}

from_lookup_file = f"{list(LOOKUPS.keys())[0]}.csv"
to_lookup_file = f"{list(LOOKUPS.keys())[1]}.csv"

LOOKUP = {
    "from": from_lookup_file,
    "to": to_lookup_file
}

RETURNS = {
    "Indicator": {
        "value": ""
    }
}

TERM_ID = 'soilQualityIndexLandTransformation'


def _indicator(value: float):
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator['value'] = value
    return indicator


def _run(transformations: List[dict]):
    values = [(transformation['factor-from'] + transformation['factor-to']) * transformation['area'] for transformation
              in transformations]
    return _indicator(list_sum(values))


def _extract_land_cover_from_indicator_id(indicator: dict) -> Optional[str]:
    """
    Given a indicator with term type `resourceUse` return the equivalent `landCover` term
    """
    term_in_id = indicator.get('term', {}).get('@id', '') \
        .removeprefix("landTransformationFrom") \
        .removesuffix("20YearAverageInputsProduction") \
        .removesuffix("20YearAverageDuringCycle")
    term_in_id = term_in_id[0].lower() + term_in_id[1:] if term_in_id else None
    return term_in_id


def _is_valid_indicator(indicator: dict, land_cover_term_ids: list[str]) -> bool:
    term_id = _extract_land_cover_from_indicator_id(indicator)
    return term_id in land_cover_term_ids


def _should_run(impact_assessment: dict) -> Tuple[bool, list]:
    resource_uses = filter_list_term_type(impact_assessment.get('emissionsResourceUse', []), TermTermType.RESOURCEUSE)
    land_cover_term_ids = get_land_cover_terms() if resource_uses else []

    land_transformation_indicators = [i for i in resource_uses if _is_valid_indicator(i, land_cover_term_ids)]

    found_transformations = [
        {
            'area': _node_value(transformation_indicator) * 20,
            'area-unit': transformation_indicator.get('term', {}).get("units"),
            'land-cover-id-from': _extract_land_cover_from_indicator_id(transformation_indicator),
            'land-cover-id-to': transformation_indicator.get('landCover', {}).get("@id"),
            'indicator-id': transformation_indicator.get('term', {}).get('@id', ''),
            'good-land-cover-term': transformation_indicator.get('landCover', {}).get('termType') == 'landCover',
            'country-id': get_country_id(impact_assessment),
            'area-is-valid': _node_value(transformation_indicator) is not None and _node_value(
                transformation_indicator) > 0,
            'area-unit-is-valid': transformation_indicator.get('term', {}).get("units") == "m2 / year",
            'lookup-country': fallback_country(get_country_id(impact_assessment),
                                               [download_lookup(from_lookup_file), download_lookup(to_lookup_file)]),
        } for transformation_indicator in land_transformation_indicators
    ]

    found_transformations_with_coefficient = [
        transformation | {
            "using-fallback-country-region-world-CFs": transformation['lookup-country'] != transformation['country-id'],
            'factor-from': get_coefficient_factor(
                lookup_name=from_lookup_file,
                country_id=transformation['lookup-country'],
                term_id=TERM_ID,
                occupation_type=get_pef_grouping(transformation['land-cover-id-from'])) if
            transformation['land-cover-id-from'] else None,
            'factor-to': get_coefficient_factor(
                lookup_name=to_lookup_file,
                country_id=transformation['lookup-country'],
                term_id=TERM_ID,
                occupation_type=get_pef_grouping(transformation['land-cover-id-to'])) if
            transformation['land-cover-id-to'] else None
        } for transformation in found_transformations
    ]

    valid_transformations_with_coef = [
        t for t in found_transformations_with_coefficient if all([
            t['area-is-valid'],
            t['area-unit-is-valid'],
            t['factor-from'] is not None,
            t['factor-to'] is not None
        ])
    ]

    has_land_transformation_indicators = bool(land_transformation_indicators)

    all_transformations_are_valid = all(
        [
            all([t['area-is-valid'], t['area-unit-is-valid'], t['good-land-cover-term']])
            for t in found_transformations_with_coefficient
        ]
    ) if found_transformations_with_coefficient else False

    logRequirements(impact_assessment, model=MODEL, term=TERM_ID,
                    has_land_occupation_indicators=has_land_transformation_indicators,
                    all_transformations_are_valid=all_transformations_are_valid,
                    has_valid_transformations_with_coef=bool(valid_transformations_with_coef),
                    found_transformations=log_as_table(found_transformations_with_coefficient)
                    )

    should_run = has_land_transformation_indicators is False or all([has_land_transformation_indicators,
                                                                     all_transformations_are_valid])

    logShouldRun(impact_assessment, MODEL, TERM_ID, should_run)
    return should_run, valid_transformations_with_coef


def run(impact_assessment: dict):
    should_run, transformations = _should_run(impact_assessment)
    return _run(transformations) if should_run else None
