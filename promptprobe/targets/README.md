# targets/

Drop your engagement-specific `ChatInterface` subclasses here. Everything in
this directory is gitignored except `__init__.py` and this README, so any
target details (URLs, auth, hostnames) you write here stay local.

Example: create `targets/acme.py`:

```python
from ai_pentest.chat_interface import ChatInterface

class AcmeChat(ChatInterface):
    def send_single_turn(self, prompt: str) -> str:
        r = self._post_json("https://acme.example/chat", json={"msg": prompt})
        return r.json()["reply"]
```

Then run from `promptprobe/`:

```
python run.py --target targets.acme:AcmeChat
```
