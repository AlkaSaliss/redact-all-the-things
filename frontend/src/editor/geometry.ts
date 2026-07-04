import type { RedactionRegion } from "../contracts/types";
import type { CSSProperties } from "react";

export function regionStyle(region: RedactionRegion): CSSProperties {
  return {
    left: `${region.x * 100}%`,
    top: `${region.y * 100}%`,
    width: `${region.width * 100}%`,
    height: `${region.height * 100}%`,
  };
}

export function createManualRegion(
  pageNumber: number,
  x: number,
  y: number,
): RedactionRegion {
  return {
    id: `manual-${pageNumber}-${Date.now()}`,
    page_number: pageNumber,
    x: Math.min(Math.max(x, 0), 0.9),
    y: Math.min(Math.max(y, 0), 0.9),
    width: 0.1,
    height: 0.06,
    source: "manual",
    category: "manual",
    confidence: null,
    selected: true,
  };
}

export function moveRegion(
  region: RedactionRegion,
  dx: number,
  dy: number,
): RedactionRegion {
  return {
    ...region,
    x: Math.min(Math.max(region.x + dx, 0), 1 - region.width),
    y: Math.min(Math.max(region.y + dy, 0), 1 - region.height),
  };
}
