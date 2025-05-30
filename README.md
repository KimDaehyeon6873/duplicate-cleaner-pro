# Duplicate Cleaner Pro

## 🚀 고성능 중복 파일 제거 프로그램 (GUI)

## 개요

Duplicate Cleaner Pro는 시스템에서 중복 파일을 찾아 안전하게 제거하는 강력한 고성능 GUI 기반 도구입니다. 정확성을 보장하기 위해 바이트 단위 비교를 수행하며, 중복 파일은 운영체제의 휴지통으로 이동시켜 복구가 가능하도록 합니다. Windows, macOS, Linux와 호환됩니다.

이 "Pro" 버전은 백그라운드 스캔, 다중 스캔 모드(폴더 또는 전체 드라이브), BLAKE3 자동 감지를 통한 매우 효율적인 해싱, 광범위한 필터링 옵션, 점진적 UI 업데이트, 삭제 후 재스캔 없음, 상세 설정 패널 등 고급 기능을 제공합니다.

## ✨ 주요 기능

### 🚀 스캔 및 탐지
*   **백그라운드 스캔**: UI 응답성을 유지하기 위해 백그라운드 스레드에서 스캔을 수행하며, 진행률 표시줄과 진행 중인 스캔을 중지할 수 있는 '취소' 버튼을 제공합니다.
*   **다중 스캔 모드**:
    *   **선택 폴더 스캔**: 특정 폴더와 그 하위 디렉토리를 대상으로 합니다.
    *   **전체 드라이브 스캔**: 전체 드라이브(예: C:\ 또는 /)를 스캔합니다. 대용량 드라이브 처리를 위해 스캔을 작은 단위로 나누어 메모리 효율적인 생산자-소비자 패턴을 활용합니다.
*   **고급 해싱 및 병렬 처리**:
    *   **BLAKE3 자동 감지**: `blake3` 라이브러리가 설치되어 있으면 자동으로 사용하여 매우 빠른 해싱 알고리즘을 제공하며, 설치되어 있지 않으면 SHA-256으로 대체됩니다. 이는 설정에서 구성할 수 있습니다.
    *   **멀티프로세스 해싱**: 다수의 CPU 코어(설정 가능, 일반적으로 UI 반응성을 위해 하나 제외)를 활용하여 많은 수의 파일에 대한 해싱 속도를 크게 향상시킵니다.
*   **효율적인 중복 식별**:
    *   **2단계 시스템**: 먼저 파일 크기(빠른 확인)로 파일을 필터링한 다음, 이러한 잠재적 중복 그룹에 대해서만 해시를 계산하여 불필요한 계산을 최소화합니다.
*   **유연한 필터링 (고급 설정 통해)**:
    *   스캔할 최소 및 최대 파일 크기를 정의합니다.
    *   특정 확장자(예: `jpg,png` 또는 `tmp,log`)를 기준으로 파일을 포함하거나 제외합니다.
    *   스캔에서 제외할 폴더 이름 목록(예: `node_modules, .git`)을 지정합니다. OS별 기본값이 제공됩니다.

### 📊 결과 및 관리 (Tkinter 트리뷰)
*   **직관적인 결과 트리**: 중복 세트를 대표 파일명(일반적으로 그룹 내 첫 번째 파일)으로 그룹화하여 표시합니다. 각 파일은 전체 경로와 그룹의 공유 파일 크기(MB 단위, 소수점 2자리)를 보여줍니다.
*   **점진적 UI 업데이트**: 스캔 과정 중 설정 가능한 배치 단위로 결과가 점진적으로 트리 뷰에 추가되어, 중복 파일이 발견되는 대로 확인할 수 있습니다.
*   **상호작용 가능한 트리 컨트롤**:
    *   **정렬**: '대표 파일명' 또는 '크기' 열 헤더를 클릭하여 중복 그룹을 오름차순/내림차순(▲/▼으로 표시)으로 정렬합니다.
    *   **모두 펼치기/접기**: 전용 버튼으로 중복 그룹 내의 모든 파일을 쉽게 보거나 숨길 수 있습니다.
    *   **파일 열기**: 트리에서 파일을 더블 클릭하면 기본 시스템 애플리케이션으로 엽니다.
    *   **폴더에서 보기**: 파일이나 그룹을 선택하고 "폴더에서 보기" 버튼을 클릭하여 시스템 파일 탐색기에서 해당 위치를 엽니다.
*   **스마트 파일 선택 (토글 버튼)**:
    *   **"첫 파일 제외 모두 선택"**: 각 중복 그룹에서 중복된 모든 복사본을 빠르게 선택하고, 하나(목록의 첫 번째)는 선택되지 않은 상태로 둡니다.
    *   **"전체 선택 해제"**: 트리에서 현재 모든 선택을 지웁니다. (위 버튼과 토글 방식입니다).
*   **안전하고 효율적인 삭제**:
    *   선택한 파일을 운영체제의 **휴지통**(`send2trash` 라이브러리 사용)으로 이동시켜, 필요시 쉽게 복구할 수 있도록 합니다.
    *   삭제 전에 파일 수와 확보될 총 디스크 공간을 보여주며 확인을 요청합니다.
    *   **삭제 후 전체 재스캔 없음**: 삭제 후 디렉토리 전체를 다시 스캔하는 시간 소모 없이 중복 목록과 확보 가능한 공간 통계가 즉시 업데이트됩니다.
*   **실시간 상태 표시줄**: 현재 작업(예: "스캔 중...", "폴더 선택"), 스캔 진행률(%), 스캔 완료 요약(발견된 총 세트 수, 확보 가능한 공간, 소요 시간), 현재 선택된 파일에 대한 정보(개수 및 총 크기)에 대한 지속적인 피드백을 제공합니다.

### ⚙️ 사용자 정의 및 편의 기능
*   **포괄적인 고급 설정 패널**
    *   (예: 해시 알고리즘 선택, 스캔 필터 상세 조정, 멀티프로세싱 코어 수, UI 배치 크기, 로깅 설정 등)
*   **최초 실행 가이드**
*   **애플리케이션 상태 초기화**
*   **창 크기 자동 조절 및 화면 중앙 배치**
*   **종료 확인**

## 📦 요구 사항

* Python 3.8 이상
* `send2trash`, `blake3` (선택)

## 🛠️ 설치 방법 및 실행

```bash
pip install send2trash blake3
python duplicate_cleaner_pro_v3.py
```

## 🚧 향후 추가 예정 기능

- [ ] 중복 파일 실시간 미리보기 및 필터링
- [ ] 영구 삭제 옵션 추가 (현재는 휴지통으로만 이동)
- [ ] 탐색 결과 CSV 내보내기
- [ ] 다크모드 전환 기능


## ☠️ 발견된 문제점 및 업데이트 내역

- 25/05/29  c:\ 전체 중복 파일 탐색 및 삭제는 시스템에 치명적    
            >> 사용자 생성 파일 경로에 한정된 탐색 제공

## 📄 라이선스

MIT License