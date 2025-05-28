from abc import ABC, abstractmethod

class RecommendationState(ABC):
    @abstractmethod
    def handle_request(self, context: 'RecommendationContext'):
        pass

class InitialState(RecommendationState):
    def handle_request(self, context: 'RecommendationContext'):
        print("System is in initial state")
        context.set_state(ProcessingState())

class ProcessingState(RecommendationState):
    def handle_request(self, context: 'RecommendationContext'):
        print("Processing recommendations...")
        context.set_state(ReadyState())

class ReadyState(RecommendationState):
    def handle_request(self, context: 'RecommendationContext'):
        print("Recommendations are ready")
        context.set_state(InitialState())

class ErrorState(RecommendationState):
    def handle_request(self, context: 'RecommendationContext'):
        print("An error occurred")
        context.set_state(InitialState())

class RecommendationContext:
    def __init__(self):
        self._state = InitialState()

    def set_state(self, state: RecommendationState):
        self._state = state

    def request(self):
        self._state.handle_request(self) 