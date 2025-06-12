import type { AppProps } from "next/app";
import { ThemeProvider } from "next-themes";
import "@/styles/globals.css"; // Ensure your global styles are imported

export default function MyApp({ Component, pageProps }: AppProps) {
    return (
        <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
        >
            <Component {...pageProps} />
        </ThemeProvider>
    );
}
