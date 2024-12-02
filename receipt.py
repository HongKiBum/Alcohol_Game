import pytesseract
from PIL import Image
import re

# Tesseract 경로 설정 (만약 다른 경로에 설치되어 있다면 변경해야 함)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
#변경
def extract_total_amount_from_image(image_path):
    """
    이미지에서 금액을 추출하여 반환하는 함수.
    이미지에서 쉼표가 포함된 금액을 찾고 가장 큰 값을 반환합니다.
    """
    # 이미지 열기
    img = Image.open(image_path)

    # pytesseract로 텍스트 추출
    result = pytesseract.image_to_string(img, lang='kor')

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
    """
    total_amount = extract_total_amount_from_image(image_path)

    if total_amount is not None:
        if num_people <= 0:
            print("인원 수는 1명 이상이어야 합니다.")
        else:
            # 1인당 금액 계산
            amount_per_person = total_amount / num_people
            
            # 쉼표 형식으로 금액 포맷팅
            formatted_total = f"{total_amount:,} 원"
            formatted_per_person = f"{amount_per_person:,.0f} 원"  # 소수점 이하 제거
            
            print(f"총 금액: {formatted_total}")
            print(f"1인당 금액: {formatted_per_person}")
    else:
        print("유효한 금액을 추출할 수 없습니다.")
