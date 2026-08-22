import json

def convert(input_path, output_path):
    with open(input_path) as f, open(output_path, "w") as out:
        for line in f:
            rec = json.loads(line)
            new_rec = {
                "contents": [
                    {"role": "user", "parts": [{"text": rec["input_text"]}]},
                    {"role": "model", "parts": [{"text": rec["output_text"]}]}
                ]
            }
            out.write(json.dumps(new_rec) + "\n")

convert("iris_v1_train.jsonl", "iris_v1_train_tuning.jsonl")
convert("iris_v2_train.jsonl", "iris_v2_train_tuning.jsonl")

print("Converted files ready for tuning.")