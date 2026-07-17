import os
import sys
import json
from phoenix.client import Client as PhoenixClient

def fetch_phoenix_logs(trace_id: str = None):
    # Connects to your running Docker instance
    client = PhoenixClient()
    
    if not trace_id:
        print("No Trace ID provided. Pulling latest trace from the local server...")
        # Get all spans, sort by time to pick the most recent trace
        spans_df = client.spans.get_spans_dataframe()
        if spans_df.empty:
            print("No traces found locally.")
            return
        trace_id = spans_df.sort_values(by="start_time", ascending=False)["context.trace_id"].iloc[0]
        print(f"Targeting latest Trace ID: {trace_id}\n")

    print("="*50)
    print(f"EXTRACTING TRACE: {trace_id}")
    print("="*50)

    try:
        # Filter operations under this specific execution path natively in pandas
        spans_df = client.spans.get_spans_dataframe()
        spans_df = spans_df[spans_df["context.trace_id"] == trace_id]
        
        # Sort sequentially so the nested graph reads chronologically
        spans_sorted = spans_df.sort_values(by="start_time")
        
        for index, row in spans_sorted.iterrows():
            kind = row.get('span_kind', 'UNKNOWN')
            name = row.get('name', 'Unnamed Span')
            span_id = row.get('context.span_id', index)
            print(f"\n[{kind}]: {name}")
            print(f"Span ID: {span_id}")
            
            # Access the input/output attributes safely (OpenTelemetry flattens them into dot notation)
            inputs = row.get('attributes.llm.input_messages') or row.get('attributes.input.value', {})
            outputs = row.get('attributes.llm.output_messages') or row.get('attributes.output.value', {})
            
            print("Inputs:")
            if isinstance(inputs, str):
                try:
                    inputs = json.loads(inputs)
                except json.JSONDecodeError:
                    pass
            print(json.dumps(inputs, indent=2, default=str)[:1500])
            
            if outputs:
                print("Outputs:")
                if isinstance(outputs, str):
                    try:
                        outputs = json.loads(outputs)
                    except json.JSONDecodeError:
                        pass
                print(json.dumps(outputs, indent=2, default=str)[:1500])
            print("-" * 30)
            
    except Exception as e:
        print(f"Error extracting logs from local Phoenix client: {e}")

if __name__ == "__main__":
    target_id = sys.argv[1] if len(sys.argv) > 1 else None
    fetch_phoenix_logs(target_id)
