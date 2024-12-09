from . import control,camera,lidar

# 동적 로드 관리
import importlib

def load_ai():
    """
    동적으로 ai 모듈을 로드합니다.
    """
    if "ai" not in globals():
        global ai
        ai = importlib.import_module(f"{__name__}.ai")
        print("ai 모듈이 성공적으로 로드되었습니다.")
    return ai