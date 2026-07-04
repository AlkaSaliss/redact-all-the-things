import { describe, expect, it } from "vitest";
import { canonicalLocalUrl } from "./local-origin";

function testLocation(rawUrl: string): Location {
  return new URL(rawUrl) as unknown as Location;
}

describe("canonicalLocalUrl", () => {
  it("redirects loopback aliases to localhost", () => {
    expect(canonicalLocalUrl(testLocation("http://127.0.0.1:5173/jobs"))).toBe(
      "http://localhost:5173/jobs",
    );
    expect(canonicalLocalUrl(testLocation("http://0.0.0.0:5173/auth/callback?code=1"))).toBe(
      "http://localhost:5173/auth/callback?code=1",
    );
  });

  it("leaves registered and non-local origins alone", () => {
    expect(canonicalLocalUrl(testLocation("http://localhost:5173/"))).toBeNull();
    expect(canonicalLocalUrl(testLocation("https://dutz0azy8p0yt.cloudfront.net/"))).toBeNull();
  });
});
