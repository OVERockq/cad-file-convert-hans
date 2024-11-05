# CAD File Converter

CAD File Converter는 DWG 파일을 전처리로 DXF로 변환하고, 이를 다시 PDF 또는 PNG 형식으로 변환하는 Python 스크립트입니다.


## 주요 기능

- DWG 파일을 PDF 또는 PNG 형식으로 변환(하위 폴더 인식)
- 한글 폰트 지원 (맑은 고딕)
- 텍스트 포함/제외 옵션
- 배경색 설정 옵션
- 스케일 조정 기능

## 설치 방법

1. 이 저장소를 클론합니다:

```bash
git clone https://github.com/yourusername/cad-file-converter.git
cd cad-file-converter
```

2. 필요한 패키지를 설치합니다:

```bash
pip install -r requirements.txt
```

3. `config.ini` 파일을 편집하여 설정을 조정합니다.

## 사용 방법

1. `Data` 폴더에 변환하고자 하는 DWG 파일을 넣습니다.

2. 다음 명령어로 스크립트를 실행합니다:

```bash
python CAD2PDF-PNG_Convert-Hans_v0.4.py
```

3. 변환된 파일은 원본 파일과 동일한 디렉토리에 저장됩니다.

## 설정

`config.ini` 파일에서 다음 설정을 조정할 수 있습니다:

- `ODAFileConverter_Dir`: ODA File Converter 실행 파일 경로
- `DATA_DIR`: 입력 파일 디렉토리
- `background_color`: 출력 파일 배경색
- `format_choice`: 출력 파일 형식 (PNG 또는 PDF)
- `Scale`: 출력 파일 스케일
- `LineWidthScale`: 선 굵기 스케일
- `TextScale`: 텍스트 크기 스케일
- `text_choice`: 텍스트 포함 여부 (1: 포함, 2: 제외, 3: 둘 다)

## 요구 사항

- Python 3.6+
- [ODA File Converter](https://www.opendesign.com/guestfiles/oda_file_converter)
- ezdxf
- matplotlib
- tqdm

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.


## 제작자

- Email : locustk@gmail.com
- Blog : https://make1solve.tistory.com

## 기여

버그 리포트, 기능 요청, 풀 리퀘스트 등 모든 기여를 환영합니다. 주요 변경 사항에 대해서는 먼저 이슈를 열어 논의해 주세요.
