"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send, Loader2, Sparkles } from "lucide-react";
import ModeToggle from "@/components/ModeToggle";
import MovieCard from "@/components/MovieCard";
import { EndpointResult } from "@/lib/types";
import { TypographyH1, TypographyMuted } from "@/components/ui/typography";
import { LLMEndpoint, MLEndpoint, TestAPI } from "@/lib/functions";

export default function Home() {
  const [summary, setSummary] = useState("");
  const [apiStatus, setApiStatus] = useState();
  const [isLLM, setIsLLM] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<EndpointResult[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [keywords, setKeywords] = useState([]);

  const handleSubmit = async () => {
    if (!summary.trim()) return;

    setIsLoading(true);
    setHasSearched(true);

    if (isLLM) {
      const result = await LLMEndpoint(summary);
      setRecommendations(result?.recommendations ?? []);
      setIsLoading(false);
    }

    if (!isLLM) {
      const result = await MLEndpoint(summary);
      setRecommendations(result?.movies ?? []);
      setIsLoading(false);
      setKeywords(result?.keywords ?? []);
      return;
    }
  };

  useEffect(() => {
    async function testStatus() {
      const status = await TestAPI();

      setApiStatus(status);
    }

    testStatus();
  }, []);

  /*
    Test queries:
      1. I want a crime movie directed by Tarantino
      2. I am looking for a visually spectacular sci-fi noir set in a dying, dystopian future where the line between artificial intelligence and humanity is blurred.
      3. Tarantino
      4. I want a period drama movie with a touch of romance with the actor Tom Hanks.
      5. I want to see a tradgic romance period movie about a young couple falling in love on a boat that then crashes into an iceberg. The boy is poor and the girl is rich
  */

  return (
    <>
      <div className="flex flex-col items-center w-full min-h-screen gradient-hero">
        <p className="mt-4">
          Api status:{" "}
          <span className="text-primary font-bold">
            {apiStatus ? "Online" : "Offline"}
          </span>
        </p>
        <div className="container flex flex-col items-center justify-center max-w-3xl gap-8 px-4 py-12 md:py-20 flex-2">
          {/* Header */}
          <header className="flex flex-col items-center gap-6 text-center">
            <div className="inline-flex items-center justify-center">
              <div className="flex items-center justify-center ">
                <TypographyH1>
                  Movie{" "}
                  <span className="text-background animate-pulse-glow bg-primary px-1.5 rounded-sm">
                    hub
                  </span>
                </TypographyH1>
              </div>
            </div>
            <p className="max-w-md text-lg text-muted-foreground">
              Your movie <span className="text-primary"> recommender,</span>{" "}
              describe the kind of movie you're in the mood for, and we'll find
              the perfect match.
            </p>
          </header>

          {/* Main Input Section */}
          <main className="space-y-6">
            <div className="p-6 border gradient-card rounded-2xl border-border md:p-8">
              <Textarea
                placeholder="I'm looking for a mind-bending sci-fi thriller with deep philosophical themes, unexpected plot twists, and stunning visuals..."
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                className="max-w-2xl text-base min-h-40 bg-background/50 w-2xl"
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
                    Finding movies...
                    <Loader2 className="w-5 h-5 animate-spin" />
                  </>
                ) : (
                  <>
                    Get Recommendations
                    <Send className="w-5 h-5" />
                  </>
                )}
              </Button>
            </div>

            <p className="text-sm text-center text-muted-foreground">
              Toggle between traditional ML and modern LLM recommendations
            </p>

            {/* Results Section */}
            {hasSearched && !isLoading && (
              <section className="space-y-4">
                <div className="flex justify-between w-full">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Sparkles className="w-4 h-4 text-primary" />
                    <span className="text-sm">
                      Found {recommendations.length} movies using{" "}
                      <span className="font-medium text-primary">
                        {isLLM ? "LLM" : "our ML Model"}
                      </span>
                    </span>
                  </div>
                  <div className="text-muted-foreground">
                    <TypographyMuted>
                      {keywords.length > 2
                        ? `Used keywords: ${keywords[0]}, ${keywords[1]}, ...`
                        : `Used full input`}
                    </TypographyMuted>
                  </div>
                </div>
                <div className="grid gap-3">
                  {recommendations.map((movie, index) => (
                    <MovieCard
                      key={movie.Series_Title}
                      movie={movie}
                      index={index}
                    />
                  ))}
                </div>
              </section>
            )}
          </main>
        </div>
      </div>
    </>
  );
}
