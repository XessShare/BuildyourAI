"use client";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    question: "What does 'self-hosted' mean?",
    answer: "Self-hosted means you can run HexaHub on your own infrastructure - your own servers, your cloud account, or even your local machine. Your code and data never leave your control. You maintain complete ownership and privacy.",
  },
  {
    question: "Can I use my own API keys?",
    answer: "Yes! HexaHub supports bring-your-own-keys (BYOK) for OpenAI, Anthropic, Google, and other providers. You can also run local models like Ollama, LLaMA, or Mistral for complete offline operation.",
  },
  {
    question: "How does HexaHub compare to Cursor or GitHub Copilot?",
    answer: "Unlike Cursor and Copilot, HexaHub is open-source and can be self-hosted. This means your code never leaves your infrastructure, you're not locked into any vendor, and you can customize it to your needs. Plus, it's free for self-hosted use.",
  },
  {
    question: "Is HexaHub really free?",
    answer: "Yes, the self-hosted version is completely free and always will be. We offer a paid Cloud Pro tier for teams who want managed hosting and premium support, but the core product is free and open-source.",
  },
  {
    question: "What AI models are supported?",
    answer: "HexaHub works with any OpenAI-compatible API, including GPT-4, Claude, Gemini, and local models via Ollama or LM Studio. You can switch between models at any time or use different models for different tasks.",
  },
  {
    question: "How do I get started?",
    answer: "You can get started in minutes. For self-hosted deployment, use our Docker image or follow our installation guide. For Cloud Pro, simply sign up and you're ready to go. We also offer a free demo to explore features.",
  },
];

export function FAQ() {
  return (
    <section className="py-20 sm:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Frequently asked{" "}
            <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
              questions
            </span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Everything you need to know about HexaHub.
          </p>
        </div>

        <div className="mx-auto max-w-3xl">
          <Accordion type="single" collapsible className="w-full">
            {faqs.map((faq, index) => (
              <AccordionItem key={index} value={`item-${index}`} className="border-border">
                <AccordionTrigger className="text-left hover:no-underline hover:text-primary">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
}
