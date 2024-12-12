from typing import List, Dict, Any

class ElementClient:
    def __init__(self, lossless: bool) -> None: ...

    def start(self, addrs: List[Dict[str, str]], host_by_key: Dict[str, str]) -> None: ...

    def send(
        self,
        message_type: int,
        slot: str,
        process_frame_data: Dict[str, Any],
        route: str,
        content_type: str,
        content: bytes,
        content2: bytes
    ) -> None: ...

    def send_close(self) -> None: ...