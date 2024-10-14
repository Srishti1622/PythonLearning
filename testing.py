import numpy as np

# Helper function to calculate DCG
def dcg_at_k(relevance_scores, k):
    relevance_scores = np.array(relevance_scores)[:k]
    if relevance_scores.size:
        return np.sum(relevance_scores / np.log2(np.arange(2, relevance_scores.size + 2)))
    return 0.

# Helper function to calculate IDCG
def idcg_at_k(relevance_scores, k):
    ideal_relevance_scores = sorted(relevance_scores, reverse=True)
    return dcg_at_k(ideal_relevance_scores, k)

# Function to calculate Precision@K
def precision_at_k(retrieved, relevant, k):
    retrieved_k = retrieved[:k]
    relevant_set = set(relevant)
    retrieved_relevant = len([table for table in retrieved_k if table in relevant_set])
    return retrieved_relevant / k

# Function to calculate Recall@K
def recall_at_k(retrieved, relevant, k):
    retrieved_k = retrieved[:k]
    relevant_set = set(relevant)
    retrieved_relevant = len([table for table in retrieved_k if table in relevant_set])
    return retrieved_relevant / len(relevant)

# Function to calculate F1 Score
def f1_score(precision, recall):
    if precision + recall == 0:
        return 0
    return 2 * (precision * recall) / (precision + recall)

# Function to calculate Mean Reciprocal Rank (MRR)
def mrr(retrieved, relevant):
    relevant_set = set(relevant)
    for i, table in enumerate(retrieved):
        if table in relevant_set:
            return 1 / (i + 1)
    return 0

# Function to calculate NDCG@K
def ndcg_at_k(retrieved, relevant, k):
    # Relevance scores: 1 for relevant, 0 for non-relevant
    relevance_scores = [1 if table in relevant else 0 for table in retrieved]
    dcg_k = dcg_at_k(relevance_scores, k)
    idcg_k = idcg_at_k(relevance_scores, k)
    if idcg_k == 0:
        return 0
    return dcg_k / idcg_k

# Main function to evaluate the retrieval system
def evaluate_retrieval_system(retrieved_tables, ground_truth_tables, k=3, f1_threshold=0.5):
    assert len(retrieved_tables) == len(ground_truth_tables), "Mismatch between queries and ground truths."
    results = []

    for retrieved, relevant in zip(retrieved_tables, ground_truth_tables):
        precision = precision_at_k(retrieved, relevant, k)
        recall = recall_at_k(retrieved, relevant, k)
        f1 = f1_score(precision, recall)
        mrr_score = mrr(retrieved, relevant)
        ndcg_score = ndcg_at_k(retrieved, relevant, k)

        # Determine if the result is "Good" or "Bad"
        quality = "Good" if f1 >= f1_threshold else "Bad"

        # Store the results for each question
        results.append({
            'Retrieved': retrieved,
            'Relevant': relevant,
            'Precision@{}:'.format(k): precision,
            'Recall@{}:'.format(k): recall,
            'F1@{}:'.format(k): f1,
            'MRR': mrr_score,
            'NDCG@{}:'.format(k): ndcg_score,
            'Quality': quality
        })

    return results

# Example usage:

retrieved_tables = [
    ['table1', 'table2', 'table3'],  # Retrieved for query 1
    ['table2', 'table4', 'table5'],  # Retrieved for query 2
    ['table3', 'table1', 'table6']   # Retrieved for query 3
]

ground_truth_tables = [
    ['table1', 'table3'],            # Relevant tables for query 1
    ['table2', 'table5'],            # Relevant tables for query 2
    ['table6', 'table3']             # Relevant tables for query 3
]

# Evaluate the retrieval system
results = evaluate_retrieval_system(retrieved_tables, ground_truth_tables, k=3, f1_threshold=0.5)

# Print the detailed results for each question
for idx, result in enumerate(results, start=1):
    print(f"Query {idx} Results:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    print()  # Newline for better separation
