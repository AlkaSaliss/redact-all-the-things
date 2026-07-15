import type { RedactionRegion } from "../contracts/types";
import type { CSSProperties } from "react";

export type Point = { x: number; y: number };
export type ResizeHandle = "nw" | "ne" | "sw" | "se";

const MIN_REGION_SIZE = 0.01;

function clamp(value: number, minimum: number, maximum: number): number {
  return Math.min(Math.max(value, minimum), maximum);
}

function rounded(value: number): number {
  return Math.round(value * 1_000_000) / 1_000_000;
}

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
  width = 0.1,
  height = 0.06,
): RedactionRegion {
  const boundedWidth = clamp(width, MIN_REGION_SIZE, 1);
  const boundedHeight = clamp(height, MIN_REGION_SIZE, 1);
  return {
    id: `manual-${pageNumber}-${Date.now()}`,
    page_number: pageNumber,
    x: rounded(clamp(x, 0, 1 - boundedWidth)),
    y: rounded(clamp(y, 0, 1 - boundedHeight)),
    width: rounded(boundedWidth),
    height: rounded(boundedHeight),
    source: "manual",
    category: "manual",
    confidence: null,
    selected: true,
  };
}

export function regionFromPoints(
  pageNumber: number,
  start: Point,
  end: Point,
): RedactionRegion {
  const left = clamp(Math.min(start.x, end.x), 0, 1);
  const top = clamp(Math.min(start.y, end.y), 0, 1);
  const right = clamp(Math.max(start.x, end.x), 0, 1);
  const bottom = clamp(Math.max(start.y, end.y), 0, 1);
  return createManualRegion(
    pageNumber,
    left,
    top,
    Math.max(right - left, MIN_REGION_SIZE),
    Math.max(bottom - top, MIN_REGION_SIZE),
  );
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

export function resizeRegion(
  region: RedactionRegion,
  handle: ResizeHandle,
  dx: number,
  dy: number,
): RedactionRegion {
  let left = region.x;
  let top = region.y;
  let right = region.x + region.width;
  let bottom = region.y + region.height;

  if (handle.includes("w")) left = clamp(left + dx, 0, right - MIN_REGION_SIZE);
  if (handle.includes("e")) right = clamp(right + dx, left + MIN_REGION_SIZE, 1);
  if (handle.includes("n")) top = clamp(top + dy, 0, bottom - MIN_REGION_SIZE);
  if (handle.includes("s")) bottom = clamp(bottom + dy, top + MIN_REGION_SIZE, 1);

  return {
    ...region,
    x: rounded(left),
    y: rounded(top),
    width: rounded(right - left),
    height: rounded(bottom - top),
  };
}
