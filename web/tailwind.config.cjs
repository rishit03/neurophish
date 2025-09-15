/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class", // <-- important
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          900: "rgb(var(--bg-900) / <alpha-value>)",
          800: "rgb(var(--bg-800) / <alpha-value>)",
        }
      },
      borderColor: {
        subtle: "rgb(var(--border) / <alpha-value>)",
      }
    },
  },
  plugins: [],
};