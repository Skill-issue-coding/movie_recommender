"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupText,
  InputGroupTextarea,
} from "@/components/ui/input-group";
import { Switch } from "@/components/ui/switch";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { TypographyH1 } from "@/components/ui/typography";
import { Separator } from "@radix-ui/react-separator";
import { ArrowUp } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black gap-24">
      <TypographyH1>Movie Recommender</TypographyH1>
      <Card className="w-full max-w-lg">
        <CardHeader>
          <CardTitle>Enter a summary</CardTitle>
          <CardDescription>Write a short summary about what movies you like etc...</CardDescription>
        </CardHeader>
        <CardContent>
          <InputGroup>
            <InputGroupTextarea placeholder="Ask, Search or Chat..." />
            <InputGroupAddon align="block-end">
              <InputGroupText className="ml-auto">{"0/300"}</InputGroupText>
              <Separator orientation="vertical" className="h-4!" />
              <Tooltip>
                <TooltipTrigger asChild>
                  <InputGroupButton variant="default" className="rounded-full" size="icon-xs">
                    <ArrowUp />
                    <span className="sr-only">Send</span>
                  </InputGroupButton>
                </TooltipTrigger>
                <TooltipContent className="text-primary-foreground">
                  Send <span className="text-ring">(&#8679; + &crarr;)</span>
                </TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Switch />
                </TooltipTrigger>
                <TooltipContent>LLM | ML</TooltipContent>
              </Tooltip>
            </InputGroupAddon>
          </InputGroup>
        </CardContent>
        <CardFooter></CardFooter>
      </Card>
    </div>
  );
}
