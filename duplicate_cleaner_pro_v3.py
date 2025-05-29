#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Duplicate Cleaner Pro
──────────────────────────────────────────────────────────────────────────────
🗑️  고성능 중복 파일 클리너 (GUI) - Tkinter 기반

    완전 동일한 (바이트 단위 비교) 중복 파일을 찾아 휴지통으로 안전하게
    이동시키는 강력한 GUI 도구입니다. Windows, macOS, Linux 환경에서 호환됩니다.

✨ 주요 기능 및 특징:

    [스캔 및 탐색]
    1.  **백그라운드 스캔 및 진행률**:
        -   선택한 폴더 또는 전체 드라이브를 백그라운드 스레드에서 탐색하여 UI 멈춤 현상을 방지합니다.
        -   진행률 표시줄(Progressbar)을 통해 실시간 진행 상황(%)을 시각적으로 제공합니다.
        -   언제든지 '취소' 버튼으로 진행 중인 스캔 작업을 안전하게 중단할 수 있습니다.
    2.  **다양한 스캔 모드**:
        -   **선택 폴더 스캔**: 사용자가 지정한 특정 폴더와 그 하위 폴더들을 대상으로 스캔합니다.
        -   **전체 드라이브 스캔**: 시스템의 루트 드라이브(예: C:\\ 또는 /) 전체를 스캔합니다.
        -   메모리 효율성과 UI 응답성 유지를 위해 루트의 1단계 하위 폴더들을
            작업 단위로 분할하여 Producer-Consumer 패턴으로 병렬 처리합니다.
    3.  **고급 해시 알고리즘 및 병렬 처리**:
        -   **BLAKE3 자동 감지**: `blake3` 라이브러리가 설치되어 있으면 우선적으로 사용하여
            매우 빠른 해시 계산 속도를 제공합니다. (미설치 시 SHA-256으로 자동 전환)
        -   **멀티프로세스 해싱**: 사용 가능한 CPU 코어 수 (GUI용 1코어 제외) 만큼
            프로세스를 생성하여 해시 계산 작업을 병렬로 수행, 대량 파일 처리 속도를 극대화합니다.
    4.  **효율적인 중복 판별**:
        -   1차: 파일 크기가 동일한 파일들만 후보로 그룹화하여 불필요한 해시 계산을 최소화합니다.
        -   2차: 후보 파일들에 대해서만 선택된 해시 알고리즘(BLAKE3 또는 SHA-256)으로 해시 값을
            계산하여 정확한 중복을 판별합니다.
        -   고급 필터링 옵션 (최소/최대 파일 크기, 포함/제외 확장자 - 고급 설정에서 구성 가능)

    [결과 표시 및 관리 (Tkinter Treeview)]
    5.  **직관적인 결과 트리**:
        -   중복 파일 그룹을 대표 파일명(기본적으로 그룹 내 첫 번째 파일명)으로 묶어 계층적으로 표시합니다.
        -   각 파일의 전체 경로와 그룹별 파일 크기(MB 단위, 소수점 2자리)를 명확하게 보여줍니다.
        -   스캔 중에도 부분 결과를 배치(Batch) 단위로 Treeview에 점진적으로 업데이트합니다. (설정 가능)
        -   그룹당 표시 파일 수 제한 가능 (고급 설정에서 구성)
    6.  **다양한 상호작용**:
        -   **정렬**: '대표 파일명' 또는 '크기' 컬럼 헤더 클릭 시 오름차순/내림차순 정렬 (▲/▼ 표시).
        -   **펼치기/접기**: '모두 펼치기'/'모두 접기' 버튼으로 모든 그룹을 한 번에 제어합니다.
        -   **파일 열기**: 개별 파일을 더블 클릭하여 기본 연결 프로그램으로 실행합니다.
        -   **폴더에서 보기**: 선택한 파일이 위치한 폴더를 OS 파일 탐색기에서 엽니다.
    7.  **유연한 파일 선택 (토글 버튼)**:
        -   **첫 파일 제외 선택**: 각 중복 그룹의 첫 번째 파일을 제외한 모든 중복 파일을 한 번의 클릭으로 빠르게 선택합니다.
        -   **전체 선택 해제**: 모든 선택된 파일을 한 번에 해제합니다. (위 버튼이 토글 형식으로 동작)
    8.  **안전하고 효율적인 삭제**:
        -   선택된 파일들을 운영체제의 **휴지통**으로 이동시킵니다 (`send2trash` 라이브러리 사용).
        -   삭제 전, 대상 파일 수와 총 예상 확보 용량(GB)을 표시하며 사용자 확인을 받습니다.
        -   파일 삭제 후, **전체 재스캔 없이** 현재 목록에서 삭제된 항목만 제거하고,
            중복 세트 개수와 확보 가능 용량을 즉시 업데이트하여 빠른 작업 흐름을 지원합니다.
            (이전 버전과 달리, 삭제 후 전체 재스캔을 하지 않아 사용자 경험 향상)
    9.  **실시간 상태 표시**:
        -   하단 상태 바를 통해 현재 작업 상태(예: "스캔 중...", "폴더 선택"), 스캔 진행률,
            스캔 완료 시 결과 요약(발견된 세트 수, 총 확보 가능 용량, 소요 시간),
            또는 현재 선택된 파일들의 정보(개수, 용량)를 실시간으로 안내합니다.

    [사용자 설정 및 편의 기능]
    10. **고급 설정 메뉴**:
        -   **폴더 선택 후 자동 스캔**: 폴더를 선택하면 즉시 스캔을 시작할지 여부를 설정합니다.
        -   **해시 알고리즘 선택**: BLAKE3 (빠름) 또는 SHA-256 (표준) 중에서 선택합니다. (BLAKE3 미설치 시 안내 및 비활성화)
        -   **멀티프로세스 코어 수 조절**: 해시 계산에 사용할 CPU 코어 수를 사용자가 직접 조절할 수 있습니다.
        -   **트리뷰 배치 크기 설정**: 스캔 중 Treeview에 결과를 표시할 때 한 번에 로드할 파일 수를 설정합니다.
        -   스캔 시 제외할 폴더 목록 지정 (OS별 기본값 제공, 세미콜론으로 구분).
        -   스캔 후 자동 정렬 (정렬 기준 및 방향 설정 가능).
        -   애플리케이션 활동 로깅 (로그 파일 생성 및 로그 레벨 선택 가능).
        -   모든 설정은 파일(`~/.DuplicateCleanerPro/settings.json`)에 자동 저장 및 로드.
        -   모든 설정을 공장 기본값으로 초기화하는 기능 제공.
        -   설정은 '확인'(저장 후 닫기), '적용'(저장 후 유지) 버튼으로 관리.
    11. **창 관리 최적화**: 프로그램 실행 시 내용물에 맞게 창 크기 자동 조절 및 화면 중앙 배치.
    12. **종료 시 확인**: 스캔 작업 중에 프로그램을 종료하려고 하면 사용자에게 확인 메시지를 표시합니다.
    13. **최초 실행 가이드 및 UI/스캔 데이터 초기화**: 프로그램 첫 실행 시 사용법 안내 팝업 제공. 
        메인 화면의 '초기화' 버튼으로 현재 스캔 결과, 선택 사항 등 UI 상태와 내부 데이터를 초기화 (애플리케이션 고급 설정은 유지됨).
──────────────────────────────────────────────────────────────────────────────
"""

# ────────────────────────────── IMPORTS ────────────────────────────────────
import os, sys, hashlib, shutil, threading, queue, subprocess, logging, re, json
import concurrent.futures as cf
import tkinter as tk
import time
import multiprocessing # freeze_support를 위해 추가
from tkinter import ttk, filedialog, messagebox
from collections import defaultdict
from pathlib import Path
from send2trash import send2trash

# blake3 가 가능한 환경이면 자동 사용
try:
    from blake3 import blake3
    USE_BLAKE3 = True
except ModuleNotFoundError:
    USE_BLAKE3 = False            # SHA-256 Fallback

# ────────────────────────────── 상수 설정 ──────────────────────────────────
BUF_SIZE    = 8 * 1024 * 1024                 # 8 MB 스트리밍 버퍼
CPU_WORKERS = max(1, (os.cpu_count() or 4)-1) # GUI 코어 1개 남기기
BATCH_SIZE  = 200                             # 트리뷰 insert batch 크기

# ────────────────────────────── 해시 유틸 ──────────────────────────────────
def fast_hash(path: Path) -> str:
    """
    지정된 파일의 해시를 계산합니다.
    BLAKE3 라이브러리가 사용 가능하면 BLAKE3를, 그렇지 않으면 SHA-256을 사용합니다.
    파일은 BUF_SIZE 단위로 스트리밍하여 메모리 효율적으로 처리합니다.
    """
    h = blake3() if USE_BLAKE3 else hashlib.sha256()
    with path.open('rb') as f:
        while chunk := f.read(BUF_SIZE):
            h.update(chunk)
    return h.hexdigest()

def _hash_and_return(fp: Path) -> tuple[str, Path]:
    """
    멀티프로세스 환경에서 파일 해시 계산을 수행하기 위한 래퍼 함수입니다.
    fast_hash 함수를 호출하고 (해시값, 파일 경로) 튜플을 반환합니다.
    이 함수는 메인 프로세스가 아닌 별도의 프로세스에서 실행될 수 있으므로,
    전역 변수나 클래스 멤버에 직접 접근하지 않도록 주의해야 합니다.
    필요한 모든 정보는 인자로 전달받아야 합니다.
    """
    return fast_hash(fp), fp

# ────────────────────────────── 파일/포맷 유틸 ──────────────────────────────
def parse_extensions(ext_string: str) -> set[str]:
    """
    쉼표로 구분된 확장자 문자열을 파싱하여, 각 확장자 앞에 점(.)을 붙이고
    소문자로 변환한 뒤 중복을 제거한 집합(set) 형태로 반환합니다.
    예: "JPG, png, .gif" -> {".jpg", ".png", ".gif"}
    """
    if not ext_string:
        return set()
    return {f".{ext.strip().lower().lstrip('.')}" for ext in ext_string.split(',') if ext.strip()}

def get_file_logger(log_file_path: Path, level=logging.INFO):
    """
    지정된 경로와 로깅 레벨로 파일 로거(FileLogger)를 설정하고 반환합니다.
    이미 핸들러가 설정된 경우 기존 로거를 반환하여 중복 로깅을 방지합니다.
    로그 파일이 저장될 디렉토리가 없으면 생성합니다.
    """
    logger = logging.getLogger(__name__) # 애플리케이션 로거
    if not logger.handlers: # 핸들러가 이미 설정되어 있지 않은 경우에만 추가
        logger.setLevel(level)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file_path, encoding='utf-8')
        fh.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    # 이미 핸들러가 있다면 기존 로거 반환 (레벨 변경 등은 추가 로직 필요)
    return logger


def bytes_to_human(n: int) -> str:
    """
    바이트 단위의 파일 크기를 사람이 읽기 쉬운 단위(B, KB, MB, GB, TB, PB)로 변환하여
    소수점 둘째 자리까지 표시하는 문자열로 반환합니다.
    """
    for unit in ("B","KB","MB","GB","TB"):
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PB"

def walk_files(root: Path, 
               skip_dirs_set: set[str],
               min_size_bytes: int = 0, 
               max_size_bytes: int = 0,
               include_exts: set[str] = None, 
               exclude_exts: set[str] = None):
    """
    지정된 `root` 디렉토리부터 시작하여 모든 하위 디렉토리를 재귀적으로 탐색하며,
    주어진 필터링 조건(제외 폴더, 최소/최대 파일 크기, 포함/제외 확장자)에 맞는
    정규 파일(regular file)의 경로(Path 객체)를 생성(yield)합니다.
    """
    logger = logging.getLogger(__name__)
    for p in root.rglob('*'):
        # 제외 폴더 확인: 경로의 일부(디렉토리명)가 skip_dirs_set에 포함되어 있으면 해당 경로(파일 또는 디렉토리)를 건너뜁니다.
        # 예: skip_dirs_set = {'node_modules'}. 경로 '/project/node_modules/some_file.js'는 'node_modules'를 포함하므로 건너뜁니다.
        # 디렉토리 자체가 제외 대상이어도, rglob은 그 하위 항목들을 계속 생성할 수 있으나,
        # 각 하위 항목들도 이 동일한 조건에 의해 걸러지게 됩니다.
        if any(skip_dir in p.parts for skip_dir in skip_dirs_set):
            # logger.debug(f"Skipping path due to exclude rule: {p}")
            continue

        if p.is_file():
            try:
                f_size = p.stat().st_size
                f_ext = p.suffix.lower()

                if min_size_bytes > 0 and f_size < min_size_bytes: continue
                if max_size_bytes > 0 and f_size > max_size_bytes: continue
                if include_exts and f_ext not in include_exts: continue
                if exclude_exts and f_ext in exclude_exts: continue
                
                yield p
            except FileNotFoundError: # 스캔 도중 파일이 삭제될 수 있음
                logger.warning(f"File not found during scan: {p}")
                continue

def find_duplicates(root: Path, skip_dirs_set: set[str], min_size_mb: int, max_size_mb: int, include_ext_str: str, exclude_ext_str: str) -> dict[str, list[Path]]:
    """
    지정된 `root` 폴더 내에서 중복 파일을 탐색합니다.
    1. `walk_files`를 통해 필터링 조건에 맞는 파일 목록을 가져옵니다.
    2. 파일 크기가 동일한 파일들끼리 1차 그룹화합니다. (메모리 및 계산 효율성 증대)
    3. 크기가 같은 파일 그룹에 대해서만 `ProcessPoolExecutor`를 사용하여 해시 값을 병렬로 계산합니다.
    4. 계산된 해시 값이 동일하고, 해당 해시 값을 가진 파일이 2개 이상인 경우에만 중복으로 간주합니다.
    결과는 {해시값: [파일_경로_리스트]} 형태의 딕셔너리로 반환됩니다.
    """
    size_map: dict[int, list[Path]] = defaultdict(list)
    # for fp in walk_files(root): # 이 호출은 아래 필터링된 walk_files로 대체됩니다.
    #     size_map[fp.stat().st_size].append(fp)
    min_size_bytes = min_size_mb * 1024 * 1024
    max_size_bytes = max_size_mb * 1024 * 1024 if max_size_mb > 0 else 0 # 0이면 제한 없음
    include_exts = parse_extensions(include_ext_str)
    exclude_exts = parse_extensions(exclude_ext_str)

    for fp in walk_files(root, skip_dirs_set, min_size_bytes, max_size_bytes, include_exts, exclude_exts): # 필터링된 파일 목록 사용
        size_map[fp.stat().st_size].append(fp)
    hash_map: dict[str, list[Path]] = defaultdict(list)
    with cf.ProcessPoolExecutor(max_workers=CPU_WORKERS) as pool:
        futs = [pool.submit(_hash_and_return, f)
                for files in size_map.values() if len(files) > 1
                for f in files]
        for fut in cf.as_completed(futs):
            h, fp = fut.result()
            hash_map[h].append(fp)

    return {h: lst for h, lst in hash_map.items() if len(lst) > 1}

# ─────────────────────────── 프로듀서/컨슈머 (드라이브 분할) ────────────────
def producer(root: Path, q: queue.Queue):
    """
    [Producer 스레드용 함수]
    전체 드라이브 스캔 시, 지정된 `root` 디렉토리의 1단계 하위 폴더들을 작업 큐(`q`)에 넣습니다.
    루트 디렉토리 자체에 있는 파일들을 처리하기 위해 루트 경로도 큐에 추가합니다.
    모든 폴더를 추가한 후에는 작업 종료를 알리는 `None` 마커를 큐에 넣습니다.
    이 함수는 메인 스레드와 다른 스레드에서 실행됩니다.
    """
    # skip_dirs_set은 메인 스레드의 DuplicateCleaner 인스턴스에서 가져와야 함.
    # 여기서는 인자로 전달받는다고 가정하거나, 또는 consumer에서 필터링하도록 수정.
    # 지금은 consumer에서 필터링하도록 find_duplicates 호출 시 넘겨줌.
    for entry in root.iterdir():
        if entry.is_dir():  # TODO: 여기서도 skip_dirs_set을 확인하여 초기에 제외할 수 있음
            q.put(entry)    # 하위 폴더를 큐에 추가
    q.put(root)             # 루트에 직접 있는 파일
    q.put(None)             # 종료 마커

def consumer(q_in: queue.Queue, q_out: queue.Queue, 
             skip_dirs_set: set[str], min_size_mb: int, max_size_mb: int, include_ext_str: str, exclude_ext_str: str,
             stop_evt: threading.Event):
    """
    [Consumer 스레드용 함수]
    작업 큐(`q_in`)에서 폴더 경로를 가져와 `find_duplicates` 함수를 호출하여 중복 파일을 탐색합니다.
    탐색 결과는 ("chunk", 결과_딕셔너리) 형태로 출력 큐(`q_out`)에 넣습니다.
    `stop_evt` 이벤트가 설정되거나 큐에서 `None` 마커를 받으면 작업을 종료합니다.
    """
    while not stop_evt.is_set():
        folder = q_in.get() # 작업 큐에서 폴더 가져오기
        if folder is None:
            break           # 종료 마커를 만나면 루프 종료
        q_out.put(("chunk", find_duplicates(folder, skip_dirs_set, min_size_mb, max_size_mb, include_ext_str, exclude_ext_str)))
class DuplicateCleaner(tk.Tk):
    """
    Tkinter 기반의 중복 파일 클리너 애플리케이션 메인 클래스입니다.
    사용자 인터페이스(UI) 구성, 스캔 로직 실행, 결과 표시, 파일 삭제 등 모든 기능을 관리합니다.
    """
    # ── 생성자
    def __init__(self):
        super().__init__()
        self.title("Duplicate Cleaner Pro")

        # ── 상태 변수
        self.target_dir  = tk.StringVar()            # 스캔 대상 폴더 경로 (UI 바인딩용)
        self.status      = tk.StringVar(value="폴더를 선택하세요.") # 하단 상태 바 메시지 (UI 바인딩용)
        self.progress    = tk.DoubleVar(value=0.0)   # 진행률 표시 바 값 (0.0 ~ 1.0, UI 바인딩용)

        self.duplicates: dict[str, list[Path]] = {}  # 탐색된 중복 파일 그룹 {해시: [경로 리스트]}
        self.reclaim_bytes = 0                       # 중복 파일을 삭제했을 때 확보 가능한 총 바이트 수

        self.sort_column  = None                     # 현재 트리뷰 정렬 기준 컬럼 ID (예: "#0" 또는 "size")
        self.sort_reverse = False                    # 현재 정렬 방향 (True: 내림차순, False: 오름차순)
        self.all_expanded = False                    # 트리뷰 그룹 전체 펼침/접힘 상태 (True: 모두 펼침)
        self.select_toggle_state = False             # '첫 파일 제외 선택' / '전체 선택 해제' 버튼의 토글 상태 (False: '첫 파일 제외 선택' 표시)
        self.scanning = False                        # 현재 스캔 작업 진행 중 여부 플래그

        self._performing_bulk_select = False         # 대량 선택 작업 진행 여부 플래그
        # 창 종료 시 호출될 콜백
        self.last_scan_duration = None # 마지막 스캔 소요 시간 저장용
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # 백그라운드 스캔 작업용 큐 및 이벤트 객체
        self.work_q = self.out_q = None # 작업 큐(producer-consumer용), 출력 큐(결과 수집용)
        self.stop_evt = None
        self.total_chunks = self.finished_chunks = 0
        
        # 설정 변수들을 __init__ 상단에서 먼저 정의
        self.auto_scan   = tk.BooleanVar(value=False) 
        self.hash_algo   = tk.StringVar(value="blake3" if USE_BLAKE3 else "sha256")
        self.core_count  = tk.IntVar(value=CPU_WORKERS)
        self.batch_size  = tk.IntVar(value=BATCH_SIZE)
        
        default_skip = ("$RECYCLE.BIN;System Volume Information"
                        if os.name == 'nt'
                        else ".Trashes;.Spotlight-V100;.fseventsd;System;.DS_Store")
        self.skip_dirs   = tk.StringVar(value=default_skip)

        # 고급 설정 변수들
        self.min_file_size_mb = tk.IntVar(value=0) # MB 단위, 0이면 제한 없음
        self.max_file_size_mb = tk.IntVar(value=0) # MB 단위, 0이면 제한 없음
        self.include_extensions = tk.StringVar(value="") # 예: jpg,png,gif
        self.exclude_extensions = tk.StringVar(value="") # 예: tmp,log,bak

        self.auto_sort_after_scan = tk.BooleanVar(value=False)
        self.auto_sort_column = tk.StringVar(value="name") # 'name' 또는 'size'
        self.auto_sort_direction = tk.BooleanVar(value=False) # False: 오름차순, True: 내림차순

        self.max_files_per_group_display = tk.IntVar(value=0) # 0이면 모두 표시

        self.enable_logging = tk.BooleanVar(value=False)
        self.log_level = tk.StringVar(value="INFO") # DEBUG, INFO, WARNING, ERROR
        
        self._load_settings_from_file() # 프로그램 시작 시 설정 불러오기
        self._build_widgets()
        self._check_first_run_and_show_guide() # 첫 실행 가이드 팝업
        self._set_min_size()
        self.center_window() # 창 크기 설정 후 중앙 정렬

    # ── UI 레이아웃
    def _build_widgets(self):
        """
        애플리케이션의 주요 GUI 위젯들을 생성하고 배치합니다.
        상단 컨트롤(폴더 선택, 스캔 버튼), 상태 바, 진행률 바, 메뉴바, Treeview, 하단 버튼 등을 설정합니다.
        """
        ## 상단 컨트롤
        top = ttk.Frame(self); top.pack(fill='x', padx=10, pady=10)
        ttk.Label(top, text="대상 폴더:").pack(side='left')
        ttk.Entry(top, textvariable=self.target_dir, width=60).pack(side='left', padx=5)
        ttk.Button(top, text="찾아보기…", command=self.browse).pack(side='left')
        self.btn_scan   = ttk.Button(top, text="스캔", command=self.start_scan)
        self.btn_drive  = ttk.Button(top, text="전체 드라이브 스캔", command=self.confirm_full_scan)
        self.btn_scan.pack(side='left', padx=5)
        self.btn_drive.pack(side='left', padx=(0,5))
        self.btn_cancel = ttk.Button(top, text="취소", command=self.cancel_scan)
        self.btn_cancel.pack(side='left', padx=(0,16))
        ## 상태 + 진행률
        ttk.Label(self, textvariable=self.status).pack(anchor='w', padx=12, pady=(0,4))
        ttk.Progressbar(self, variable=self.progress, maximum=1.0,
                        mode="determinate").pack(fill='x', padx=(10,27), pady=(0,8)) # padx를 12에서 10으로 변경
        
        ## 메뉴바
        menubar = tk.Menu(self); self.config(menu=menubar)
        menubar.add_command(label=" 고급 설정", command=self.open_settings) 
        
        # 설정 변수 정의는 __init__ 상단으로 이동됨

        ## 트리뷰
        cols=("path","size")
        self.tree = ttk.Treeview(self, columns=cols, show='tree headings', selectmode='extended')
        self.tree.heading("#0", text="대표 파일명 (정렬 가능)",
                          command=lambda: self._on_header("#0"))
        self.tree.heading("path", text="File Path")
        self.tree.heading("size", text="Size (MB) (정렬 가능)",
                          command=lambda: self._on_header("size"))
        self.tree.column("#0", width=300); self.tree.column("path", width=200)
        self.tree.column("size", width=100, anchor='e')
        self.tree.bind("<Double-1>", self._open_file)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_selection_changed)

        ysb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb.set)
        ysb.pack(side='right', fill='y'); self.tree.pack(expand=True, fill='both', padx=10)

        ## 하단 버튼
        bottom = ttk.Frame(self)
        bottom.pack(fill='x', pady=10)

        # ▼ 토글 버튼 하나만 생성 – 위젯 객체를 변수에 잡아둠
        self.select_toggle_btn = ttk.Button(
                bottom, text="첫 파일 제외 선택",
                command=self.toggle_select)
        self.select_toggle_btn.pack(side='left', padx=10)

        # 나머지 버튼은 그대로
        self.toggle_btn = ttk.Button(bottom, text="모두 펼치기",
                                    command=self.toggle_expand_all)
        self.toggle_btn.pack(side='left', padx=(0,10))
        ttk.Button(bottom, text="초기화",
                   command=self.reset_application_state).pack(side='left', padx=(0, 10))

        self.btn_delete_selected = ttk.Button(bottom, text="선택 파일 휴지통 이동",
                                              command=self.delete_selected)
        self.btn_delete_selected.pack(side='right', padx=10)

        ttk.Button(bottom, text="폴더에서 보기",
                   command=self._open_selected_in_folder).pack(side='right')
    
    # ── 버튼 잠금/해제 메서드 (클래스 레벨)
    def _disable_scan_buttons(self):
        """스캔 진행 중에 관련 버튼들을 비활성화하고, 취소 버튼을 활성화합니다."""
        self.btn_scan.configure(state="disabled")
        self.btn_drive.configure(state="disabled")
        self.btn_cancel.configure(state="normal") # 취소 버튼은 활성화
        self.select_toggle_btn.configure(state="disabled")
        self.btn_delete_selected.configure(state="disabled")

    def _enable_scan_buttons(self):
        """스캔이 중단되거나 완료되었을 때 관련 버튼들을 활성화하고, 취소 버튼을 비활성화합니다."""
        self.btn_scan.configure(state="normal")
        self.btn_drive.configure(state="normal")
        self.btn_cancel.configure(state="disabled") # 스캔 안 할땐 취소 버튼 비활성화
        self.select_toggle_btn.configure(state="normal")
        self.btn_delete_selected.configure(state="normal")

    # ── 창 사이즈 최적화
    def _set_min_size(self):
        """
        애플리케이션 창의 초기 최소 크기를 설정합니다.
        모든 위젯이 렌더링된 후 필요한 최소 너비와 높이를 계산하여,
        창이 너무 작게 시작되어 내용이 잘리는 것을 방지합니다.
        """
        self.update_idletasks()                 # 모든 위젯 실제 크기 계산
        w = self.winfo_reqwidth()               # 루트 윈도우 요구 너비
        h = self.winfo_reqheight()              # 루트 윈도우 요구 높이
        self.minsize(w, h)                      # 최소 크기 고정
        self.geometry(f"{w}x{h}")               # 첫 표시 크기 = 요구 크기

    def center_window(self):
        """애플리케이션 창을 화면 중앙에 배치합니다."""
        self.update_idletasks() # 창 크기 정보 업데이트
        width = self.winfo_width()
        height = self.winfo_height()
        x_offset = (self.winfo_screenwidth() // 2) - (width // 2)
        y_offset = (self.winfo_screenheight() // 2) - (height // 2)
        # geometry 메서드는 이미 _set_min_size에서 호출되었으므로,
        # 여기서는 위치만 조정하거나, 크기와 위치를 함께 다시 설정할 수 있습니다.
        # 여기서는 크기와 위치를 함께 설정합니다.
        self.geometry(f'{width}x{height}+{x_offset}+{y_offset}')

    # ── 폴더 선택
    def browse(self):
        """
        '찾아보기...' 버튼 클릭 시 호출됩니다.
        폴더 선택 대화상자를 열고, 사용자가 폴더를 선택하면 해당 경로를 UI에 표시합니다.
        만약 "폴더 선택 후 자동 스캔" 옵션이 켜져 있다면, 폴더 선택 후 즉시 스캔을 시작합니다.
        """
        p = filedialog.askdirectory()
        if p:
            self.target_dir.set(p)
            if self.auto_scan.get(): # "폴더 선택 후 자동 스캔" 옵션이 켜져 있으면
                self.start_scan()    # 바로 스캔 시작

    # ── 일반 스캔(선택 폴더)
    def start_scan(self):
        """
        '스캔' 버튼 클릭 시 또는 자동 스캔 옵션에 의해 호출됩니다.
        사용자가 지정한 단일 폴더에 대해 중복 파일 스캔을 시작합니다.
        폴더 유효성을 검사하고, 스캔 준비 상태로 UI를 변경한 후 백그라운드 스캔 스레드를 시작합니다.
        """
        if self.scanning: # 재진입 차단
            messagebox.showinfo("알림", "이미 스캔이 진행 중입니다.")
            return

        # ── 폴더 유효성 확인 ──────────────────────────
        folder_path_str = self.target_dir.get().strip()
        if not folder_path_str: # 경로가 비어있으면 찾아보기 호출
            self.browse()
            folder_path_str = self.target_dir.get().strip()
            if not folder_path_str: # 여전히 비어있으면 종료
                return

        folder = Path(folder_path_str)
        if not folder.is_dir(): # 디렉토리인지 확인
            messagebox.showerror("오류", f"유효한 폴더를 선택하세요.\n선택한 경로: {folder}")
            return

        # ── 스캔 시작 준비 OK → 버튼 잠금 & 플래그 세팅 ──
        self._disable_scan_buttons()
        self.scanning = True
        self._kickoff_threaded_scan([folder])

    # ── 전체 드라이브 스캔
    def confirm_full_scan(self):
        """
        '전체 드라이브 스캔' 버튼 클릭 시 호출됩니다.
        시스템의 루트 드라이브 전체를 스캔하기 전에 사용자에게 확인을 받습니다.
        확인 후, 프로듀서-컨슈머 패턴을 사용하는 백그라운드 스캔 스레드를 시작합니다.
        """
        if self.scanning:
            messagebox.showinfo("알림", "현재 스캔이 진행 중입니다.")
            return

        # 루트 경로 계산 (OS 별)
        root = Path("C:\\") if os.name == 'nt' else Path("/")
        gb   = shutil.disk_usage(root).total / (1024**3)

        # ── 사용자 확인 먼저 ──
        if not messagebox.askyesno(
                "전체 드라이브 스캔",
                f"{root} 전체({gb:,.0f} GB)를 스캔하시겠습니까?\n"
                "완료까지 시간이 걸릴 수 있습니다."):
            return  # 사용자가 ‘아니오’ 선택

        # ── 여기서부터 실제 스캔 시작 ──
        self._disable_scan_buttons()
        self.scanning = True
        self._kickoff_drive_scan(root)

    # ── 취소
    def cancel_scan(self):
        """
        '취소' 버튼 클릭 시 호출됩니다.
        현재 진행 중인 백그라운드 스캔 작업에 중단 신호(Event)를 보냅니다.
        """
        if self.stop_evt and not self.stop_evt.is_set():
            self.stop_evt.set() # 백그라운드 스레드에 중단 신호 전송
            self.status.set("스캔 취소 중...")
            self.btn_cancel.configure(state="disabled") # 취소 버튼 즉시 비활성화
            # 스캔이 실제로 멈추면 _enable_scan_buttons가 호출되어 정리됨
        self.scanning = False # 스캔 상태 플래그 해제
        # self._enable_scan_buttons() # 여기서 바로 호출하면 너무 빠를 수 있음. 폴링 루프 종료 시 처리.

    # ── 시간 측정
    def start_scan_timer(self):
        """스캔 시작 시간을 기록합니다. (현재는 _kickoff_... 함수 내에서 직접 처리)"""
        self.scan_start = time.perf_counter()

    # ── 스캐너 스타터 2종
    def _kickoff_threaded_scan(self, folders:list[Path]):
        """
        단일 폴더 또는 소규모 폴더 목록에 대한 스캔을 시작합니다.
        하나의 백그라운드 스레드에서 주어진 폴더들을 순차적으로 처리합니다.
        스캔 시작 전 상태를 초기화하고, UI 버튼을 비활성화하며,
        결과를 수신할 출력 큐와 중단 이벤트를 설정합니다.
        작업 완료 후에는 `_poll_out` 메소드를 통해 결과를 처리합니다.
        """
        self.scan_start = time.perf_counter()
        self._reset_state()
        self._disable_scan_buttons() # 버튼 비활성화
        self.stop_evt   = threading.Event() # 스캔 중단용 이벤트 객체
        self.out_q      = queue.Queue()
        self.total_chunks = len(folders)
        
        skip_dirs_set = set(self.skip_dirs.get().split(';')) if self.skip_dirs.get() else set()
        min_mb, max_mb = self.min_file_size_mb.get(), self.max_file_size_mb.get()
        inc_ext, exc_ext = self.include_extensions.get(), self.exclude_extensions.get()
        def worker():
            for idx, f in enumerate(folders, 1):
                if self.stop_evt.is_set(): break
                self.out_q.put(("chunk", find_duplicates(f, skip_dirs_set, min_mb, max_mb, inc_ext, exc_ext)))
                self.out_q.put(("prog", idx/self.total_chunks))
            self.out_q.put(("done", None))
        threading.Thread(target=worker, daemon=True).start() # 데몬 스레드로 실행
        self.after(100, self._poll_out) # 출력 큐 폴링 시작

    def _kickoff_drive_scan(self, root: Path):
        """
        전체 드라이브 스캔을 시작합니다.
        프로듀서-컨슈머 패턴을 사용하여 드라이브의 1단계 하위 폴더들을 작업 단위로 분할하고,
        여러 컨슈머 스레드(각 스레드는 내부적으로 `find_duplicates`를 통해 멀티프로세싱 활용 가능)에서 병렬로 처리합니다.
        스캔 시작 전 상태를 초기화하고, UI 버튼을 비활성화하며,
        작업 큐, 출력 큐, 중단 이벤트를 설정합니다.
        """
        self.scan_start = time.perf_counter()
        self._reset_state()
        self._disable_scan_buttons() # 버튼 비활성화
        self.stop_evt = threading.Event()
        self.work_q   = queue.Queue()
        self.out_q    = queue.Queue()

        skip_dirs_set = set(self.skip_dirs.get().split(';')) if self.skip_dirs.get() else set()
        min_mb, max_mb = self.min_file_size_mb.get(), self.max_file_size_mb.get()
        inc_ext, exc_ext = self.include_extensions.get(), self.exclude_extensions.get()

        # Producer: 폴더를 work_q에 push
        threading.Thread(target=producer,
                         args=(root, self.work_q), daemon=True).start()

        # Consumer: find_duplicates 병렬 실행
        for _ in range(self.core_count.get()): # 설정된 코어 수 사용
            threading.Thread(target=consumer,
                             args=(self.work_q, self.out_q, skip_dirs_set, min_mb, max_mb, inc_ext, exc_ext, self.stop_evt),
                             daemon=True).start()

        self.total_chunks = sum(1 for _ in root.iterdir() if _.is_dir()) + 1 # 루트의 하위 폴더 개수 + 루트 자체
        self.after(100, self._poll_out) # 출력 큐 폴링 시작

    # ── 첫 파일 제외 선택' ↔ '전체 선택 해제' 토글
    def toggle_select(self):
        """
        '첫 파일 제외 선택' / '전체 선택 해제' 버튼의 토글 기능을 수행합니다.
        - "첫 파일 제외 선택" 모드: 각 중복 그룹의 첫 번째 파일을 제외한 모든 파일을 선택합니다. `selection_set`을 사용하여 빠르게 처리합니다.
        - "전체 선택 해제" 모드: 현재 선택된 모든 파일을 해제합니다.
        선택 작업 후에는 상태 바를 업데이트하고 사용자에게 알림 메시지를 표시합니다.
        """
        # "첫 파일 제외 선택" (select_toggle_state가 False일 때)
        if not self.select_toggle_state:
            
            self._performing_bulk_select = True # 대량 선택 시작 플래그
            try:
                # 기존 선택 모두 제거 (selection_set은 기존 선택을 대체하므로 명시적 제거는 선택사항이나,
                # 만약 selection_add와 혼용하거나 다른 시나리오를 고려한다면 유지하는 것이 안전할 수 있음)
                # self.tree.selection_remove(self.tree.selection()) # selection_set 사용 시 이 줄은 불필요할 수 있음

                to_select = []
                for g in self.tree.get_children(''):
                    children = self.tree.get_children(g)
                    if len(children) > 1: # 자식 노드가 2개 이상일 때만 (첫 파일 제외 의미)
                        to_select.extend(children[1:])
                
                if to_select:
                    self.tree.selection_set(to_select) # 한 번에 모든 대상 아이템 선택
                else: # 선택할 아이템이 없는 경우 (예: 모든 그룹이 파일 1개씩만 가짐)
                    self.tree.selection_remove(self.tree.selection()) # 모든 선택 해제

            finally:
                self._performing_bulk_select = False # 대량 선택 종료 플래그

            self.select_toggle_state = True
            self.select_toggle_btn.config(text="전체 선택 해제")
            
            count = len(self.tree.selection())
            
            # 상태바는 파일 개수만 빠르게 업데이트 (calculate_size_override=False로 용량 계산 방지)
            self._on_tree_selection_changed(calculate_size_override=False)
            messagebox.showinfo("선택 완료", # 상태바 업데이트 후 메시지 박스 표시
                                f"{count}개 파일이 선택되었습니다.")
        else:
            # "전체 선택 해제" (select_toggle_state가 True일 때)
            self.tree.selection_remove(self.tree.selection())
            self.select_toggle_state = False
            self.select_toggle_btn.config(text="첫 파일 제외 선택")
            messagebox.showinfo("선택 해제", "모든 선택이 해제되었습니다.")
            self._on_tree_selection_changed(calculate_size_override=True) # 상태바 업데이트 (스캔 요약 등 표시)

    # ── 상태 초기화
    def _reset_state(self):
        """
        새로운 스캔 작업을 시작하기 전에 애플리케이션의 내부 상태와 UI의 일부를 초기화합니다.
        Treeview 내용, 중복 파일 데이터, 확보 가능 용량, 진행률, 상태 메시지 등을 리셋합니다.
        """
        self.tree.delete(*self.tree.get_children())
        self.duplicates.clear(); self.reclaim_bytes = 0
        self.finished_chunks = 0
        self.status.set("스캔 중… 잠시만 기다려 주세요."); self.progress.set(0)
        self.last_scan_duration = None # 스캔 시간 초기화
        self.select_toggle_state = False # 선택 토글 버튼 상태 초기화
        self.select_toggle_btn.config(text="첫 파일 제외 선택")
        self._enable_scan_buttons() # 초기에는 스캔 버튼 활성화, 취소는 비활성화

    def reset_application_state(self):
        """
        사용자가 '초기화' 버튼을 눌렀을 때 호출됩니다.
        진행 중인 스캔이 있다면 사용자 확인 후 취소하고, Treeview 내용, 내부 데이터(중복 파일, 용량, 스캔 시간),
        선택된 폴더 경로, UI 상태(상태 바, 진행률, 정렬, 펼치기/접기, 선택 토글)를 모두 초기 상태로 되돌립니다.
        """
        if self.scanning:
            if messagebox.askyesno("초기화 확인", "스캔이 진행 중입니다. 취소하고 모든 상태를 초기화하시겠습니까?"):
                self.cancel_scan() # 진행 중인 스캔 취소
            else:
                return # 사용자가 취소하면 초기화하지 않음

        # Treeview 비우기
        self.tree.delete(*self.tree.get_children())

        # 내부 데이터 초기화
        self.duplicates.clear()
        self.reclaim_bytes = 0
        self.last_scan_duration = None
        self.target_dir.set("") # 대상 폴더 경로 초기화

        # UI 상태 초기화
        self.status.set("폴더를 선택하세요.")
        self.progress.set(0.0)
        self._reset_sorting_state() # 정렬 상태 초기화 및 헤더 업데이트
        self._reset_expansion_state() # 펼치기/접기 상태 초기화
        self._reset_selection_toggle_state() # 선택 토글 버튼 초기화
        self._enable_scan_buttons() # 버튼 상태 초기화

    # ── 설정 창
    def open_settings(self):
        """
        '고급 설정' 메뉴(또는 버튼) 클릭 시 호출됩니다.
        탭(Notebook)으로 구성된 설정 창을 생성하여 사용자에게 다양한 옵션
        (일반, 필터링, 고급)을 제공하고, 설정을 적용하거나 취소할 수 있도록 합니다.
        """
        win = tk.Toplevel(self); win.title("고급 설정")
        
        notebook = ttk.Notebook(win)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # --- 일반 탭 ---
        tab_general = ttk.Frame(notebook); notebook.add(tab_general, text="일반")

        tab_general.columnconfigure(1, weight=1)  # 오른쪽 열 확장 허용

        # 폴더 자동 스캔
        ttk.Checkbutton(tab_general, text="폴더 선택 후 자동 스캔", variable=self.auto_scan).grid(
            row=0, column=0, columnspan=2, sticky='w', pady=5, padx=5
        )

        # 해시 알고리즘 선택 박스 (LabelFrame 전체 너비)
        lf_hash = ttk.LabelFrame(tab_general, text="해시 알고리즘")
        lf_hash.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky='ew')
        ttk.Radiobutton(lf_hash, text="BLAKE3 (빠름)", variable=self.hash_algo, value="blake3").pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(lf_hash, text="SHA-256 (표준)", variable=self.hash_algo, value="sha256").pack(anchor='w', padx=5, pady=2)
        if not USE_BLAKE3:
            blake3_radio = lf_hash.winfo_children()[0]
            blake3_radio.configure(state='disabled')
            ttk.Label(lf_hash, text="BLAKE3 미설치 (pip install blake3 권장)", foreground="gray", font=("Segoe UI", 8)).pack(anchor='w', padx=25, pady=(0,2))

        # 멀티코어
        ttk.Label(tab_general, text="멀티프로세스 코어 수:").grid(row=2, column=0, sticky='w', pady=5, padx=5)
        ttk.Spinbox(tab_general, from_=1, to=os.cpu_count() or 1, textvariable=self.core_count, width=7).grid(
            row=2, column=1, sticky='e', pady=5, padx=5
        )

        # 트리뷰 배치 크기
        ttk.Label(tab_general, text="스캔 중 트리뷰 배치 크기:").grid(row=3, column=0, sticky='w', pady=5, padx=5)
        ttk.Combobox(tab_general, values=(50, 100, 200, 500, 1000), textvariable=self.batch_size, state='readonly', width=7).grid(
            row=3, column=1, sticky='e', pady=5, padx=5
        )

        # 자동 정렬 (LabelFrame 전체 너비)
        lf_autosort = ttk.LabelFrame(tab_general, text="스캔 후 자동 정렬")
        lf_autosort.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky='ew')

        ttk.Checkbutton(lf_autosort, text="활성화", variable=self.auto_sort_after_scan).grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=2)

        # 정렬 기준
        autosort_criteria_frame = ttk.Frame(lf_autosort)
        autosort_criteria_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5)
        ttk.Label(autosort_criteria_frame, text="기준:").pack(side='left', pady=2)
        ttk.Combobox(autosort_criteria_frame, values=("대표 파일명", "크기"), textvariable=self.auto_sort_column, state='readonly', width=12).pack(side='left', padx=5, pady=2)

        # 정렬 방향
        autosort_dir_frame = ttk.Frame(lf_autosort)
        autosort_dir_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=5)
        ttk.Label(autosort_dir_frame, text="방향:").pack(side='left', pady=2)
        ttk.Radiobutton(autosort_dir_frame, text="오름차순", variable=self.auto_sort_direction, value=False).pack(side='left', padx=(5,0), pady=2)
        ttk.Radiobutton(autosort_dir_frame, text="내림차순", variable=self.auto_sort_direction, value=True).pack(side='left', padx=5, pady=2)

        # --- 필터링 탭 ---
        tab_filter = ttk.Frame(notebook); notebook.add(tab_filter, text="필터링")

        # 필터링 탭 내용
        ttk.Label(tab_filter, text="최소 파일 크기 (MB, 0=제한없음):").grid(row=0, column=0, sticky='w', pady=5, padx=5)
        ttk.Spinbox(tab_filter, from_=0, to=1024*10, increment=1, textvariable=self.min_file_size_mb, width=10).grid(row=0, column=1, sticky='e', pady=5, padx=5)
        ttk.Label(tab_filter, text="최대 파일 크기 (MB, 0=제한없음):").grid(row=1, column=0, sticky='w', pady=5, padx=5)
        ttk.Spinbox(tab_filter, from_=0, to=1024*100, increment=10, textvariable=self.max_file_size_mb, width=10).grid(row=1, column=1, sticky='e', pady=5, padx=5)

        ttk.Label(tab_filter, text="포함할 확장자 (예: jpg,png):").grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.entry_include_ext = ttk.Entry(tab_filter, textvariable=self.include_extensions, width=25); self.entry_include_ext.grid(row=2, column=1, sticky='ew', pady=5, padx=5)
        ttk.Label(tab_filter, text="제외할 확장자 (예: log,tmp):").grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.entry_exclude_ext = ttk.Entry(tab_filter, textvariable=self.exclude_extensions, width=25); self.entry_exclude_ext.grid(row=3, column=1, sticky='ew', pady=5, padx=5)

        ttk.Label(tab_filter, text="제외 폴더 목록 (; 구분):").grid(row=4, column=0, columnspan=2, sticky='w', pady=(10,2), padx=5)
        self.txt_skip_dirs = tk.Text(tab_filter, width=38, height=4); self.txt_skip_dirs.insert('1.0', self.skip_dirs.get())
        self.txt_skip_dirs.grid(row=5, column=0, columnspan=2, pady=2, padx=5, sticky='ew')
        # 필터링 탭 컬럼 가중치 설정 (Entry가 늘어나도록)
        tab_filter.columnconfigure(1, weight=1)

        # --- 고급 탭 ---
        tab_advanced = ttk.Frame(notebook); notebook.add(tab_advanced, text="고급")

        # 고급 탭 내용
        ttk.Label(tab_advanced, text="그룹당 최대 표시 파일 수 (0=모두):").grid(row=0, column=0, sticky='w', pady=5, padx=5)
        ttk.Spinbox(tab_advanced, from_=0, to=1000, increment=10, textvariable=self.max_files_per_group_display, width=10).grid(row=0, column=1, sticky='e', pady=5, padx=5)

        lf_logging = ttk.LabelFrame(tab_advanced, text="로깅"); lf_logging.grid(row=3, column=0, columnspan=2, pady=(10,5), padx=5, sticky='ew')
        ttk.Checkbutton(lf_logging, text="로그 파일 사용", variable=self.enable_logging).grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        
        log_level_frame = ttk.Frame(lf_logging); log_level_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5)
        ttk.Label(log_level_frame, text="로그 레벨:").pack(side='left', pady=2)
        ttk.Combobox(log_level_frame, values=("DEBUG", "INFO", "WARNING", "ERROR"), textvariable=self.log_level, state='readonly', width=12).pack(side='left', padx=5, pady=2)

        # --- 설정 저장/적용/취소 버튼 ---
        btn_frame = ttk.Frame(win)
        btn_frame.pack(side='bottom', fill='x', padx=10, pady=(0,10), anchor='e')

        def _internal_apply_settings(): # 설정 적용 로직 (이전과 동일)
            self.skip_dirs.set(self.txt_skip_dirs.get('1.0','end-1c').strip())
            
            # 로깅 설정 적용
            if self.enable_logging.get():
                log_file = Path.home() / ".DuplicateCleanerPro" / "app.log"
                log_level_str = self.log_level.get()
                level_map = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR}
                logger = get_file_logger(log_file, level_map.get(log_level_str, logging.INFO))
                logger.info("Settings applied.")
            else: # 로깅 비활성화 시 핸들러 제거 (선택적)
                logger = logging.getLogger(__name__)
                for handler in logger.handlers[:]: # 복사본으로 반복하여 안전하게 제거
                    if isinstance(handler, logging.FileHandler):
                        logger.removeHandler(handler)
                        handler.close()
                logger.info("Logging disabled by user setting.")

            # CPU_WORKERS 전역 변수 업데이트 (ProcessPoolExecutor 생성 시 사용)
            global CPU_WORKERS
            CPU_WORKERS = self.core_count.get()

            # 해시 알고리즘 변경에 따라 fast_hash가 사용할 전역 USE_BLAKE3 플래그 업데이트
            global USE_BLAKE3
            # 프로그램 시작 시 blake3 모듈 사용 가능 여부에 따라 고급 설정의 BLAKE3 라디오 버튼이 활성화/비활성화됩니다.
            # 사용자가 BLAKE3를 선택했다면, 이는 시작 시 사용 가능했음을 의미합니다.
            # (UI에서 비활성화된 옵션은 선택할 수 없으므로)
            if self.hash_algo.get() == "blake3":
                USE_BLAKE3 = True
            else: # SHA-256 선택
                USE_BLAKE3 = False
            self._save_settings_to_file() # 설정 변경 시 파일에 저장

        def apply_action_with_confirmation():
            _internal_apply_settings()
            messagebox.showinfo("설정 저장됨", "설정이 성공적으로 적용 및 저장되었습니다.", parent=win)
            # 창은 닫지 않음

        # "확인" 버튼 제거
        # "적용" 버튼: 설정 적용, 팝업 알림, 창 유지
        ttk.Button(btn_frame, text="적용", command=apply_action_with_confirmation).pack(side='right', padx=2)
        ttk.Button(btn_frame, text="모든 설정 초기화", command=lambda: self.reset_all_settings_to_default(win)).pack(side='left', padx=(0,10))

        win.transient(self) # 부모 창 위에 표시

        # Toplevel 창 중앙 정렬
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x_offset = (win.winfo_screenwidth() // 2) - (width // 2)
        y_offset = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x_offset}+{y_offset}')

        win.grab_set()      # 모달 창으로 만듦
        
        def on_settings_close():
            win.destroy()
        win.protocol("WM_DELETE_WINDOW", on_settings_close) # 창 닫기(X) 버튼 클릭 시 호출

        
    def _check_first_run_and_show_guide(self):
        """
        프로그램 첫 실행 여부를 확인하고, 첫 실행일 경우 사용자에게 간단한 시작 가이드 팝업을 표시합니다.
        첫 실행 여부는 사용자 홈 디렉토리 내 `.DuplicateCleanerPro` 폴더의 마커 파일을 통해 판단합니다.
        파일 시스템 오류 발생 시에는 콘솔에만 경고를 출력하고 프로그램 실행은 계속합니다.
        """
        try:
            app_data_dir = Path.home() / ".DuplicateCleanerPro"
            app_data_dir.mkdir(parents=True, exist_ok=True) # 설정 폴더 생성 (이미 있으면 무시)
            marker_file = app_data_dir / ".first_run_complete.marker"

            if not marker_file.exists():
                guide_message = (
                    "**Duplicate Cleaner Pro 시작 가이드**\n\n"
                    "1. '찾아보기'로 스캔할 폴더를 선택하거나,\n"
                    "   '전체 드라이브 스캔'을 사용하세요.\n\n"
                    "2. '스캔' 버튼으로 중복 파일 검색을 시작합니다.\n\n"
                    "3. 결과 확인 후, '첫 파일 제외 선택' 버튼 등으로\n"
                    "   정리할 파일을 선택하세요.\n\n"
                    "4. '선택 파일 휴지통 이동'으로 안전하게 삭제합니다.\n\n"
                    "팁: 메뉴 > 설정에서 고급 옵션 변경이 가능합니다."
                )
                messagebox.showinfo("Duplicate Cleaner Pro에 오신 것을 환영합니다!", guide_message, parent=self)
                marker_file.touch() # 마커 파일 생성
        except OSError as e:
            # 마커 파일 생성/확인 중 오류 발생 시 콘솔에만 경고 출력 (프로그램 실행에 영향 X)
            print(f"경고: 첫 실행 가이드 마커 파일 처리 중 오류 발생 - {e}")


    # ── 큐 폴링
    def _poll_out(self):
        """
        백그라운드 스캔 스레드의 작업 결과를 담고 있는 출력 큐(`self.out_q`)를 주기적으로 확인(폴링)합니다.
        큐에서 메시지를 가져와 처리 유형("chunk", "prog", "done")에 따라 적절한 동작
        (결과 병합, 진행률 업데이트, 스캔 완료 처리)을 수행합니다.
        """
        try:
            msg, payload = self.out_q.get_nowait()
        except queue.Empty:
            if not self.stop_evt or not self.stop_evt.is_set():
                self.after(100, self._poll_out) # 큐가 비어있고 중단 요청이 없으면 다시 폴링
            elif self.stop_evt.is_set() and self.scanning: # 취소되었지만 아직 scanning=True인 경우
                self.scanning = False
                self._enable_scan_buttons()
                self.status.set("스캔이 취소되었습니다.")
            return
        
        if msg == "chunk":
            self._merge_results(payload)
            self.finished_chunks += 1 
        elif msg == "prog":
            self.progress.set(payload) # 진행률 업데이트
        elif msg == "done": # 모든 작업 완료
            elapsed = time.perf_counter() - self.scan_start
            self.last_scan_duration = elapsed

            # 스캔 후 자동 정렬
            if self.auto_sort_after_scan.get() and self.duplicates:
                sort_key_map = {"대표 파일명": "name", "크기": "size"}
                sort_key = sort_key_map.get(self.auto_sort_column.get(), "name")
                sort_rev = self.auto_sort_direction.get()
                self._sort_groups(sort_key, sort_rev)
                self._update_heads() # 정렬 후 헤더 업데이트

            gb   = self.reclaim_bytes / (1024**3)
            dup_cnt = len(self.duplicates)

            self.status.set(
                f"스캔 완료({elapsed:,.1f}s) · "
                f"중복 세트 {dup_cnt}개 발견 · 확보 가능 용량 ≈ {gb:,.2f} GB"
            )
            self.progress.set(1.0)
            self.scanning = False # 스캔 상태 플래그 해제
            self._enable_scan_buttons() # 스캔 버튼 활성화
            self._on_tree_selection_changed() # 최종 상태 업데이트 (선택된 것 없으면 스캔 완료 메시지)
            
            logger = logging.getLogger(__name__)
            if self.enable_logging.get():
                logger.info(f"Scan completed. Found {dup_cnt} duplicate sets. Reclaimable: {gb:,.2f} GB. Duration: {elapsed:,.1f}s")
            return
        
        self.after(50, self._poll_out)  # 계속 폴링

    # ── 결과 병합 & 배치 UI 갱신
    def _merge_results(self, sub_dup: dict[str, list[Path]]):
        """
        개별 스캔 작업(청크)의 결과(`sub_dup`)를 메인 중복 파일 목록(`self.duplicates`)에 병합합니다.
        일정 간격(현재는 매 청크 처리 시)으로 `_update_tree_and_status_batch`를 호출하여 UI를 업데이트합니다.
        """
        for h, lst in sub_dup.items():
            self.duplicates.setdefault(h, []).extend(lst)
        if self.finished_chunks % 1 == 0: # 매 청크 처리 시 또는 특정 간격으로 UI 업데이트
            self._update_tree_and_status_batch() # 이름 변경 및 기능 통합

    def _update_tree_and_status_batch(self):
        """
        현재까지 수집된 전체 중복 파일 목록(`self.duplicates`)을 바탕으로 Treeview를 업데이트하고,
        상태 바(진행률, 중복 세트 수, 확보 가능 용량)도 함께 갱신합니다.
        Treeview에 각 그룹의 파일을 표시할 때는 `self.max_files_per_group_display` 설정을 따릅니다.
        """
        pct = self.finished_chunks / self.total_chunks if self.total_chunks else 0
        # ── 상태바 업데이트 ──────────────────────────────────
        dup_cnt = len(self.duplicates)
        
        # 트리뷰 업데이트 로직 (기존 _update_tree_batch 내용)
        self.tree.delete(*self.tree.get_children()) # 매번 클리어하면 깜빡임 심할 수 있음. 더 나은 방법 고려 가능.
                                                  # 하지만 현재 구조에서는 청크별로 전체를 다시 그림.
        current_reclaim_bytes = 0
        for h, flist in self.duplicates.items(): # self.duplicates는 병합된 전체 결과
            if not flist: continue
            gid = self.tree.insert('', 'end',
                                   text=flist[0].name, # TODO: 그룹 헤더에 파일 수, 총 크기 표시 제안
                                   open=self.all_expanded)
            sz_mb = flist[0].stat().st_size / (1024*1024)
            current_reclaim_bytes += flist[0].stat().st_size * (len(flist)-1)
            
            display_limit = self.max_files_per_group_display.get()
            files_to_display = flist
            if display_limit > 0 and len(flist) > display_limit:
                files_to_display = flist[:display_limit]
                # TODO: 여기에 "...더 보기" 같은 표시를 추가할 수 있음 (Treeview 아이템으로)

            for fp in files_to_display:
                self.tree.insert(gid, 'end', values=(str(fp), f"{sz_mb:,.2f}"))
        self.reclaim_bytes = current_reclaim_bytes # 실제 계산된 값으로 업데이트
        gb_updated  = self.reclaim_bytes / (1024**3)

        self.status.set(f"진행 {pct*100:5.1f}% · 중복 세트 {dup_cnt}개 ({gb_updated:,.2f} GB)")
        self.progress.set(pct)

    # ── 모두 펼치기/접기 토글
    def toggle_expand_all(self):
        """
        '모두 펼치기'/'모두 접기' 버튼 클릭 시 호출됩니다.
        Treeview의 모든 최상위 그룹(중복 파일 세트)의 펼침/접힘 상태를 토글하고 버튼 텍스트를 변경합니다.
        """    
        new_open = not self.all_expanded
        for g in self.tree.get_children(''):
            self.tree.item(g, open=new_open)
        self.all_expanded = new_open
        self.toggle_btn.config(text="모두 접기" if new_open else "모두 펼치기")

    # ── 파일(하위 노드) 더블클릭 → OS 기본 앱 열기
    def _open_file(self, event):
        """
        Treeview의 파일 항목(자식 노드)을 더블 클릭했을 때 호출됩니다.
        선택된 파일을 운영체제의 기본 연결 프로그램으로 실행합니다.
        """
        sel = self.tree.selection()
        if not sel or not self.tree.parent(sel[0]): return
        path_str = self.tree.set(sel[0], "path") # 경로 문자열 가져오기
        try:
            if sys.platform.startswith('darwin'): # macOS
                subprocess.run(['open', path_str], check=False)
            elif os.name == 'nt': # Windows
                os.startfile(path_str)
            elif os.name == 'posix': # Linux 및 기타 POSIX 호환 시스템
                subprocess.run(['xdg-open', path_str], check=False)
        except Exception as e:
            messagebox.showerror("오류", f"파일 열기 실패:\n{e}")

    def _open_selected_in_folder(self):
        """
        '폴더에서 보기' 버튼 클릭 시 호출됩니다.
        Treeview에서 현재 선택된 항목(파일 또는 그룹)이 위치한 폴더를
        운영체제의 파일 탐색기에서 엽니다.
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("알림", "파일 또는 그룹을 선택하세요.")
            return

        item_id = sel[0]
        path_to_open = None

        if self.tree.parent(item_id): # 파일 항목(자식 노드)이 선택된 경우
            path_str = self.tree.set(item_id, "path")
            if path_str:
                path_to_open = Path(path_str).parent # 파일의 부모 폴더
        else: # 그룹 항목(최상위 노드)이 선택된 경우
            children = self.tree.get_children(item_id)
            if children:
                first_child_path_str = self.tree.set(children[0], "path")
                if first_child_path_str:
                    path_to_open = Path(first_child_path_str).parent # 첫 번째 파일의 부모 폴더

        if path_to_open and path_to_open.is_dir():
            try:
                if sys.platform.startswith('darwin'): # macOS
                    subprocess.run(['open', str(path_to_open)], check=False)
                elif os.name == 'nt': # Windows
                    os.startfile(str(path_to_open)) # 폴더도 잘 열림
                elif os.name == 'posix': # Linux
                    subprocess.run(['xdg-open', str(path_to_open)], check=False)
            except Exception as e:
                messagebox.showerror("오류", f"폴더 열기 실패:\n{e}")
        elif path_to_open:
            messagebox.showerror("오류", f"폴더를 찾을 수 없습니다: {path_to_open}")
        else:
            messagebox.showinfo("알림", "유효한 파일 경로를 가진 항목을 선택하세요.")

    # ── 삭제
    def delete_selected(self):
        """
        '선택 파일 휴지통 이동' 버튼 클릭 시 호출됩니다.
        Treeview에서 선택된 파일들을 OS의 휴지통으로 이동시킵니다.
        삭제 전 사용자 확인을 받고, 삭제 후에는 전체 재스캔 없이 UI와 내부 데이터를 업데이트합니다.
        """
        selected_tree_item_ids = self.tree.selection()
        if not selected_tree_item_ids:
            messagebox.showinfo("알림", "삭제할 파일을 선택하세요.")
            return

        paths_to_delete_from_ui = []
        for item_id in selected_tree_item_ids:
            if self.tree.parent(item_id): # 실제 파일 노드인지 확인
                path_str = self.tree.set(item_id, "path")
                if path_str:
                    paths_to_delete_from_ui.append(Path(path_str))
        
        if not paths_to_delete_from_ui:
            messagebox.showinfo("알림", "삭제할 실제 파일을 선택하세요 (그룹 헤더 제외).")
            return

        total_bytes_to_delete = sum(p.stat().st_size for p in paths_to_delete_from_ui if p.exists())
        if not messagebox.askyesno(
            "삭제 확인",
            f"{len(paths_to_delete_from_ui)}개 파일({bytes_to_human(total_bytes_to_delete)})을 "
            "휴지통으로 이동할까요?"):
            return

        errors = []
        successfully_deleted_paths = set()
        for p in paths_to_delete_from_ui:
            try:
                logger = logging.getLogger(__name__)
                if self.enable_logging.get():
                    logger.info(f"Attempting to delete: {p}")
                send2trash(str(p))
                successfully_deleted_paths.add(p)
            except Exception as e:
                errors.append((p, e))

        if errors:
            error_messages = "\n".join([f"- {path.name}: {err}" for path, err in errors])
            messagebox.showerror("삭제 오류", f"다음 파일들을 휴지통으로 옮기는 데 실패했습니다:\n{error_messages}")
            logger = logging.getLogger(__name__)
            if self.enable_logging.get():
                logger.error(f"Deletion errors: {error_messages}")
        
        if not successfully_deleted_paths:
            if not errors: # 오류도 없고 성공도 없으면 (예: 이미 삭제된 파일 선택)
                messagebox.showinfo("알림", "실제로 삭제된 파일이 없습니다 (이미 삭제되었거나 접근 불가).")
            # 실제로 삭제된 파일이 없으면 여기서 종료 (UI 변경 없음)
            return
        
        if not errors: # 모든 파일이 성공적으로 삭제된 경우에만 전체 성공 메시지 표시
            messagebox.showinfo("삭제 완료", f"{len(successfully_deleted_paths)}개 파일이 휴지통으로 이동되었습니다.")
            logger = logging.getLogger(__name__)
            if self.enable_logging.get():
                logger.info(f"Successfully deleted {len(successfully_deleted_paths)} files.")
        elif successfully_deleted_paths: # 일부 성공, 일부 실패
            messagebox.showinfo("부분 완료", f"{len(successfully_deleted_paths)}개 파일이 휴지통으로 이동되었으나, 일부 파일 삭제에 실패했습니다.")
            logger = logging.getLogger(__name__)
            if self.enable_logging.get():
                logger.warning(f"Partially completed deletion. Success: {len(successfully_deleted_paths)}, Failed: {len(errors)}")

        # 1. 내부 데이터 구조 (self.duplicates) 업데이트
        new_duplicates_data = {}
        for h, path_list in self.duplicates.items():
            updated_path_list = [p for p in path_list if p not in successfully_deleted_paths]
            if len(updated_path_list) >= 2: # 여전히 중복 그룹으로 유효한 경우
                new_duplicates_data[h] = updated_path_list
        self.duplicates = new_duplicates_data

        # 2. 확보 가능 용량 (self.reclaim_bytes) 재계산
        self.reclaim_bytes = 0
        for path_list in self.duplicates.values():
            if path_list: # 리스트가 비어있지 않고, 최소 2개 이상 파일을 가짐
                file_size = path_list[0].stat().st_size # 그룹 내 파일 크기는 동일
                self.reclaim_bytes += file_size * (len(path_list) - 1)

        # 3. Treeview UI 갱신 (기존 스캔 결과에서 삭제된 항목만 반영)
        self.tree.delete(*self.tree.get_children()) # Treeview 초기화
        for h_key, file_list_val in self.duplicates.items(): # 업데이트된 self.duplicates 사용
            if not file_list_val: continue
            file_list_val.sort(key=lambda p: str(p)) # 대표 파일 일관성 유지
            rep_name = file_list_val[0].name
            group_id_new = self.tree.insert('', 'end', text=rep_name, open=self.all_expanded) # 펼침 상태 유지
            size_mb = file_list_val[0].stat().st_size / (1024 * 1024) # 그룹 크기는 동일

            display_limit = self.max_files_per_group_display.get()
            files_to_display_in_group = file_list_val
            if display_limit > 0 and len(file_list_val) > display_limit:
                files_to_display_in_group = file_list_val[:display_limit]

            for fp_val in files_to_display_in_group: # 그룹 내 파일 표시 (제한 적용)
                self.tree.insert(group_id_new, 'end', values=(str(fp_val), f"{size_mb:,.2f}"))

        # 4. 상태 바 업데이트
        self._on_tree_selection_changed(calculate_size_override=True) # 스캔 요약 정보로 업데이트

    # ── 트리뷰 헤더 클릭 정렬
    def _on_header(self, cid: str):
        """
        Treeview의 컬럼 헤더('대표 파일명' 또는 'Size (MB)')를 클릭했을 때 호출됩니다.
        클릭된 컬럼을 기준으로 정렬 방향(오름차순/내림차순)을 토글하고,
        `_sort_groups`를 호출하여 실제 정렬을 수행한 뒤, `_update_heads`로 헤더 표시를 업데이트합니다.
        """
        self.sort_reverse = (self.sort_column == cid) and not self.sort_reverse
        self.sort_column  = cid
        key = 'name' if cid == "#0" else 'size'
        self._sort_groups(key, self.sort_reverse)
        self._update_heads()

    def _sort_groups(self, key: str, rev: bool):
        """
        Treeview의 최상위 그룹(중복 파일 세트)들을 지정된 `key`('name' 또는 'size')와
        정렬 방향(`rev`)에 따라 정렬하고, Treeview에 재배치합니다.
        """
        groups = self.tree.get_children('')
        if key == 'name':
            kf = lambda g: self.tree.item(g,'text').lower()
        else:
            def sz(g):
                c = self.tree.get_children(g)[0]
                return float(self.tree.set(c,'size').replace(',',''))
            kf = sz
        for idx, gid in enumerate(sorted(groups, key=kf, reverse=rev)):
            self.tree.move(gid, '', idx)

    def _update_heads(self):
        """
        현재 정렬 상태(`self.sort_column`, `self.sort_reverse`)에 따라
        Treeview 컬럼 헤더의 텍스트를 업데이트하여 정렬 기준과 방향(화살표)을 시각적으로 표시합니다.
        """
        base = {"#0":"대표 파일명", "size":"Size (MB)"}
        for cid, label in base.items():
            if cid == self.sort_column:
                arrow = " ▼" if self.sort_reverse else " ▲"
                self.tree.heading(cid, text=label+arrow)
            else:
                self.tree.heading(cid, text=label+" (정렬 가능)")

    def _reset_sorting_state(self):
        """
        정렬 관련 상태 변수(`self.sort_column`, `self.sort_reverse`)와
        Treeview 헤더 표시를 초기 상태로 되돌립니다.
        """
        self.sort_column = None
        self.sort_reverse = False
        self._update_heads() # 헤더 텍스트 업데이트 (화살표 제거)

    def _reset_expansion_state(self):
        """
        Treeview 그룹의 펼치기/접기 관련 상태 변수(`self.all_expanded`)와
        '모두 펼치기/접기' 버튼의 텍스트를 초기 상태로 되돌립니다.
        """
        self.all_expanded = False
        self.toggle_btn.config(text="모두 펼치기")

    def _reset_selection_toggle_state(self):
        """
        '첫 파일 제외 선택'/'전체 선택 해제' 토글 버튼의 상태 변수(`self.select_toggle_state`)와
        버튼 텍스트를 초기 상태로 되돌립니다.
        """
        self.select_toggle_state = False
        self.select_toggle_btn.config(text="첫 파일 제외 선택")
    def _on_tree_selection_changed(self, event=None, calculate_size_override=None):
        """
        Treeview에서 선택된 항목이 변경될 때마다 호출됩니다 (<<TreeviewSelect>> 이벤트 바인딩).
        상태 바에 현재 선택된 파일의 개수와 (필요시) 총용량을 표시하거나,
        선택된 파일이 없을 경우 스캔 결과 요약 또는 초기 메시지를 표시합니다.
        `calculate_size_override` 파라미터나 `_performing_bulk_select` 플래그를 통해
        대량 선택 시에는 비용이 큰 용량 계산을 건너뛸 수 있습니다.
        """
        if self.scanning: # 스캔 중에는 상태바 업데이트 안 함 (진행률 표시)
            return
        selected_items = self.tree.selection()
        num_selected_files = 0
        current_selected_bytes = 0

        if selected_items:
            for item_id in selected_items:
                if self.tree.parent(item_id): # 실제 파일(자식 노드)만 계산
                    num_selected_files += 1
                    if self._should_calculate_size_for_selection(calculate_size_override):
                        try:
                            file_path_str = self.tree.set(item_id, "path")
                            if file_path_str: 
                                current_selected_bytes += Path(file_path_str).stat().st_size
                        except FileNotFoundError: pass
                        except Exception: pass

        if num_selected_files > 0:
            if self._should_calculate_size_for_selection(calculate_size_override):
                self.status.set(f"{num_selected_files}개 파일 선택됨 ({bytes_to_human(current_selected_bytes)} 확보 가능)")
            else:
                self.status.set(f"{num_selected_files}개 파일 선택됨")
        elif self.duplicates: # 스캔 완료 후 아무것도 선택되지 않았고, 중복 파일이 있었던 경우
            gb_total = self.reclaim_bytes / (1024**3)
            dup_cnt = len(self.duplicates)
            duration_info = f"({self.last_scan_duration:.1f}s)" if self.last_scan_duration is not None else ""
            self.status.set(f"스캔 완료{duration_info} · 중복 세트 {dup_cnt}개 발견 · 확보 가능 용량 ≈ {gb_total:,.2f} GB")
        elif hasattr(self, 'scan_start'): # 스캔은 실행되었으나 중복이 없거나 초기 상태
            duration_info = f"({self.last_scan_duration:.1f}s)" if self.last_scan_duration is not None else ""
            self.status.set(f"스캔 완료{duration_info} · 중복 파일 없음")
        # 초기 상태("폴더를 선택하세요.")는 __init__에서 설정되므로 여기서는 특별히 처리 안 함

    def on_close(self):
        """
        애플리케이션 창의 닫기 버튼(X)을 눌렀을 때 호출됩니다.
        만약 스캔 작업이 진행 중이라면 사용자에게 종료 여부를 확인합니다.
        확인 후 또는 스캔 중이 아닐 경우, 백그라운드 스레드에 중단 신호를 보내고 창을 닫습니다.
        """
        if self.work_q or self.finished_chunks < self.total_chunks:
            if not messagebox.askyesno(
                    "작업 중지 확인",
                    "현재 스캔이 진행 중입니다.\n정말로 종료하시겠습니까?"):
                return           # 취소 → 창 닫지 않음
        # 백그라운드 스레드에 중단 플래그
        if self.stop_evt:
            self.stop_evt.set()
        # self._save_settings_to_file() # 프로그램 종료 시 현재 설정 저장 (선택 사항)
        self.destroy()           # 루트 창 닫기 → 프로그램 종료

    def _should_calculate_size_for_selection(self, calculate_size_override=None) -> bool:
        """
        `_on_tree_selection_changed` 메소드 내부에서 현재 선택된 파일들의 총용량을
        계산해야 할지 여부를 결정하는 헬퍼 함수입니다.
        대량 선택 작업 중이거나 `calculate_size_override`가 False로 명시된 경우 용량 계산을 건너뜁니다.
        """
        if calculate_size_override is not None:
            return calculate_size_override
        if hasattr(self, '_performing_bulk_select') and self._performing_bulk_select:
            return False # 대량 선택 중에는 용량 계산 안 함
        return True # 그 외의 경우 기본적으로 용량 계산

    # ── 설정 파일 저장 및 불러오기 
    def _get_settings_file_path(self) -> Path:
        """설정 파일의 경로를 반환합니다."""
        app_data_dir = Path.home() / ".DuplicateCleanerPro"
        app_data_dir.mkdir(parents=True, exist_ok=True)
        return app_data_dir / "settings.json"

    def _save_settings_to_file(self):
        """현재 설정 값들을 JSON 파일에 저장합니다."""
        settings_path = self._get_settings_file_path()
        settings_data = {
            "auto_scan": self.auto_scan.get(),
            "hash_algo": self.hash_algo.get(),
            "core_count": self.core_count.get(),
            "batch_size": self.batch_size.get(),
            "skip_dirs": self.skip_dirs.get(),
            "min_file_size_mb": self.min_file_size_mb.get(),
            "max_file_size_mb": self.max_file_size_mb.get(),
            "include_extensions": self.include_extensions.get(),
            "exclude_extensions": self.exclude_extensions.get(),
            "auto_sort_after_scan": self.auto_sort_after_scan.get(),
            "auto_sort_column": self.auto_sort_column.get(),
            "auto_sort_direction": self.auto_sort_direction.get(),
            "max_files_per_group_display": self.max_files_per_group_display.get(),
            "enable_logging": self.enable_logging.get(),
            "log_level": self.log_level.get(),
        }
        try:
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=4)
            # print(f"Settings saved to {settings_path}") # 디버깅용
        except OSError as e:
            print(f"경고: 설정을 파일에 저장하는 중 오류 발생 - {e}")

    def _load_settings_from_file(self):
        """JSON 파일에서 설정 값들을 불러와 적용합니다."""
        settings_path = self._get_settings_file_path()
        if settings_path.exists():
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings_data = json.load(f)
                
                self.auto_scan.set(settings_data.get("auto_scan", False)) # 설정 파일에 없으면 기본값 False 사용
                self.hash_algo.set(settings_data.get("hash_algo", "blake3" if USE_BLAKE3 else "sha256"))
                self.core_count.set(settings_data.get("core_count", CPU_WORKERS))
                self.batch_size.set(settings_data.get("batch_size", BATCH_SIZE))
                self.skip_dirs.set(settings_data.get("skip_dirs", self._get_default_skip_dirs()))
                self.min_file_size_mb.set(settings_data.get("min_file_size_mb", 0))
                self.max_file_size_mb.set(settings_data.get("max_file_size_mb", 0))
                self.include_extensions.set(settings_data.get("include_extensions", ""))
                self.exclude_extensions.set(settings_data.get("exclude_extensions", ""))
                self.auto_sort_after_scan.set(settings_data.get("auto_sort_after_scan", False))
                self.auto_sort_column.set(settings_data.get("auto_sort_column", "name"))
                self.auto_sort_direction.set(settings_data.get("auto_sort_direction", False))
                self.max_files_per_group_display.set(settings_data.get("max_files_per_group_display", 0))
                self.enable_logging.set(settings_data.get("enable_logging", False))
                self.log_level.set(settings_data.get("log_level", "INFO"))

                # print(f"Settings loaded from {settings_path}") # 디버깅용
            except (OSError, json.JSONDecodeError) as e:
                print(f"경고: 설정 파일 불러오기 중 오류 발생 - {e}. 기본 설정을 사용합니다.")
        # 설정 파일이 없으면 기본값으로 self.tk.Variable들이 이미 초기화되어 있음

    def _get_default_skip_dirs(self) -> str:
        """OS별 기본 제외 폴더 문자열을 반환합니다."""
        return ("$RECYCLE.BIN;System Volume Information"
                if os.name == 'nt'
                else ".Trashes;.Spotlight-V100;.fseventsd;System;.DS_Store")

# ─────────────────────────────── main ──────────────────────────────────────
    def reset_all_settings_to_default(self, settings_window: tk.Toplevel = None):
        """모든 설정을 기본값으로 초기화하고 저장된 설정 파일을 삭제합니다."""
        if not messagebox.askyesno("모든 설정 초기화 확인",
                                   "정말로 모든 설정을 기본값으로 되돌리고 저장된 설정을 삭제하시겠습니까?\n"
                                   "이 작업은 되돌릴 수 없습니다.", parent=settings_window):
            return

        # 2. 저장된 설정 파일 삭제
        settings_path = self._get_settings_file_path()
        try:
            if settings_path.exists():
                settings_path.unlink()
                # print(f"Deleted settings file: {settings_path}") # 디버깅용
        except OSError as e:
            messagebox.showerror("오류", f"설정 파일 삭제 중 오류 발생:\n{e}", parent=settings_window)
            # 파일 삭제 실패 시에도 나머지 초기화는 진행

        # 3. tk.Variable들을 기본값으로 재설정
        self.auto_scan.set(False)
        self.hash_algo.set("blake3" if USE_BLAKE3 else "sha256") # USE_BLAKE3는 프로그램 시작 시 결정됨
        self.core_count.set(CPU_WORKERS) # CPU_WORKERS는 프로그램 시작 시 결정된 값
        self.batch_size.set(BATCH_SIZE)  # BATCH_SIZE는 상수
        self.skip_dirs.set(self._get_default_skip_dirs())
        self.min_file_size_mb.set(0)
        self.max_file_size_mb.set(0)
        self.include_extensions.set("")
        self.exclude_extensions.set("")
        self.auto_sort_after_scan.set(False)
        self.auto_sort_column.set("name")
        self.auto_sort_direction.set(False)
        self.max_files_per_group_display.set(0)
        self.enable_logging.set(False)
        self.log_level.set("INFO")        

        messagebox.showinfo("초기화 완료", "모든 설정이 기본값으로 초기화되었습니다.", parent=settings_window)
        # 설정 창을 닫거나, 사용자가 직접 닫도록 둘 수 있음
        if settings_window:
            settings_window.destroy() # 초기화 후 설정 창 닫기

if __name__ == "__main__":
    multiprocessing.freeze_support() # Windows에서 .exe 실행 시 멀티프로세싱 오류 방지
    DuplicateCleaner().mainloop()
