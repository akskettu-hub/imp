def wer(ref: str, hyp: str) -> float:
    """
    Calculate Word Error Rate (WER) between reference and hypothesis strings.
    """
    r = ref.split()
    h = hyp.split()

    # Initialize the matrix
    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]

    # Fill borders
    for i in range(len(r) + 1):
        d[i][0] = i
    for j in range(len(h) + 1):
        d[0][j] = j

    # Populate matrix
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                cost = 0
            else:
                cost = 1

            d[i][j] = min(
                d[i - 1][j] + 1,  # deletion
                d[i][j - 1] + 1,  # insertion
                d[i - 1][j - 1] + cost,  # substitution
            )

    return d[len(r)][len(h)] / float(len(r))


def wer_from_files(ref_path: str, hyp_path: str) -> float:
    with open(ref_path, "r", encoding="utf-8") as f:
        ref = f.read()

    with open(hyp_path, "r", encoding="utf-8") as f:
        hyp = f.read()

    return wer(ref, hyp)


if __name__ == "__main__":
    # a = "This is a test. Trying to figure out how to get this to work."
    # b = "This is a test. Trying to eat some beans."
    # res = wer(ref=a, hyp=b)
    res = wer_from_files(
        ref_path="transcriptions/CLIFT_024.txt",
        hyp_path="transcriptions/clift_024_nop.txt",
    )
    print("No processing: ", 1 - res)

    res = wer_from_files(
        ref_path="transcriptions/CLIFT_024.txt",
        hyp_path="transcriptions/clift_024_grey.txt",
    )
    print("Greyscale: ", 1 - res)
