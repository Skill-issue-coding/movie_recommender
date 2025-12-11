import { cn } from "@/lib/utils";
import { ComponentProps } from "react";

function TypographyH1({ className, children, ...props }: ComponentProps<"h1">) {
  return (
    <h1
      className={cn(
        "text-4xl font-semibold font-display md:text-5xl text-foreground scroll-m-20 text-left tracking-tight text-balance",
        className
      )}
      {...props}>
      {children}
    </h1>
  );
}

function TypographyMuted({ className, children, ...props }: ComponentProps<"p">) {
  return (
    <p className={cn("text-muted-foreground text-sm", className)} {...props}>
      {children}
    </p>
  );
}

export { TypographyH1, TypographyMuted };
