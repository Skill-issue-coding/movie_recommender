"use client";

import { EndpointResult } from "@/lib/types";
import { ChartColumnIncreasing, Film, Star } from "lucide-react";
import { TypographyMuted } from "./ui/typography";
import { useState } from "react";

const MovieCard = ({ movie, index }: { movie: EndpointResult; index: number }) => {
  const [imageFailed, setImageFailed] = useState(false);

  const hasLink = !!movie.Poster_Link;

  const displayElement =
    imageFailed || !hasLink ? (
      <Film className="h-7 w-7" />
    ) : (
      <img
        src={movie.Poster_Link}
        className="rounded-sm object-cover w-full h-full"
        alt={`Poster for ${movie.Series_Title}`}
        onError={() => setImageFailed(true)}
      />
    );
  return (
    <div
      className="gradient-card rounded-xl border border-border px-5 py-7 hover:border-primary/50 transition-all duration-300 hover:glow-primary animate-slide-up"
      style={{ animationDelay: `${index * 100}ms` }}>
      <div className="flex items-start gap-4">
        <div className="flex h-14 w-14 items-center justify-center rounded-lg bg-primary/10 text-primary">
          {displayElement}
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-display font-semibold text-lg text-foreground truncate">
            {movie.Series_Title}
          </h3>
          <p className="text-muted-foreground text-sm mt-1">
            {movie.Released_Year} • {movie.Genre}
          </p>
        </div>

        {movie.IMDB_Rating !== 0 && (
          <div className="flex flex-col gap-2 items-center">
            <div
              className={`flex items-center gap-1 ${
                movie.IMDB_Rating < 4
                  ? "bg-destructive/10"
                  : movie.IMDB_Rating < 7
                  ? "bg-chart-5/10"
                  : movie.IMDB_Rating < 8.5
                  ? "bg-chart-3/10"
                  : "bg-chart-2/10"
              } px-3 py-1.5 rounded-full`}>
              <Star
                className={`${
                  movie.IMDB_Rating < 4
                    ? "text-destructive"
                    : movie.IMDB_Rating < 7
                    ? "text-chart-5"
                    : movie.IMDB_Rating < 8.5
                    ? "text-chart-3"
                    : "text-chart-2"
                } h-4
            w-4`}
              />
              <span
                className={`text-sm font-medium ${
                  movie.IMDB_Rating < 4
                    ? "text-destructive"
                    : movie.IMDB_Rating < 7
                    ? "text-chart-5"
                    : movie.IMDB_Rating < 8.5
                    ? "text-chart-3"
                    : "text-chart-2"
                }`}>
                {movie.IMDB_Rating}
              </span>
            </div>
            <TypographyMuted>IMDB</TypographyMuted>
          </div>
        )}

        {movie.Meta_score && (
          <div className="flex flex-col gap-2 items-center">
            <div
              className={`flex items-center gap-1 ${
                movie.Meta_score < 39
                  ? "bg-destructive/10"
                  : movie.Meta_score < 40
                  ? "bg-chart-5/10"
                  : movie.Meta_score < 80
                  ? "bg-chart-3/10"
                  : "bg-chart-2/10"
              } px-3 py-1.5 rounded-full`}>
              <ChartColumnIncreasing
                className={`${
                  movie.Meta_score < 39
                    ? "text-destructive"
                    : movie.Meta_score < 40
                    ? "text-chart-5"
                    : movie.Meta_score < 80
                    ? "text-chart-3"
                    : "text-chart-2"
                } h-4
            w-4`}
              />
              <span
                className={`text-sm font-medium ${
                  movie.Meta_score < 39
                    ? "text-destructive"
                    : movie.Meta_score < 40
                    ? "text-chart-5"
                    : movie.Meta_score < 80
                    ? "text-chart-3"
                    : "text-chart-2"
                }`}>
                {movie.Meta_score}
              </span>
            </div>
            <TypographyMuted>Metascore</TypographyMuted>
          </div>
        )}
      </div>
    </div>
  );
};

export default MovieCard;
