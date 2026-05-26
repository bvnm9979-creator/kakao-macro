import pyautogui
import pyperclip
import time
import datetime
import os

def load_settings():
    # 기본값 설정
    settings = {
        "시간대": ["14:30"],
        "채팅방개수": 30,
        "이미지경로": ""
    }
    
    # 파일이 없으면 템플릿 생성 (윈도우 메모장 호환을 위해 utf-8-sig 사용)
    if not os.path.exists("setting.txt"):
        with open("setting.txt", "w", encoding="utf-8-sig") as f:
            f.write("시간대=14:30,15:00,18:00\n")
            f.write("채팅방개수=30\n")
            f.write("이미지경로=C:\\사진\\광고.jpg\n")
    else:
        # 파일이 있으면 읽어서 설정 업데이트
        with open("setting.txt", "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line: continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                
                if key == "시간대":
                    settings["시간대"] = [t.strip() for t in val.split(",")]
                elif key == "채팅방개수":
                    try: settings["채팅방개수"] = int(val)
                    except: pass
                elif key == "이미지경로":
                    settings["이미지경로"] = val
                    
    return settings

def load_message():
    # 파일이 없으면 템플릿 생성
    if not os.path.exists("message.txt"):
        with open("message.txt", "w", encoding="utf-8-sig") as f:
            f.write("여기에 전송할 메시지 내용을 입력하세요.\n줄바꿈을 포함하여 여러 줄 입력이 자유롭게 가능합니다.")
        return "여기에 전송할 메시지 내용을 입력하세요."
    
    # 파일이 있으면 전체 내용 읽기
    with open("message.txt", "r", encoding="utf-8-sig") as f:
        return f.read().strip()

def send_kakao_message(room_count, image_path, message_text):
    for i in range(room_count):
        # 1. Enter (채팅방 열기) -> 0.5초 대기
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # [사진 전송 파트]
        # 2. Ctrl + T (파일 첨부 열기) -> 0.6초 대기
        pyautogui.hotkey('ctrl', 't')
        time.sleep(0.6)
        
        # 3. 이미지 경로 복사 후 Ctrl + V (경로 입력) -> 0.1초 대기
        pyperclip.copy(image_path)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        
        # 4. Enter (이미지 파일 선택 및 전송) -> 0.2초 대기
        pyautogui.press('enter')
        time.sleep(0.2)
        
        # [메시지 전송 파트]
        # 5. 메시지 텍스트 복사 후 Ctrl + V (텍스트 입력) -> 0.1초 대기
        pyperclip.copy(message_text)
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
    print(" 폴더 안의 setting.txt 와 message.txt 를 실시간으로 읽습니다.")
    print("==================================================\n")
    
    executed_times = []
    last_date = datetime.date.today()
    
    while True:
        # 매 초마다 파일 내용을 새로 읽어옴 (프로그램 켜둔 상태로 메모장 수정 가능!)
        settings = load_settings()
        message_text = load_message()
        
        now = datetime.datetime.now()
        current_date = now.date()
        current_time_str = now.strftime("%H:%M")
        
        # 하루가 지나면(자정) 실행 기록 초기화
        if current_date != last_date:
            executed_times.clear()
            last_date = current_date
            print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 자정이 지나 실행 기록이 초기화되었습니다.")
            
        # 지정된 시간이 되었고, 오늘 아직 실행되지 않은 시간대일 경우 실행
        if current_time_str in settings["시간대"] and current_time_str not in executed_times:
            print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 예약 시간({current_time_str}) 도달. 매크로를 실행합니다.")
            print(f"발송 대상: {settings['채팅방개수']}개 채팅방 / 사진 전송 후 메시지 전송")
            print("주의: 카카오톡 채팅 목록의 첫 번째 방을 선택한 상태로 두세요.")
            
            # 발송 시작
            send_kakao_message(settings["채팅방개수"], settings["이미지경로"], message_text)
            
            executed_times.append(current_time_str)
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 전송 완료. 다음 예약 시간을 대기합니다.\n")
            
        time.sleep(1) # 1초마다 시간 확인

if __name__ == "__main__":
    main()
