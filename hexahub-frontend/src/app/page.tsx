import { Hero } from "@/components/Hero";
import { Features } from "@/components/Features";
import { Comparison } from "@/components/Comparison";
import { Pricing } from "@/components/Pricing";
import { Testimonials } from "@/components/Testimonials";
import { FAQ } from "@/components/FAQ";
import { Newsletter } from "@/components/Newsletter";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />
      <Features />
      <Comparison />
      <Pricing />
      <Testimonials />
      <FAQ />
      <Newsletter />
      <Footer />
    </main>
  );
}
