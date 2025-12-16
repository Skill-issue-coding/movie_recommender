import { Switch } from "@/components/ui/switch";
import { CloudLightning, Cpu } from "lucide-react";

interface ModeToggleProps {
  isLLM: boolean;
  currentToggle: boolean;
  onToggle: (value: boolean) => void;
}

const LLMToggle = ({ isLLM, currentToggle, onToggle }: ModeToggleProps) => {
  return (
    <div className="flex items-center justify-center gap-4 py-4">
      <div
        className={`flex items-center gap-2 transition-all duration-300 ${
          !currentToggle ? "text-primary" : "text-muted-foreground"
        }`}>
        <Cpu className="h-5 w-5" />
        <span className="font-medium text-sm">2.5 flash</span>
      </div>

      <Switch
        checked={currentToggle}
        onCheckedChange={onToggle}
        aria-label="Toggle between ML and LLM"
      />

      <div
        className={`flex items-center gap-2 transition-all duration-300 ${
          currentToggle ? "text-primary" : "text-muted-foreground"
        }`}>
        <CloudLightning className="h-5 w-5" />
        <span className="font-medium text-sm">2.5 lite</span>
      </div>
    </div>
  );
};

export default LLMToggle;
