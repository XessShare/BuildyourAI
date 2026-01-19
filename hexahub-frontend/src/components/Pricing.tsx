"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Check } from "lucide-react";

const tiers = [
  {
    name: "Free Self-Hosted",
    price: "$0",
    period: "forever",
    description: "Perfect for individual developers and small teams.",
    features: [
      "Unlimited usage",
      "All core features",
      "Bring your own API keys",
      "Local AI model support",
      "Community support",
      "Self-hosted deployment",
    ],
    cta: "Get Started",
    popular: true,
  },
  {
    name: "Cloud Pro",
    price: "$49",
    period: "per month",
    description: "Managed hosting with premium features and support.",
    features: [
      "Everything in Free",
      "Managed cloud hosting",
      "Priority support",
      "Advanced analytics",
      "Team management",
      "SSO integration",
    ],
    cta: "Start Trial",
    popular: false,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "pricing",
    description: "For large organizations with custom requirements.",
    features: [
      "Everything in Pro",
      "Dedicated infrastructure",
      "Custom integrations",
      "SLA guarantee",
      "On-premise deployment",
      "24/7 premium support",
    ],
    cta: "Contact Sales",
    popular: false,
  },
];

export function Pricing() {
  return (
    <section className="py-20 sm:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Simple,{" "}
            <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
              transparent pricing
            </span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Start free with self-hosting. Scale to managed cloud when you need it.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {tiers.map((tier) => (
            <Card
              key={tier.name}
              className={`relative bg-card/50 border-border flex flex-col ${
                tier.popular ? 'border-primary ring-2 ring-primary/20' : ''
              }`}
            >
              {tier.popular && (
                <Badge className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground">
                  Most Popular
                </Badge>
              )}
              <CardHeader className="text-center pb-8 pt-6">
                <CardTitle className="text-xl">{tier.name}</CardTitle>
                <div className="mt-4">
                  <span className="text-4xl font-bold">{tier.price}</span>
                  <span className="text-muted-foreground ml-2">/{tier.period}</span>
                </div>
                <CardDescription className="mt-2">{tier.description}</CardDescription>
              </CardHeader>
              <CardContent className="flex-1">
                <ul className="space-y-3">
                  {tier.features.map((feature) => (
                    <li key={feature} className="flex items-center gap-3">
                      <Check className="h-5 w-5 text-primary flex-shrink-0" />
                      <span className="text-sm text-muted-foreground">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
              <CardFooter className="pt-6">
                <Button
                  className="w-full"
                  variant={tier.popular ? "default" : "outline"}
                >
                  {tier.cta}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
