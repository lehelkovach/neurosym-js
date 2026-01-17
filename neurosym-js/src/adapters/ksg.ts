import { NeuroJSONProgram } from '../types';

export interface KsgAdapter {
  upsertProgram: (program: NeuroJSONProgram) => Promise<string>;
  writePosteriors: (
    programRef: string,
    posteriors: Record<string, number>,
    runMeta?: Record<string, unknown>
  ) => Promise<void>;
}
