import cv2

def start_video_recorder_with_stream(stream_url):
    # 스트리밍 주소로 비디오 캡처 객체 생성
    cap = cv2.VideoCapture(stream_url)

    # 비디오 코덱 설정 및 비디오 파일 저장 설정 (FourCC 코덱 사용)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 코덱 설정 (XVID)
    out = cv2.VideoWriter('Recode.avi', fourcc, 30.0, (640, 480))  # FPS: 30, 해상도: 640x480

    # 초기 모드는 Preview
    is_recording = False
    flip_enabled = False  # 좌우 반전 상태 (처음에는 비활성화)

    if not cap.isOpened():
        print("RTSP 스트림에 연결할 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 가져올 수 없습니다.")
            break

        # 좌우 반전 기능이 활성화된 경우 영상 좌우 반전
        if flip_enabled:
            frame = cv2.flip(frame, 1)  # 1은 좌우 반전, 0은 상하 반전

        # 녹화할 때 화면에만 빨간 원을 그리지만, 파일에는 저장하지 않음
        display_frame = frame.copy()  # 화면에 표시할 프레임을 복사

        if is_recording:
            # 화면에 빨간색 원 그리기 (녹화 중 표시)
            cv2.circle(display_frame, (50, 50), 20, (0, 0, 255), -1)  # 빨간색 원 그리기
            out.write(frame)  # 원이 없는 원본 프레임을 비디오 파일에 저장

        # 현재 프레임을 화면에 표시
        cv2.imshow('Video Recorder', display_frame)

        # 키보드 입력 처리
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # 스페이스바 입력 시 모드 전환
            is_recording = not is_recording
            if is_recording:
                print("녹화 시작")
            else:
                print("녹화 중지")
        elif key == ord('f'):  # 'f' 키 입력 시 좌우 반전 토글
            flip_enabled = not flip_enabled
            if flip_enabled:
                print("좌우 반전 활성화")
            else:
                print("좌우 반전 비활성화")
        elif key == 27:  # ESC 키 입력 시 종료
            print("프로그램 종료")
            break

    # 자원 해제
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# RTSP 스트림 주소로 함수 실행
stream_url = 'rtsp://210.99.70.120:1935/live/cctv001.stream'
start_video_recorder_with_stream(stream_url)