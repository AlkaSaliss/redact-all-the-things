import { describe, expect, it } from "vitest";
import {
  createManualRegion,
  moveRegion,
  regionFromPoints,
  resizeRegion,
} from "./geometry";

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

  it("creates a manual region from pointer-defined normalized bounds", () => {
    const region = regionFromPoints(2, { x: 0.8, y: 0.7 }, { x: 0.2, y: 0.1 });

    expect(region).toMatchObject({
      page_number: 2,
      x: 0.2,
      y: 0.1,
      width: 0.6,
      height: 0.6,
      source: "manual",
    });
  });

  it("resizes regions from a corner while clamping them to page bounds", () => {
    const region = createManualRegion(1, 0.8, 0.8, 0.15, 0.15);
    const resized = resizeRegion(region, "se", 0.5, 0.5);

    expect(resized.width).toBeCloseTo(0.2);
    expect(resized.height).toBeCloseTo(0.2);
    expect(resized.x + resized.width).toBe(1);
    expect(resized.y + resized.height).toBe(1);
  });
});
