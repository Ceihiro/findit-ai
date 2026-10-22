"""The matching engine: attribute (rule-based) score + TF-IDF text similarity.

Both scores are between 0 and 1. The final score mixes them using the shares in config.py.
"""
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import config


def _norm(value):
    return (value or "").strip().lower()


def _hours_apart(time_a, time_b):
    try:
        a = datetime.fromisoformat(time_a)
        b = datetime.fromisoformat(time_b)
    except (TypeError, ValueError):
        return None
    return abs((a - b).total_seconds()) / 3600


def attribute_score(lost, found):
    """Rule-based score. Returns (score 0..1, list of reasons).

    If an attribute is blank on either side (for example no brand), it is skipped and the
    remaining weights are rescaled, so missing information does not unfairly lower the score.
    """
    weights = config.ATTRIBUTE_WEIGHTS
    parts = {}      # attribute -> 0..1
    reasons = []

    if _norm(lost["category"]) and _norm(found["category"]):
        same = _norm(lost["category"]) == _norm(found["category"])
        parts["category"] = 1.0 if same else 0.0
        if same:
            reasons.append(f"Same category: {found['category']}")

    if _norm(lost["color"]) and _norm(found["color"]):
        same = _norm(lost["color"]) == _norm(found["color"])
        parts["color"] = 1.0 if same else 0.0
        if same:
            reasons.append(f"Same color: {found['color']}")

    if _norm(lost["brand"]) and _norm(found["brand"]):
        same = _norm(lost["brand"]) == _norm(found["brand"])
        parts["brand"] = 1.0 if same else 0.0
        if same:
            reasons.append(f"Same brand: {found['brand']}")

    if _norm(lost["location"]) and _norm(found["location"]):
        same = _norm(lost["location"]) == _norm(found["location"])
        parts["location"] = 1.0 if same else 0.0
        if same:
            reasons.append(f"Same location: {found['location']}")

    hours = _hours_apart(lost["event_time"], found["event_time"])
    if hours is not None:
        parts["time"] = max(0.0, 1.0 - hours / config.TIME_WINDOW_HOURS)
        if hours <= config.TIME_WINDOW_HOURS:
            reasons.append(f"Found within {hours:.0f} hour(s) of the lost time")

    used_weight = sum(weights[k] for k in parts)
    if used_weight == 0:
        return 0.0, reasons
    score = sum(weights[k] * v for k, v in parts.items()) / used_weight
    return score, reasons


def _doc(item):
    """Turn an item into one piece of text for TF-IDF."""
    return " ".join([item["category"] or "", item["color"] or "",
                     item["brand"] or "", item["description"] or ""]).lower()


def text_scores(lost, found_items):
    """TF-IDF cosine similarity between the lost description and each found description."""
    if not found_items:
        return []
    docs = [_doc(lost)] + [_doc(f) for f in found_items]
    try:
        matrix = TfidfVectorizer().fit_transform(docs)
    except ValueError:            # empty vocabulary (all descriptions blank)
        return [0.0] * len(found_items)
    return list(cosine_similarity(matrix[0], matrix[1:])[0])


def rank_matches(lost, found_items, top_n=None,
                 attribute_share=None, text_share=None):
    """Rank found items for one lost report.

    attribute_share / text_share can be overridden to compare methods, e.g.
    (1, 0) = attributes only, (0, 1) = text only, defaults = combined.
    """
    top_n = top_n or config.TOP_N
    a_share = config.ATTRIBUTE_SHARE if attribute_share is None else attribute_share
    t_share = config.TEXT_SHARE if text_share is None else text_share

    texts = text_scores(lost, found_items)
    results = []
    for found, t_score in zip(found_items, texts):
        a_score, reasons = attribute_score(lost, found)
        final = a_share * a_score + t_share * t_score
        if t_score > 0:
            reasons.append(f"Description similarity: {t_score:.0%}")
        results.append({
            "found": found,
            "attribute_score": a_score,
            "text_score": t_score,
            "final_score": final,
            "reasons": reasons,
        })
    results.sort(key=lambda r: r["final_score"], reverse=True)
    return results[:top_n]
