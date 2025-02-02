import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
from sqlalchemy.orm import Session
from models.interaction_model import Interaction

MODEL_NAME = "mistralai/Mistral-7B-Instruct"    # Change if needed
MODEL_SAVE_PATH = "storage/fine_tuned_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

def prepare_training_data(db: Session):
    interactions = db.query(Interaction).filter(Interaction.feedback == 1).all()
    texts = [f"User: {i.user_query}\nAI: {i.ai_response}" for i in interactions]
    return Dataset.from_dict({"text": texts})

def fine_tune_model(db: Session):
    dataset = prepare_training_data(db)
    
    training_args = TrainingArguments(
        output_dir= MODEL_SAVE_PATH,
        per_device_train_batch_size= 2,
        num_train_epochs= 1,
        logging_dir= "./logs",
        save_strategy= "epoch"
    )
    
    trainer = Trainer(
        model= model,
        args= training_args,
        train_dataset= dataset,
        tokenizer= tokenizer,
        data_collator= DataCollatorForLanguageModeling(tokenizer, mlm= False)
    )
    
    trainer.train()
    model.save_pretrained(MODEL_SAVE_PATH)
    tokenizer.save_pretrained(MODEL_SAVE_PATH)
    
    return "Fine-tuning completed!"