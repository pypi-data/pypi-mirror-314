import os
from langfuse import Langfuse
from datetime import datetime
from langchain.evaluation import load_evaluator
from langchain_openai import ChatOpenAI
import json
import openai
import sklearn
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import numpy as np
from openai import OpenAI


class Evaluator:
    def __init__(self, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_HOST, OPENAI_INTERFACE_KEY,
                 LLM_AS_A_JUDGE_PRIVATE_KEY, config_path):
        self.__LANGFUSE_SECRET_KEY = LANGFUSE_SECRET_KEY
        self.__LANGFUSE_PUBLIC_KEY = LANGFUSE_PUBLIC_KEY
        self.__LANGFUSE_HOST = LANGFUSE_HOST
        self.__OPENAI_INTERFACE_KEY = OPENAI_INTERFACE_KEY
        self.__LLM_AS_A_JUDGE_PRIVATE_KEY = LLM_AS_A_JUDGE_PRIVATE_KEY

        if not os.path.exists(config_path):
            raise FileNotFoundError
        else:
            self.__config_path = config_path
            with open(self.__config_path, 'r') as json_file:
                self.__config = json.load(json_file)

        print("Evaluating model: ", self.__config["eval_model"])

        self.__langfuse = self.__set_langfuse()
        self.__expected_output = self.__set_expected_outputs()
        self.__dataset_preparation()

        self.__llm_as_a_judge_evaluator, self.__string_distance_evaluator = self.__set_up_evaluators()

    def __set_langfuse(self):
        langfuse = Langfuse(public_key=self.__LANGFUSE_PUBLIC_KEY,
                            secret_key=self.__LANGFUSE_SECRET_KEY,
                            host=self.__LANGFUSE_HOST)

        langfuse.create_prompt(
            name=self.__config["eval_model_prompt_name"],
            prompt=(json.dumps(self.__config["eval_model_prompt"], separators=(',', ':'))),
            config={
                "model": self.__config["eval_model"],
                "temperature": self.__config["eval_model_temperature"],
            },
            labels=[self.__config["label"]]
        )

        return langfuse

    def __set_expected_outputs(self):
        expected_output = []
        with open(self.__config["eval_model_dataset_file_path"], 'r') as file:
            local_items = json.load(file)
            # Upload to Langfuse
        for item in local_items:
            expected_output.insert(0, item["expected_output"])

        return expected_output

    def __dataset_preparation(self):
        dataset = None
        try:
            dataset = self.__langfuse.get_dataset(self.__config["eval_model_dataset_name"])
        except Exception as error:
            print("An error occurred:", error)

        if not dataset:
            print(True)
        else:
            print(False)

        dataset = None
        try:
            dataset = self.__langfuse.get_dataset(self.__config["eval_model_dataset_name"])
        except Exception as error:
            print("An error occurred:", error)

        if not dataset:
            self.__langfuse.create_dataset(name=self.__config["eval_model_dataset_name"])
            # Open and read the JSON file
            with open(self.__config["eval_model_dataset_file_path"], 'r') as file:
                local_items = json.load(file)
                # Upload to Langfuse
            for item in local_items:
                self.__langfuse.create_dataset_item(
                    dataset_name=self.__config["eval_model_dataset_name"],
                    # any python object or value
                    input=item["input"],
                    # any python object or value, optional
                    expected_output=item["expected_output"]
                )

    @staticmethod
    def __simple_evaluation(output, expected_output):
        return output == expected_output

    def __calculate_f1_score(self, traces, completions):
        f1 = f1_score(completions, self.__expected_output, average='weighted')
        print(f1)
        for trace in traces:
            self.__langfuse.score(
                trace_id=trace,
                name=self.__config["f1_score_exact_match_summary_evaluators"],
                value=f1
            )

    def __set_up_evaluators(self):
        llm_as_a_judge_evaluator = load_evaluator(
            "labeled_score_string",
            criteria=self.__config["llm_as_a_judge_accuracy_criteria"],
            normalize_by=1,
            llm=ChatOpenAI(api_key=os.environ["LLM_AS_A_JUDGE_PRIVATE_KEY"],
                           model=self.__config["llm_as_a_judge_model"],
                           base_url=self.__config["llm_as_a_judge_model_api_base"]),
        )

        string_distance_evaluator = load_evaluator("string_distance")
        return llm_as_a_judge_evaluator, string_distance_evaluator

    def __run_my_custom_llm_app(self, input):
        print(input)
        langfuse_prompt = self.__langfuse.get_prompt(name=self.__config["eval_model_prompt_name"], label="development")

        langfuse_prompt_json = json.loads(langfuse_prompt.prompt)
        print(langfuse_prompt_json)
        messages = [
            {"role": "system", "content": langfuse_prompt_json["system"]},
            {"role": "user",
             "content": langfuse_prompt_json["user"].format(Triple=input["Triple"], Sentence=input["Sentence"])}
        ]
        print(messages)
        trace = self.__langfuse.trace(input=input, name=self.__config["eval_trace_name"])
        generationStartTime = datetime.now()

        client = OpenAI(api_key=os.environ["OPENAI_INTERFACE_KEY"], base_url=self.__config["eval_model_api_base"])

        openai_completion = client.chat.completions.create(
            model=self.__config["eval_model"],
            messages=messages,
            max_tokens=self.__config["eval_model_max_tokens_completion"]
            , temperature=self.__config["eval_model_temperature"],
            logprobs=self.__config["eval_model_logprobs"]
        )

        langfuse_generation = trace.generation(
            name=self.__config["eval_model_generation_name"],
            prompt=langfuse_prompt,
            input=messages,
            output=openai_completion,
            model=self.__config["eval_model"],
            start_time=generationStartTime,
            end_time=datetime.now()
        )
        print(openai_completion.choices[0].message.content)
        trace.update(output=openai_completion.choices[0].message.content.strip())
        return openai_completion.choices[0].message.content.strip(), trace

    def __run_experiment(self, experiment_name):
        dataset = self.__langfuse.get_dataset(self.__config["eval_model_dataset_name"])

        traces = []
        completions = []

        for item in dataset.items:
            completion, trace = self.__run_my_custom_llm_app(item.input)
            traces.append(trace.trace_id)
            completions.append(completion)

            item.link(trace, experiment_name)  # pass the observation/generation object or the id
            if "llm_as_a_judge_evaluator_name" in self.__config:
                trace.score(
                    name=self.__config["llm_as_a_judge_evaluator_name"],
                    value=self.__llm_as_a_judge_evaluator.evaluate_strings(prediction=completion,
                                                                           reference=item.expected_output,
                                                                           input=item.input)['score']
                )

            if "exact_match_evaluator_name" in self.__config:
                trace.score(
                    name=self.__config["exact_match_evaluator_name"],
                    value=self.__simple_evaluation(completion, item.expected_output)
                )

            if "string_distance_evaluator_name" in self.__config:
                trace.score(
                    name=self.__config["string_distance_evaluator_name"],
                    value=self.__string_distance_evaluator.evaluate_strings(prediction=completion,
                                                                            reference=item.expected_output,
                                                                            input=item.input)['score']
                )

        return traces, completions

    def run(self):
        traces, completions = self.__run_experiment(
            self.__config["eval_model_simple_experiment_name"]
        )

        if "f1_score_exact_match_summary_evaluators" in self.__config:
            self.__calculate_f1_score(traces, completions)
