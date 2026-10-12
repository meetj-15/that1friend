import argparse

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--adapter", required=True)
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.base)
    base = AutoModelForCausalLM.from_pretrained(args.base, torch_dtype="auto")
    model = PeftModel.from_pretrained(base, args.adapter)

    prompt = "<REGION=BENGALURU> <HUMOR=MEDIUM> User: I am stuck in traffic again. Assistant:"
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=80, do_sample=True, temperature=0.7)
    print(tokenizer.decode(output[0], skip_special_tokens=True))


if __name__ == "__main__":
    main()
