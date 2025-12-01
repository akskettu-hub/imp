import os
import csv
from jiwer import wer, cer
from collections import Counter


def bow_wer(ref: str, hyp: str) -> float:
    ref_words = ref.split()
    hyp_words = hyp.split()

    ref_count = Counter(ref_words)
    hyp_count = Counter(hyp_words)

    diff_in_counts = 0
    all_words = set(ref_count.keys()) | set(hyp_count.keys())

    for w in all_words:
        diff_in_counts += abs(ref_count[w] - hyp_count[w])

    return diff_in_counts / (len(ref_words) + len(hyp_words))


def evaluate_cer_wer(ref: str, hyp: str) -> tuple[float, float, float]:
    cer_error_rate = cer(reference=ref, hypothesis=hyp)
    wer_error_rate = wer(reference=ref, hypothesis=hyp)
    wer_bow_error_rate = bow_wer(ref=ref, hyp=hyp)

    return (cer_error_rate, wer_error_rate, wer_bow_error_rate)


def evaluation_from_files(ref_path: str, hyp_path: str):
    with open(ref_path, "r", encoding="utf-8") as f:
        ref = f.read()

    with open(hyp_path, "r", encoding="utf-8") as f:
        hyp = f.read()

    res = evaluate_cer_wer(ref, hyp)
    return res


def find_eval_dirs(path):
    eval_dirs = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            eval_dirs.append(full_path)

    return eval_dirs


def process_eval_dir(gt_file: str, eval_files: list):
    res_dir = []
    for f in eval_files:
        res = evaluation_from_files(gt_file, f)
        print(f"{f}: {res}")
        res_dir.append((f, res))

    return res_dir


def process_eval_dirs():
    eval_dirs = find_eval_dirs("eval")
    results = []
    for d in eval_dirs:
        gt_file = ""
        eval_files = []
        for f in os.listdir(d):
            if f.endswith(".txt"):
                full_path = os.path.join(d, f)

                if f.endswith("gt.txt"):
                    gt_file = full_path

                else:
                    eval_files.append(full_path)

        res_for_dir = process_eval_dir(gt_file, eval_files)
        for r in res_for_dir:
            results.append(r)

    return results


def results_to_csv(results, csv_path):
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "CER", "WER", "WER-BOW"])

        for filename, (cer, wer, wer_bow) in results:
            writer.writerow([filename, cer, wer, wer_bow])


if __name__ == "__main__":
    results = process_eval_dirs()
    # results_to_csv(results, "results.csv")
