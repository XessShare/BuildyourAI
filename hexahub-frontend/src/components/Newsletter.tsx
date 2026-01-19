"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Mail } from "lucide-react";

export function Newsletter() {
  return (
    <section className="py-20 sm:py-32 bg-secondary/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/20 mb-6">
            <Mail className="h-8 w-8 text-primary" />
          </div>

          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Stay in the{" "}
            <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
              loop
            </span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Get updates on new features, releases, and tips for getting the most out of HexaHub.
          </p>

          <form className="mt-8 flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <Input
              type="email"
              placeholder="Enter your email"
              className="flex-1 bg-background border-border"
            />
            <Button type="submit" className="px-8">
              Subscribe
            </Button>
          </form>

          <p className="mt-4 text-xs text-muted-foreground">
            No spam, ever. Unsubscribe at any time.
          </p>
        </div>
      </div>
    </section>
  );
}
