"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Star, Github, Users, Clock } from "lucide-react";

const testimonials = [
  {
    quote: "Finally, an AI coding assistant that respects my privacy. Running HexaHub on my own server gives me complete peace of mind.",
    author: "Sarah Chen",
    role: "Senior Engineer at TechCorp",
    avatar: "SC",
  },
  {
    quote: "The self-hosted option was a game-changer for our team. We can now use AI assistance without worrying about data leaving our infrastructure.",
    author: "Marcus Johnson",
    role: "CTO at StartupXYZ",
    avatar: "MJ",
  },
  {
    quote: "Switching from Copilot to HexaHub was seamless. Better privacy, same productivity, and I love being able to use my own API keys.",
    author: "Elena Rodriguez",
    role: "Full Stack Developer",
    avatar: "ER",
  },
];

const metrics = [
  { icon: Github, value: "2.4k+", label: "GitHub Stars" },
  { icon: Users, value: "500+", label: "Beta Users" },
  { icon: Clock, value: "99.9%", label: "Uptime" },
];

export function Testimonials() {
  return (
    <section className="py-20 sm:py-32 bg-secondary/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Loved by{" "}
            <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
              developers
            </span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Join hundreds of developers who have made the switch to privacy-first AI.
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto mb-16">
          {testimonials.map((testimonial) => (
            <Card key={testimonial.author} className="bg-card/50 border-border">
              <CardContent className="pt-6">
                <div className="flex gap-1 mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 fill-yellow-500 text-yellow-500" />
                  ))}
                </div>
                <blockquote className="text-muted-foreground mb-6">
                  &ldquo;{testimonial.quote}&rdquo;
                </blockquote>
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/20 text-primary font-semibold text-sm">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <p className="font-semibold text-sm">{testimonial.author}</p>
                    <p className="text-xs text-muted-foreground">{testimonial.role}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Metrics Bar */}
        <div className="max-w-3xl mx-auto">
          <div className="grid grid-cols-3 gap-8 py-8 px-6 rounded-xl bg-card/50 border border-border">
            {metrics.map((metric) => (
              <div key={metric.label} className="text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <metric.icon className="h-5 w-5 text-primary" />
                  <span className="text-2xl sm:text-3xl font-bold">{metric.value}</span>
                </div>
                <p className="text-sm text-muted-foreground">{metric.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
