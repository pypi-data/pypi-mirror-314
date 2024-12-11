# roksana/evaluation/metrics.py

from typing import List

def hit_at_k(retrieved: List[int], gold_set: List[int], k: int) -> float:
    """
    Calculate Hit@k metric.

    Args:
        retrieved (List[int]): List of retrieved node indices.
        gold_set (List[int]): List of gold node indices.
        k (int): The k in Hit@k.

    Returns:
        float: Hit@k value (1 if at least one gold node is in the top-k, else 0).
    """
    top_k = retrieved[:k]
    return 1.0 if any(node in top_k for node in gold_set) else 0.0

def recall_at_k(retrieved: List[int], gold_set: List[int], k: int) -> float:
    """
    Calculate Recall@k metric.

    Args:
        retrieved (List[int]): List of retrieved node indices.
        gold_set (List[int]): List of gold node indices.
        k (int): The k in Recall@k.

    Returns:
        float: Recall@k value.
    """
    top_k = set(retrieved[:k])
    gold = set(gold_set)
    if not gold:
        return 0.0
    return len(top_k.intersection(gold)) / len(gold)

def demotion_value(before_attack_rank: int, after_attack_rank: int) -> int:
    """
    Calculate the Demotion Value metric.

    Args:
        before_attack_rank (int): The rank of the target node before the attack.
        after_attack_rank (int): The rank of the target node after the attack.

    Returns:
        int: Difference in rank (after_attack_rank - before_attack_rank).
             A positive value indicates demotion.
    """
    return after_attack_rank - before_attack_rank