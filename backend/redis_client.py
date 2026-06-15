import json
import logging
from redis import Redis
from backend.config import settings

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        try:
            self.client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.client.ping()
            self.is_connected = True
            logger.info("Connected to Redis successfully.")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis. Using in-memory fallback. Error: {e}")
            self.client = None
            self.is_connected = False
            self._fallback_db = {}

    def get(self, key: str) -> str | None:
        if self.is_connected:
            try:
                return self.client.get(key)
            except Exception as e:
                logger.error(f"Redis get error for {key}: {e}")
        return self._fallback_db.get(key)

    def set(self, key: str, value: str, ex: int | None = None) -> bool:
        if self.is_connected:
            try:
                self.client.set(key, value, ex=ex)
                return True
            except Exception as e:
                logger.error(f"Redis set error for {key}: {e}")
        self._fallback_db[key] = value
        return True

    def delete(self, key: str) -> bool:
        if self.is_connected:
            try:
                self.client.delete(key)
                return True
            except Exception as e:
                logger.error(f"Redis delete error for {key}: {e}")
        if key in self._fallback_db:
            del self._fallback_db[key]
        return True

    # Helper: Set JSON data
    def set_json(self, key: str, value: dict | list, ex: int | None = None) -> bool:
        return self.set(key, json.dumps(value), ex=ex)

    # Helper: Get JSON data
    def get_json(self, key: str) -> dict | list | None:
        val = self.get(key)
        if val:
            try:
                return json.loads(val)
            except Exception as e:
                logger.error(f"JSON decode error for key {key}: {e}")
        return None

    # --- Session Cache ---
    def set_session(self, user_id: int | str, session_data: dict, ex: int = 3600) -> bool:
        return self.set_json(f"session:{user_id}", session_data, ex=ex)

    def get_session(self, user_id: int | str) -> dict | None:
        return self.get_json(f"session:{user_id}")

    # --- Agent Memory ---
    def set_agent_memory(self, agent_name: str, user_id: int | str, memory_data: dict) -> bool:
        return self.set_json(f"agent:{agent_name}:{user_id}", memory_data)

    def get_agent_memory(self, agent_name: str, user_id: int | str) -> dict | None:
        return self.get_json(f"agent:{agent_name}:{user_id}") or {}

    # --- LLM Response Cache ---
    def set_llm_cache(self, prompt: str, response: str, ex: int = 86400) -> bool:
        # Simple hash of the prompt to avoid extremely long keys
        import hashlib
        prompt_hash = hashlib.md5(prompt.encode("utf-8")).hexdigest()
        return self.set(f"llm_cache:{prompt_hash}", response, ex=ex)

    def get_llm_cache(self, prompt: str) -> str | None:
        import hashlib
        prompt_hash = hashlib.md5(prompt.encode("utf-8")).hexdigest()
        return self.get(f"llm_cache:{prompt_hash}")

    # --- Conversation History ---
    def get_conversation_history(self, user_id: int | str, category: str = "interview") -> list:
        key = f"conversation:{category}:{user_id}"
        if self.is_connected:
            try:
                history = self.client.lrange(key, 0, -1)
                return [json.loads(m) for m in history]
            except Exception as e:
                logger.error(f"Redis conversation fetch error: {e}")
        return self.get_json(key) or []

    def add_conversation_message(self, user_id: int | str, message: dict, category: str = "interview") -> bool:
        key = f"conversation:{category}:{user_id}"
        if self.is_connected:
            try:
                self.client.rpush(key, json.dumps(message))
                # Expire after 7 days
                self.client.expire(key, 7 * 86400)
                return True
            except Exception as e:
                logger.error(f"Redis conversation append error: {e}")
        
        hist = self.get_json(key) or []
        hist.append(message)
        return self.set_json(key, hist)

    def clear_conversation_history(self, user_id: int | str, category: str = "interview") -> bool:
        key = f"conversation:{category}:{user_id}"
        return self.delete(key)

    # --- Workflow State (LangGraph Checkpointer) ---
    def set_workflow_state(self, user_id: int | str, state: dict) -> bool:
        return self.set_json(f"workflow_state:{user_id}", state)

    def get_workflow_state(self, user_id: int | str) -> dict | None:
        return self.get_json(f"workflow_state:{user_id}")

    def clear_workflow_state(self, user_id: int | str) -> bool:
        return self.delete(f"workflow_state:{user_id}")

redis_client = RedisClient()
