import type {
  FactorContribution,
  InferenceOptions,
  InferenceSummary,
  ProgramIR,
  VariableExplanation
} from '../types';
import { activationFromInputs, applyInhibit, applySupport } from './logic';

const DEFAULT_ITERATIONS = 10000;

const mulberry32 = (seed: number): (() => number) => {
  let t = seed >>> 0;
  return () => {
    t += 0x6d2b79f5;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r ^= r + Math.imul(r ^ (r >>> 7), 61 | r);
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
};

const resolveValue = (value: number | undefined, prior: number): number => {
  if (typeof value === 'number') {
    return value;
  }
  return prior >= 0.5 ? 1 : 0;
};

const computeProbability = (
  varIndex: number,
  assignments: Array<number | undefined>,
  ir: ProgramIR
): { probability: number; activeFactors: number[] } => {
  const currentVariable = ir.variables[varIndex];
  if (!currentVariable) {
    return { probability: 0.5, activeFactors: [] };
  }
  let p = currentVariable.prior;
  const factorIndices = ir.factorsByOutput[varIndex] ?? [];
  const activeFactors: number[] = [];

  factorIndices.forEach((factorIndex) => {
    const factor = ir.factors[factorIndex];
    if (!factor) {
      return;
    }
    const inputValues = factor.inputs.map((inputIdx) =>
      resolveValue(assignments[inputIdx], ir.variables[inputIdx]?.prior ?? 0.5)
    );
    const activation = activationFromInputs(factor.op, inputValues);
    if (activation === 0) {
      return;
    }
    activeFactors.push(factorIndex);

    if (factor.mode === 'support') {
      p = applySupport(p, factor.weight);
    } else {
      p = applyInhibit(p, factor.weight);
    }
  });

  return { probability: p, activeFactors };
};

export const runSampler = (
  ir: ProgramIR,
  evidence: Record<string, 0 | 1> | undefined,
  options: InferenceOptions = {}
): InferenceSummary => {
  const iterations = options.iterations ?? DEFAULT_ITERATIONS;
  const rng = options.rng ?? mulberry32(options.seed ?? 1337);

  const variableCount = ir.variables.length;
  const factorCount = ir.factors.length;

  const evidenceIndices = new Map<number, 0 | 1>();
  const clamped: string[] = [];
  const ignored: string[] = [];
  if (evidence) {
    Object.entries(evidence).forEach(([name, value]) => {
      const idx = ir.indexByName[name];
      if (idx !== undefined) {
        evidenceIndices.set(idx, value);
        clamped.push(name);
      } else {
        ignored.push(name);
      }
    });
  }

  const posteriorSums = new Array<number>(variableCount).fill(0);
  const factorActivationCounts = new Array<number>(factorCount).fill(0);
  const factorContributionSums = new Array<number>(factorCount).fill(0);
  let weightSum = 0;
  let weightSquareSum = 0;

  const order = ir.topoOrder ?? [...Array(variableCount).keys()];

  for (let i = 0; i < iterations; i += 1) {
    const assignments: Array<number | undefined> = new Array(variableCount).fill(undefined);
    let sampleWeight = 1;

    order.forEach((varIndex) => {
      const { probability, activeFactors } = computeProbability(varIndex, assignments, ir);

      const evidenceValue = evidenceIndices.get(varIndex);
      if (evidenceValue !== undefined) {
        sampleWeight *= evidenceValue === 1 ? probability : 1 - probability;
        assignments[varIndex] = evidenceValue;
      } else {
        assignments[varIndex] = rng() < probability ? 1 : 0;
      }

      activeFactors.forEach((factorIndex) => {
        factorActivationCounts[factorIndex] = (factorActivationCounts[factorIndex] ?? 0) + 1;
        const factorWeight = ir.factors[factorIndex]?.weight ?? 0;
        factorContributionSums[factorIndex] =
          (factorContributionSums[factorIndex] ?? 0) + sampleWeight * factorWeight;
      });
    });

    weightSum += sampleWeight;
    weightSquareSum += sampleWeight * sampleWeight;

    for (let v = 0; v < variableCount; v += 1) {
      const value = assignments[v] ?? 0;
      posteriorSums[v] = (posteriorSums[v] ?? 0) + sampleWeight * value;
    }
  }

  const posteriors = ir.variables.reduce<Record<string, number>>((acc, variable, idx) => {
    const sum = posteriorSums[idx] ?? 0;
    const value = weightSum > 0 ? sum / weightSum : variable.prior;
    acc[variable.name] = value;
    return acc;
  }, {});

  const explanations = ir.variables.reduce<Record<string, VariableExplanation>>((acc, variable, idx) => {
    const factorIndices = ir.factorsByOutput[idx] ?? [];
    const supporting: FactorContribution[] = [];
    const inhibiting: FactorContribution[] = [];

    factorIndices.forEach((factorIndex) => {
      const factor = ir.factors[factorIndex];
      if (!factor) {
        return;
      }
      const activationCount = factorActivationCounts[factorIndex] ?? 0;
      if (activationCount === 0) {
        return;
      }
      const contributionSum = factorContributionSums[factorIndex] ?? 0;
      const contribution = weightSum > 0 ? contributionSum / weightSum : 0;
      const entry: FactorContribution = {
        factorIndex,
        factorId: factor.id,
        op: factor.op,
        mode: factor.mode,
        weight: factor.weight,
        activationCount,
        contribution
      };
      if (factor.mode === 'support') {
        supporting.push(entry);
      } else {
        inhibiting.push(entry);
      }
    });

    supporting.sort((a, b) => b.contribution - a.contribution);
    inhibiting.sort((a, b) => b.contribution - a.contribution);

    acc[variable.name] = {
      supportingFactors: supporting,
      inhibitingFactors: inhibiting
    };
    return acc;
  }, {});

  return {
    posteriors,
    samplesUsed: iterations,
    effectiveSampleSize:
      weightSum > 0 ? (weightSum * weightSum) / (weightSquareSum || 1) : 0,
    evidenceStats: { clamped, ignored: ignored.length > 0 ? ignored : undefined },
    explanations
  };
};
