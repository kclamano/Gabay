import json
import os
import ollama

def load_coordinates(json_path):
    if not os.path.exists(json_path):
        print(f"Error: Hindi mahanap ang file sa {json_path}")
        return None
    with open(json_path, 'r') as f:
        return json.load(f)

def generate_taglish_tutorial(keyframe_name, coords):
    nx = coords["normalized_x"]
    ny = coords["normalized_y"]
    
    prompt = f"""
    You are an empathetic, patient, and sweet AI assistant creating high-accessibility smartphone simulation tutorials for older Filipino adults (Lolos and Lolas).
    
    Context:
    The user is interactive-training on a GCash workflow video step.
    A touch action was captured at normalized coordinates: X={nx}, Y={ny} (where 0.0 is top/left and 1.0 is bottom/right).
    
    Analyze the region based on these general UI heuristic approximations:
    - If Y is between 0.85 and 0.98: This is likely a bottom action button (e.g., 'Next', 'Send PHP', 'Confirm').
    - If Y is between 0.25 and 0.45: This is likely a primary navigation grid option or input field.
    - If Y is between 0.05 and 0.20: This is likely a header, back button, or upper category tab.
    
    Generate a JSON response mapping this exact step. The response MUST strictly follow this JSON format structure:
    {{
        "step_file": "{keyframe_name}",
        "detected_action_zone": "Provide a guess of the UI element name based on the context and coordinates",
        "taglish_instruction": "A gentle, clear, conversational Taglish guide for Lola using endearments like 'Lola po' or 'pindutin po natin'. Focus on visual cues like colors or positions."
    }}
    
    Return ONLY raw JSON, do not include markdown blocks or extra explanations.
    """

    try:
        response = ollama.generate(model='llama3', prompt=prompt)
        raw_text = response['response'].strip()
        return raw_text
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return None

def main():
    JSON_PATH = "output_keyframes/touch_coordinates.json"
    coordinates_data = load_coordinates(JSON_PATH)
    
    if not coordinates_data:
        print("❌ Error: Walang nakitang data sa touch_coordinates.json o hindi mabasa ang file.")
        return

    print(f"📋 May nahanap na {len(coordinates_data)} entries sa coordinate map.")
    print("Sending structured coordinate maps to local Llama-3 text engine...")
    compiled_steps = []

    for keyframe, metadata in coordinates_data.items():
        print(f"Processing step for {keyframe}...")
        ai_response = generate_taglish_tutorial(keyframe, metadata)
        
        if ai_response:
            try:
                parsed_json = json.loads(ai_response)
                compiled_steps.append(parsed_json)
                print(f"✅ Generated instructions for {keyframe}")
            except:
                print(f"⚠️ Raw output captured for {keyframe}. Saved raw payload data.")
                compiled_steps.append({"step_file": keyframe, "raw_payload": ai_response})

    output_manifest = "output_keyframes/gabay_simulation_manifest.json"
    with open(output_manifest, "w", encoding='utf-8') as f:
        json.dump(compiled_steps, f, indent=4, ensure_ascii=False)
        
    print(f"\nPipeline Stage 3 Complete! Simulation manifest compiled at: {output_manifest}")

if __name__ == "__main__":
    main()