
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

def load_model( engine_config,  model_path ):
    tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code = engine_config["trust_remote_code"])
    sampling_params = SamplingParams( temperature = engine_config["temperature"],
                                    top_p = engine_config["top_p"],
                                    max_tokens = engine_config["max_tokens"],
                                    stop = engine_config["stop"],
                                    use_beam_search = engine_config["use_beam_search"],
                                    best_of = engine_config["best_of"])
    llm = LLM(
        model = model_path,
        trust_remote_code = engine_config["trust_remote_code"],
        dtype = engine_config["dtype"],
        max_model_len = engine_config["max_model_len"],
        gpu_memory_utilization = engine_config["gpu_memory_utilization"],
        seed = engine_config["seed"],
    )
    return sampling_params, llm, tokenizer

def get_input_message( query, tokenizer ):
    _input = []
    for line in query:
        '''messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": line}
        ]'''
        messages = [
            {"role": "user", "content": line}
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        _input.append( text  )
    return _input

def split_inner_list( prompt ):
    # aaa = [i for i in range(99)]
    inner_list = []
    interval = []
    for j in range( 0, len(prompt)+1, 10):
        interval.append(j)
    if len(prompt)%10 != 0:
        interval.append(len(prompt))
    for j in range(len(interval)-1):
        inner_list.append( prompt[ interval[j]: interval[j+1] ])
    return inner_list