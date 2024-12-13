import random
from sklearn.metrics import adjusted_rand_score
from itertools import combinations
from sklearn.metrics import silhouette_score
from sklearn.metrics import normalized_mutual_info_score



def get_cluster_pairs(uuids, labels):
    pairs = set()
    for cluster in set(labels):
        if cluster != -1:  # ignore unclustered items (noise)
            cluster_uuids = [uuid for uuid, label in zip(uuids, labels) if label == cluster]
            pairs.update(combinations(cluster_uuids, 2))
    return pairs

def calculate_rates(predicted_pairs, expected_pairs, total_pairs):
    false_positives = len(predicted_pairs - expected_pairs)
    false_negatives = len(expected_pairs - predicted_pairs)
    true_positives = len(predicted_pairs & expected_pairs)
    true_negatives = len(total_pairs - predicted_pairs - expected_pairs)
    
    false_positive_rate = false_positives / (false_positives + true_negatives) if (false_positives + true_negatives) > 0 else 0
    false_negative_rate = false_negatives / (false_negatives + true_positives) if (false_negatives + true_positives) > 0 else 0
    
    return false_positive_rate, false_negative_rate, true_positives, false_positives, false_negatives

def calculate_metrics(true_positives, false_positives, false_negatives):
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1_score


def evaluate(uuids, predicted_labels, expected_labels, embeddings=None):
    predicted_pairs = get_cluster_pairs(uuids, predicted_labels)
    expected_pairs = get_cluster_pairs(uuids, expected_labels)
    total_pairs = set(combinations(uuids, 2))
    
    false_positive_rate, false_negative_rate, true_positives, false_positives, false_negatives = calculate_rates(
        predicted_pairs, expected_pairs, total_pairs
    )
    
    precision, recall, f1_score = calculate_metrics(true_positives, false_positives, false_negatives)
    
    ari = adjusted_rand_score(expected_labels, predicted_labels)
    nmi = normalized_mutual_info_score(expected_labels, predicted_labels)
    
    if embeddings is not None and len(set(predicted_labels)) > 1:
        sil_score = silhouette_score(embeddings, predicted_labels)
    else:
        sil_score = float('nan')
    
    valid_scores = [metric for metric in [f1_score, ari, sil_score, nmi, (1-false_negative_rate)] if not (isinstance(metric, float) and metric != metric)]
    final_score = sum(valid_scores) / len(valid_scores)

    return {
        "false_positive_rate": false_positive_rate,
        "false_negative_rate": false_negative_rate,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "silhouette_score": sil_score,
        "adjusted_rand_index": ari,
        "normalized_mutual_information": nmi,
        "final_score": final_score
    }


import uuid
def create_dummy_data():
    uuids = [str(uuid.uuid4()) for _ in range(10)]
    
    # predicted labels: 3 clusters and 1 outlier
    predicted_labels = [0, 0, 0, 1, 1, 2, 2, 2, -1, 1]
    
    # expected labels: 2 clusters and 2 outliers
    expected_labels = [3, 3, 3, 2, 2, 2, 2, -1, -1, 3]

    expected_labels = predicted_labels

    expected_labels = [random.randint(0, 5) for _ in range(10)]
    
    return uuids, predicted_labels, expected_labels


