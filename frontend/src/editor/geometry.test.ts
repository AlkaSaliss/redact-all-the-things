import { describe, expect, it } from "vitest";
import { createManualRegion, moveRegion } from "./geometry";

describe("editor geometry", () => {
  it("keeps manual regions inside normalized page bounds", () => {
    const region = createManualRegion(1, 1.2, -0.4);

    expect(region.x).toBe(0.9);
    expect(region.y).toBe(0);
    expect(region.source).toBe("manual");
  });

  it("clamps moved regions to the visible page", () => {
    const region = createManualRegion(1, 0.5, 0.5);
    const moved = moveRegion(region, 2, 2);

    expect(moved.x + moved.width).toBeLessThanOrEqual(1);
    expect(moved.y + moved.height).toBeLessThanOrEqual(1);
  });
});
