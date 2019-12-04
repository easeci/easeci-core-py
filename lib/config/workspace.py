class WorkspaceContext:
    __instance = None

    def __init__(self):
        raise RuntimeError('Cannot instantiate singleton by constructor!')

    @classmethod
    def get_instance(cls, workspace):
        print(f"==> [EaseCI] workspace mounted in: {workspace}")
        if workspace is None:
            return Exception('Workspace must be initialized value with correct path!')
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
        return cls.__instance
