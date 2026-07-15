import { describe, expect, it } from "vitest";
import type { RedactionRegion } from "../contracts/types";
import {
  HISTORY_LIMIT,
  commitHistory,
  createHistory,
  redoHistory,
  undoHistory,
} from "./history";

function regions(id: string): RedactionRegion[] {
  return [
    {
      id,
      page_number: 1,
      x: 0,
      y: 0,
      width: 0.1,
      height: 0.1,
      source: "manual",
      category: "manual",
      confidence: null,
      selected: true,
    },
  ];
}

describe("page edit history", () => {
  it("undoes and redoes one committed gesture", () => {
    const edited = commitHistory(createHistory(regions("one")), regions("two"));

    expect(undoHistory(edited).present[0].id).toBe("one");
    expect(redoHistory(undoHistory(edited)).present[0].id).toBe("two");
  });

  it("bounds retained snapshots", () => {
    let history = createHistory(regions("initial"));
    for (let index = 0; index < HISTORY_LIMIT + 5; index += 1) {
      history = commitHistory(history, regions(String(index)));
    }

    expect(history.past).toHaveLength(HISTORY_LIMIT);
  });
});
