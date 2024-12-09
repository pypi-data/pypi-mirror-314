import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import signal
from .Model import Model
def handle_timeout(sig, frame):
    raise TimeoutError('took too long')
signal.signal(signal.SIGALRM, handle_timeout)

class HF_model(Model):
    def __init__(self, config, device="cuda:0"):
        self.provider = config["model_info"]["provider"]
        self.name = config["model_info"]["name"]
        self.temperature = float(config["params"]["temperature"])
        self.max_output_tokens = int(config["params"]["max_output_tokens"])

        api_pos = int(config["api_key_info"]["api_key_use"])
        hf_token = config["api_key_info"]["api_keys"][api_pos]
        self.tokenizer = AutoTokenizer.from_pretrained(self.name, use_auth_token=hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.name,
            torch_dtype=torch.bfloat16,
            device_map=device,
            use_auth_token=hf_token
        )
        self.terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        torch.set_default_tensor_type(torch.cuda.HalfTensor)

    def query(self, msg, max_tokens=128000):    
        messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": msg}
        ]
        #text = self.tokenizer.apply_chat_template(
        #    messages,
        #    tokenize=False,
        #    add_generation_prompt=True
        #)
        model_inputs = self.tokenizer([msg], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        #result = self.tokenizer.decode(output_tokens[0][input_ids.shape[-1]:], skip_special_tokens=True)
        return response

    def get_prompt_length(self, msg):
        input_ids = self.tokenizer.encode(msg, return_tensors="pt").to(self.model.device)
        return len(input_ids[0])

    def cut_context(self, msg, max_length):
        tokens = self.tokenizer.encode(msg, add_special_tokens=True)
        truncated_tokens = tokens[:max_length]
        truncated_text = self.tokenizer.decode(truncated_tokens, skip_special_tokens=True)
        return truncated_text