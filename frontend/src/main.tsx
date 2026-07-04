import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { canonicalLocalUrl } from "./local-origin";
import "./styles.css";

const canonicalUrl = canonicalLocalUrl(window.location);
if (canonicalUrl) {
  window.location.replace(canonicalUrl);
} else {
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
}
