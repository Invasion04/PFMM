from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class Expense:
    name: str
    amount: float
    category: str = "Uncategorized"
    date: str = datetime.now().isoformat()
    user_id: str = None
    
    def to_dict(self):
        return asdict(self)