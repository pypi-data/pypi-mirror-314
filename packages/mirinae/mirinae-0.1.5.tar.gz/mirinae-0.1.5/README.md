# Mirinae

마고 프레임워크를 사용할 수 있는 CLI 도구입니다.

## 마고 서비스

- [Audion](https://audion.mago52.com)

## Local에서 사용하기

- 소스 코드를 다운로드 받습니다.

    ```bash
    git clone https://github.com/holamago/mirinae-cli.git
    ```

- 설치를 다음과 같이 합니다.

    ```bash
    cd mirinae-cli
    pip install -e .
    ```

- 이제 CLI를 사용할 수 있습니다.

## Demo

### Login

```bash
mirinae user login -v -e <email> -w <password>
```

### Audion API 사용하기

- 로컬에 있는 오디오 파일 사용하기

  - Subtitle Generation

  ```bash
  mirinae api call -s SubtitleGeneration -a <audio_path>
  ```

  - Voice Separation

  ```bash
  mirinae api call -s VoiceSeparation -a <audio_path>
  ```

  - Youtube URL 사용하기

  - Subtitle Generation

    ```bash
    mirinae api call_url -s SubtitleGeneration -u <youtube url>
    ```

  - Voice Separation

    ```bash
    mirinae api call_url -s VoiceSeparation -u <youtube url>
    ```

    ### Audion 대시보드 사용하기

```bash
mirinae dashboard get -s SubtitleGeneration
mirinae dashboard get -s VoiceSeparation
```

- Query 사용하기

```bash
mirinae dashboard get -s SubtitleGeneration --query last
mirinae dashboard get -s VoiceSeparation --query last
```

** 오늘 날짜 데이터 가져오기 **
이전에 시간 저장 방법이 변경되어서 동작 안할 수 있습니다.
오늘 날짜에 테스트를 했다면 사용해 보세요.

```bash
mirinae dashboard get -s SubtitleGeneration --query today
mirinae dashboard get -s VoiceSeparation --query today
```