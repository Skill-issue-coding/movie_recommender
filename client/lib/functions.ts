import { EndpointResult, TestEndpointResult } from "@/lib/types";
import { TryCatch } from "@/lib/utils";
import axios from "axios";

export async function TestAPI() {
  const { data, error } = await TryCatch(
    axios.get("http://localhost:8080/test")
  );

  if (error !== null) {
    console.error(error);
    return;
  }

  return data.data.api;
}

export async function MLEndpoint(
  summary: string
): Promise<null | { movies: EndpointResult[]; keywords: [] }> {
  const { data, error } = await TryCatch(
    axios.post("http://localhost:8080/ml", { summary: summary })
  );

  if (error !== null) {
    console.error(error);
    return null;
  }

  return { movies: data.data.recommendations, keywords: data.data.keywords };
}

// Fix this later
export async function LLMEndpoint(summary: string): Promise<any> {
  // TODO: fix type etc.
  const { data, error } = await TryCatch(
    axios.post("http://localhost:8080/llm", { summary: summary })
  );

  if (error !== null) {
    console.error(error);
    return null;
  }

  return data.data;
}
