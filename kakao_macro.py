import pyautogui
import pyperclip
import time
import datetime

# ==============================================================================
# [사용자 설정 변수] 아래의 값들을 환경에 맞게 수정해주세요.
# ==============================================================================
SCHEDULE_TIMES = ["14:30", "15:00", "18:00"]  # 실행할 시간대 목록 (HH:MM 형식)
ROOM_COUNT = 30                               # 전송을 반복할 총 채팅방 개수
IMAGE_PATH = r"C:\path\to\image.jpg"          # 전송할 이미지의 절대 경로
MESSAGE_TEXT = """여기에 전송할 메시지 내용을
입력하세요. (여러 줄 가능)"""
# ==============================================================================

def send_kakao_message():
    for i in range(ROOM_COUNT):
        # 1. Enter (채팅방 열기) -> 0.5초 대기
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # 2. Ctrl + T (파일 첨부 열기) -> 0.6초 대기
        pyautogui.hotkey('ctrl', 't')
        time.sleep(0.6)
        
        # 3. 이미지 경로 복사 후 Ctrl + V (경로 입력) -> 0.1초 대기
        pyperclip.copy(IMAGE_PATH)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        
        # 4. Enter (이미지 파일 선택) -> 0.2초 대기
        pyautogui.press('enter')
        time.sleep(0.2)
        
        # 5. 메시지 텍스트 복사 후 Ctrl + V (텍스트 입력) -> 0.1초 대기
        pyperclip.copy(MESSAGE_TEXT)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        
        # 6. Enter (텍스트 전송) -> 0.3초 대기
        pyautogui.press('enter')
        time.sleep(0.3)
        
        # 7. Esc (채팅방 닫기) -> 0.1초 대기
        pyautogui.press('esc')
        time.sleep(0.1)
        
        # 8. Down 방향키 (다음 채팅방 이동) -> 0.1초 대기
        pyautogui.press('down')
        time.sleep(0.1)

def main():
    print("==================================================")
    print(" 카카오톡 자동 발송 매크로가 시작되었습니다.")
    print("==================================================")
    print(f"- 설정된 시간: {SCHEDULE_TIMES}")
    print(f"- 채팅방 개수: {ROOM_COUNT}개")
    print(f"- 이미지 경로: {IMAGE_PATH}")
    print("- 프로그램을 종료하려면 터미널 창에서 Ctrl+C를 누르세요.")
    print("==================================================\n")
    
    executed_times = []
    last_date = datetime.date.today()
    
    while True:
        now = datetime.datetime.now()
        current_date = now.date()
        current_time_str = now.strftime("%H:%M")
        
        # 하루가 지나면(자정) 실행 기록 초기화
        if current_date != last_date:
            executed_times.clear()
            last_date = current_date
            print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 자정이 지나 실행 기록이 초기화되었습니다.")
            
        # 지정된 시간이 되었고, 오늘 아직 실행되지 않은 시간대일 경우 실행
        if current_time_str in SCHEDULE_TIMES and current_time_str not in executed_times:
            print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 예약 시간({current_time_str}) 도달. 매크로를 실행합니다.")
            print("주의: 카카오톡 채팅 목록의 첫 번째 방을 선택한 상태로 두세요.")
            
            # 발송 시작
            send_kakao_message()
            
            executed_times.append(current_time_str)
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {ROOM_COUNT}개 채팅방 전송 완료. 다음 예약 시간을 대기합니다.\n")
            
        time.sleep(1) # 1초마다 시간 확인

if __name__ == "__main__":
    main()
