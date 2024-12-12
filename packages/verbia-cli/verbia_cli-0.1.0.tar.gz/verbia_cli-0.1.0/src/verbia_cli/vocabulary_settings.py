import hashlib
import uuid
from dataclasses import dataclass, field

from verbia_core.utils import time_provider


def _generate_short_id() -> str:
    uuid_value = uuid.uuid4()
    return hashlib.sha256(uuid_value.bytes).hexdigest()[:8]


@dataclass
class VocabularySettings:
    name: str
    word_language_code: str
    native_language_code: str
    dictionary: str = "Gemini"
    review_strategy: str = "SM2"

    id: str = field(default_factory=_generate_short_id)
    created_at: int = field(default_factory=time_provider.time_mills_from_now)
