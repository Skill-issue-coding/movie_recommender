import { EndpointResult, TestEndpointResult } from "@/lib/types";
import { TryCatch } from "@/lib/utils";
import axios from "axios";

export async function TestEndpoints() {
  const LLMData: null | TestEndpointResult = await TestLLMEndpoint();
  console.log("LLM Endpoint", LLMData?.message, "\n");

  const MLData: null | TestEndpointResult = await TestMLEndpoint();
  console.log("LLM Endpoint", MLData?.message, "\n");
}

async function TestLLMEndpoint(): Promise<null | TestEndpointResult> {
  const { data, error } = await TryCatch(axios.post("http://localhost:8080/llm"));

  if (error !== null) {
    console.error(error);
    return null;
  }

  console.log(data);

  return data.data;
}

async function TestMLEndpoint(): Promise<null | TestEndpointResult> {
  const { data, error } = await TryCatch(axios.post("http://localhost:8080/ml"));

  if (error !== null) {
    console.error(error);
    return null;
  }

  return data.data;
}

export async function MLEndpoint(summary: string): Promise<null | EndpointResult[]> {
  const { data, error } = await TryCatch(
    axios.post("http://localhost:8080/ml", { summary: summary })
  );

  if (error !== null) {
    console.error(error);
    return null;
  }

  console.log(data.data);

  return data.data.recommendations;
}
