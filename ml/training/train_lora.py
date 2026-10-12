import argparse
from datasets import load_datasets
from transformers import AutoModelForCausallLM, AutoTokenizer, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--dataset", default="ml/datasets/friend.jsonl")
    parser.add_argument("--output", default="ml/adapters/that1friend")
    return parser.parse_args()

def main():
    args=parse_args()
    tokenizer=AutoTokenizer.from_pretrained(args.model)
    model=AutoModelForCausallLM.from_pretrained(args.model, torch_dtype="auto")
    if tokenizer.pad_token is None:
        tokenizer.pad_token=tokenizer.eos_token

    dataset=load_dataset("json", data_files=args.dataset, split="train")

    def tokenize(example):
        text=example["text"]
        encoded=tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=512,
        )
        encoded["labels"]=encoded["input_ids"].copy()
        return encoded
    
    tokenized=dataset.map(tokenize, remove_columns=dataset.column_names)
    
    lora=LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        task_type="CAUSAL_LM",
    )
    model=get_peft_model(model, lora)
    model.print_trainable_parameters()
    args_train=TrainingArguments(
        output_dir=args.output,
        learning_rate=2e-4,
        num_train_epochs=2,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        logging_steps=10,
        save_strategy="epoch",
        report_to="none"
    )
    trainer=Trainer(
        model=model,
        args=args_train, 
        train_dataset=tokenized,
    )
    trainer.train()
    model.save_pretrained(args.output)
    tokenizer.save_pretrained(args.output)

if __name__=="__main__":
    main()