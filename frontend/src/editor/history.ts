import type { RedactionRegion } from "../contracts/types";

export const HISTORY_LIMIT = 50;

export interface PageHistory {
  past: RedactionRegion[][];
  present: RedactionRegion[];
  future: RedactionRegion[][];
}

export function createHistory(regions: RedactionRegion[]): PageHistory {
  return { past: [], present: regions, future: [] };
}

export function commitHistory(
  history: PageHistory,
  regions: RedactionRegion[],
): PageHistory {
  return {
    past: [...history.past, history.present].slice(-HISTORY_LIMIT),
    present: regions,
    future: [],
  };
}

export function undoHistory(history: PageHistory): PageHistory {
  const previous = history.past.at(-1);
  if (!previous) return history;
  return {
    past: history.past.slice(0, -1),
    present: previous,
    future: [history.present, ...history.future],
  };
}

export function redoHistory(history: PageHistory): PageHistory {
  const next = history.future[0];
  if (!next) return history;
  return {
    past: [...history.past, history.present].slice(-HISTORY_LIMIT),
    present: next,
    future: history.future.slice(1),
  };
}
