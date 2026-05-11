/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        background: "#0a0a0f",
        card: "#12121a",
        accent: "#00d4ff",
      },
      fontFamily: {
        display: ["Outfit", "sans-serif"],
        mono: ["Space Mono", "monospace"],
      },
      boxShadow: {
        glow: "0 0 25px rgba(0, 212, 255, 0.35)",
      },
    },
  },
  plugins: [],
};
