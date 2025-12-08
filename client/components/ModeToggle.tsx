import { Switch } from "@/components/ui/switch";
import { Brain, Cpu } from "lucide-react";

interface ModeToggleProps {
  isLLM: boolean;
  onToggle: (value: boolean) => void;
}

const ModeToggle = ({ isLLM, onToggle }: ModeToggleProps) => {
  return (
    <div className="flex items-center justify-center gap-4 py-4">
      <div
        className={`flex items-center gap-2 transition-all duration-300 ${
          !isLLM ? "text-primary" : "text-muted-foreground"
        }`}>
        <Cpu className="h-5 w-5" />
        <span className="font-medium text-sm">ML Model</span>
      </div>

      <Switch checked={isLLM} onCheckedChange={onToggle} aria-label="Toggle between ML and LLM" />

      <div
        className={`flex items-center gap-2 transition-all duration-300 ${
          isLLM ? "text-primary" : "text-muted-foreground"
        }`}>
        <Brain className="h-5 w-5" />
        <span className="font-medium text-sm">LLM</span>
      </div>
    </div>
  );
};

export default ModeToggle;
