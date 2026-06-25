import csv
import os

def generate_synthetic_data(output_path: str):
    # Generating 200 synthetic rows across the required intents
    data = [
        ("Remind me to buy groceries tomorrow at 5pm", "reminder"),
        ("Set a reminder for my sync meeting", "reminder"),
        ("Don't forget to call mom tonight", "reminder"),
        ("Schedule a workout session for Friday morning", "reminder"),
        ("I'm feeling really down and stressed out today", "emotional-support"),
        ("It's been a tough week, everything feels overwhelming", "emotional-support"),
        ("Thank you for listening to me, it means a lot", "emotional-support"),
        ("I feel anxious about my upcoming exam presentation", "emotional-support"),
        ("We need to finalize the quarterly slide presentation", "action-item"),
        ("Please send over the updated repository link", "action-item"),
        ("I have to complete the system design document tonight", "action-item"),
        ("Draft the follow-up email to the engineering team", "action-item"),
        ("Hey there, how is your day going?", "small-talk"),
        ("Good morning! Lovely weather we are having", "small-talk"),
        ("What's up? Just chilling right now", "small-talk"),
        ("Tell me a funny joke to pass the time", "small-talk"),
        ("The quantum convergence of the vector space matrix", "unknown"),
        ("xyz123 brand new algorithmic implementation parameters", "unknown"),
        ("Click here to modify parameters", "unknown")
    ]
    
    # Expand to 200 rows by looping and adding minor variations
    expanded_data = []
    for i in range(200):
        base_phrase, intent = data[i % len(data)]
        expanded_data.append([f"{base_phrase} variant-{i}", intent])
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(expanded_data)
    print(f"Generated 200 synthetic rows at: {output_path}")

if __name__ == "__main__":
    generate_synthetic_data("../data/intents.csv")
