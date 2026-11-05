import json
import random
from pathlib import Path

INPUT_FILE = Path("data/faq_dataset.json")
OUTPUT_DIR = Path("data/processed")

random.seed(42)


def prepare_dataset():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    cleaned_data = []
    seen_questions = set()

    for item in data:
        question = item.get("question", "").strip()
        answer = item.get("answer", "").strip()

        if not question or not answer:
            continue

        key = question.lower()

        if key in seen_questions:
            continue

        seen_questions.add(key)

        cleaned_data.append({
            "question": question,
            "answer": answer
        })

    random.shuffle(cleaned_data)

    total = len(cleaned_data)
    train_end = int(total * 0.70)
    val_end = train_end + int(total * 0.15)

    train_data = cleaned_data[:train_end]
    val_data = cleaned_data[train_end:val_end]
    test_data = cleaned_data[val_end:]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for name, dataset in [
        ("train.json", train_data),
        ("validation.json", val_data),
        ("test.json", test_data)
    ]:
        with open(OUTPUT_DIR / name, "w", encoding="utf-8") as file:
            json.dump(dataset, file, indent=4, ensure_ascii=False)

    print("Dataset preparation completed!")
    print("Total records:", total)
    print("Training records:", len(train_data))
    print("Validation records:", len(val_data))
    print("Testing records:", len(test_data))


if __name__ == "__main__":
    prepare_dataset()
    