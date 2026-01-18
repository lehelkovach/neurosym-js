from knowshowgo.neuro_artifacts import InMemoryNeuroStore


def sample_program() -> dict:
    return {
        "version": "0.1",
        "variables": {"rain": {"type": "boolean", "prior": 0.2}},
        "factors": [],
    }


def test_upsert_program_is_stable() -> None:
    store = InMemoryNeuroStore()
    program = sample_program()
    first_id = store.upsert_program(program)
    second_id = store.upsert_program(program)

    assert first_id == second_id
    assert store.get_program(first_id) is not None


def test_write_posteriors_requires_program() -> None:
    store = InMemoryNeuroStore()
    try:
        store.write_posteriors("missing", {"rain": 0.5})
    except ValueError as exc:
        assert "Unknown program_id" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing program_id")


def test_write_posteriors_stores_run_metadata() -> None:
    store = InMemoryNeuroStore()
    program_id = store.upsert_program(sample_program())

    run_id = store.write_posteriors(
        program_id,
        {"rain": 0.6},
        {
            "evidence": {"rain": 1},
            "queries": ["rain"],
            "warnings": ["ignored evidence"],
            "evidenceStats": {"clamped": ["rain"]},
            "samplesUsed": 100,
            "effectiveSampleSize": 90.0,
            "source": "test",
        },
    )

    runs = store.list_runs(program_id)
    assert len(runs) == 1
    run = runs[0]
    assert run.id == run_id
    assert run.posteriors["rain"] == 0.6
    assert run.warnings == ["ignored evidence"]
    assert run.evidence_stats["clamped"] == ["rain"]
    assert run.samples_used == 100
    assert run.effective_sample_size == 90.0
    assert run.metadata["source"] == "test"
