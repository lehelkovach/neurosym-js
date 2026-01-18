from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def canonical_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def program_hash(program: Dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(program).encode("utf-8")).hexdigest()


@dataclass
class NeuroProgramArtifact:
    id: str
    version: str
    program: Dict[str, Any]
    created_at: datetime = field(default_factory=now_utc)
    created_by: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NeuroInferenceRun:
    id: str
    program_id: str
    posteriors: Dict[str, float]
    evidence: Dict[str, Any] = field(default_factory=dict)
    queries: List[str] = field(default_factory=list)
    samples_used: Optional[int] = None
    effective_sample_size: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    evidence_stats: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=now_utc)
    metadata: Dict[str, Any] = field(default_factory=dict)


class InMemoryNeuroStore:
    """Minimal in-memory store for NeuroJSON programs and inference runs."""

    def __init__(self) -> None:
        self.programs: Dict[str, NeuroProgramArtifact] = {}
        self.runs: Dict[str, NeuroInferenceRun] = {}

    def upsert_program(
        self,
        program: Dict[str, Any],
        created_by: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        version = str(program.get("version", "unknown"))
        program_id = program_hash(program)
        if program_id not in self.programs:
            self.programs[program_id] = NeuroProgramArtifact(
                id=program_id,
                version=version,
                program=program,
                created_by=created_by,
                metadata=metadata or {},
            )
        return program_id

    def write_posteriors(
        self,
        program_id: str,
        posteriors: Dict[str, float],
        run_meta: Optional[Dict[str, Any]] = None,
    ) -> str:
        if program_id not in self.programs:
            raise ValueError(f"Unknown program_id: {program_id}")

        run_meta = run_meta or {}
        run_id = hashlib.sha256(f"{program_id}:{len(self.runs)}".encode("utf-8")).hexdigest()

        evidence = run_meta.get("evidence", {})
        queries = run_meta.get("queries", [])
        warnings = run_meta.get("warnings", [])
        evidence_stats = run_meta.get("evidence_stats", run_meta.get("evidenceStats", {}))
        samples_used = run_meta.get("samples_used", run_meta.get("samplesUsed"))
        effective_sample_size = run_meta.get("effective_sample_size", run_meta.get("effectiveSampleSize"))

        reserved_keys = {
            "evidence",
            "queries",
            "warnings",
            "evidence_stats",
            "evidenceStats",
            "samples_used",
            "samplesUsed",
            "effective_sample_size",
            "effectiveSampleSize",
        }
        metadata = {k: v for k, v in run_meta.items() if k not in reserved_keys}

        self.runs[run_id] = NeuroInferenceRun(
            id=run_id,
            program_id=program_id,
            posteriors=posteriors,
            evidence=evidence,
            queries=queries,
            samples_used=samples_used,
            effective_sample_size=effective_sample_size,
            warnings=warnings,
            evidence_stats=evidence_stats,
            metadata=metadata,
        )
        return run_id

    def get_program(self, program_id: str) -> Optional[NeuroProgramArtifact]:
        return self.programs.get(program_id)

    def list_runs(self, program_id: str) -> List[NeuroInferenceRun]:
        return [run for run in self.runs.values() if run.program_id == program_id]
