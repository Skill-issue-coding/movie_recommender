"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Clapperboard, Send, Loader2, Sparkles } from "lucide-react";
import ModeToggle from "@/components/ModeToggle";
import MovieCard from "@/components/MovieCard";

interface Movie {
  title: string;
  year: number;
  genre: string;
  matchScore: number;
}

const mockMLMovies: Movie[] = [
  { title: "Inception", year: 2010, genre: "Sci-Fi", matchScore: 94 },
  { title: "The Matrix", year: 1999, genre: "Sci-Fi", matchScore: 91 },
  { title: "Interstellar", year: 2014, genre: "Sci-Fi", matchScore: 88 },
  { title: "Blade Runner 2049", year: 2017, genre: "Sci-Fi", matchScore: 85 },
];

const mockLLMMovies: Movie[] = [
  { title: "Arrival", year: 2016, genre: "Sci-Fi", matchScore: 96 },
  { title: "Ex Machina", year: 2014, genre: "Thriller", matchScore: 93 },
  { title: "Her", year: 2013, genre: "Romance", matchScore: 90 },
  { title: "Eternal Sunshine of the Spotless Mind", year: 2004, genre: "Drama", matchScore: 87 },
];

export default function Home() {
  const [summary, setSummary] = useState("");
  const [isLLM, setIsLLM] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<Movie[]>([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSubmit = async () => {
    if (!summary.trim()) return;

    setIsLoading(true);
    setHasSearched(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    setRecommendations(isLLM ? mockLLMMovies : mockMLMovies);
    setIsLoading(false);
  };
  return (
    <div className="min-h-screen gradient-hero">
      <div className="container max-w-3xl mx-auto px-4 py-12 md:py-20">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="inline-flex items-center justify-center gap-3 mb-6">
            <div className="p-3 rounded-2xl bg-primary/10 animate-pulse-glow">
              <Clapperboard className="h-8 w-8 text-primary" />
            </div>
          </div>
          <h1 className="font-display text-4xl md:text-5xl font-bold text-foreground mb-4">
            Movie <span className="text-primary">Recommender</span>
          </h1>
          <p className="text-muted-foreground text-lg max-w-md mx-auto">
            Describe the kind of movie you're in the mood for, and we'll find the perfect match.
          </p>
        </header>

        {/* Main Input Section */}
        <main className="space-y-6">
          <div className="gradient-card rounded-2xl border border-border p-6 md:p-8">
            <Textarea
              placeholder="I'm looking for a mind-bending sci-fi thriller with deep philosophical themes, unexpected plot twists, and stunning visuals..."
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              className="min-h-40 text-base bg-background/50"
            />

            <ModeToggle isLLM={isLLM} onToggle={setIsLLM} />

            <Button
              variant="glow"
              size="lg"
              className="w-full font-semibold"
              onClick={handleSubmit}
              disabled={isLoading || !summary.trim()}>
              {isLoading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Finding movies...
                </>
              ) : (
                <>
                  <Send className="h-5 w-5" />
                  Get Recommendations
                </>
              )}
            </Button>
          </div>

          {/* Results Section */}
          {hasSearched && !isLoading && (
            <section className="space-y-4">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Sparkles className="h-4 w-4 text-primary" />
                <span className="text-sm">
                  Found {recommendations.length} movies using{" "}
                  <span className="text-primary font-medium">{isLLM ? "LLM" : "ML Model"}</span>
                </span>
              </div>
              <div className="grid gap-3">
                {recommendations.map((movie, index) => (
                  <MovieCard
                    key={movie.title}
                    title={movie.title}
                    year={movie.year}
                    genre={movie.genre}
                    matchScore={movie.matchScore}
                    index={index}
                  />
                ))}
              </div>
            </section>
          )}
        </main>

        {/* Footer */}
        <footer className="text-center mt-16 text-muted-foreground text-sm">
          <p>Toggle between traditional ML and modern LLM recommendations</p>
        </footer>
      </div>
    </div>
  );
}
