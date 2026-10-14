import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  // FastAPI serves the compiled bundle from /app/.
  base: "/app/",
});
