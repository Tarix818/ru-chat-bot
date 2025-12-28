import asyncio
import pathlib
import torch
from torch.nn import functional as f
from .model import IntentModel
from .phrases import phrase_manager
from .vectorizer import vectorize

_CURRENT_DIR = pathlib.Path(__file__).parent.resolve()
_MODEL_PATH = str(_CURRENT_DIR.parent / "resources" / "model.pt")


class NLUManager:
    def __init__(self,
                 input_dim: int = 312,
                 num_classes: int = 7,
                 best_t: float = 1.55,
                 best_confidence: float = 0.9):
        self.best_t = best_t
        self.best_confidence = best_confidence
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = IntentModel(input_dim, num_classes).to(self.device)
        self.model.load_state_dict(torch.load(_MODEL_PATH, map_location=self.device))
        self.model.eval()
        self.mapping = {
            0: 'fallback',
            1: 'origin',
            2: 'time',
            3: 'date',
            4: 'weather',
            5: 'news',
            6: 'wiki'
        }

    def get_intent(self, message: str) -> tuple[int, float]:
        vec = vectorize(message)
        if vec.ndim == 1:
            vec = vec.reshape(1, -1)
        vec_tensor = torch.tensor(vec, dtype=torch.float32).to(self.device)
        with torch.no_grad():
            logits = self.model(vec_tensor)
            scaled_logits = logits / self.best_t
            probs = f.softmax(scaled_logits, dim=1)
        confidence, intent_tensor = torch.max(probs, dim=1)
        conf_value = confidence.item()
        intent_id = intent_tensor.item()
        if intent_id == 0 or conf_value < self.best_confidence:
            return -1, conf_value
        return intent_id, conf_value

    async def get_answer(self, intent_id: int, user_id: int, text: str) -> str | None:
        if intent_id == -1:
            return None
        tag = self.mapping.get(intent_id)
        if not tag:
            return None
        response = phrase_manager.get(tag, user_id, text=text)
        if asyncio.iscoroutine(response):
            return await response
        return response


nlu_manager = NLUManager()
