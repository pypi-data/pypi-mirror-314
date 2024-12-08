from typing import Optional, Dict, Any, Union, List
import traceback
from pathlib import Path
import io
import requests
import numpy as np
from PIL import Image
import re

from owlsight.hugging_face.constants import HUGGINGFACE_MEDIA_TASKS

from owlsight.processors.base import TextGenerationProcessor
from owlsight.processors.text_generation_processors import TextGenerationProcessorTransformers
from owlsight.processors.constants import DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE
from owlsight.utils.custom_classes import MediaObject
from owlsight.utils.logger import logger


class MediaPreprocessor:
    """
    Handles preprocessing for different media types and integrates with text generation.

    This class preprocesses media inputs (images, audio, documents) before passing them
    to the appropriate model pipeline.
    """

    def __init__(self, task: str):
        """
        Initialize preprocessor for specific task.

        Parameters
        ----------
        task : str
            The task to handle. Must be one of HUGGINGFACE_MEDIA_TASKS or a text task.
        """
        self.task = task
        self._validate_task()

    def _validate_task(self) -> None:
        """Validate that the task is supported."""
        if self.task not in HUGGINGFACE_MEDIA_TASKS and not self.task.endswith("generation"):
            raise ValueError(
                f"Task {self.task} is not supported. Must be one of {HUGGINGFACE_MEDIA_TASKS} "
                f"or end with 'generation'"
            )

    def preprocess_input(self, input_data: Union[str, bytes, Path], question: Optional[str] = None) -> Any:
        """
        Preprocess input data based on task type.

        Parameters
        ----------
        input_data : Union[str, bytes, Path]
            The input data. Can be a file path, URL, or bytes.
        question : Optional[str]
            Question for VQA or document QA tasks.

        Returns
        -------
        Dict[str, Any]
            Preprocessed data in format expected by the model.
        """
        if self.task not in HUGGINGFACE_MEDIA_TASKS:
            raise ValueError(
                f"Task {self.task} is not supported for media preprocessing. Should be one of {HUGGINGFACE_MEDIA_TASKS}"
            )

        try:
            if isinstance(input_data, (str, Path)):
                input_data = self._load_from_path_or_url(input_data)

            if self.task == "automatic-speech-recognition":
                return self._preprocess_audio(input_data)
            elif self.task in ["image-to-text", "visual-question-answering", "document-question-answering"]:
                processed = self._preprocess_image(input_data)
                if question and self.task in ["visual-question-answering", "document-question-answering"]:
                    return {"image": processed, "question": question}
            else:
                raise ValueError(f"Task {self.task} is not supported for media preprocessing.")
            return processed

        except Exception:
            logger.error(f"Error preprocessing input for task {self.task}: {traceback.format_exc()}")
            raise

    def _load_from_path_or_url(self, source: Union[str, Path]) -> bytes:
        """Load data from file path or URL."""
        if isinstance(source, str) and source.startswith(("http://", "https://")):
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            return response.content
        else:
            p = Path(source)
            if not p.exists():
                raise FileNotFoundError(f"File not found: {source}")
            return p.read_bytes()

    def _preprocess_audio(self, audio_data: bytes) -> Dict[str, Any]:
        """Preprocess audio data."""
        # Convert to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        audio_array = audio_array.astype(np.float32) / 32768.0

        # Convert stereo to mono if needed
        if len(audio_array.shape) > 1:
            audio_array = audio_array.mean(axis=1)

        return {"array": audio_array, "sampling_rate": 16000}  # Standard sampling rate for most models

    def _preprocess_image(self, image_data: bytes) -> Image.Image:
        """Preprocess image data."""
        image = Image.open(io.BytesIO(image_data))
        return image


class MultiModalProcessorTransformers(TextGenerationProcessor):
    def __init__(self, model_id: str, task: str, save_history: bool = False, system_prompt: str = "", **kwargs):
        if task not in HUGGINGFACE_MEDIA_TASKS:
            raise ValueError(
                f"Task {task} is not supported for media preprocessing. Should be one of {HUGGINGFACE_MEDIA_TASKS}"
            )

        super().__init__(model_id=model_id, save_history=save_history, system_prompt=system_prompt)
        self.task = task
        self.text_processor = TextGenerationProcessorTransformers(model_id=model_id, task=task, **kwargs)
        self.media_preprocessor = MediaPreprocessor(self.text_processor.task)

    def generate(
        self,
        input_data: str,
        media_objects: Dict[str, MediaObject],
        stopwords: Optional[List[str]] = None,
        max_new_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        generation_kwargs: Optional[Dict[str, Any]] = None,
    ) -> str:
        # First prepare the generation parameters
        input_data, generate_kwargs = self.text_processor.prepare_generation(
            input_data=input_data,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            stopwords=stopwords,
            streaming=False,
            generation_kwargs=generation_kwargs,
            apply_chat_template=False,
        )
        generate_kwargs.pop("eos_token_id", None)

        # Extract any referenced media objects and their positions if in the input text
        media_refs = re.finditer(r"__MEDIA_\d+__", input_data)

        # For each media reference, preprocess the media and store question if present
        preprocessed_data = []
        for ref in media_refs:
            media_id = ref.group()
            media_object = media_objects[media_id]

            # Get the question from the input text before the media reference
            text_before = input_data[: ref.start()].strip()
            question = text_before if text_before else None

            # Preprocess the media file
            preprocessed = self.media_preprocessor.preprocess_input(media_object.path, question)
            preprocessed_data.append(preprocessed)

        # If we have only one media object, unpack it
        if len(preprocessed_data) == 1:
            preprocessed_data = preprocessed_data[0]

        try:
            response = self.text_processor.pipe(preprocessed_data, generate_kwargs=generate_kwargs)
            response = str(response)
            print(response)
        except Exception as e:
            logger.error(f"Error generating text with media input: {traceback.format_exc()}")
            raise

        self.update_history(str(input_data), response.strip())
        return response

    def preprocess_input(self, input_data: Union[str, bytes, Path], question: Optional[str] = None) -> Any:
        processed = self.media_preprocessor.preprocess_input(input_data, question)
        return processed
