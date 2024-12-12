import json
import spacy
from rouge_score import rouge_scorer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from json import *
import io 
import pandas as pd
from typing import List, Dict, Union
import nltk
from bert_score import score as bert_score
from decimal import Decimal
import os
from typing import Union, List, Dict
import spacy
import pandas as pd
from io import StringIO


nltk.download('punkt')
# Load spaCy model for SVO extraction
nlp = spacy.load("en_core_web_sm")


def compute_confidence(subject, verb, obj):
    confidence = 1.0
    if subject.dep_ in {"nsubj", "nsubjpass"}:
        confidence += 0.5
    if verb.pos_ == "VERB":
        confidence += 0.5
    if obj.dep_ in {"dobj", "attr", "pobj"}:
        confidence += 0.5
    if subject.dep_ not in {"nsubj", "nsubjpass"}:
        confidence -= 0.5
    if verb.pos_ != "VERB":
        confidence -= 0.5
    if obj.dep_ not in {"dobj", "attr", "pobj"}:
        confidence -= 0.5
    if subject.head == verb:
        confidence += 0.2
    if obj.head == verb:
        confidence += 0.2
    distance = abs(subject.i - verb.i) + abs(verb.i - obj.i)
    confidence -= (distance * 0.05)
    if subject.ent_type_:
        confidence += 0.1
    if obj.ent_type_:
        confidence += 0.1
    confidence = max(0.0, min(1.0, confidence / 2.5))
    return confidence

# Function to extract SVO relations
def extract_relations_and_svo_with_confidence_score(text,confidence_threshold=0.5):
    doc = nlp(text)
    relations_with_confidence = []

    for sent in doc.sents:
        subjects = []
        verbs = []
        objects = []
        preps = []
        adjectives = []
        compounds = []
        possessives = []
        appositives = []
        conjuncts = []
        aux_verbs = []
        adverbs = []

        for token in sent:
            if "subj" in token.dep_:
                subjects.append(token)
            if token.pos_ == "VERB":
                verbs.append(token)
            if "obj" in token.dep_ or "attr" in token.dep_:
                objects.append(token)
            if token.dep_ == "prep":
                preps.append(token)
            if token.dep_ == "amod":
                adjectives.append(token)
            if token.dep_ == "compound":
                compounds.append(token)
            if token.dep_ == "poss":
                possessives.append(token)
            if token.dep_ == "appos":
                appositives.append(token)
            if token.dep_ in {"cc", "conj"}:
                conjuncts.append(token)
            if token.dep_ == "aux":
                aux_verbs.append(token)
            if token.dep_ == "advmod":
                adverbs.append(token)

        # Filter and validate relations
        for verb in verbs:
            for subject in subjects:
                for obj in objects:
                    # Skip if subject, verb, and object are too similar
                    if subject.text == obj.text or subject.text == verb.text or verb.text == obj.text:
                        continue

                    confidence = compute_confidence(subject, verb, obj)
                    if confidence >= confidence_threshold:
                        relations_with_confidence.append({
                            "subject": subject.text,
                            "verb": verb.text,
                            "object": obj.text,
                            "confidence": confidence
                        })

        for prep in preps:
            pobj = [child for child in prep.children if child.dep_ == "pobj"]
            if pobj:
                if prep.head.text == pobj[0].text or prep.text == pobj[0].text:
                    continue
                
                confidence = compute_confidence(prep.head, prep, pobj[0])
                if confidence >= confidence_threshold:
                    relations_with_confidence.append({
                        "subject": prep.head.text,
                        "verb": prep.text,
                        "object": pobj[0].text,
                        "confidence": confidence
                    })

        for adj in adjectives:
            adj_mod = " ".join(
                [child.text for child in adj.head.children if child.dep_ in {"nummod", "compound"}]
            )
            if adj_mod:
                if adj.head.text == adj_mod or adj.text == adj_mod:
                    continue

                confidence = compute_confidence(adj.head, adj, nlp(adj_mod)[0])
                if confidence >= confidence_threshold:
                    relations_with_confidence.append({
                        "subject": adj.head.text,
                        "verb": adj.text,
                        "object": adj_mod,
                        "confidence": confidence
                    })
            else:
                if adj.head.text == adj.text:
                    continue
                
                confidence = compute_confidence(adj.head, adj, adj.head)
                if confidence >= confidence_threshold:
                    relations_with_confidence.append({
                        "subject": adj.head.text,
                        "verb": adj.text,
                        "object": adj.head.text,
                        "confidence": confidence
                    })

        for comp in compounds:
            if comp.head.pos_ == "NOUN":
                if comp.head.text == comp.text:
                    continue
                
                confidence = compute_confidence(comp.head, comp, comp.head)
                if confidence >= confidence_threshold:
                    relations_with_confidence.append({
                        "subject": comp.head.text,
                        "verb": comp.text,
                        "object": comp.head.text,
                        "confidence": confidence
                    })

        for poss in possessives:
            if poss.head.text == poss.text:
                continue
            
            confidence = compute_confidence(poss.head, poss, poss.head)
            if confidence >= confidence_threshold:
                relations_with_confidence.append({
                    "subject": poss.head.text,
                    "verb": "'s",
                    "object": poss.text,
                    "confidence": confidence
                })

        for appos in appositives:
            if appos.head.text == appos.text:
                continue
            
            confidence = compute_confidence(appos.head, appos, appos.head)
            if confidence >= confidence_threshold:
                relations_with_confidence.append({
                    "subject": appos.head.text,
                    "verb": ",",
                    "object": appos.text,
                    "confidence": confidence
                })

        for conj in conjuncts:
            if conj.dep_ == "conj" and conj.head.pos_ == "NOUN":
                if conj.head.text == conj.text:
                    continue
                
                confidence = compute_confidence(conj.head, conj, conj.head)
                if confidence >= confidence_threshold:
                    relations_with_confidence.append({
                        "subject": conj.head.text,
                        "verb": "and",
                        "object": conj.text,
                        "confidence": confidence
                    })

        for aux in aux_verbs:
            if aux.head.pos_ == "VERB":
                if aux.head.text == aux.text:
                    continue
                
                confidence = compute_confidence(aux.head, aux, aux.head)
                if confidence >= confidence_threshold:
                    relations_with_confidence.append({
                        "subject": aux.head.text,
                        "verb": aux.text,
                        "object": aux.head.text,
                        "confidence": confidence
                    })

        for adv in adverbs:
            if adv.head.text == adv.text:
                continue
            
            confidence = compute_confidence(adv.head, adv, adv.head)
            if confidence >= confidence_threshold:
                relations_with_confidence.append({
                    "subject": adv.head.text,
                    "verb": adv.text,
                    "object": adv.head.text,
                    "confidence": confidence
                })

    # Filter out relations without valid values and exclude unwanted verb types
    filtered_relations = [
        rel for rel in relations_with_confidence
        if all(rel.values()) and not (nlp(rel["verb"])[0].pos_ in {"AUX", "CCONJ", "DET", "PART", "SCONJ"})
    ]

    # Sort the filtered relations by confidence
    filtered_relations.sort(key=lambda x: x["confidence"], reverse=True)

    # st.write("=====================================")
    # st.write("Filtered Relations :",filtered_relations)
    # st.write("=====================================")
    # Return only the filtered relations as a list
    return filtered_relations

# Function to compute ROUGE scores
def compute_all_rouge_scores(predicted, reference):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, predicted)
    return scores

def compute_rouge_mean(rouge_scores):
    """
    Compute average ROUGE scores from a dictionary of precomputed ROUGE scores.

    Args:
        rouge_scores (dict): A dictionary containing 'rouge1', 'rouge2', and 'rougeL' score lists.

    Returns:
        dict: A dictionary with average ROUGE scores.
    """
    # Calculate average ROUGE-1
    avg_rouge1 = sum(rouge_scores['rouge1']) / len(rouge_scores['rouge1'])
    
    # Calculate average ROUGE-2
    avg_rouge2 = sum(rouge_scores['rouge2']) / len(rouge_scores['rouge2'])
    
    # Calculate average ROUGE-L
    avg_rougeL = sum(rouge_scores['rougeL']) / len(rouge_scores['rougeL'])

    return {
        'avg_rouge1': avg_rouge1,
        'avg_rouge2': avg_rouge2,
        'avg_rougeL': avg_rougeL
    }



# Define unwanted symbols to filter out
unwanted_symbols = {'.', ',', '(', ')', '{', '}', '[', ']', '%','$', ';', ':','&',' ','"','\"'}

# Function to filter out unwanted symbols from a set of tuples
def filter_unwanted_symbols(tuples_set):
    return {t for t in tuples_set if not any(sym in t for sym in unwanted_symbols)}

def calculate_exact_intersection_count(set1, set2):
    """
    Calculate the count of exact and partial matches between two sets.
    Partial matches are weighted as 1/3, 2/3, or 1 based on the number of matching components.
    """
    match_count = Decimal(0)
    matched_tups = set()

    # Sort sets for consistent order
    set1 = sorted(set1)
    set2 = sorted(set2)

    for tup2 in set2:
        subject2, verb2, object2 = tup2[:-1]  # Extract SVO components from set2

        for tup1 in set1:
            if tup1 in matched_tups:
                continue  # Skip already counted matches

            subject1, verb1, object1 = tup1[:-1]  # Extract SVO components from set1
            match_elements = sum([subject1 == subject2, verb1 == verb2, object1 == object2])

            if match_elements > 0:
                match_count += Decimal(match_elements) / Decimal(3)  # Use Decimal for precision
                matched_tups.add(tup1)  # Track matched tuple to avoid double counting
                break

    return float(match_count)

def calculate_exact_triple_intersection_count(set1, set2, set3):
    """
    Calculate the count of exact and partial matches in the intersection of three sets.
    Partial matches are weighted as 1/3, 2/3, or 1 based on the number of matching components.
    """
    match_count = Decimal(0)
    matched_tups = set()

    # Sort sets for consistent order
    set1 = sorted(set1)
    set2 = sorted(set2)
    set3 = sorted(set3)

    # Check if set2 and set3 are identical to avoid double-counting
    if set2 == set3:
        for tup2 in set2:
            subject2, verb2, object2 = tup2[:-1]  # Extract SVO components from set2

            for tup1 in set1:
                if tup1 in matched_tups:
                    continue  # Skip already counted matches

                subject1, verb1, object1 = tup1[:-1]  # Extract SVO components from set1
                match_elements = sum([subject1 == subject2, verb1 == verb2, object1 == object2])

                if match_elements > 0:
                    match_count += Decimal(match_elements) / Decimal(3)
                    matched_tups.add(tup1)
                    break

    else:
        # If set2 and set3 are not identical, perform the full calculation
        for tup3 in set3:
            subject3, verb3, object3 = tup3[:-1]  # Extract SVO components from set3

            for tup2 in set2:
                subject2, verb2, object2 = tup2[:-1]  # Extract SVO components from set2

                if (subject2, verb2, object2) == (subject3, verb3, object3):  # Exact match with set3
                    for tup1 in set1:
                        if tup1 in matched_tups:
                            continue  # Skip already counted matches

                        subject1, verb1, object1 = tup1[:-1]  # Extract SVO components from set1
                        match_elements = sum([subject1 == subject2, verb1 == verb2, object1 == object2])

                        if match_elements > 0:
                            match_count += Decimal(match_elements) / Decimal(3)
                            matched_tups.add(tup1)
                            break

    return float(match_count)
import numpy as np
import torch

def convert_to_serializable(obj):
    """
    Recursively converts non-serializable types (like float32, int32, and PyTorch tensors) to serializable types.
    """
    if isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, np.ndarray):
        # Convert numpy arrays to lists
        return obj.tolist()
    elif isinstance(obj, torch.Tensor):
        # Convert PyTorch tensors to lists
        return obj.tolist()
    elif isinstance(obj, dict):
        # Recursively convert dictionary values
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Recursively convert list elements
        return [convert_to_serializable(i) for i in obj]
    elif isinstance(obj, tuple):
        # Convert tuple elements
        return tuple(convert_to_serializable(i) for i in obj)
    else:
        # Return the object as is if it doesn't need conversion
        return obj

def save_json_to_string(data):
    """
    Converts the given data into a JSON serializable string.
    """
    try:
        serializable_data = convert_to_serializable(data)  # Convert any non-serializable data
        json_str = json.dumps(serializable_data, indent=4)
        return json_str
    except TypeError as e:
        print(f"Serialization error: {e}")
        raise

def calculate_hallucination_factors(pred_words, ref_words, inp_words, input_relations, ref_relations, model_relations):
    # Filter symbols and get tuple counts
    pred_tuples = filter_unwanted_symbols(set(model_relations))
    ref_tuples = filter_unwanted_symbols(set(ref_relations))
    inp_tuples = filter_unwanted_symbols(set(input_relations))
    
    # Set lengths for easy formula use
    len_I = len(inp_tuples)
    len_R = len(ref_tuples)
    len_G = len(pred_tuples)
    print("*****COMPUTE******\n")
    print("Input tuples: ",inp_tuples,"lenI: ",len_I)
    print("\nRef tuples: ",ref_tuples,"lenR: ",len_R)
    print("\npred tuples: ",pred_tuples,"lenG: ",len_G)

   

    # Calculate intersections
    I_intersect_R_count = calculate_exact_intersection_count(inp_tuples, ref_tuples)
    I_intersect_G_count = calculate_exact_intersection_count(inp_tuples, pred_tuples)
    R_intersect_G_count = calculate_exact_intersection_count(ref_tuples, pred_tuples)
    I_intersect_R_intersect_G_count = calculate_exact_triple_intersection_count(inp_tuples, ref_tuples, pred_tuples)
    
     # Precision, recall, F1
    precision = I_intersect_G_count / len_G if len_G > 0 else 0
    recall = R_intersect_G_count / len_R if len_R > 0 else 0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    # Hallucination metrics with capped values
    ef = (3 * I_intersect_R_intersect_G_count) / (len_I + len_R + len_G) if (len_I + len_R + len_G) > 0 else 0
    ph = (2 * R_intersect_G_count) / (len_R + len_G) if (len_R + len_G) > 0 else 0
    of = (2 * (I_intersect_G_count-I_intersect_R_intersect_G_count)) / (len_I + len_G) if (len_I + len_G) > 0 else 0

    nh_numerator = (len_G - (R_intersect_G_count + I_intersect_G_count - I_intersect_R_intersect_G_count))
    nh = abs(nh_numerator) / len_G if len_G > 0 else 0
    nh = abs(nh)
    
    #Lost Focus:
    # lf = I_intersect_R_count - I_intersect_R_intersect_G_count) / len_G
    
    lf_numerator = (I_intersect_R_count -  I_intersect_R_intersect_G_count)
    lf = lf_numerator / (len_G) if (len_G) > 0 else 0
    
    # lf_numerator = len_R - (I_intersect_R_count - I_intersect_R_intersect_G_count)
    # lf = lf_numerator / (len_R + len_G) if (len_R + len_G) > 0 else 0
    
    
    # LH=2 *(R-(I INTER R) -((R INTER G) - (I INTER R INTER G)))/ R+G 

    # lh_numerator =  len_I - I_intersect_G_count
    
    lh_numerator =  2*(len_R-(I_intersect_R_count)-((R_intersect_G_count)-(I_intersect_R_intersect_G_count)))
    
    lh = lh_numerator / (len_I + len_G) if (len_I + len_G) > 0 else 0

    # rhi = 2 + (ef * ph) - (of + nh + lf + lh)
    
    rhi = 1+( (ef *ph)/2) - ( (of + lh + lf + nh)/4 )

    result = {
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "ef": ef,
        "ph": ph,
        "of": of,
        "nh": nh,
        "lf": lf,
        "Lost Hallucination": lh,
        "rhi": rhi,
        "intersection_counts": {
            "I_intersect_R_count": I_intersect_R_count,
            "I_intersect_G_count": I_intersect_G_count,
            "R_intersect_G_count": R_intersect_G_count,
            "I_intersect_R_intersect_G_count": I_intersect_R_intersect_G_count,
            "lenI": len_I,
            "lenG": len_G,
            "lenR": len_R,
            "lh_numerator": lh_numerator,
            "nh_numerator":nh_numerator
        }
    }

    return convert_to_serializable(result)



def convert_svo_to_tuples(svo_relations):
    # Convert confidence to string to avoid type issues
    return [
        (rel['subject'], rel['verb'], rel['object'], str(rel['confidence'])) 
        for rel in svo_relations
    ]
from typing import List, Dict, Union
import nltk
from typing import Dict, List, Union
import nltk
from typing import Dict, List, Union
import json


import json
import os
from typing import Union, List, Dict

def save_as_json(data: List[Dict], output_file: str):
    """
    Saves the processed data to a JSON file.
    
    Args:
        data (List[Dict]): Processed data to be saved.
        output_file (str): The path of the output JSON file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {output_file}.")

from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict, Union


def process_text_and_compute_metrics(
    data: Union[Dict, List[Dict]],
    batch_mode=True,
    field_mapping: Dict = None,
    output_file: str = 'processed_data.json'
) -> List[Dict]:
    """
    Processes JSON data to extract relations, compute ROUGE scores, and hallucination metrics.
    Handles both single-entry and batch processing, and dynamically adapts to any number of models.
    Allows customization of field names (e.g., InputText, ReferenceSummary) via field_mapping.

    Args:
        data (Union[Dict, List[Dict]]): Input JSON data containing entries to process.
        batch_mode (bool): If True, processes multiple entries. If False, processes a single entry.
        field_mapping (Dict, optional): A dictionary mapping field names (e.g., "InputText" -> "inputTextField").
        output_file (str, optional): The output file name for saving the processed data as JSON.

    Returns:
        List[Dict]: Processed data with extracted relations and metrics.
    """
    if not field_mapping:
        field_mapping = {
            "input_text": "InputText",
            "reference_summary": "ReferenceSummary"
        }

    if isinstance(data, dict) and not batch_mode:
        data_items = [(0, data)]
    else:
        data_items = enumerate(data) if batch_mode else [(0, data)]

    processed_data = []

    for index, entry in data_items:
        try:
            input_text_field = field_mapping.get("input_text", "InputText")
            reference_summary_field = field_mapping.get("reference_summary", "ReferenceSummary")

            if input_text_field in entry and reference_summary_field in entry:
                input_text = convert_to_string(entry.get(input_text_field, ""))
                reference_summary = convert_to_string(entry.get(reference_summary_field, ""))

                entry["svo_relations_input"] = extract_relations_and_svo_with_confidence_score(input_text)
                entry["svo_relations_ref"] = extract_relations_and_svo_with_confidence_score(reference_summary)

                model_summaries = {
                    k: v for k, v in entry.items()
                    if k not in [input_text_field, reference_summary_field, "Index"] and
                    k not in field_mapping.values()
                }

                for model_name, summary in model_summaries.items():
                    if model_name in {input_text_field, reference_summary_field}:
                        continue

                    summary = convert_to_string(summary)
                    entry[f"svo_relations_{model_name}"] = extract_relations_and_svo_with_confidence_score(summary)

                    try:
                        pred_words = nltk.word_tokenize(summary)
                        ref_words = nltk.word_tokenize(reference_summary)
                        inp_words = nltk.word_tokenize(input_text)
                    except Exception as e:
                        print(f"Error during tokenization for model '{model_name}': {e}")
                        continue

                    rouge_scores = compute_all_rouge_scores(summary, reference_summary)
                    entry[f"{model_name}_rouge"] = rouge_scores

                    rouge_avg = compute_rouge_mean(rouge_scores)
                    entry[f"{model_name}_rouge_avg"] = rouge_avg

                    input_relations = convert_svo_to_tuples(entry["svo_relations_input"])
                    ref_relations = convert_svo_to_tuples(entry["svo_relations_ref"])
                    model_relations = convert_svo_to_tuples(entry[f"svo_relations_{model_name}"])

                    hallucination_metrics = calculate_hallucination_factors(
                        pred_words, ref_words, inp_words, input_relations, ref_relations, model_relations
                    )
                    entry[f"{model_name}_hallucination_metrics"] = hallucination_metrics

            # Remove unwanted fields from the entry
            entry.pop("svo_relations_input_hallucination_metrics", None)
            entry.pop("svo_relations_ref_hallucination_metrics", None)

            processed_data.append(entry)

        except KeyError as e:
            print(f"KeyError: {e} in entry with index: {index}. Skipping this entry.")
        except Exception as e:
            print(f"An error occurred while processing entry {index}: {e}. Skipping this entry.")

    save_as_json(processed_data, output_file)
    return processed_data

def convert_to_string(data):
    """
    Converts input data (list or dict) to a string representation.

    Args:
        data (any): The data to convert to string.

    Returns:
        str: The string representation of the data.
    """
    if isinstance(data, list):
        return " ".join([convert_to_string(item) for item in data])  # Recursively join lists
    elif isinstance(data, dict):
        # Convert the dictionary to a JSON string
        return json.dumps(data)
    elif isinstance(data, str):
        return data
    else:
        # Handle unexpected data types by converting them to string
        return str(data)
