from analyse import evaluate, detection_limit, fp_near_truth, parse_report

TRUTH = {"A b": 50.0, "C d": 1.0, "E f": 0.01, "G h": 0.0}


def test_perfect_call():
    r = evaluate({"A b": 500, "C d": 100, "E f": 20}, TRUTH)
    assert r["precision"] == 1.0 and r["recall"] == 1.0 and r["f1"] == 1.0


def test_false_positive_and_missed_species():
    r = evaluate({"A b": 500, "G h": 50}, TRUTH)
    assert r["fp"] == ["G h"]
    assert set(r["fn"]) == {"C d", "E f"}
    assert abs(r["precision"] - 0.5) < 1e-9
    assert abs(r["recall"] - 1 / 3) < 1e-9


def test_min_reads_filters_noise():
    r = evaluate({"A b": 500, "G h": 3}, TRUTH, min_reads=10)
    assert r["fp"] == []


def test_detection_limit():
    r = evaluate({"A b": 500, "C d": 100}, TRUTH)
    assert detection_limit(r, TRUTH) == 1.0


def test_fp_near_truth_same_genus():
    truth = {"Escherichia coli": 50.0}
    assert fp_near_truth(["Escherichia albertii", "Vibrio cholerae"], truth) == {
        "Escherichia albertii": True, "Vibrio cholerae": False}


def test_parse_report():
    species, unclass = parse_report("tests/data/report_example_c0.0.txt")
    assert unclass == 2.0
    assert species == {"Escherichia coli": 5000, "Shigella flexneri": 120}
