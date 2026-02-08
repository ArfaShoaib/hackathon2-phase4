# Gemini API Integration Guide with OpenAI SDK Compatibility

## Overview

This document outlines how to integrate Google's Gemini API with the OpenAI Agents SDK framework using a compatibility layer. This approach allows you to leverage Gemini's capabilities while maintaining the familiar OpenAI SDK interface.

## Architecture

The integration uses a compatibility wrapper that translates OpenAI SDK calls to Gemini API equivalents:

```
OpenAI Agents SDK → Compatibility Layer → Google Gemini API
```

## Required Dependencies

```bash
# Core dependencies
pip install google-generativeai
pip install openai  # Still needed for the SDK interface
pip install openai-gemini-adapter  # Compatibility wrapper (or custom implementation)

# Alternative: Custom compatibility layer
pip install requests
```

## Implementation Approach

### Option 1: Using Existing Compatibility Wrapper

```python
# If using an existing adapter
import openai
from openai_gemini_adapter import configure_gemini

# Configure the adapter to use Gemini instead of OpenAI
configure_gemini(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

# Now you can use OpenAI SDK calls which will be translated to Gemini
client = openai.OpenAI()
completion = client.chat.completions.create(
    model="gemini-pro",  # or "gemini-1.5-pro"
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)
```

### Option 2: Custom Compatibility Layer

If no suitable adapter exists, you'll need to create a custom compatibility layer:

```python
import openai
from google import genai
import os

class GeminiAdapter:
    def __init__(self):
        self.gemini_client = genai.GenerativeModel('gemini-pro')

    def chat_completions_create(self, model, messages, **kwargs):
        # Convert OpenAI message format to Gemini format
        gemini_messages = self._convert_messages(messages)

        # Generate response using Gemini
        response = self.gemini_client.generate_content(gemini_messages)

        # Convert Gemini response back to OpenAI format
        return self._convert_response(response)

    def _convert_messages(self, openai_messages):
        # Convert from [{"role": "...", "content": "..."}] to Gemini format
        gemini_messages = []
        for msg in openai_messages:
            gemini_messages.append(msg["content"])
        return gemini_messages

    def _convert_response(self, gemini_response):
        # Convert Gemini response to OpenAI format
        # This would need to match the OpenAI response structure
        pass

# Monkey patch the OpenAI client
original_client = openai.OpenAI
def patched_init(self, api_key=None):
    self.gemini_adapter = GeminiAdapter()

openai.OpenAI = patched_init
```

## Configuration

### Environment Variables

```env
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro  # or gemini-pro
```

### Client Initialization

```python
import os
from openai import OpenAI

# The compatibility layer should automatically use Gemini when this is called
client = OpenAI(
    # Normally would pass api_key here, but compatibility layer handles it differently
)
```

## Mapping OpenAI Concepts to Gemini

| OpenAI Concept | Gemini Equivalent | Notes |
|----------------|-------------------|-------|
| `gpt-3.5-turbo` | `gemini-pro` | Main text generation model |
| `gpt-4` | `gemini-1.5-pro` | More capable model |
| `messages` | `contents` | Input format differs |
| `role: system` | System instructions | May require different handling |
| `temperature` | `temperature` | Same parameter |
| `max_tokens` | `max_output_tokens` | Similar concept, different name |

## Limitations and Considerations

### Functional Differences
- Gemini may not support all OpenAI features (function calling, etc.)
- Response formats may differ slightly
- Rate limits and pricing structures are different
- Some OpenAI-specific parameters may not translate

### Error Handling
- Error types and messages will come from Gemini API
- Need to handle Gemini-specific error conditions
- Rate limiting will follow Gemini's policies

### Tool Calling
- If using MCP tools, ensure the compatibility layer properly handles tool calling
- Gemini has its own function calling mechanism that may need mapping

## Testing the Integration

```python
# Basic test to verify the compatibility layer works
def test_gemini_integration():
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gemini-pro",  # or whatever identifier the adapter expects
            messages=[{"role": "user", "content": "Say hello"}]
        )
        print(f"Success: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"Integration failed: {e}")
        return False
```

## Fallback Strategy

Consider implementing a fallback mechanism in case the compatibility layer fails:

```python
def get_completion(messages, use_fallback=False):
    if not use_fallback:
        try:
            # Try Gemini through compatibility layer
            return call_gemini_compatibility_layer(messages)
        except Exception:
            # Fall back to actual OpenAI if needed
            return call_openai_official(messages)
    else:
        return call_openai_official(messages)
```

## Security Considerations

- Store Gemini API keys with same security measures as OpenAI keys
- Monitor usage separately for billing purposes
- Ensure the compatibility layer doesn't introduce vulnerabilities
- Log appropriately without exposing sensitive API keys