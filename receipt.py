import pytesseract
from PIL import Image
import re

# Tesseract 경로 설정 (필요한 경우 수정)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Tesseract 경로 설정

def extract_total_amount_from_image(image_path):
    """
    이미지에서 금액을 추출하여 반환하는 함수.
    이미지에서 쉼표가 포함된 금액을 찾고 가장 큰 값을 반환합니다.
    """
    # 이미지 열기
    img = Image.open(image_path)

    # pytesseract로 텍스트 추출
    result = pytesseract.image_to_string(img, lang='kor')

    # OCR로 추출된 텍스트 출력

    # 쉼표가 포함된 금액 추출을 위한 정규식 (숫자와 쉼표 포함된 부분)
    numbers_with_commas = re.findall(r'\d{1,3}(?:,\d{3})*', result)

    # 쉼표를 제거하고 정수로 변환하여 리스트에 저장
    numbers = [int(num.replace(',', '')) for num in numbers_with_commas]

    if numbers:
        # 가장 큰 금액을 찾아 반환
        return max(numbers)
    else:
        print("이미지에서 금액을 추출할 수 없습니다.")
        return None

def split_bill_from_image(image_path, num_people):
    """
    이미지에서 금액을 추출하여 나누어 1인당 금액을 출력하는 함수.
    금액과 인원 수를 입력받아 1인당 금액을 반환합니다.
    """
    total_amount = extract_total_amount_from_image(image_path)
    
    if total_amount is not None:
        if num_people <= 0:
            raise ValueError("인원 수는 1명 이상이어야 합니다.")
        else:
            amount_per_person = total_amount / num_people
            print("총 금액 : ",total_amount)
            print("1인당 금액 : ",amount_per_person) 
    else:
        raise ValueError("유효한 금액을 추출할 수 없습니다.")
