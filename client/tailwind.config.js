/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './src/pages/**/*.{js,ts,jsx,tsx}',
        './src/components/**/*.{js,ts,jsx,tsx}',
    ],
    // tailwind.config.ts
    // tailwind.config.js
    darkMode: 'class', // Enable dark mode support
    theme: {
        extend: {
            colors: {
                background: 'hls(var(--background))',  // ✅ use rgb() not hsl()
                foreground: 'hls(var(--foreground))',
            },
        },
    },
    plugins: [],
};