import time
import csv
from collections import deque, defaultdict
from heapq import heappush, heappop
from typing import List, Dict, Tuple, Optional


class RateLimitWindow:
    def __init__(self, duration_sec, max_requests=None, max_tokens=None):
        self.duration_sec = duration_sec
        self.max_requests = max_requests
        self.max_tokens = max_tokens
        self.events = deque()

    def _clean(self):
        cutoff = time.time() - self.duration_sec
        while self.events and self.events[0][0] <= cutoff:
            self.events.popleft()

    def can_use(self, tokens):
        self._clean()
        req_count = len(self.events) + 1
        tok_count = sum(e[1] for e in self.events) + tokens
        if (self.max_requests is not None and req_count > self.max_requests) or (
            self.max_tokens is not None and tok_count > self.max_tokens
        ):
            return False
        return True

    def record_usage(self, tokens):
        self._clean()
        self.events.append((time.time(), tokens))


class Model:
    def __init__(self, name, limits):
        self.name = name
        self.windows = []
        if "req_min" in limits or "tok_min" in limits:
            self.windows.append(
                RateLimitWindow(60, limits.get("req_min"), limits.get("tok_min"))
            )
        if "req_hour" in limits or "tok_hour" in limits:
            self.windows.append(
                RateLimitWindow(3600, limits.get("req_hour"), limits.get("tok_hour"))
            )
        if "req_day" in limits or "tok_day" in limits:
            self.windows.append(
                RateLimitWindow(86400, limits.get("req_day"), limits.get("tok_day"))
            )

    def can_use(self, tokens):
        for w in self.windows:
            if not w.can_use(tokens):
                return False
        return True

    def record_usage(self, tokens):
        for w in self.windows:
            w.record_usage(tokens)


class KeySlot:
    def __init__(self, models_config):
        # We'll store models in a min-heap keyed by "pressure" (like total requests)
        self.models = {}
        self.heap = []
        for m_name, cfg in models_config.items():
            model = Model(m_name, cfg)
            self.models[m_name] = model
            # Initial pressure = 0
            heappush(self.heap, (0, m_name))

    def find_and_use_model(self, tokens):
        # We'll try models in order of their current "pressure"
        tried = []
        found = None
        while self.heap:
            pressure, m_name = heappop(self.heap)
            model = self.models[m_name]
            if model.can_use(tokens):
                model.record_usage(tokens)
                # Increase pressure by 1 request unit for now
                heappush(self.heap, (pressure + 1, m_name))
                found = m_name
                break
            else:
                # Temporarily store and re-push after checking all
                tried.append((pressure, m_name))
        for t in tried:
            heappush(self.heap, t)
        return found


class Provider:
    def __init__(self, keys, models_config):
        self.slots = [KeySlot(models_config) for _ in keys]
        # For round-robin: maintain an index
        self.idx = 0

    def find_and_use(self, tokens):
        for _ in self.slots:
            slot = self.slots[self.idx]
            model = slot.find_and_use_model(tokens)
            self.idx = (self.idx + 1) % len(self.slots)
            if model:
                return self.idx - 1 if self.idx > 0 else len(self.slots) - 1, model
        return None, None


class ModelRouter:
    def __init__(self, keys_file: str, models_file: str, provider_order_file: Optional[str] = None):
        # Load keys
        provider_keys = defaultdict(list)
        with open(keys_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # Skip empty lines and comments
                parts = line.split(",")
                if len(parts) != 2:
                    continue  # Skip malformed lines
                p, k = parts
                provider_keys[p].append(k)

        # Load models
        provider_models = defaultdict(dict)

        # models_file is CSV with headers: provider,model,req_min,req_hour,req_day,tok_min,tok_hour,tok_day
        # Empty fields interpreted as None
        def to_int_or_none(x):
            if x is None:
                return None
            x = x.strip()
            return int(x) if x else None

        with open(models_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = row["provider"]
                m = row["model"]
                limits = {
                    "req_min": to_int_or_none(row.get("req_min", "")),
                    "req_hour": to_int_or_none(row.get("req_hour", "")),
                    "req_day": to_int_or_none(row.get("req_day", "")),
                    "tok_min": to_int_or_none(row.get("tok_min", "")),
                    "tok_hour": to_int_or_none(row.get("tok_hour", "")),
                    "tok_day": to_int_or_none(row.get("tok_day", "")),
                }
                # Filter out None
                limits = {k: v for k, v in limits.items() if v is not None}
                provider_models[p][m] = limits

        self.providers = {
            p: Provider(keys, provider_models[p])
            for p, keys in provider_keys.items()
            if p in provider_models
        }

        # Load provider preferences if provided
        if provider_order_file:
            with open(provider_order_file, "r", encoding="utf-8") as f:
                provider_order = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            # Reorder self.providers based on provider_order
            ordered_providers = {}
            for p in provider_order:
                if p in self.providers:
                    ordered_providers[p] = self.providers[p]
            # Add any remaining providers not in provider_order
            for p in self.providers:
                if p not in ordered_providers:
                    ordered_providers[p] = self.providers[p]
            self.providers = ordered_providers
        else:
            # Default to sorted order or as loaded
            pass

    def select_best_model(self, tokens: int) -> Optional[Tuple[str, str, str]]:
        # Iterate providers in the order of preference
        for p_name, prov in self.providers.items():
            k_idx, model = prov.find_and_use(tokens)
            if model:
                return p_name, k_idx, model
        return None

    def record_usage(self, provider_name: str, key_index: int, model_name: str, tokens: int) -> None:
        self.providers[provider_name].slots[key_index].models[model_name].record_usage(tokens)

    def query(self, messages: List[Dict[str, Optional[str]]]) -> Optional[Tuple[str, str, str]]:
        """
        Given a list of messages, selects the appropriate model based on token count.

        Args:
            messages (List[Dict[str, Optional[str]]]): List of messages where each message is a dict with 'content' and 'role'.

        Returns:
            Optional[Tuple[str, str, str]]: Tuple containing (provider, key_index, model_name) if a model is available, else None.
        """
        total_tokens = self._count_tokens(messages)
        selection = self.select_best_model(total_tokens)
        return selection

    def record(self, identifier: Tuple[str, str, str], num_tokens: int) -> None:
        """
        Records the usage of a model identified by the identifier tuple.

        Args:
            identifier (Tuple[str, str, str]): Tuple containing (provider, key_index, model_name).
            num_tokens (int): Number of tokens used.
        """
        if identifier and len(identifier) == 3:
            provider, key_index, model_name = identifier
            self.record_usage(provider, key_index, model_name, num_tokens)
        else:
            raise ValueError("Identifier must be a tuple of (provider, key_index, model_name)")

    def _count_tokens(self, messages: List[Dict[str, Optional[str]]]) -> int:
        """
        Counts the total number of tokens from the 'content' fields of the messages.

        Args:
            messages (List[Dict[str, Optional[str]]]): List of messages.

        Returns:
            int: Total number of tokens.
        """
        total_tokens = 0
        for message in messages:
            content = message.get('content', '')
            tokens = self._count_tokens_in_content(content)
            total_tokens += tokens
        return total_tokens

    def _count_tokens_in_content(self, content: str) -> int:
        """
        Counts the number of tokens in a single content string.
        This is a placeholder for a real tokenizer.

        Args:
            content (str): The content string.

        Returns:
            int: Number of tokens.
        """
        # Simple approximation: number of words
        return len(content.split())
