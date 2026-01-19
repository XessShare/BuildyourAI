"use client";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Star, Github, ArrowRight, Play } from "lucide-react";

export function Hero() {
  return (
    <section className="relative overflow-hidden py-20 sm:py-32">
      {/* Background gradient */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-b from-blue-500/10 via-transparent to-transparent" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-blue-500/20 rounded-full blur-3xl opacity-20" />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl text-center">
          {/* Trust Badges */}
          <div className="mb-8 flex flex-wrap items-center justify-center gap-3">
            <Badge variant="secondary" className="gap-1.5 px-3 py-1.5 text-sm bg-secondary/80 hover:bg-secondary">
              <Github className="h-4 w-4" />
              Open Source
            </Badge>
            <Badge variant="secondary" className="gap-1.5 px-3 py-1.5 text-sm bg-secondary/80 hover:bg-secondary">
              <Star className="h-4 w-4 text-yellow-500" />
              2.4k Stars
            </Badge>
          </div>

          {/* Headline */}
          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
            Self-Hosted AI Workspace{" "}
            <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
              for Developers
            </span>
          </h1>

          {/* Subheadline */}
          <p className="mt-6 text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            The open-source, privacy-first alternative to Cursor and GitHub Copilot.
            Deploy anywhere, own your data, and build with AI on your terms.
          </p>

          {/* CTAs */}
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button size="lg" className="gap-2 text-base px-8 py-6 bg-primary hover:bg-primary/90">
              Start Free Beta
              <ArrowRight className="h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" className="gap-2 text-base px-8 py-6">
              <Play className="h-4 w-4" />
              View Demo
            </Button>
          </div>

          {/* Social Proof */}
          <p className="mt-8 text-sm text-muted-foreground">
            Trusted by 500+ developers in beta. No credit card required.
          </p>
        </div>

        {/* Hero Visual Placeholder */}
        <div className="mt-16 sm:mt-20">
          <div className="relative mx-auto max-w-5xl">
            <div className="rounded-xl border border-border bg-card/50 backdrop-blur-sm p-2">
              <div className="aspect-video rounded-lg bg-gradient-to-br from-secondary to-secondary/50 flex items-center justify-center">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/20 mb-4">
                    <Play className="h-8 w-8 text-primary" />
                  </div>
                  <p className="text-muted-foreground">Product Demo Video</p>
                </div>
              </div>
            </div>
            {/* Decorative blur */}
            <div className="absolute -inset-x-20 -bottom-20 h-40 bg-gradient-to-t from-background to-transparent" />
          </div>
        </div>
      </div>
    </section>
  );
}
