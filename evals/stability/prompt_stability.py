"""
This is an advanced prompt stability evaluation module with controlled, intent- preserving,noise injection.
It supports deterministic perturbations and bounded user like noise (typos,grammar,informal parsing).

This module answers Does the system behave consistently under realistic user variation.

We do this by:
Generating many slightly modified versions of the same prompt
Sending each version to the model
Comparing how similar the answers are
Reporting where the instability comes from

"""
from typing import List,Dict,Callable
from dataclasses import dataclass
from enum import Enum
import numpy as np
import re
import random

# Perturbation types
class PerturbationType(Enum):

    # These represent DIFFERENT WAYS we slightly change a prompt.
    # Each type tests a different failure mode of the system.

    LEXICAL = "lexical" # Small wording changes
    SYNTACTIC = 'syntactic' # Small sentence strucutre changes
    INSTRUCTION_NOISE = 'instruction_noise' # Extra instructions without effecting meaning
    CONTEXT_RECORDER = 'context_recorder' #Instruction Ordering changes
    NOISY_USER_INPUT = 'noisy_user_input'  # Realistic human noise: typos, grammar mistakes, informal phrasing

@dataclass(frozen=True)
class PromptVariant:
    base_prompt:str     #Original User change
    variant_prompt:str      #Modified Version
    perturbation_type:PerturbationType   # What kind of change was happened
"""

"""
class PromptPerturbationGenerator:
    """
    This class is responsible for generating many realistic versions for a given prompt by preserving the 
    same intent.
    - We DO NOT change meaning
    - We DO NOT add random garbage
    - We ONLY simulate realistic user variations
    """
    def __init__(self,noise_sample_per_prompt:int=16):
        
        self.noise_sample_per_prompt = noise_sample_per_prompt
        self.perturbations.Dict[PerturbationType,Callable[[str],List[str]]] = {
            PerturbationType.LEXICAL: self._lexical,
            PerturbationType.SYNTACTIC: self._syntactic,
            PerturbationType.INSTRUCTION_NOISE: self._instruction_noise,
            PerturbationType.CONTEXT_REORDER: self._context_reorder,
            PerturbationType.NOISY_USER_INPUT: self._noisy_user_inputs,
        }

    def _lexical(self, prompt: str) -> List[str]:
        # Adds polite wording, meaning stays same
        return [f"Please answer the following question:\n{prompt}"]
    
    def _syntactic(self, prompt: str) -> List[str]:
        # Changes sentence structure
        return [f"{prompt}\n\nExplain your answer."]
    
    def _instruction_noise(self, prompt: str) -> List[str]:
        # Adds extra instructions that SHOULD NOT change the answer
        return [
            "Answer concisely and clearly.\n"
            "Do not alter the original intent.\n"
            f"{prompt}"
        ]
    
    def _context_reorder(self, prompt: str) -> List[str]:
        # Reorders instructions (important in RAG systems)
        return [f"{prompt}\n\nUse the above information to answer."]
    
    # Bounded stochastic noise
    # (Random but controlled)

    def _introduce_typo(self, text: str) -> str:
        """Introduces a small typo by swapping characters.Simulates real human typing mistakes."""
        words = text.split()
        idx = random.randint(0,len(words)-1)
        word = words[idx]

        if len(word) < 3:
            char_idx = random.randint(1, len(word) - 2)
            word = (
                word[:char_idx]+ word[char_idx + 1]+ word[char_idx]+ word[char_idx + 2:]
            )
            words[idx] = word
        return " ".join(words)
    
    def _drop_punctuation(self, text: str) -> str:
        """Removes punctuation.Very common in casual user inputs."""
        return re.sub(r"[?.!,]", "", text)
    
    def _informal_rephrase(self, text: str) -> str:
        """Makes the prompt more conversational."""
        return f"Hey, can you tell me {text.lower()}"
    
    def _grammar_noise(self, text: str) -> str:
        """Introduces mild grammar mistakes."""
        return text.replace("What is", "What")
    
    def _noisy_user_inputs(self, prompt: str) -> List[str]:
        """Generates MANY noisy prompts that:look like real user input and still clearly preserve intent"""
        generators = [self._introduce_typo,self._drop_punctuation,
            self._informal_rephrase,self._grammar_noise]
        noisy_variants = set()
        # Keep generating until we reach the desired count
        while len(noisy_variants) < self.noisy_samples_per_prompt:
            fn = random.choice(generators)
            noisy_variant = fn(prompt)
            noisy_variants.add(noisy_variant)

        return list(noisy_variants)

    def generate(self, prompt: str) -> List[PromptVariant]:
        """ Main entry point. Takes ONE prompt and returns MANY PromptVariant objects. """
        variants: List[PromptVariant] = []
        for p_type, fn in self.perturbations.items():
            generated_prompts = fn(prompt)

            for variant_prompt in generated_prompts:
                variants.append(
                    PromptVariant(
                        base_prompt=prompt,
                        variant_prompt=variant_prompt,
                        perturbation_type=p_type
                    )
                )

        return variants

class PromptStabilityEvaluator:
    """
    High-level orchestrator.

    It:
    1. Generates prompt variants
    2. Calls the model on each variant
    3. Groups answers by perturbation type
    4. Measures semantic variance
    """
    def __init__(self,model_fn: Callable[[str], str],variance_fn: Callable[[List[str]], Dict[str, float]],
        noisy_samples_per_prompt: int = 16):
        self.model_fn = model_fn
        self.variance_fn = variance_fn
        self.generator = PromptPerturbationGenerator(
            noisy_samples_per_prompt=noisy_samples_per_prompt
        )
    def evaluate(self, prompt: str) -> Dict:
        """
        Runs full prompt stability evaluation for ONE prompt.
        """

        # Step 1: Generate prompt variants
        variants = self.generator.generate(prompt)

        # Step 2: Collect model outputs grouped by perturbation type
        outputs_by_type: Dict[PerturbationType, List[str]] = {}

        for variant in variants:
            output = self.model_fn(variant.variant_prompt)

            outputs_by_type.setdefault(
                variant.perturbation_type, []
            ).append(output)

        # Step 3: Compute answer variance per perturbation category
        stability_by_type: Dict[str, Dict[str, float]] = {}

        for p_type, outputs in outputs_by_type.items():
            metrics = self.variance_fn(outputs)
            stability_by_type[p_type.value] = metrics

        # Step 4: Aggregate a global stability score
        mean_scores = [
            metrics["mean_similarity"]
            for metrics in stability_by_type.values()
        ]

        global_stability = float(np.mean(mean_scores))

        # Final structured result
        return {
            "num_prompt_variants": len(variants),
            "prompt_stability_score": global_stability,
            "by_perturbation": stability_by_type,
            "unstable": global_stability < 0.85
        }


    

