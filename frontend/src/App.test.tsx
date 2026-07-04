import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { App } from "./App";

describe("App", () => {
  it("shows the signed-out Cognito shell", async () => {
    render(<App />);

    await waitFor(() =>
      expect(screen.getByText("Continue with Cognito")).toBeInTheDocument(),
    );
    expect(screen.getByText("Invited users only")).toBeInTheDocument();
  });
});
