from .engine import MatchingRuleEngine


class SingletonEngine(MatchingRuleEngine):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(
                SingletonEngine, cls
            ).__new__(cls, *args, **kwargs)
        return cls._instance


engine = MatchingRuleEngine()
get_score = engine.get_name_matching_score