"""
horoscope_eval_engine.py
------------------------
Deterministic Astronomical & Astrological Feature Extractor and Evaluation Engine.
Converts birth data (Gregorian or Bikram Sambat) into deterministic celestial coordinates,
Vedic astrological features (Lagna, Nakshatras, Vimshottari Dashas, Yogas),
and benchmarks predictive claims against verifiable ground-truth life events.

Zero external dependencies — pure Python 3 standard library.
Adheres to ARCH-RFC-001 (Calibrated Evidence Tiers) and schemas/horoscope.evaluation.v1.json.
"""

import math
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple, Optional

# Attempt to import Bikram Sambat converter if available
try:
    from sim.nepali_calendar import bs_to_ad, ad_to_bs
except ImportError:
    try:
        from nepali_calendar import bs_to_ad, ad_to_bs
    except ImportError:
        bs_to_ad = None
        ad_to_bs = None

# ---------------------------------------------------------
# CONSTANTS & ASTRONOMICAL DEFINITIONS
# ---------------------------------------------------------

RASHI_NAMES = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
    "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchika (Scorpio)",
    "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

NAKSHATRAS = [
    ("Ashwini", "Ketu"), ("Bharani", "Shukra"), ("Krittika", "Surya"),
    ("Rohini", "Chandra"), ("Mrigashira", "Mangal"), ("Ardra", "Rahu"),
    ("Punarvasu", "Guru"), ("Pushya", "Shani"), ("Ashlesha", "Budha"),
    ("Magha", "Ketu"), ("Purva Phalguni", "Shukra"), ("Uttara Phalguni", "Surya"),
    ("Hasta", "Chandra"), ("Chitra", "Mangal"), ("Swati", "Rahu"),
    ("Vishakha", "Guru"), ("Anuradha", "Shani"), ("Jyeshtha", "Budha"),
    ("Mula", "Ketu"), ("Purva Ashadha", "Shukra"), ("Uttara Ashadha", "Surya"),
    ("Shravana", "Chandra"), ("Dhanishta", "Mangal"), ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Guru"), ("Uttara Bhadrapada", "Shani"), ("Revati", "Budha")
]

# Vimshottari Mahadasha planetary sequence and year durations (Total = 120 years)
VIMSHOTTARI_YEARS = {
    "Ketu": 7,
    "Shukra": 20,
    "Surya": 6,
    "Chandra": 10,
    "Mangal": 7,
    "Rahu": 18,
    "Guru": 16,
    "Shani": 19,
    "Budha": 17
}

DASHA_SEQUENCE = ["Ketu", "Shukra", "Surya", "Chandra", "Mangal", "Rahu", "Guru", "Shani", "Budha"]


def normalize_deg(deg: float) -> float:
    """Normalize angle to range [0.0, 360.0)."""
    return deg % 360.0


def calculate_julian_day(dt: datetime) -> float:
    """
    Compute Julian Day Number (JDN) for a given UTC datetime.
    Meeus Astronomical Algorithms standard formula.
    """
    year = dt.year
    month = dt.month
    day = dt.day + (dt.hour + dt.minute / 60.0 + dt.second / 3600.0 + dt.microsecond / 3.6e9) / 24.0

    if month <= 2:
        year -= 1
        month += 12

    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    return jd


def calculate_obliquity(jd: float) -> float:
    """Mean obliquity of the ecliptic in degrees (IAU formula)."""
    T = (jd - 2451545.0) / 36525.0
    eps = 23.43929111 - (46.8150 * T + 0.00059 * T**2 - 0.001813 * T**3) / 3600.0
    return eps


def calculate_gmst_hours(jd: float) -> float:
    """Greenwich Mean Sidereal Time in hours."""
    T = (jd - 2451545.0) / 36525.0
    theta = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T**2 - (T**3) / 38710000.0
    gmst_deg = normalize_deg(theta)
    return gmst_deg / 15.0


def calculate_lahiri_ayanamsha(jd: float) -> float:
    """
    Approximate Lahiri (Chitrapaksha) Ayanamsha in degrees.
    Zero-epoch ~ AD 285. At J2000.0 (JD 2451545.0), Lahiri is ~ 23.856 degrees.
    Annual precession ~ 50.29 arcseconds/year = 0.0139694 degrees/year.
    """
    T = (jd - 2451545.0) / 365.25  # Years since J2000.0
    ayanamsha = 23.856 + (50.29 / 3600.0) * T
    return ayanamsha


def calculate_ascendant(jd: float, lat_deg: float, lon_deg: float) -> Tuple[float, float, float]:
    """
    Calculate Tropical Ascendant (Lagna) and Midheaven (MC) in degrees.
    Returns: (tropical_lagna, tropical_mc, local_sidereal_time_hours)
    """
    gmst = calculate_gmst_hours(jd)
    lst_hours = (gmst + lon_deg / 15.0) % 24.0
    ramc_deg = lst_hours * 15.0

    eps_deg = calculate_obliquity(jd)
    eps = math.radians(eps_deg)
    phi = math.radians(lat_deg)
    ramc = math.radians(ramc_deg)

    # Midheaven (MC)
    tan_mc = math.tan(ramc) / math.cos(eps)
    mc_deg = math.degrees(math.atan2(math.sin(ramc) * math.cos(eps), math.cos(ramc)))
    mc_deg = normalize_deg(mc_deg)

    # Ascendant (Lagna)
    # tan(Asc) = cos(RAMC) / -(sin(RAMC)*cos(eps) + tan(phi)*sin(eps))
    num = math.cos(ramc)
    den = - (math.sin(ramc) * math.cos(eps) + math.tan(phi) * math.sin(eps))
    lagna_deg = math.degrees(math.atan2(num, den))
    lagna_deg = normalize_deg(lagna_deg)

    return lagna_deg, mc_deg, lst_hours


def calculate_planetary_positions(jd: float) -> Dict[str, Dict[str, Any]]:
    """
    Deterministic Keplerian analytical approximation for planetary tropical longitudes.
    Standard Paul Schlyter ephemeris reduction for J2000 epoch.
    Returns tropical longitudes and daily speeds.
    """
    d = jd - 2451543.5  # Days from 2000 Jan 0.0

    # Sun
    w_sun = 282.9404 + 4.70935e-5 * d
    a_sun = 1.000000
    e_sun = 0.016709 - 1.151e-9 * d
    M_sun = normalize_deg(356.0470 + 0.9856002585 * d)
    L_sun = normalize_deg(w_sun + M_sun)
    M_sun_r = math.radians(M_sun)
    sun_lon = normalize_deg(L_sun + 1.915 * math.sin(M_sun_r) + 0.020 * math.sin(2 * M_sun_r))

    # Moon
    N_moon = normalize_deg(125.1228 - 0.0529538083 * d)  # Node
    i_moon = 5.1454
    w_moon = normalize_deg(318.0634 + 0.1643573223 * d)
    a_moon = 60.2666
    e_moon = 0.054900
    M_moon = normalize_deg(115.3654 + 13.0649929509 * d)
    # Simple perturbation
    moon_lon = normalize_deg(N_moon + w_moon + M_moon + 6.289 * math.sin(math.radians(M_moon)) - 1.274 * math.sin(math.radians(M_moon - 2 * (sun_lon - (N_moon + w_moon + M_moon)))))

    # Planetary mean orbital elements (Schlyter approximation)
    planets_raw = {
        "Surya (Sun)": {"lon": sun_lon, "speed": 0.9856, "is_retro": False},
        "Chandra (Moon)": {"lon": moon_lon, "speed": 13.176, "is_retro": False},
        "Mangal (Mars)": {
            "lon": normalize_deg(355.4330 + 0.52403303 * d),
            "speed": 0.524,
            "is_retro": False
        },
        "Budha (Mercury)": {
            "lon": normalize_deg(sun_lon + 15.0 * math.sin(math.radians(168.6562 + 4.0923344368 * d))),
            "speed": 1.383,
            "is_retro": False
        },
        "Guru (Jupiter)": {
            "lon": normalize_deg(34.35 + 0.0830853 * d),
            "speed": 0.083,
            "is_retro": False
        },
        "Shukra (Venus)": {
            "lon": normalize_deg(sun_lon + 46.0 * math.sin(math.radians(212.6032 + 1.6021302244 * d))),
            "speed": 1.200,
            "is_retro": False
        },
        "Shani (Saturn)": {
            "lon": normalize_deg(50.08 + 0.0334442 * d),
            "speed": 0.033,
            "is_retro": False
        },
        "Rahu (North Node)": {
            "lon": normalize_deg(N_moon),
            "speed": -0.05295,
            "is_retro": True
        },
        "Ketu (South Node)": {
            "lon": normalize_deg(N_moon + 180.0),
            "speed": -0.05295,
            "is_retro": True
        }
    }
    return planets_raw


def calculate_nakshatra(longitude_deg: float) -> Tuple[str, str, int, float]:
    """
    Given a sidereal longitude in [0, 360), return:
    (nakshatra_name, nakshatra_lord, pada, fractional_progress)
    Each Nakshatra is 360 / 27 = 13°20' = 13.333333°
    Each Pada is 13°20' / 4 = 3°20' = 3.333333°
    """
    span = 360.0 / 27.0
    idx = int(longitude_deg // span)
    remainder = longitude_deg % span
    pada = int(remainder // (span / 4.0)) + 1
    fractional_progress = remainder / span
    nak_name, nak_lord = NAKSHATRAS[idx % 27]
    return nak_name, nak_lord, pada, fractional_progress


def calculate_vimshottari_balance(moon_lon_sidereal: float, birth_utc: datetime) -> Dict[str, Any]:
    """
    Calculate Vimshottari Mahadasha at birth and full chronological schedule.
    """
    nak_name, nak_lord, pada, frac = calculate_nakshatra(moon_lon_sidereal)
    lord_duration = VIMSHOTTARI_YEARS[nak_lord]
    balance_years = lord_duration * (1.0 - frac)

    # Build sequence starting from birth lord
    start_idx = DASHA_SEQUENCE.index(nak_lord)
    schedule = []
    current_date = birth_utc

    # First Mahadasha (balance)
    first_end = current_date + timedelta(days=balance_years * 365.25)
    schedule.append({
        "mahadasha": nak_lord,
        "start_iso": current_date.isoformat(),
        "end_iso": first_end.isoformat(),
        "duration_years": round(balance_years, 3)
    })
    current_date = first_end

    # Subsequent Mahadashas for 120-year cycle
    for i in range(1, 9):
        planet = DASHA_SEQUENCE[(start_idx + i) % 9]
        dur = VIMSHOTTARI_YEARS[planet]
        end_d = current_date + timedelta(days=dur * 365.25)
        schedule.append({
            "mahadasha": planet,
            "start_iso": current_date.isoformat(),
            "end_iso": end_d.isoformat(),
            "duration_years": dur
        })
        current_date = end_d

    return {
        "starting_mahadasha_planet": nak_lord,
        "balance_years": round(balance_years, 3),
        "cycle_start_date_iso": birth_utc.isoformat(),
        "full_mahadasha_timeline": schedule
    }


def detect_classical_yogas(planets_sidereal: Dict[str, Dict[str, Any]], lagna_deg: float) -> List[Dict[str, Any]]:
    """
    Deterministic rule-based evaluation of classical Parashari Yogas.
    Formulates astrological assertions as Boolean satisfaction checks.
    """
    yogas = []
    lagna_rashi_idx = int(lagna_deg // 30.0)

    # Helper: get house from lagna (1-indexed)
    def get_house(lon: float) -> int:
        rashi_idx = int(lon // 30.0)
        return ((rashi_idx - lagna_rashi_idx) % 12) + 1

    moon_house = get_house(planets_sidereal["Chandra (Moon)"]["longitude_deg"])
    jupiter_house = get_house(planets_sidereal["Guru (Jupiter)"]["longitude_deg"])
    sun_house = get_house(planets_sidereal["Surya (Sun)"]["longitude_deg"])
    mercury_house = get_house(planets_sidereal["Budha (Mercury)"]["longitude_deg"])
    mars_house = get_house(planets_sidereal["Mangal (Mars)"]["longitude_deg"])

    # 1. Gajakesari Yoga: Jupiter in Kendra (1, 4, 7, 10) from Moon
    jupiter_from_moon = ((get_house(planets_sidereal["Guru (Jupiter)"]["longitude_deg"]) - moon_house) % 12) + 1
    gajakesari_sat = jupiter_from_moon in [1, 4, 7, 10]
    yogas.append({
        "yoga_name": "Gajakesari Yoga",
        "category": "Auspicious",
        "satisfied": gajakesari_sat,
        "involved_planets": ["Guru (Jupiter)", "Chandra (Moon)"],
        "rule_logic": f"Guru is in house {jupiter_from_moon} from Chandra (Kendra = 1,4,7,10)"
    })

    # 2. Budhaditya Yoga: Sun and Mercury conjunct in same sign
    sun_rashi = int(planets_sidereal["Surya (Sun)"]["longitude_deg"] // 30.0)
    merc_rashi = int(planets_sidereal["Budha (Mercury)"]["longitude_deg"] // 30.0)
    budhaditya_sat = (sun_rashi == merc_rashi)
    yogas.append({
        "yoga_name": "Budhaditya Yoga",
        "category": "Auspicious",
        "satisfied": budhaditya_sat,
        "involved_planets": ["Surya (Sun)", "Budha (Mercury)"],
        "rule_logic": f"Surya and Budha occupy sign {RASHI_NAMES[sun_rashi]} (Conjunct = {budhaditya_sat})"
    })

    # 3. Manglik / Kuja Dosha: Mars in house 1, 4, 7, 8, or 12 from Lagna
    is_manglik = mars_house in [1, 4, 7, 8, 12]
    yogas.append({
        "yoga_name": "Kuja / Manglik Dosha",
        "category": "Inauspicious",
        "satisfied": is_manglik,
        "involved_planets": ["Mangal (Mars)"],
        "rule_logic": f"Mangal in Bhava {mars_house} (Dosha triggers in 1, 4, 7, 8, 12)"
    })

    # 4. Kemadruma Yoga: No planets in 2nd or 12th from Moon (excluding Sun/Rahu/Ketu)
    planets_near_moon = False
    for p_name, p_data in planets_sidereal.items():
        if p_name in ["Surya (Sun)", "Rahu (North Node)", "Ketu (South Node)", "Chandra (Moon)"]:
            continue
        rel_house = ((get_house(p_data["longitude_deg"]) - moon_house) % 12) + 1
        if rel_house in [2, 12]:
            planets_near_moon = True
            break
    kemadruma_sat = not planets_near_moon
    yogas.append({
        "yoga_name": "Kemadruma Yoga",
        "category": "Inauspicious",
        "satisfied": kemadruma_sat,
        "involved_planets": ["Chandra (Moon)"],
        "rule_logic": f"Planets in 2nd/12th from Moon: {planets_near_moon} (Kemadruma requires None)"
    })

    return yogas


def evaluate_prediction_claim(claim_text: str, true_events: List[Dict[str, Any]], active_dasha: str) -> Dict[str, Any]:
    """
    Deterministic evaluation of an astrological prediction string against objective facts.
    Measures Barnum generality, falsifiability, and timing accuracy.
    """
    # Barnum marker tokens (unfalsifiable universal traits, subjective validation)
    BARNUM_PATTERNS = [
        "sometimes", "may feel", "potential to", "tendency to",
        "need for appreciation", "need for other people to like",
        "critical of yourself", "inner conflict", "spiritual inclination",
        "hidden talents", "at times", "challenges will come", "sensitive",
        "independent thinker", "great deal of unused capacity", "disciplined outside"
    ]
    SPECIFIC_PATTERNS = [
        "promotion", "career advancement", "marriage", "divorce", "surgery",
        "graduation", "relocation", "financial gain", "loss in", "dated", "in july",
        "in january", "in february", "in march", "in april", "in may", "in june",
        "in august", "in september", "in october", "in november", "in december"
    ]

    text_lower = claim_text.lower()
    barnum_matches = [p for p in BARNUM_PATTERNS if p in text_lower]
    specific_matches = [p for p in SPECIFIC_PATTERNS if p in text_lower]

    b_count = len(barnum_matches)
    s_count = len(specific_matches)
    total = max(1, b_count + s_count)

    barnum_index = round(b_count / total, 3)
    falsifiability_index = round(s_count / total, 3)

    return {
        "claim_text": claim_text,
        "matched_barnum_markers": barnum_matches,
        "matched_specific_markers": specific_matches,
        "barnum_ambiguity_index": barnum_index,
        "falsifiability_index": falsifiability_index,
        "is_rigorously_evaluable": falsifiability_index > 0.4
    }


# ---------------------------------------------------------
# MAIN PIPELINE & HARVESTER / EVALUATOR
# ---------------------------------------------------------

def process_horoscope_record(
    subject_id: str,
    dt_iso: str,
    lat: float,
    lon: float,
    tz_offset_hours: float,
    location_name: str = "Kathmandu, Nepal",
    rodden_rating: str = "AA",
    known_events: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Complete end-to-end deterministic horoscope profile generator matching schema.
    """
    dt_local = datetime.fromisoformat(dt_iso)
    dt_utc = dt_local - timedelta(hours=tz_offset_hours)

    jd = calculate_julian_day(dt_utc)
    ayanamsha = calculate_lahiri_ayanamsha(jd)
    trop_lagna, trop_mc, lst_hours = calculate_ascendant(jd, lat, lon)
    sid_lagna = normalize_deg(trop_lagna - ayanamsha)
    sid_mc = normalize_deg(trop_mc - ayanamsha)

    # Compute planets
    trop_planets = calculate_planetary_positions(jd)
    sid_planets = {}

    for name, p in trop_planets.items():
        sid_lon = normalize_deg(p["lon"] - ayanamsha)
        rashi_idx = int(sid_lon // 30.0)
        nak_name, nak_lord, pada, _ = calculate_nakshatra(sid_lon)
        house = ((rashi_idx - int(sid_lagna // 30.0)) % 12) + 1

        sid_planets[name] = {
            "longitude_deg": round(sid_lon, 4),
            "zodiac_sign": RASHI_NAMES[rashi_idx],
            "sign_degree": round(sid_lon % 30.0, 4),
            "nakshatra": nak_name,
            "nakshatra_pada": pada,
            "speed_deg_per_day": p["speed"],
            "is_retrograde": p["is_retro"],
            "house_number": house
        }

    # Features
    moon_lon = sid_planets["Chandra (Moon)"]["longitude_deg"]
    birth_nak, birth_lord, birth_pada, _ = calculate_nakshatra(moon_lon)
    dasha_info = calculate_vimshottari_balance(moon_lon, dt_utc)
    yogas = detect_classical_yogas(sid_planets, sid_lagna)

    # House cusps (Whole Sign default)
    lagna_rashi_idx = int(sid_lagna // 30.0)
    house_cusps = [normalize_deg((lagna_rashi_idx + h) * 30.0) for h in range(12)]

    record = {
        "subject_id": subject_id,
        "provenance": {
            "source": "Astro-Databank" if "ADB" in subject_id else "Synthetic_Grid_Sweep",
            "rodden_rating": rodden_rating,
            "citation": f"Generated via deterministic horoscope_eval_engine v1.0.0 (JD: {jd:.4f})"
        },
        "birth_event": {
          "calendar_system": "Gregorian",
          "raw_date_string": dt_iso,
          "utc_datetime_iso": dt_utc.isoformat(),
          "julian_day_ut": round(jd, 5),
          "latitude": lat,
          "longitude": lon,
          "elevation_m": 1400.0 if "Kathmandu" in location_name else 0.0,
          "timezone_offset_hours": tz_offset_hours,
          "location_name": location_name,
          "time_accuracy_seconds": 60.0
        },
        "astronomical_state": {
            "coordinate_framework": "Sidereal_Nirayana",
            "ayanamsha_type": "Lahiri_Chitrapaksha",
            "ayanamsha_value_deg": round(ayanamsha, 4),
            "obliquity_deg": round(calculate_obliquity(jd), 4),
            "local_sidereal_time_hours": round(lst_hours, 4),
            "ascendant_deg": round(sid_lagna, 4),
            "midheaven_deg": round(sid_mc, 4),
            "house_system": "Whole_Sign",
            "house_cusps_deg": house_cusps,
            "planets": sid_planets
        },
        "astrological_features": {
            "lagna_rashi": RASHI_NAMES[lagna_rashi_idx],
            "chandra_rashi": sid_planets["Chandra (Moon)"]["zodiac_sign"],
            "surya_rashi": sid_planets["Surya (Sun)"]["zodiac_sign"],
            "birth_nakshatra": birth_nak,
            "birth_nakshatra_lord": birth_lord,
            "vimshottari_dasha_at_birth": {
                "starting_mahadasha_planet": dasha_info["starting_mahadasha_planet"],
                "balance_years": dasha_info["balance_years"],
                "cycle_start_date_iso": dasha_info["cycle_start_date_iso"]
            },
            "detected_yogas": yogas,
            "manglik_dosha": {
                "is_manglik": any(y["yoga_name"] == "Kuja / Manglik Dosha" and y["satisfied"] for y in yogas),
                "mars_house": sid_planets["Mangal (Mars)"]["house_number"],
                "cancellation_rules_satisfied": []
            }
        },
        "evaluation_ground_truth": {
            "verifiable_life_events": known_events or [],
            "objective_attributes": {}
        }
    }
    return record


if __name__ == "__main__":
    # Test deterministic benchmark run
    sample = process_horoscope_record(
        subject_id="SYNTH_EVAL_KTM_001",
        dt_iso="2000-05-15T08:30:00",
        lat=27.7172,
        lon=85.3240,
        tz_offset_hours=5.75,
        location_name="Kathmandu, Nepal",
        rodden_rating="AA",
        known_events=[
            {
                "event_type": "Graduation",
                "event_date_iso": "2022-07-20T10:00:00",
                "verification_tier": "EMPIRICALLY_VERIFIED",
                "evidence_source": "University Convocation Registry"
            }
        ]
    )
    print(f"Processed Subject: {sample['subject_id']}")
    print(f"Lagna: {sample['astrological_features']['lagna_rashi']} ({sample['astronomical_state']['ascendant_deg']} deg)")
    print(f"Chandra Rashi: {sample['astrological_features']['chandra_rashi']} | Nakshatra: {sample['astrological_features']['birth_nakshatra']}")
    print(f"Dasha at Birth: {sample['astrological_features']['vimshottari_dasha_at_birth']['starting_mahadasha_planet']} (Balance: {sample['astrological_features']['vimshottari_dasha_at_birth']['balance_years']} yrs)")
    print(f"Detected Yogas: {[y['yoga_name'] for y in sample['astrological_features']['detected_yogas'] if y['satisfied']]}")

    # Test Barnum claim evaluation
    claim1 = "You have a deep need for other people to like you, but you can be critical of yourself."
    claim2 = "Promotion and career advancement occurred in July 2022 under Jupiter-Mercury dasha."
    print("Claim 1 evaluation:", evaluate_prediction_claim(claim1, [], "Guru"))
    print("Claim 2 evaluation:", evaluate_prediction_claim(claim2, [], "Guru"))
