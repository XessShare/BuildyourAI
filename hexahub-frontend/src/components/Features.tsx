"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Server,
  Lock,
  Shield,
  Command,
  Users,
  Puzzle
} from "lucide-react";

const features = [
  {
    icon: Server,
    title: "Deploy Anywhere",
    description: "Run on your own infrastructure - cloud, on-premise, or local. Full control over your AI deployment.",
  },
  {
    icon: Lock,
    title: "No Vendor Lock-In",
    description: "Bring your own API keys. Switch between OpenAI, Anthropic, or local models like Ollama anytime.",
  },
  {
    icon: Shield,
    title: "Privacy-First",
    description: "Your code never leaves your infrastructure. Complete data sovereignty and compliance ready.",
  },
  {
    icon: Command,
    title: "Cmd+K Everything",
    description: "Lightning-fast command palette for AI chat, code generation, refactoring, and documentation.",
  },
  {
    icon: Users,
    title: "Team Workspaces",
    description: "Shared prompts, templates, and knowledge bases. Collaborate with your team in real-time.",
  },
  {
    icon: Puzzle,
    title: "Plugin Marketplace",
    description: "Extend functionality with community plugins. Build and share your own integrations.",
  },
];

export function Features() {
  return (
    <section className="py-20 sm:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Everything you need to{" "}
            <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
              build with AI
            </span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            A complete developer workspace with AI at its core. No compromises on privacy or control.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => (
            <Card
              key={feature.title}
              className="bg-card/50 border-border hover:border-primary/50 transition-colors duration-300"
            >
              <CardHeader>
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                    <feature.icon className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base text-muted-foreground">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
