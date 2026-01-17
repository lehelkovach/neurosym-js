import { assertValidProgram } from '../schema/validate';
import type { FactorMode, FactorOpV01, NeuroJSONProgram, ProgramIR } from '../types';
import { buildTopoOrder } from './topo';

const DEFAULT_PRIOR = 0.5;

const ensureArity = (op: FactorOpV01, inputs: string[], factorIndex: number): void => {
  if ((op === 'IF_THEN' || op === 'NOT') && inputs.length !== 1) {
    throw new Error(`Factor ${factorIndex} op ${op} requires exactly 1 input`);
  }
  if ((op === 'AND' || op === 'OR') && inputs.length < 1) {
    throw new Error(`Factor ${factorIndex} op ${op} requires at least 1 input`);
  }
};

export const compileProgram = (programInput: NeuroJSONProgram | unknown): ProgramIR => {
  const program = assertValidProgram(programInput);
  const variableEntries = Object.entries(program.variables);
  const variables = variableEntries.map(([name, variable]) => ({
    name,
    prior: typeof variable.prior === 'number' ? variable.prior : DEFAULT_PRIOR
  }));

  const indexByName: Record<string, number> = {};
  variables.forEach((variable, idx) => {
    indexByName[variable.name] = idx;
  });

  const warnings: string[] = [];
  const factorsByOutput: number[][] = Array.from({ length: variables.length }, () => []);
  const resolveIndex = (name: string, context: string): number => {
    const idx = indexByName[name];
    if (idx === undefined) {
      throw new Error(`${context} "${name}" is not a defined variable`);
    }
    return idx;
  };

  const factors = program.factors.map((factor, factorIndex) => {
    ensureArity(factor.op, factor.inputs, factorIndex);

    if (factor.weight < 0 || factor.weight > 1) {
      throw new Error(`Factor ${factorIndex} weight must be in [0,1]`);
    }

    const outputIndex = resolveIndex(factor.output, `Factor ${factorIndex} output`);
    const inputIndices = factor.inputs.map((name) =>
      resolveIndex(name, `Factor ${factorIndex} input`)
    );

    const compiledFactor = {
      id: factor.id,
      inputs: inputIndices,
      output: outputIndex,
      op: factor.op,
      weight: factor.weight,
      mode: (factor.mode ?? 'support') as FactorMode
    };

    const outputBucket = factorsByOutput[compiledFactor.output];
    if (!outputBucket) {
      throw new Error(`Factor ${factorIndex} output index is out of range`);
    }
    outputBucket.push(factorIndex);
    return compiledFactor;
  });

  const edges: Array<[number, number]> = [];
  factors.forEach((factor) => {
    factor.inputs.forEach((input) => {
      edges.push([input, factor.output]);
    });
  });

  const topo = buildTopoOrder(variables.length, edges);
  if (topo.hasCycle) {
    warnings.push(
      `Cycle detected among variables: ${topo.cyclicNodes
        .map((idx) => variables[idx]?.name)
        .filter(Boolean)
        .join(', ')}`
    );
  }

  if (program.evidence) {
    Object.keys(program.evidence).forEach((name) => {
      if (!(name in indexByName)) {
        warnings.push(`Unknown evidence variable "${name}"`);
      }
    });
  }

  if (program.queries) {
    program.queries.forEach((name) => {
      if (!(name in indexByName)) {
        warnings.push(`Unknown query variable "${name}"`);
      }
    });
  }

  return {
    version: program.version,
    variables,
    factors,
    topoOrder: topo.order,
    indexByName,
    factorsByOutput,
    warnings
  };
};
