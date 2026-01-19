import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "HexaHub - Self-Hosted AI Workspace for Developers",
  description: "Open-source, privacy-first AI workspace. Deploy anywhere, own your data. The self-hosted alternative to Cursor and GitHub Copilot.",
  keywords: ["AI", "developer tools", "self-hosted", "open source", "code assistant", "privacy"],
  authors: [{ name: "HexaHub Team" }],
  openGraph: {
    title: "HexaHub - Self-Hosted AI Workspace",
    description: "Open-source, privacy-first AI workspace for developers.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen bg-background`}
      >
        {children}
      </body>
    </html>
  );
}
