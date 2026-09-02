from app.services.competency_service import calculate_gap, get_priority_label

def test_gap_mathematics():
    gap = calculate_gap(required=80.0, current=45.0)
    assert gap == 35.0

    met_gap = calculate_gap(required=80.0, current=85.0)
    assert met_gap == 0.0

def test_priority_labeling():
    assert get_priority_label(35.0) == "High"
    assert get_priority_label(20.0) == "Medium"
    assert get_priority_label(5.0) == "Low"
    assert get_priority_label(0.0) == "Met"

def test_role_benchmark_resolution():
    from app.services.competency_service import resolve_role_benchmarks
    
    # Test National Accounts Division Director
    nad_meta = resolve_role_benchmarks("MoSPI National Accounts Division (NAD)", "Director (ISS)")
    assert nad_meta["division_code"] == "NAD"
    assert nad_meta["benchmarks"]["STAT_NAT_ACC"] == 96.0 # 90 base + 6 Director delta
    assert nad_meta["weights"]["STAT_NAT_ACC"] > 1.5 # weighted higher
    assert "STAT_NAT_ACC" in nad_meta["core_competencies"]

    # Test Field Operations Division Investigator
    fod_meta = resolve_role_benchmarks("MoSPI Field Operations Division (FOD)", "Statistical Investigator")
    assert fod_meta["division_code"] == "FOD"
    assert fod_meta["benchmarks"]["STAT_SURVEY"] == 90.0 # 92 base - 2 Investigator delta
    assert "STAT_SURVEY" in fod_meta["core_competencies"]
