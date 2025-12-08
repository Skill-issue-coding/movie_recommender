import { Film, Star } from "lucide-react";

interface MovieCardProps {
  title: string;
  year: number;
  genre: string;
  matchScore: number;
  index: number;
}

const MovieCard = ({ title, year, genre, matchScore, index }: MovieCardProps) => {
  return (
    <div
      className="gradient-card rounded-xl border border-border p-5 hover:border-primary/50 transition-all duration-300 hover:glow-primary animate-slide-up"
      style={{ animationDelay: `${index * 100}ms` }}>
      <div className="flex items-start gap-4">
        <div className="flex h-14 w-14 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <Film className="h-7 w-7" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-display font-semibold text-lg text-foreground truncate">{title}</h3>
          <p className="text-muted-foreground text-sm mt-1">
            {year} • {genre}
          </p>
        </div>
        <div className="flex items-center gap-1 bg-primary/10 px-3 py-1.5 rounded-full">
          <Star className="h-4 w-4 text-primary fill-primary" />
          <span className="text-sm font-medium text-primary">{matchScore}%</span>
        </div>
      </div>
    </div>
  );
};

export default MovieCard;
