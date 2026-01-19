"use client";

import { Check, X, Minus } from "lucide-react";

const features = [
  { name: "Self-Hosted Option", hexahub: true, cursor: false, copilot: false },
  { name: "Open Source", hexahub: true, cursor: false, copilot: false },
  { name: "Data Privacy", hexahub: "Full Control", cursor: "Cloud Only", copilot: "Cloud Only" },
  { name: "Bring Your Own Keys", hexahub: true, cursor: "partial", copilot: false },
  { name: "Team Workspaces", hexahub: true, cursor: true, copilot: true },
  { name: "Local AI Models", hexahub: true, cursor: false, copilot: false },
  { name: "Plugin System", hexahub: true, cursor: "partial", copilot: true },
  { name: "Pricing", hexahub: "Free Self-Hosted", cursor: "$20/mo", copilot: "$19/mo" },
];

function FeatureValue({ value }: { value: boolean | string }) {
  if (value === true) {
    return (
      <div className="flex justify-center">
        <Check className="h-5 w-5 text-green-500" />
      </div>
    );
  }
  if (value === false) {
    return (
      <div className="flex justify-center">
        <X className="h-5 w-5 text-red-500" />
      </div>
    );
  }
  if (value === "partial") {
    return (
      <div className="flex justify-center">
        <Minus className="h-5 w-5 text-yellow-500" />
      </div>
    );
  }
  return <span className="text-sm text-muted-foreground">{value}</span>;
}

export function Comparison() {
  return (
    <section className="py-20 sm:py-32 bg-secondary/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            How HexaHub{" "}
            <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
              compares
            </span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            See why developers are choosing HexaHub over traditional AI coding assistants.
          </p>
        </div>

        <div className="mx-auto max-w-4xl overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b border-border">
                <th className="py-4 px-4 text-left text-sm font-semibold">Feature</th>
                <th className="py-4 px-4 text-center text-sm font-semibold">
                  <span className="text-primary">HexaHub</span>
                </th>
                <th className="py-4 px-4 text-center text-sm font-semibold text-muted-foreground">
                  Cursor
                </th>
                <th className="py-4 px-4 text-center text-sm font-semibold text-muted-foreground">
                  GitHub Copilot
                </th>
              </tr>
            </thead>
            <tbody>
              {features.map((feature, index) => (
                <tr
                  key={feature.name}
                  className={`border-b border-border/50 ${index % 2 === 0 ? 'bg-secondary/20' : ''}`}
                >
                  <td className="py-4 px-4 text-sm font-medium">{feature.name}</td>
                  <td className="py-4 px-4 text-center bg-primary/5">
                    <FeatureValue value={feature.hexahub} />
                  </td>
                  <td className="py-4 px-4 text-center">
                    <FeatureValue value={feature.cursor} />
                  </td>
                  <td className="py-4 px-4 text-center">
                    <FeatureValue value={feature.copilot} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
